"""Support for Panasonic sensors."""
import logging

from homeassistant.const import CONF_ICON, CONF_NAME, TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

from . import DOMAIN as PANASONIC_DOMAIN, PANASONIC_DEVICES
from .const import ATTR_INSIDE_TEMPERATURE, ATTR_OUTSIDE_TEMPERATURE, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    
    for device in hass.data[PANASONIC_DEVICES]:
        sensors = [ATTR_INSIDE_TEMPERATURE]
        if device.support_outside_temperature:
            sensors.append(ATTR_OUTSIDE_TEMPERATURE)
        add_entities([PanasonicClimateSensor(device, sensor) for sensor in sensors])


class PanasonicClimateSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, api, monitored_state) -> None:
        """Initialize the sensor."""
        self._api = api
        self._sensor = SENSOR_TYPES[monitored_state]
        self._name = f"{api.name} {self._sensor[CONF_NAME]}"
        self._device_attribute = monitored_state

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._api.id}-{self._device_attribute}"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._sensor[CONF_ICON]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._device_attribute == ATTR_INSIDE_TEMPERATURE:
            return self._api.inside_temperature
        if self._device_attribute == ATTR_OUTSIDE_TEMPERATURE:
            return self._api.outside_temperature
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Retrieve latest state."""
        self._api.update()

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._api.device_info
