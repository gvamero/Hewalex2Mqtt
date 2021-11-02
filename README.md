A word of warning: to make use of this script you will have to connect a rs485 connector to your equipment. This means working on mains-voltage equipment so use your head. Always power down equipment before screwing them open and poking around in them. 
Also, all of this software is provided AS-IS with no implied warranty or liability under sections 15, and 16 of the GPL V3. So whatever happens, it is not my fault ;)

# Hewalex 2 Mqtt

Mqtt gateway for hewalex heat pumps and solar pumps.

Solar Pump Hewalex / Geco controllers
G-422-P09
G-422-P09A

Heat Pump (Hewalex solmax)
PCWU 2.5kW
PCWU 3.0kW


Provides read and write access on mqtt topics. A typical use case is integration of hewalex solar pumps and/or heat pumps in Home Automation (HA) software.
This script is based on a domotics plugin. So if you use domotics a ready made plugin is available at: xx

## Hardware Prerequisites

Hewalex devices are equipped with empty RS485 connectors. 
This is basically a serial port. This script uses a 'serial for url' connection. 

You can buy a (cheap) wifi 2 rs485 or ethernet 2 rs485 device wich you attach to the rs485 port you want to interface with. And you need a piece of wire with 4 strands.

### Heat pumps (PCWU) setup

Remove the plastic case and open up the "fuse box". In here you will find a spre rs485 connector. Remove it and screw in a 4 strand wire. Connect the wire to the rs485wifi device.
Make sure you connect them correctly. It is wise to measure ac and grnd to be sure!

In the controller, navigate to rs485 settings. Change baud rate to 38500, Actual address to 2 and Logic address to 2.

Setup the rs485-to-wifi device. Make sure baud settings match above settings.
It is probably wise to assign static ip-address. Take note of this.

### Solar pumps (ZPS) setup

Remove G-422 controller from the casing. Connect the RS485 port on the backside of the G-422 controller to the wifi controller. 

## Software Prerequisities

You will need (and if you are reading this probably have) Home Automation software with/and MQTT broker.

Openhab
https://www.openhab.org/

Home Assistant
https://www.home-assistant.io/

But it'll work with any HA system that can process and send MQTT / Json messages.

## Using the script
just run the python script hewalex2mqtt.py, or use the docker image.

### Parameters
All parameters are listed in the .ini file.
Modify them according to your needs when you are not using the pre-made docker image.

When you are using docker, make sure to set the environment variables. Or use the provided docker-compose and modify that accoriding to your setup.


**MQTT**
| Parameter | Value |
| ----------------------- | ----------- |
| MQTT_ip | 192.168.1.2
| MQTT_port | 1883
| MQTT_authentication | True
| MQTT_user | 
| MQTT_pass | 
| MQTT_GatewayDevice_Topic | HewaGate

**ZPS**
| Parameter | Value |
| ----------------------- | ----------- |
| Device_Zps_Enabled | False
| Device_Zps_Address | IP of the RS485 to Wi-Fi device eg. 192.168.1.7
| Device_Zps_Port | Port of the RS485 to Wi-Fi device eg. 8899
| Device_Zps_MqttTopic | SolarBoiler


**Pcwu**
| Parameter | Value |
| ----------------------- | ----------- |
| Device_Pcwu_Enabled | True
| Device_Pcwu_Address | IP of the RS485 to Wi-Fi device eg. 192.168.1.8
| Device_Pcwu_Port | Port of the RS485 to Wi-Fi device eg. 8899
| Device_Pcwu_MqttTopic | Heatpump


### Docker
A pre made docker image is available at XX. 


## MQTT Topics

There are 2 kinds of topics: state and command. 
Command topics (marked command) allow the sending of commands to topics to control equipment.

