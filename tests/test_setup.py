"""Tests pour l'intégration Bbox2 utilisant config_entries."""

from typing import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant

from custom_components.bbox.const import CONF_INCLUDE_OTHER_DEVICES


@pytest.mark.asyncio
async def test_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    router: Generator[AsyncMock | MagicMock],
) -> None:
    """Test du setup via une config entry."""

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state == ConfigEntryState.LOADED


@pytest.mark.asyncio
async def test_setup_entry_without_devices(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    router: Generator[AsyncMock | MagicMock],
) -> None:
    """Test the setup does not call the devices endpoint when disabled."""

    config_entry.options = {CONF_INCLUDE_OTHER_DEVICES: False}

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    router.return_value.lan.async_get_connected_devices.assert_not_called()
