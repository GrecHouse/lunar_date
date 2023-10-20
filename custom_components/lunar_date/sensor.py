"""
Sensor to indicate today's lunar date.
For more details about this platform, please refer to the documentation at
https://github.com/GrecHouse/lunar_date

HA 음력센서 : 오늘의 음력 날짜를 알려줍니다.
* korean-lunar-calendar 라이브러리를 이용합니다.
"""

from datetime import timedelta
import logging

from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
import homeassistant.util.dt as dt_util
from homeassistant.helpers.event import async_track_point_in_utc_time
from korean_lunar_calendar import KoreanLunarCalendar

from .const import DOMAIN, CONF_NAME, ATTRIBUTION, MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """통합 구성요소의 sensor 플랫폼 Entry 설정"""

    if hass.config.time_zone is None:
        _LOGGER.error("Timezone is not set in Home Assistant configuration")
        return False

    device = LunarDateSensor(hass, CONF_NAME)

    async_track_point_in_utc_time(hass, device.point_in_time_listener, device.get_next_interval())

    async_add_entities([device])


class LunarDateSensor(Entity):
    """Implementation of a Time and Date sensor."""

    def __init__(self, hass, name):
        """Initialize the sensor."""
        self._name = name
        self._state = None
        self.hass = hass
        self._update_internal_state(dt_util.utcnow())

    @property
    def unique_id(self):
        """Return the entity ID."""
        return f'sensor.{DOMAIN}'

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
    def attribution(self):
        """Return the attribution."""
        return ATTRIBUTION

    @property
    def extra_state_attributes(self):
        """Return the attribute(s) of the sensor"""
        return self._attribute

    def get_next_interval(self, now=None):
        """Compute next time an update should occur."""
        if now is None:
            now = dt_util.utcnow()
        today_midnight = dt_util.start_of_local_day(dt_util.as_local(now))
        tomorrow_midnight = today_midnight + timedelta(days=1)
        _LOGGER.debug("next_interval : %s -> %s", today_midnight, today_midnight)
        return tomorrow_midnight

    def _update_internal_state(self, time_date):
        date = dt_util.as_local(time_date).date()
        calendar = KoreanLunarCalendar()
        calendar.setSolarDate(date.year, date.month, date.day)
        lunar_date = calendar.LunarIsoFormat()
        self._state = lunar_date
        self._attribute = { 'korean_gapja': calendar.getGapJaString(), 'chinese_gapja': calendar.getChineseGapJaString() }
        _LOGGER.debug("_update_internal_state : %s -> %s", date, lunar_date)

    @callback
    def point_in_time_listener(self, time_date):
        """Get the latest data and update state."""
        self._update_internal_state(time_date)
        self.async_schedule_update_ha_state()
        async_track_point_in_utc_time(
            self.hass, self.point_in_time_listener, self.get_next_interval())