### Solar Pump
| Topic | Description |
| ----------------------- | ----------- |
| SolarBoiler/date |
| SolarBoiler/time |
| SolarBoiler/T1 |
| SolarBoiler/T2 |
| SolarBoiler/T3 |
| SolarBoiler/T4 |
| SolarBoiler/T5 |
| SolarBoiler/T6 |
| SolarBoiler/CollectorPower |
| SolarBoiler/Consumption |
| SolarBoiler/CollectorActive |
| SolarBoiler/FlowRate |
| SolarBoiler/CollectorPumpON |
| SolarBoiler/CirculationPumpON |
| SolarBoiler/CollectorPumpSpeed |
| SolarBoiler/TotalEnergy |
| SolarBoiler/InstallationScheme |
| SolarBoiler/DisplayTimeout |
| SolarBoiler/Command/DisplayTimeout |
| SolarBoiler/DisplayBrightness |
| SolarBoiler/Command/DisplayBrightness |
| SolarBoiler/AlarmSoundEnabled |
| SolarBoiler/Command/AlarmSoundEnabled | 
| SolarBoiler/KeySoundEnabled |
| SolarBoiler/Command/KeySoundEnabled |
| SolarBoiler/DisplayLanguage |
| SolarBoiler/Command/DisplayLanguage |
| SolarBoiler/FluidFreezingTemp |
| SolarBoiler/Command/FluidFreezingTemp |
| SolarBoiler/FlowRateNominal |
| SolarBoiler/Command/FlowRateNominal |
| SolarBoiler/FlowRateMeasurement |
| SolarBoiler/Command/FlowRateMeasurement |
| SolarBoiler/FlowRateWeight |
| SolarBoiler/Command/FlowRateWeight |
| SolarBoiler/HolidayEnabled |
| SolarBoiler/Command/HolidayEnabled |
| SolarBoiler/HolidayStartDay |
| SolarBoiler/Command/HolidayStartDay |
| SolarBoiler/HolidayStartMonth |
| SolarBoiler/Command/HolidayStartMonth |
| SolarBoiler/HolidayStartYear |
| SolarBoiler/Command/HolidayStartYear |
| SolarBoiler/HolidayEndDay |
| SolarBoiler/Command/HolidayEndDay |
| SolarBoiler/HolidayEndMonth |
| SolarBoiler/Command/HolidayEndMonth |
| SolarBoiler/HolidayEndYear |
| SolarBoiler/Command/HolidayEndYear |
| SolarBoiler/CollectorType |
| SolarBoiler/Command/CollectorType |
| SolarBoiler/CollectorPumpHysteresis |
| SolarBoiler/Command/CollectorPumpHysteresis |
| SolarBoiler/ExtraPumpHysteresis |
| SolarBoiler/Command/ExtraPumpHysteresis |
| SolarBoiler/CollectorPumpMaxTemp |
| SolarBoiler/Command/CollectorPumpMaxTemp |
| SolarBoiler/BoilerPumpMinTemp |
| SolarBoiler/Command/BoilerPumpMinTemp |
| SolarBoiler/HeatSourceMaxTemp |
| SolarBoiler/Command/HeatSourceMaxTemp |
| SolarBoiler/BoilerPumpMaxTemp |
| SolarBoiler/Command/BoilerPumpMaxTemp |
| SolarBoiler/PumpRegulationEnabled |
| SolarBoiler/Command/PumpRegulationEnabled |
| SolarBoiler/HeatSourceMaxCollectorPower |
| SolarBoiler/Command/HeatSourceMaxCollectorPower |
| SolarBoiler/CollectorOverheatProtEnabled |
| SolarBoiler/Command/CollectorOverheatProtEnabled |
| SolarBoiler/CollectorOverheatProtMaxTemp |
| SolarBoiler/Command/CollectorOverheatProtMaxTemp |
| SolarBoiler/CollectorFreezingProtEnabled |
| SolarBoiler/Command/CollectorFreezingProtEnabled |
| SolarBoiler/HeatingPriority |
| SolarBoiler/Command/HeatingPriority |
| SolarBoiler/LegionellaProtEnabled |
| SolarBoiler/Command/LegionellaProtEnabled |
| SolarBoiler/LockBoilerKWithBoilerC |
| SolarBoiler/Command/LockBoilerKWithBoilerC |
| SolarBoiler/NightCoolingEnabled |
| SolarBoiler/Command/NightCoolingEnabled |
| SolarBoiler/NightCoolingStartTemp |
| SolarBoiler/Command/NightCoolingStartTemp |
| SolarBoiler/NightCoolingStopTemp |
| SolarBoiler/Command/NightCoolingStopTemp |
| SolarBoiler/NightCoolingStopTime |
| SolarBoiler/Command/NightCoolingStopTime |
| SolarBoiler/TimeProgramCM-F |
| SolarBoiler/Command/TimeProgramCM-F |
| SolarBoiler/TimeProgramCSat |
| SolarBoiler/Command/TimeProgramCSat |
| SolarBoiler/TimeProgramCSun |
| SolarBoiler/Command/TimeProgramCSun |
| SolarBoiler/TimeProgramKM-F |
| SolarBoiler/Command/TimeProgramKM-F |
| SolarBoiler/TimeProgramKSat |
| SolarBoiler/Command/TimeProgramKSat |
| SolarBoiler/TimeProgramKSun |
| SolarBoiler/Command/TimeProgramKSun |
| SolarBoiler/CollectorPumpMinRev |
| SolarBoiler/Command/CollectorPumpMinRev |
| SolarBoiler/CollectorPumpMaxRev |
| SolarBoiler/Command/CollectorPumpMaxRev |
| SolarBoiler/CollectorPumpMinIncTime |
| SolarBoiler/Command/CollectorPumpMinIncTime |
| SolarBoiler/CollectorPumpMinDecTime |
| SolarBoiler/Command/CollectorPumpMinDecTime | 
| SolarBoiler/CollectorPumpStartupSpeed |
| SolarBoiler/Command/CollectorPumpStartupSpeed |
| SolarBoiler/PressureSwitchEnabled |
| SolarBoiler/Command/PressureSwitchEnabled |
| SolarBoiler/TankOverheatProtEnabled |
| SolarBoiler/Command/TankOverheatProtEnabled |
| SolarBoiler/CirculationPumpEnabled |
| SolarBoiler/Command/CirculationPumpEnabled |
| SolarBoiler/CirculationPumpMode |
| SolarBoiler/Command/CirculationPumpMode |
| SolarBoiler/CirculationPumpMinTemp |
| SolarBoiler/Command/CirculationPumpMinTemp |
| SolarBoiler/CirculationPumpONTime |
| SolarBoiler/Command/CirculationPumpONTime |
| SolarBoiler/CirculationPumpOFFTime |
| SolarBoiler/Command/CirculationPumpOFFTime |
| SolarBoiler/TotalOperationTime |
| SolarBoiler/Command/TotalOperationTime |
| SolarBoiler/Reg320 |
| SolarBoiler/Command/Reg320 |

