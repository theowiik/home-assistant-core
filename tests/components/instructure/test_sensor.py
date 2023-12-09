"""Tests for Instucture sensor platform."""


from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


# These logs might be beneficial for testing in sensors. Because it says the name of the sensor.
# sensor.test_assignment
# sensor.test_announcement
# sensor.test_conversation
# sensor.assignment_1
# Registered new calendar.instructure entity: calendar.canvas_calendar_assignments
# Is it creating two assignment sensor and no grade?
# TODO ADD CALENDAR sensor somewhere maybe in __init__.py
# TODO Understand why there is two assignment sensor
# TODO add grade and quick links entity.
async def test_sensor(
    hass: HomeAssistant, mock_api: MagicMock, mock_config_entry: MockConfigEntry
) -> None:
    """Test sensors."""
    # print(
    #     hass.data[DOMAIN]["0797477940f9f91760ab6051d3fb0df0"]["entities"][
    #         "assignments"
    #     ]["assignment-1"]
    # )
    # print(hass.states.get("sensor.assignment_1").state)


# def print_hass(hass: HomeAssistant):
#     """Print HASS object."""
#     print_dict_separately(hass.data)

#     print("\n state")
#     print(hass.state)

#     print("\n states")
#     print(hass.states)

#     print("\n data instructure")
#     print(hass.data["instructure"])

#     print("\n data entity_registry")
#     print(hass.data["entity_registry"])

#     print("\n data component")
#     print(hass.data["components"]["instructure"])


# def print_entry(mock_config_entry: MockConfigEntry):
#     """Print Entry object."""
#     print(f"\n Domain: {mock_config_entry.domain}")
#     print(f"\n Entry ID: {mock_config_entry.entry_id}")
#     print(f"\n State: {mock_config_entry.state}")
#     print("\n Entry data:")
#     print(mock_config_entry.data)
#     print("\n Entry options:")
#     print(mock_config_entry.options)

# def print_dict_separately(data_dict):
#     """Print hass data ."""
#     for key, value in data_dict.items():
#         print(f"{key}: {value}")
