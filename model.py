from datetime import datetime
import SmartESS

class SmartEssData:
    """Provides data of LUNA Smart meter values"""

    _Type = ""
    _Currency = "IQD"
    _MeterNo = ""
    _ReadDate = datetime.now()
    _TotalIndex = 0.0
    _GeneratorKwh = 0.0
    _GeneratorIndex = 0.0
    _GeneratorBalance = 0.0
    _GeneratorUnitPrice = 0.0
    _PowerLineIndex = 0.0
    _PowerLineKwh = 0.0
    _PowerLineBalance = 0.0
    _PowerLineUnitPrice = 0.0


SmartEssDataDictionary = {
    "grid_voltage": -1,
    "grid_frequency": -1,
    "ac_output_voltage": -1,
    "ac_output_frequency": -1,
    "ac_output_active_power": -1,
    "ac_output_load_percent": -1,
    "battery_voltage": -1,
    "battery_charging_current": -1,
    "battery_capacity": -1,
    "battery_discharge_current": -1,
    "pv_input_current_for_battery": -1,
    "pv_input_voltage": -1,
    "pv_charging_power": -1,
}

def mapdata(devdata:SmartESS.DeviceStatus):
    SmartEssDataDictionary["grid_voltage"] =devdata.gd_status.voltage
    SmartEssDataDictionary["grid_frequency"] =devdata.gd_status.freq
    SmartEssDataDictionary["ac_output_voltage"] =devdata.bc_status.voltage
    SmartEssDataDictionary["ac_output_frequency"] =devdata.bc_status.freq
    SmartEssDataDictionary["ac_output_active_power"] =devdata.bc_status.power
    SmartEssDataDictionary["ac_output_load_percent"] =devdata.bc_status.load
    SmartEssDataDictionary["battery_voltage"] =devdata.bt_status.voltage
    SmartEssDataDictionary["battery_charging_current"] =devdata.bt_status.chargingcurrent
    SmartEssDataDictionary["battery_capacity"] =devdata.bt_status.capacity
    SmartEssDataDictionary["battery_discharge_current"] =devdata.bt_status.dischargecurent
    SmartEssDataDictionary["pv_input_current_for_battery"] =devdata.pv_status.current
    SmartEssDataDictionary["pv_input_voltage"] =devdata.pv_status.voltage
    SmartEssDataDictionary["pv_charging_power"] =devdata.pv_status.power

class EntityInput:
    """Provides input for the entity template"""

    do_update = False
    entitiy_name = ""
    varname = ""
    icon = ""
    picture = ""
    dev_class = ""
    dev_state_class = ""
    dev_unit = ""
    multiplier = 0

    def __init__(
        self,
        doUpdate,
        eName,
        vName,
        icon,
        picture,
        dev_class,
        dev_state_class,
        dev_unit,
        multiplier,
    ) -> None:
        self.do_update = doUpdate
        self.entitiy_name = eName
        self.varname = vName
        self.icon = icon
        self.picture = picture
        self.dev_class = dev_class
        self.dev_state_class = dev_state_class
        self.dev_unit = dev_unit
        self.multiplier = multiplier