### Heat Pump
| Topic | Description | 
| ----------------------- | ----------- |
| Heatpump/date | 
| Heatpump/time | 
| Heatpump/T1 | 
| Heatpump/T2 | 
| Heatpump/T3 | 
| Heatpump/T6 | 
| Heatpump/T7 | 
| Heatpump/T8 | 
| Heatpump/T9 | 
| Heatpump/T10 | 
| Heatpump/IsManual | 
| Heatpump/FanON | 
| Heatpump/CirculationPumpON |       
| Heatpump/HeatPumpON | 
| Heatpump/CompressorON | 
| Heatpump/HeaterEON | 
| Heatpump/EV1 | 
| Heatpump/WaitingStatus | 
| Heatpump/InstallationScheme |      
| Heatpump/HeatPumpEnabled |         
| Heatpump/Command/HeatPumpEnabled | 
| Heatpump/TapWaterSensor | 
| Heatpump/Command/TapWaterSensor |  
| Heatpump/TapWaterTemp |
| Heatpump/Command/TapWaterTemp |
| Heatpump/TapWaterHysteresis |
| Heatpump/Command/TapWaterHysteresis |
| Heatpump/AmbientMinTemp |
| Heatpump/Command/AmbientMinTemp |
| Heatpump/TimeProgramHPM-F |
| Heatpump/Command/TimeProgramHPM-F |
| Heatpump/TimeProgramHPSat |
| Heatpump/Command/TimeProgramHPSat |
| Heatpump/TimeProgramHPSun |
| Heatpump/Command/TimeProgramHPSun |
| Heatpump/AntiFreezingEnabled |
| Heatpump/Command/AntiFreezingEnabled |
| Heatpump/WaterPumpOperationMode |
| Heatpump/Command/WaterPumpOperationMode |
| Heatpump/FanOperationMode |
| Heatpump/Command/FanOperationMode |
| Heatpump/DefrostingInterval |
| Heatpump/Command/DefrostingInterval |
| Heatpump/DefrostingStartTemp |
| Heatpump/Command/DefrostingStartTemp |
| Heatpump/DefrostingStopTemp |
| Heatpump/Command/DefrostingStopTemp |
| Heatpump/DefrostingMaxTime |
| Heatpump/Command/DefrostingMaxTime |
| Heatpump/ExtControllerHPOFF |
| Heatpump/Command/ExtControllerHPOFF |

## Acknowledgements

Based on
* https://github.com/mvdklip/Domoticz-Hewalex
* https://www.elektroda.pl/rtvforum/topic3499254.html 
* https://github.com/aelias-eu/hewalex-geco-protocol
