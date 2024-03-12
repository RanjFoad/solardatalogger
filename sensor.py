from __future__ import annotations
from datetime import datetime
from homeassistant.helpers.entity import Entity

import model
from model import SmartEssDataDictionary,EntityInput

from SmartESS import *
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import requests
import json
import logging
from pprint import pformat

all_status = DeviceStatus()
smartess=None
DEVICE_DOMAIN = "meter"
_LOGGER = logging.getLogger(__name__)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the SMARTESS platform."""
    # Add devices
    username = config.get("username")
    password = config.get("password")
    server_url = config.get("host")
    smartess=SmartESS(username,password)
    _LOGGER.info(pformat(config))

    sensors = getitem()

    for data in sensors:
        add_entities([SMartEssSensorTemplate(data)])

class SMartEssSensorTemplate(SensorEntity):
    """Representation of a Sensor(Template)."""

    _attr_name = ""
    _update = False
    _var_name = ""
    _attr_icon = "mdi:lightning-bolt-circle"
    _attr_entity_picture: str | None
    _attr_native_unit_of_measurement: str | None
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _multiplier = 0

    def __init__(self, entityinfo: EntityInput) -> None:
        self._update = entityinfo.do_update
        self._attr_name = entityinfo.entitiy_name
        self._var_name = entityinfo.varname
        self._attr_icon = entityinfo.icon
        self._attr_entity_picture = entityinfo.picture
        self._attr_device_class = entityinfo.dev_class
        self._attr_state_class = entityinfo.dev_state_class
        self._attr_native_unit_of_measurement = entityinfo.dev_unit
        self._multiplier = entityinfo.multiplier
        self.update()

        super().__init__()

    def update(self) -> None:
        """Update Smart Meter readings."""

        if self._update:
            _LOGGER.info("Getting an update from LUNA Server")
            global all_status
            global smartess
            all_status = smartess.getdevicestatus(0)
            model.mapdata(all_status)
            # self.syncdata()

    def geticon(self, dataelement: str, value) -> str:
        """Conditional icon based on value, when needed"""
        if dataelement == "Type" and value == "Generator":
            return "mdi:lightning-bolt-circle"
        if dataelement == "Type" and value == "PowerGrid":
            return "mdi:home-lightning-bolt-outline"
        return ""

    @property
    def state(self):
        """Return the state of the sensor."""
        global all_status
        global SmartEssDataDictionary
        if self._var_name.substr(0,2)=="ac":
            tmpvar = all_status.bc_status
        if self._multiplier != 0:
            return SmartEssDataDictionary[self._var_name] * self._multiplier
        return SmartEssDataDictionary[self._var_name]

    # entity id is required if the name use other characters not in ascii
    @property
    def entity_id(self):
        """Return the unique id of the switch."""
        entity_id = "{}.{}".format(DOMAIN, self._attr_name.replace(" ", "")).lower()
        return entity_id

    @property
    def entity_picture(self):
        return self._attr_entity_picture

    @property
    def icon(self):
        """Return the icon."""
        if self._var_name == "Type":
            return self.geticon(dataelement=self._var_name, value=self.state)
        return self._attr_icon

    # def syncdata(self):
        # LunaDataDictionary["Type"] = all_status._Type
        # LunaDataDictionary["Currency"] = all_status._Currency
        # LunaDataDictionary["MeterNo"] = all_status._MeterNo
        # LunaDataDictionary["ReadDate"] = all_status._ReadDate
        # LunaDataDictionary["TotalIndex"] = all_status._TotalIndex
        # LunaDataDictionary["GeneratorKwh"] = all_status._GeneratorKwh
        # LunaDataDictionary["GeneratorIndex"] = all_status._GeneratorIndex
        # LunaDataDictionary["GeneratorBalance"] = all_status._GeneratorBalance
        # LunaDataDictionary["GeneratorUnitPrice"] = all_status._GeneratorUnitPrice
        # LunaDataDictionary["PowerLineIndex"] = all_status._PowerLineIndex
        # LunaDataDictionary["PowerLineKwh"] = all_status._PowerLineKwh
        # LunaDataDictionary["PowerLineBalance"] = all_status._PowerLineBalance
        # LunaDataDictionary["PowerLineUnitPrice"] = all_status._PowerLineUnitPrice

def getitem()->list:
    itemlist=list()
    with open('sensors.json') as sensor_file:

        sensors = json.load(sensor_file)
    for item in sensors:
        tmpitem=EntityInput(doUpdate=item["doupdate"].lower(),eName=item["name"],vName=item["vname"],icon=item["icon"],picture="",dev_class=item["devclass"],dev_state_class=item["statclass"],dev_unit=item["unit"],multiplier=item["multi"])
        itemlist.append(tmpitem)
    return itemlist