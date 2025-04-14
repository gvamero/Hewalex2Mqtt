"""AppDaemon app to read data from Hewalex ZPS and PCWU devices and publish to MQTT/HA.

Program Flow:
------------
1. INITIALIZATION:
   - Loads configuration from apps.yaml (polling interval, device addresses, IDs, etc.)
   - Validates required parameters for enabled devices (PCWU/ZPS)
   - Initializes device handlers with controller/device IDs

2. RUNTIME OPERATION:
   - Starts automatic polling loop (configurable interval)
   └── For each enabled device:
       a) Establishes serial-over-socket connection
       b) Reads status registers via device-specific protocol
       c) Parses response into key-value pairs
       d) Publishes changes to MQTT topics
       e) Updates Home Assistant sensor entities

3. DATA PROCESSING:
   - Implements message caching to avoid duplicate updates
   - Auto-detects sensor types (temperature/pressure/flow) for HA metadata
   - Handles device responses asynchronously via callback

4. AUXILIARY FEATURES:
   - Manual refresh via service call (hewalex2mqtt/refresh)
   - Graceful error handling for serial comms and parsing
   - Detailed logging at multiple levels (DEBUG to ERROR)

Configuration:
--------------
Requires serial-over-socket access to devices. Each device type (PCWU/ZPS) needs:
- IP address and port
- Controller/device hardware/software IDs
- Optional: MQTT topic prefix (default: 'hewalex/[pcwu|zps]')
"""""

import appdaemon.plugins.hass.hassapi as hass
import serial
from hewalex_geco.devices import PCWU, ZPS
from typing import Optional, Dict, Any, Union

