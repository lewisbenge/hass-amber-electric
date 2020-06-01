from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.util.dt as dt_util
import voluptuous as vol
from .ambermodel import AmberData
import requests
import json
from datetime import timedelta
import base64
import logging


SCAN_INTERVAL = timedelta(minutes=5)
URL = "https://api.amberelectric.com.au/prices/listprices"
UNIT_NAME = "c/kWh"
CONF_POSTCODE = "postcode"

ATTRIBUTION = "Data provided by the Amber Electric pricing API"
ATTR_LAST_UPDATE = "last_update"
ATTR_SENSOR_ID = "sensor_id"
ATTR_POSTCODE_ID = "postcode_id"
ATTR_GRID_NAME = "grid_name"

CONST_SOLARFIT = "amberSolarFIT"
CONST_GENRALUSE = "amberGeneralUsage"

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Optional(CONF_NAME): cv.string, vol.Optional(CONF_POSTCODE): cv.string}
)


def setup_platform(hass, config, add_entities, discovery_info=None):

    postcode = config.get(CONF_POSTCODE)
    amber_data = None
    if(postcode):
        add_entities(
            [
                AmberPricingSensor(amber_data, postcode, CONST_SOLARFIT, "Amber solar feed in tariff", "mdi:solar-power"),
                AmberPricingSensor(amber_data, postcode, CONST_GENRALUSE, "Amber general usage price", "mdi:transmission-tower")
            ]
        )


class AmberPricingSensor(Entity):
    """ Entity object for Amber Electric sensor."""

    def __init__(self, amber_data, postcode, sensor_type, friendly_name, icon) :
        self.postcode = postcode
        self.amber_data = amber_data
        self.price_updated_datetime = None
        self.network_provider = None
        self.sensor_type = sensor_type
        self.friendly_name = friendly_name
        self.icon_uri = icon

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self.icon_uri

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.friendly_name

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.amber_data is None:
            return 0

        if(self.sensor_type == CONST_GENRALUSE):
            return round(
                (
                    float(self.amber_data.data.static_prices.e1.totalfixed_kwh_price)
                    + float(self.amber_data.data.static_prices.e1.loss_factor)
                    * float(
                        self.amber_data.data.variable_prices_and_renewables[
                            0
                        ].wholesale_kwh_price
                    )
                )
                / 1.1,
                2,
            )
        if(self.sensor_type == CONST_SOLARFIT):
            ## Solar FIT
            return round(
                abs((
                    float(self.amber_data.data.static_prices.b1.totalfixed_kwh_price)
                    + float(self.amber_data.data.static_prices.b1.loss_factor)
                    * float(
                        self.amber_data.data.variable_prices_and_renewables[
                            0
                        ].wholesale_kwh_price
                    )
                )
                / 1.1),
                2,
            )
        
        return 0

    @property
    def device_state_attributes(self):
        attr = {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            ATTR_LAST_UPDATE: self.price_updated_datetime,
            ATTR_SENSOR_ID:  self.sensor_type,
            ATTR_GRID_NAME: self.network_provider,
            ATTR_POSTCODE_ID: self.postcode,
        }

        return attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return UNIT_NAME

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the Amber Electric data from the REST API"""
        response = requests.post(URL, '{"postcode":"' + self.postcode + '"}')
        _LOGGER.debug(response.text)
        self.amber_data = AmberData.from_dict(json.loads(response.text))

        if self.amber_data is not None:
            self.price_updated_datetime = self.amber_data.data.variable_prices_and_renewables[
                0
            ].created_at
            self.network_provider = self.amber_data.data.network_provider

  