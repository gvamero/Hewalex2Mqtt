Created copy from https://github.com/Chibald/Hewalex2Mqtt
Followed the discussion on https://gathering.tweakers.net/forum/list_messages/2069540
I want to use AppDeamon, user jojan265 described the steps to be taken https://gathering.tweakers.net/forum/view_message/79522762 
I think jojan265 created https://github.com/HJKLMN/HomeAssistant-Hewalex2MQTT, but it is not complete (e.g. jojan has not included devices like PCWU, which Chibald has) , so i updated 
HJKLMN repository with the missing files from Chibald.

On top of these changes, i added mqtt.yaml and modified this Readme.yaml (see https://www.home-assistant.io/integrations/sensor.mqtt/) as these make they covert the mqtt messags into home assistant instances.
The YAML files are located in the root installation folder of where you installed Home Assistant
Do not overwrite the existing files as these contain parameters for other Home Assistant components. Instead add the contents of the new files to the existing files.

# Hewalex 2 Mqtt
Mqtt gateway for solar pump Hewalex ZPS-18e? with Geco controller G-422-P09(A)? and 
Hewalex PCWU 3kW heat pump

It Provides read and write access on mqtt topics, from Home Assistant.

# Installation
## Elfin EW11a
Configure as TCP server
Test with "C:\Users\gertj\OneDrive\Documenten\Zonneboiler\Zonneboiler set\Pompgroep en control\Elfin EW11A\TCP\TCPUDPDbg.exe

### Warmtepomp
Elfin voor Warmtepomp
http://192.168.3.98 --> Communication settings --> Add 
Basic Settings
	Name: WP-HA
	Protocol: TCP Server
Socket Settings
	Local Port: 502
	Buffer Size: 512
	Keep Alive(s): 60
	Timeout(s): 0
Protocol Settings
	Max Accept: 3
More Settings
	SecurityP: Disable
	Route: UART

Elfin voor Zonneboiler
Elfin voor Warmtepomp
http://192.168.3.99 --> Communication settings --> Add 
Basic Settings
	Name: ZB-HA
	Protocol: TCP Server
Socket Settings
	Local Port: 9999
	Buffer Size: 512
	Keep Alive(s): 60
	Timeout(s): 0
Protocol Settings
	Max Accept: 3
More Settings
	SecurityP: Disable
	Route: UART

Debuggen Elfin settings ：
Zie test tcp server
http://ftp.hi-flying.com:9000/IOTService/

### AppDeamon (Home Assistant)

De scripts moeten in addon/configs/a0d7b954_appdaemon geplaatst worden.
/addon_configs/a0d7b954_appdaemon/apps/hewalex2mqtt.py
/addon_configs/a0d7b954_appdaemon/apps/hewalex2mqttconfig.ini
/addon_configs/a0d7b954_appdaemon/apps/hewalex_geco/devices/pcwu.py
/addon_configs/a0d7b954_appdaemon/apps/hewalex_geco/devices/zps.py

## Using the script
just run the python script hewalex2mqtt.py
Dependencies: from hewalex_geco.devices import PCWU

### Parameters
All parameters are listed in the .ini file, which I modified to my needs.

## MQTT Topics
There are 2 kinds of topics: state and command. 
Command topics (marked command) allow the sending of commands to topics to control equipment.

### Solar Pump ZPS
| Topic | Type | Description |
| ----------------------- | ----------- | ---------------------------
| SolarBoiler/date | date | Date
| SolarBoiler/time | time | Time
| SolarBoiler/T1 | temp | T1 (Collectors temp)
| SolarBoiler/T2 | temp | T2 (Tank bottom temp)
| SolarBoiler/T3 | temp | T3 (Air separator temp)
| SolarBoiler/T4 | temp | T4 (Tank top temp)
| SolarBoiler/T5 | temp | T5 (Boiler outlet temp)
| SolarBoiler/T6 | temp | T6
| SolarBoiler/CollectorPower | word | Collector Power (W)
| SolarBoiler/Consumption | fl10 | Consumption (W)
| SolarBoiler/CollectorActive | bool | Collector Active (True/False)
| SolarBoiler/FlowRate | fl10 | Flow Rate (l/min)
| SolarBoiler/CollectorPumpON | mask | None
| SolarBoiler/CirculationPumpON | mask | None
| SolarBoiler/CollectorPumpSpeed | word | Collector Pump Speed (0-15)
| SolarBoiler/TotalEnergy | fl10 | Total Energy (kWh)
| SolarBoiler/InstallationScheme | word | Installation Scheme (1-19)
| SolarBoiler/DisplayTimeout | word | Display Timeout (1-10 min)
| SolarBoiler/Command/DisplayTimeout | word | Display Timeout (1-10 min)
| SolarBoiler/DisplayBrightness | word | Display Brightness (1-10)
| SolarBoiler/Command/DisplayBrightness | word | Display Brightness (1-10)
| SolarBoiler/AlarmSoundEnabled | bool | Alarm Sound Enabled (True/False)
| SolarBoiler/Command/AlarmSoundEnabled | bool | Alarm Sound Enabled (True/False)
| SolarBoiler/KeySoundEnabled | bool | Key Sound Enabled (True/False)
| SolarBoiler/Command/KeySoundEnabled | bool | Key Sound Enabled (True/False)
| SolarBoiler/DisplayLanguage | word | Display Language (0=PL, 1=EN, 2=DE, 3=FR, 4=PT, 5=ES, 6=NL, 7=IT, 8=CZ, 9=SL, ...)
| SolarBoiler/Command/DisplayLanguage | word | Display Language (0=PL, 1=EN, 2=DE, 3=FR, 4=PT, 5=ES, 6=NL, 7=IT, 8=CZ, 9=SL, ...)
| SolarBoiler/FluidFreezingTemp | temp | Fluid Freezing Temp
| SolarBoiler/Command/FluidFreezingTemp | temp | Fluid Freezing Temp
| SolarBoiler/FlowRateNominal | fl10 | Flow Rate Nominal (l/min)
| SolarBoiler/Command/FlowRateNominal | fl10 | Flow Rate Nominal (l/min)
| SolarBoiler/FlowRateMeasurement | word | Flow Rate Measurement (0=Rotameter, 1=Electronic G916, 2=Electronic)
| SolarBoiler/Command/FlowRateMeasurement | word | Flow Rate Measurement (0=Rotameter, 1=Electronic G916, 2=Electronic)
| SolarBoiler/FlowRateWeight | f100 | Flow Rate Weight (imp/l)
| SolarBoiler/Command/FlowRateWeight | f100 | Flow Rate Weight (imp/l)
| SolarBoiler/HolidayEnabled | bool | Holiday Enabled (True/False)
| SolarBoiler/Command/HolidayEnabled | bool | Holiday Enabled (True/False)
| SolarBoiler/HolidayStartDay | word | Holiday Start Day
| SolarBoiler/Command/HolidayStartDay | word | Holiday Start Day
| SolarBoiler/HolidayStartMonth | word | Holiday Start Month
| SolarBoiler/Command/HolidayStartMonth | word | Holiday Start Month
| SolarBoiler/HolidayStartYear | word | Holiday Start Year
| SolarBoiler/Command/HolidayStartYear | word | Holiday Start Year
| SolarBoiler/HolidayEndDay | word | Holiday End Day
| SolarBoiler/Command/HolidayEndDay | word | Holiday End Day
| SolarBoiler/HolidayEndMonth | word | Holiday End Month
| SolarBoiler/Command/HolidayEndMonth | word | Holiday End Month
| SolarBoiler/HolidayEndYear | word | Holiday End Year
| SolarBoiler/Command/HolidayEndYear | word | Holiday End Year
| SolarBoiler/CollectorType | word | Collector Type (0=Flat, 1=Tube)
| SolarBoiler/Command/CollectorType | word | Collector Type (0=Flat, 1=Tube)
| SolarBoiler/CollectorPumpHysteresis | temp | Collector Pump Hysteresis (Difference between T1 and T2 to turn on collector pump)
| SolarBoiler/Command/CollectorPumpHysteresis | temp | Collector Pump Hysteresis (Difference between T1 and T2 to turn on collector pump)
| SolarBoiler/ExtraPumpHysteresis | temp | Extra Pump Hysteresis (Temp difference to turn on extra pump)
| SolarBoiler/Command/ExtraPumpHysteresis | temp | Extra Pump Hysteresis (Temp difference to turn on extra pump)
| SolarBoiler/CollectorPumpMaxTemp | temp | Collector Pump Max Temp (Maximum T2 temp to turn off collector pump)
| SolarBoiler/Command/CollectorPumpMaxTemp | temp | Collector Pump Max Temp (Maximum T2 temp to turn off collector pump)
| SolarBoiler/BoilerPumpMinTemp | word | Boiler Pump Min Temp (Minimum T5 temp to turn on boiler pump)
| SolarBoiler/Command/BoilerPumpMinTemp | word | Boiler Pump Min Temp (Minimum T5 temp to turn on boiler pump)
| SolarBoiler/HeatSourceMaxTemp | word | Heat Source Max Temp (Maximum T4 temp to turn off heat sources)
| SolarBoiler/Command/HeatSourceMaxTemp | word | Heat Source Max Temp (Maximum T4 temp to turn off heat sources)
| SolarBoiler/BoilerPumpMaxTemp | word | Boiler Pump Max Temp (Maximum T4 temp to turn off boiler pump)
| SolarBoiler/Command/BoilerPumpMaxTemp | word | Boiler Pump Max Temp (Maximum T4 temp to turn off boiler pump)
| SolarBoiler/PumpRegulationEnabled | bool | Pump Regulation Enabled (True/False)
| SolarBoiler/Command/PumpRegulationEnabled | bool | Pump Regulation Enabled (True/False)
| SolarBoiler/HeatSourceMaxCollectorPower | word | Heat Source Max Collector Power (Maximum collector power to turn off heat sources) (100-9900W)
| SolarBoiler/Command/HeatSourceMaxCollectorPower | word | Heat Source Max Collector Power (Maximum collector power to turn off heat sources) (100-9900W)
| SolarBoiler/CollectorOverheatProtEnabled | bool | Collector Overheat Protection Enabled (True/False)
| SolarBoiler/Command/CollectorOverheatProtEnabled | bool | Collector Overheat Protection Enabled (True/False)
| SolarBoiler/CollectorOverheatProtMaxTemp | temp | Collector Overheat Protection Max Temp (Maximum T2 temp for overheat protection)
| SolarBoiler/Command/CollectorOverheatProtMaxTemp | temp | Collector Overheat Protection Max Temp (Maximum T2 temp for overheat protection)
| SolarBoiler/CollectorFreezingProtEnabled | bool | Collector Freezing Protection Enabled (True/False)
| SolarBoiler/Command/CollectorFreezingProtEnabled | bool | Collector Freezing Protection Enabled (True/False)
| SolarBoiler/HeatingPriority | word | Heating Priority
| SolarBoiler/Command/HeatingPriority | word | Heating Priority
| SolarBoiler/LegionellaProtEnabled | bool | Legionella Protection Enabled (True/False)
| SolarBoiler/Command/LegionellaProtEnabled | bool | Legionella Protection Enabled (True/False)
| SolarBoiler/LockBoilerKWithBoilerC | bool | Lock Boiler K With Boiler C (True/False)
| SolarBoiler/Command/LockBoilerKWithBoilerC | bool | Lock Boiler K With Boiler C (True/False)
| SolarBoiler/NightCoolingEnabled | bool | Night Cooling Enabled (True/False)
| SolarBoiler/Command/NightCoolingEnabled | bool | Night Cooling Enabled (True/False)
| SolarBoiler/NightCoolingStartTemp | temp | Night Cooling Start Temp
| SolarBoiler/Command/NightCoolingStartTemp | temp | Night Cooling Start Temp
| SolarBoiler/NightCoolingStopTemp | temp | Night Cooling Stop Temp
| SolarBoiler/Command/NightCoolingStopTemp | temp | Night Cooling Stop Temp
| SolarBoiler/NightCoolingStopTime | word | Night Cooling Stop Time (hr)
| SolarBoiler/Command/NightCoolingStopTime | word | Night Cooling Stop Time (hr)
| SolarBoiler/TimeProgramCM-F | tprg | Time Program C M-F (True/False per hour of the day)
| SolarBoiler/Command/TimeProgramCM-F | tprg | Time Program C M-F (True/False per hour of the day)
| SolarBoiler/TimeProgramCSat | tprg | Time Program C Sat (True/False per hour of the day)
| SolarBoiler/Command/TimeProgramCSat | tprg | Time Program C Sat (True/False per hour of the day)
| SolarBoiler/TimeProgramCSun | tprg | Time Program C Sun (True/False per hour of the day)
| SolarBoiler/Command/TimeProgramCSun | tprg | Time Program C Sun (True/False per hour of the day)
| SolarBoiler/TimeProgramKM-F | tprg | Time Program K M-F (True/False per hour of the day)
| SolarBoiler/Command/TimeProgramKM-F | tprg | Time Program K M-F (True/False per hour of the day)
| SolarBoiler/TimeProgramKSat | tprg | Time Program K Sat (True/False per hour of the day)
| SolarBoiler/Command/TimeProgramKSat | tprg | Time Program K Sat (True/False per hour of the day)
| SolarBoiler/TimeProgramKSun | tprg | Time Program K Sun (True/False per hour of the day)
| SolarBoiler/Command/TimeProgramKSun | tprg | Time Program K Sun (True/False per hour of the day)
| SolarBoiler/CollectorPumpMinRev | word | Collector Pump Min Rev (rev/min)
| SolarBoiler/Command/CollectorPumpMinRev | word | Collector Pump Min Rev (rev/min)
| SolarBoiler/CollectorPumpMaxRev | word | Collector Pump Max Rev (rev/min)
| SolarBoiler/Command/CollectorPumpMaxRev | word | Collector Pump Max Rev (rev/min)
| SolarBoiler/CollectorPumpMinIncTime | word | Collector Pump Min Increase Time (s)
| SolarBoiler/Command/CollectorPumpMinIncTime | word | Collector Pump Min Increase Time (s)
| SolarBoiler/CollectorPumpMinDecTime | word | Collector Pump Min Decrease Time (s)
| SolarBoiler/Command/CollectorPumpMinDecTime | word | Collector Pump Min Decrease Time (s)
| SolarBoiler/CollectorPumpStartupSpeed | word | Collector Pump Startup Speed (1-15)
| SolarBoiler/Command/CollectorPumpStartupSpeed | word | Collector Pump Startup Speed (1-15)
| SolarBoiler/PressureSwitchEnabled | bool | Pressure Switch Enabled (True/False)
| SolarBoiler/Command/PressureSwitchEnabled | bool | Pressure Switch Enabled (True/False)
| SolarBoiler/TankOverheatProtEnabled | bool | Tank Overheat Protection Enabled (True/False)
| SolarBoiler/Command/TankOverheatProtEnabled | bool | Tank Overheat Protection Enabled (True/False)
| SolarBoiler/CirculationPumpEnabled | bool | Circulation Pump Enabled (True/False)
| SolarBoiler/Command/CirculationPumpEnabled | bool | Circulation Pump Enabled (True/False)
| SolarBoiler/CirculationPumpMode | word | Circulation Pump Mode (0=Discontinuous, 1=Continuous)
| SolarBoiler/Command/CirculationPumpMode | word | Circulation Pump Mode (0=Discontinuous, 1=Continuous)
| SolarBoiler/CirculationPumpMinTemp | temp | Circulation Pump Min Temp (Minimum T4 temp to turn on circulation pump)
| SolarBoiler/Command/CirculationPumpMinTemp | temp | Circulation Pump Min Temp (Minimum T4 temp to turn on circulation pump)
| SolarBoiler/CirculationPumpONTime | word | Circulation Pump ON Time (1-59 min)
| SolarBoiler/Command/CirculationPumpONTime | word | Circulation Pump ON Time (1-59 min)
| SolarBoiler/CirculationPumpOFFTime | word | Circulation Pump OFF Time (1-59 min)
| SolarBoiler/Command/CirculationPumpOFFTime | word | Circulation Pump OFF Time (1-59 min)
| SolarBoiler/TotalOperationTime | dwrd | Total Operation Time (min) - lives in config space but is status register
| SolarBoiler/Command/TotalOperationTime | dwrd | Total Operation Time (min) - lives in config space but is status register
| SolarBoiler/Reg320 | word | Unknown register - value changes constantly
| SolarBoiler/Command/Reg320 | word | Unknown register - value changes constantly

### Heat Pump
| Topic | Type | Description | 
| ----------------------- | ----------- | ---------------------------
| Heatpump/date | date | Date
| Heatpump/time | time | Time
| Heatpump/T1 | te10 | T1 (Ambient temp)
| Heatpump/T2 | te10 | T2 (Tank bottom temp)
| Heatpump/T3 | te10 | T3 (Tank top temp)
| Heatpump/T6 | te10 | T6 (HP water inlet temp)
| Heatpump/T7 | te10 | T7 (HP water outlet temp)
| Heatpump/T8 | te10 | T8 (HP evaporator temp)
| Heatpump/T9 | te10 | T9 (HP before compressor temp)
| Heatpump/T10 | te10 | T10 (HP after compressor temp)
| Heatpump/IsManual | bool | None
| Heatpump/FanON | mask | None
| Heatpump/CirculationPumpON | mask | None
| Heatpump/HeatPumpON | mask | None
| Heatpump/CompressorON | mask | None
| Heatpump/HeaterEON | mask | None
| Heatpump/EV1 | word | Expansion valve
| Heatpump/WaitingStatus | word |  0 when available for operation, 2 when disabled through register 304
| Heatpump/InstallationScheme | word | Installation Scheme (1-9)
| Heatpump/HeatPumpEnabled | bool | Heat Pump Enabled (True/False)
| Heatpump/Command/HeatPumpEnabled | bool | Heat Pump Enabled (True/False)
| Heatpump/TapWaterSensor | word | Temp. sensor controlling heat pump operation [T2,T3,T7, factory setting T2]
| Heatpump/Command/TapWaterSensor | word | Temp. sensor controlling heat pump operation [T2,T3,T7, factory setting T2]
| Heatpump/TapWaterTemp | te10 | HUW temperature for heat pump [10-60°C, factory setting 50°C]
| Heatpump/Command/TapWaterTemp | te10 | HUW temperature for heat pump [10-60°C, factory setting 50°C]
| Heatpump/TapWaterHysteresis | te10 | Heat pump start-up hysteresis [2-10°C, factory setting 5°C]
| Heatpump/Command/TapWaterHysteresis | te10 | Heat pump start-up hysteresis [2-10°C, factory setting 5°C]
| Heatpump/AmbientMinTemp | te10 | Minimum ambient temperature (T1) [-10-10°C]
| Heatpump/Command/AmbientMinTemp | te10 | Minimum ambient temperature (T1) [-10-10°C]
| Heatpump/TimeProgramHPM-F | tprg | Time Program HP M-F (True/False per hour of the day)
| Heatpump/Command/TimeProgramHPM-F | tprg | Time Program HP M-F (True/False per hour of the day)
| Heatpump/TimeProgramHPSat | tprg | Time Program HP Sat (True/False per hour of the day)
| Heatpump/Command/TimeProgramHPSat | tprg | Time Program HP Sat (True/False per hour of the day)
| Heatpump/TimeProgramHPSun | tprg | Time Program HP Sun (True/False per hour of the day)
| Heatpump/Command/TimeProgramHPSun | tprg | Time Program HP Sun (True/False per hour of the day)
| Heatpump/AntiFreezingEnabled | bool | Function protecting against freezing [YES/NO], factory setting YES
| Heatpump/Command/AntiFreezingEnabled | bool | Function protecting against freezing [YES/NO], factory setting YES
| Heatpump/WaterPumpOperationMode | word | Water Pump Operation Mode (0=Continuous, 1=Synchronous)
| Heatpump/Command/WaterPumpOperationMode | word | Water Pump Operation Mode (0=Continuous, 1=Synchronous)
| Heatpump/FanOperationMode | word | Fan Operation Mode (0=Max, 1=Min, 2=Day/Night), factory MAX
| Heatpump/Command/FanOperationMode | word | Fan Operation Mode (0=Max, 1=Min, 2=Day/Night), factory MAX
| Heatpump/DefrostingInterval | word | Defrosting cycle start-up delay [30-90 min., factory setting 45 min.]
| Heatpump/Command/DefrostingInterval | word | Defrosting cycle start-up delay [30-90 min., factory setting 45 min.]
| Heatpump/DefrostingStartTemp | te10 | Temperature activating defrosting [-30 - 0°C, factory setting -7°C]
| Heatpump/Command/DefrostingStartTemp | te10 | Temperature activating defrosting [-30 - 0°C, factory setting -7°C]
| Heatpump/DefrostingStopTemp | te10 | Temperature finishing defrosting [2-30°C, factory setting 13°C]
| Heatpump/Command/DefrostingStopTemp | te10 | Temperature finishing defrosting [2-30°C, factory setting 13°C]
| Heatpump/DefrostingMaxTime | word | Maximum defrosting duration [1-12 min., factory setting 8 min.]
| Heatpump/Command/DefrostingMaxTime | word | Maximum defrosting duration [1-12 min., factory setting 8 min.]
| Heatpump/ExtControllerHPOFF | bool | Heat pump deactivation [YES/NO, factory setting YES]
| Heatpump/Command/ExtControllerHPOFF | bool | Heat pump deactivation [YES/NO, factory setting YES]


### extend configuration.yamlmqtt:
  switch:
    - name: "Heatpump On"
      command_topic: "Heatpump/Command/HeatPumpEnabled"
      payload_on: "True"
      payload_off: "False"
      state_on: "On"
      state_off: "Off"
      unique_id: hewalex_heatpump_on_switch
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Hewalex Heatpump"
    - name: "Heatpump Deactivation"
      command_topic: "Heatpump/Command/ExtControllerHPOFF"
      payload_on: "True"
      payload_off: "False"
      state_on: "On"
      state_off: "Off"
      unique_id: hewalex_heatpump_extcontrol_switch
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Hewalex Heatpump"
  number:
    - name: "Hewalex Heatpump Set Hysteresis"
      command_topic: "Heatpump/Command/TapWaterHysteresis"
      state_topic: "Heatpump/TapWaterHysteresis"
      unit_of_measurement: "°C"
      max: "10"
      unique_id: "hewalex_heatpump_hysteresis_set"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex Heatpump Set Tapwater Temp"
      command_topic: "Heatpump/Command/TapWaterTemp"
      state_topic: "Heatpump/TapWaterTemp"
      unit_of_measurement: "°C"
      max: "60"
      min: "40"
      unique_id: "hewalex_heatpump_tapwater_set"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
  sensor:
    - name: "Hewalex T1 Ambient Temp"
      state_topic: "Heatpump/T1"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t1"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Hewalex Heatpump"
    - name: "Hewalex T2 Bottom Tank Temp"
      state_topic: "Heatpump/T2"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t2"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex T3 Top Tank Temp"
      state_topic: "Heatpump/T3"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t3"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex T6 HP Water Inlet Temp"
      state_topic: "Heatpump/T6"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t6"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex T7 HP Water Outlet Temp)"
      state_topic: "Heatpump/T7"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t7"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex T8 HP Evaporator Temp"
      state_topic: "Heatpump/T8"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t8"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex T9 HP Pre Compressor Temp)"
      state_topic: "Heatpump/T9"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t9"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex T10 HP Post Compressor Temp)"
      state_topic: "Heatpump/T10"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_t10"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex HP Temp Setting"
      state_topic: "Heatpump/TapWaterTemp"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_tapwater"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex HP Status"
      state_topic: "Heatpump/HeatPumpEnabled"
      unique_id: "hewalex_heatpump_status"
      value_template: >-
        {% if value == "True" %}
             On
        {% else %}
            Off
        {% endif %}
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex HP Hysteresis"
      state_topic: "Heatpump/TapWaterHysteresis"
      unit_of_measurement: "°C"
      unique_id: "hewalex_heatpump_hysteresis"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex HP Circulation Pump"
      state_topic: "Heatpump/CirculationPumpON"
      unique_id: "hewalex_heatpump_waterpump"
      value_template: >-
        {% if value == "True" %}
             On
        {% else %}
            Off
        {% endif %}
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex HP Fan"
      state_topic: "Heatpump/FanON"
      unique_id: "hewalex_heatpump_fan"
      value_template: >-
        {% if value == "True" %}
             On
        {% else %}
            Off
        {% endif %}
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"
    - name: "Hewalex HP Expansion Valve"
      state_topic: "Heatpump/EV1"
      unit_of_measurement: "-/-"
      unique_id: "hewalex_heatpump_ev1"
      device:
        identifiers:
          - "hewalex_heatpump"
        name: "Heatpump Hewalex"


### Examples
Turn off heat pump
`Heatpump/Command/HeatPumpEnabled False`

Change T2 temperature setting to 52°C
`Heatpump/Command/TapWaterTemp 52`

## Acknowledgements

Based on
* https://github.com/mvdklip/Domoticz-Hewalex
* https://www.elektroda.pl/rtvforum/topic3499254.html 
* https://github.com/aelias-eu/hewalex-geco-protocol
* https://github.com/Chibald/Hewalex2Mqtt
* https://github.com/HJKLMN/HomeAssistant-Hewalex2MQTT
