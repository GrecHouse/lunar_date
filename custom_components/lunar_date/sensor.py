"""
Sensor to indicate today's lunar date.
For more details about this platform, please refer to the documentation at
https://github.com/GrecHouse/lunar_date

* korean-lunar-calendar 라이브러리를 이용합니다.
에러가 발생할 경우 pip 로 설치해주세요.
https://pypi.org/project/korean-lunar-calendar/

HA 음력센서 : 오늘의 음력 날짜를 알려줍니다.
- 2019-06-24 다모아님의 요청으로 제작
- 2019-06-25 korean-lunar-calendar 를 설치하지 않고 소스에 통합함
- 2020-03-16 korean-lunar-calendar 분리
"""

from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.core import callback
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
from homeassistant.helpers.event import async_track_point_in_utc_time
from korean_lunar_calendar import KoreanLunarCalendar

import datetime

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Lunar Date'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Time and Date sensor."""
    if hass.config.time_zone is None:
        _LOGGER.error("Timezone is not set in Home Assistant configuration")
        return False

    sensor_name = config.get(CONF_NAME)
    device = LunarDateSensor(hass, sensor_name)

    async_track_point_in_utc_time(
        hass, device.point_in_time_listener, device.get_next_interval())

    async_add_entities([device], True)

class LunarDateSensor(Entity):
    """Implementation of a Time and Date sensor."""

    def __init__(self, hass, name):
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self.hass = hass
        self._update_internal_state(dt_util.utcnow())

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:calendar-star'

    @property
    def extra_state_attributes(self):
        """Return the attribute(s) of the sensor"""
        return self._attribute

    def get_next_interval(self, now=None):
        """Compute next time an update should occur."""
        if now is None:
            now = dt_util.utcnow()
        now = dt_util.start_of_local_day(dt_util.as_local(now))
        return now + timedelta(seconds=86400)

    def _update_internal_state(self, time_date):
        date = dt_util.as_local(time_date).date()
        calendar = KoreanLunarCalendar()
        calendar.setSolarDate(date.year, date.month, date.day)
        lunar_date = calendar.LunarIsoFormat()
        self._state = lunar_date
        self._attribute = { 'korean_gapja': calendar.getGapJaString(), 'chinese_gapja': calendar.getChineseGapJaString() }

    @callback
    def point_in_time_listener(self, time_date):
        """Get the latest data and update state."""
        self._update_internal_state(time_date)
        self.async_schedule_update_ha_state()
        async_track_point_in_utc_time(
            self.hass, self.point_in_time_listener, self.get_next_interval())
