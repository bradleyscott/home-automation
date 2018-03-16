import asyncio
import logging

from homeassistant.components.konnected import (DOMAIN, PIN_TO_ZONE)
from homeassistant.helpers.entity import ToggleEntity

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['konnected']


@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    if discovery_info is None:
        return

    data = hass.data[DOMAIN]
    device_id = discovery_info['device_id']
    client = data['devices'][device_id]['client']
    actuators = [KonnectedActuator(device_id, pin_num, pin_data, client)
                 for pin_num, pin_data in data['devices'][device_id]['actuators'].items()]
    async_add_devices(actuators, True)


class KonnectedActuator(ToggleEntity):
    def __init__(self, device_id, pin_num, data, client):
        # This device's config and state only (shared with the global data object)
        self._data = data
        self._device_id = device_id
        self._pin_num = pin_num
        self._state = self._data.get('state')
        self._name = self._data.get('name', 'Konnected {} Actuator {}'.format(device_id, PIN_TO_ZONE[pin_num]))
        self._data['entity'] = self
        self._client = client
        _LOGGER.info('Created new sensor: %s', self._name)

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        """Return the status of the sensor."""
        return self._state

    def turn_on(self, **kwargs):
        self._client.put_device(self._pin_num, 1)
        self._set_state(True)

    def turn_off(self, **kwargs):
        self._client.put_device(self._pin_num, 0)
        self._set_state(False)

    def _set_state(self, state):
        self._state = state
        self._data['state'] = state
        self.schedule_update_ha_state()
        _LOGGER.info('Setting status of %s actuator pin %s to %s', self._device_id, self.name, state)

    @asyncio.coroutine
    def async_set_state(self, state):
        self._state = state
        self._data['state'] = state
        self.async_schedule_update_ha_state()
        _LOGGER.info('Setting status of %s actuator pin %s to %s', self._device_id, self.name, state)