class Hewalex2MqttApp(hass.Hass):
    """Main application class for Hewalex device integration."""
    
    def initialize(self) -> None:
        """Initialize the application with configuration."""
        self.log("Initializing Hewalex2Mqtt App", level="INFO")
        
        # Validate and load configuration
        if not self._validate_config():
            self.log("Invalid configuration, app will not start", level="ERROR")
            return
        
        # Initialize device connections
        self._init_devices()
        
        # Register service for manual refresh
        self.register_service("hewalex2mqtt/refresh", self.handle_refresh_service)
        
        # Start polling loop
        self.run_every(self.read_devices, self.datetime(), self.polling_interval)
        self.log("Hewalex2Mqtt App initialized successfully", level="INFO")

    def _validate_config(self) -> bool:
        """Validate the configuration from apps.yaml."""
        try:
            self.polling_interval = float(self.args.get("polling_interval", 10.0))
            if self.polling_interval <= 0:
                raise ValueError("Polling interval must be positive")
            
            # PCWU config validation
            self.pcwu_enabled = self.args.get("pcwu_enabled", False)
            if self.pcwu_enabled:
                if not all(key in self.args for key in ["pcwu_address", "pcwu_port"]):
                    raise ValueError("PCWU enabled but missing required configuration")
                
                self.pcwu_address = str(self.args["pcwu_address"])
                self.pcwu_port = int(self.args["pcwu_port"])
                self.pcwu_topic = str(self.args.get("pcwu_topic", "hewalex/pcwu"))
                self.pcwu_chid = int(self.args.get("pcwu_controller_hard_id", 3))
                self.pcwu_csid = int(self.args.get("pcwu_controller_soft_id", 3))
                self.pcwu_dhid = int(self.args.get("pcwu_device_hard_id", 4))
                self.pcwu_dsid = int(self.args.get("pcwu_device_soft_id", 4))
            
            # ZPS config validation
            self.zps_enabled = self.args.get("zps_enabled", False)
            if self.zps_enabled:
                if not all(key in self.args for key in ["zps_address", "zps_port"]):
                    raise ValueError("ZPS enabled but missing required configuration")
                
                self.zps_address = str(self.args["zps_address"])
                self.zps_port = int(self.args["zps_port"])
                self.zps_topic = str(self.args.get("zps_topic", "hewalex/zps"))
                self.zps_chid = int(self.args.get("zps_controller_hard_id", 1))
                self.zps_csid = int(self.args.get("zps_controller_soft_id", 1))
                self.zps_dhid = int(self.args.get("zps_device_hard_id", 2))
                self.zps_dsid = int(self.args.get("zps_device_soft_id", 2))
            
            self.message_cache: Dict[str, str] = {}
            self._devices_initialized = False
            return True
            
        except Exception as e:
            self.log(f"Configuration error: {str(e)}", level="ERROR")
            return False

    def _init_devices(self) -> None:
        """Initialize device instances."""
        try:
            if self.pcwu_enabled:
                self.pcwu_device = PCWU(
                    self.pcwu_chid, self.pcwu_csid, 
                    self.pcwu_dhid, self.pcwu_dsid, 
                    self.handle_response
                )
            
            if self.zps_enabled:
                self.zps_device = ZPS(
                    self.zps_chid, self.zps_csid,
                    self.zps_dhid, self.zps_dsid,
                    self.handle_response
                )
            
            self._devices_initialized = True
            self.log("Devices initialized successfully", level="INFO")
        except Exception as e:
            self.log(f"Device initialization failed: {str(e)}", level="ERROR")
            self._devices_initialized = False

    def read_devices(self, kwargs: Dict[str, Any]) -> None:
        """Read data from all enabled devices."""
        if not self._devices_initialized:
            self.log("Devices not initialized, skipping read", level="WARNING")
            return
        
        if self.pcwu_enabled:
            self._read_single_device(
                device=self.pcwu_device,
                address=self.pcwu_address,
                port=self.pcwu_port,
                topic_prefix=self.pcwu_topic,
                device_type="PCWU"
            )
        
        if self.zps_enabled:
            self._read_single_device(
                device=self.zps_device,
                address=self.zps_address,
                port=self.zps_port,
                topic_prefix=self.zps_topic,
                device_type="ZPS"
            )

    def _read_single_device(
        self,
        device: Union[PCWU, ZPS],
        address: str,
        port: int,
        topic_prefix: str,
        device_type: str
    ) -> None:
        """Read data from a single device with proper error handling."""
        ser = None
        try:
            self.log(f"Reading {device_type} device at {address}:{port}", level="DEBUG")
            ser = serial.serial_for_url(f"socket://{address}:{port}", timeout=2)
            device.readStatusRegisters(ser)
        except serial.SerialException as e:
            self.log(f"Serial communication error with {device_type}: {str(e)}", level="ERROR")
        except Exception as e:
            self.log(f"Unexpected error reading {device_type}: {str(e)}", level="ERROR")
        finally:
            if ser is not None:
                try:
                    ser.close()
                except Exception as e:
                    self.log(f"Error closing serial connection: {str(e)}", level="WARNING")

    def handle_response(
        self,
        device: Union[PCWU, ZPS],
        h: Dict[str, Any],
        sh: Dict[str, Any],
        m: Dict[str, Any]
    ) -> None:
        """Handle response from device and update MQTT/HA."""
        if sh.get("FNC") != 0x50:
            self.log("Received non-status response, ignoring", level="DEBUG")
            return

        try:
            topic_prefix = self.pcwu_topic if isinstance(device, PCWU) else self.zps_topic
            device_name = "PCWU" if isinstance(device, PCWU) else "ZPS"
            
            mp = device.parseRegisters(sh["RestMessage"], sh["RegStart"], sh["RegLen"])
            
            for key, value in mp.items():
                if isinstance(value, dict):
                    continue
                
                self._process_sensor_value(
                    device_name=device_name,
                    topic_prefix=topic_prefix,
                    sensor_key=key,
                    sensor_value=value
                )
                
        except KeyError as e:
            self.log(f"Missing expected key in response: {str(e)}", level="ERROR")
        except Exception as e:
            self.log(f"Error processing device response: {str(e)}", level="ERROR")

    def _process_sensor_value(
        self,
        device_name: str,
        topic_prefix: str,
        sensor_key: str,
        sensor_value: Any
    ) -> None:
        """Process and publish a single sensor value."""
        try:
            topic = f"{topic_prefix}/{sensor_key}"
            value = str(sensor_value)
            entity_id = f"sensor.{device_name.lower()}_{sensor_key}".replace(" ", "_")
            
            # Only update if value changed
            if topic not in self.message_cache or self.message_cache[topic] != value:
                self.message_cache[topic] = value
                
                # Publish to MQTT
                self.call_service(
                    "mqtt/publish",
                    topic=topic,
                    payload=value,
                    retain=True
                )
                
                # Update HA entity
                self.set_state(
                    entity_id,
                    state=value,
                    attributes={
                        "friendly_name": f"{device_name} {sensor_key}",
                        "device_class": self._determine_device_class(sensor_key),
                        "unit_of_measurement": self._determine_unit(sensor_key)
                    }
                )
                
                self.log(
                    f"Updated {device_name} {sensor_key} = {value}",
                    level="DEBUG"
                )
                
        except Exception as e:
            self.log(f"Error processing sensor {sensor_key}: {str(e)}", level="ERROR")

    def _determine_device_class(self, sensor_key: str) -> Optional[str]:
        """Determine device class based on sensor key."""
        key = sensor_key.lower()
        if "temp" in key:
            return "temperature"
        elif "pressure" in key:
            return "pressure"
        elif "flow" in key:
            return None  # No standard device class for flow
        return None

    def _determine_unit(self, sensor_key: str) -> Optional[str]:
        """Determine unit of measurement based on sensor key."""
        key = sensor_key.lower()
        if "temp" in key:
            return "°C"
        elif "pressure" in key:
            return "bar"
        elif "flow" in key:
            return "l/min"
        return None

    def handle_refresh_service(self, service: str, data: Dict[str, Any]) -> None:
        """Handle manual refresh service call."""
        self.log("Manual refresh triggered via service call", level="INFO")
        self.read_devices({})

    def terminate(self) -> None:
        """Clean up resources when app is stopped."""
        self.log("Hewalex2Mqtt App terminating", level="INFO")
        # Add any cleanup logic needed here