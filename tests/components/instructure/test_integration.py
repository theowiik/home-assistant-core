"""Tests for integrations of modules."""


from unittest.mock import MagicMock

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


async def test_integration_different_modules(
    hass: HomeAssistant,
    mock_api: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test sensors."""
    assert mock_config_entry.state == ConfigEntryState.LOADED
    assert mock_config_entry.domain == "instructure"
    mock_api.access_token = "mock_access_token"
    mock_api.host = "https://chalmers.instructure.com/api/v1"

    coordinator = hass.data["instructure"][mock_config_entry.entry_id]["coordinator"]
    coordinator.api = mock_api

    assert coordinator.selected_courses is mock_config_entry.options["courses"]
    assert coordinator.api.access_token == "mock_access_token"
    assert coordinator.api.host == "https://chalmers.instructure.com/api/v1"
    assert coordinator.config_entry is mock_config_entry

    assert mock_config_entry.domain == "instructure"
