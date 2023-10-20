"""Config flow for Lunar Date."""
from __future__ import annotations

import logging

from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_NAME

_LOGGER = logging.getLogger(__name__)

class LunaDateConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lunar Date."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize flow."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title=CONF_NAME, data={})

        return self.async_show_form(step_id="user")

    async def async_step_import(self, user_input: dict[str, Any]) -> FlowResult:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)
