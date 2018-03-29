

"""
Support for IntesisHome Smart AC Controllers
Based on the work of https://github.com/jnimmo
"""
import logging
# from datetime import timedelta
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
# from homeassistant.util import Throttle
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.components import persistent_notification

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'intesishome'
REQUIREMENTS = ['pyIntesisHome==0.4']

controller = None
hass = None
    
# MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=180)

def setup(hass, config):
    """Setup IntesisHome platform."""
    global controller
    from pyintesishome import IntesisHome

    #Been intending to fix this up to ingest from config.
    _user = "XXXXXX"
    _pass = "XXXXXX"

    if controller is None:
        controller = IntesisHome(_user,_pass, hass.loop)
        controller.connect()

    # This was causing duplicate entities
    # hass.async_add_job(async_load_platform(hass, 'climate', DOMAIN))

    if controller.error_message:
        persistent_notification.create(hass, controller.error_message, "IntesisHome Error", 'intesishome')

    return True


def stop_intesishome():
    controller.stop()


def get_devices():
    return controller.get_devices()

