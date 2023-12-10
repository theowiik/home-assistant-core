from homeassistant.core import CoreState, HomeAssistant
from unittest.mock import MagicMock

import pytest

from homeassistant.components.instructure.calendar import CanvasCalendarEntity, async_setup_entry

from homeassistant.components.instructure.const import DOMAIN, HOST_PREFIX, ACCESS_TOKEN, CONF_COURSES, ASSIGNMENTS_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from tests.common import MockConfigEntry, MockEntityPlatform, MockPlatform, MockEntity

async def test_async_setup_entry(hass: HomeAssistant, ) -> None:
    """Test async_setup_entry."""
    assert hass.state is CoreState.running
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            HOST_PREFIX: "chalmers",
            ACCESS_TOKEN: "test_access_token",
        },
        options={
            CONF_COURSES: {
                "12345": "Test Course 1",
                "67890": "Test Course 2"
            }
        },
        title="Canvas"
    )
    entry.add_to_hass(hass)
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    hass.data[DOMAIN][entry.entry_id]["coordinator"] = MagicMock()

    assert DOMAIN in hass.data
    
    fake_async_add_entities = MagicMock()
    await async_setup_entry(hass, entry, fake_async_add_entities)
    await hass.async_block_till_done()
    assert fake_async_add_entities.called == True

@pytest.mark.parametrize(
    "assignment_data, start, end, output_length",
    [
        (
            {
                "12345": {
                    "name": "Test Course 1",
                    "due_at": "2023-12-10T10:59:59Z",
                    "html_url": "test_html_url_1"
                },
                "67890": {
                    "name": "Test Course 2",
                    "due_at": "2023-12-10T18:59:59Z",
                    "html_url": "test_html_url_2"
                },
            },
            "2023-12-09T10:59:59Z",
            "2023-12-11T10:59:59Z",
            2
        ),
        (
            {
                "12345": {
                    "name": "Test Course 1",
                    "due_at": "2023-12-10T10:59:59Z",
                    "html_url": "test_html_url_1"
                },
                "67890": {
                    "name": "Test Course 2",
                    "due_at": "2023-12-10T18:59:59Z",
                    "html_url": "test_html_url_2"
                },
            },
            "2023-12-09T10:59:59Z",
            "2023-12-09T17:59:59Z",
            0
        ),
        (
            {
                "12345": {
                    "name": "Test Course 1",
                    "due_at": "2023-12-10T10:59:59Z",
                    "html_url": "test_html_url_1"
                },
                "67890": {
                    "name": "Test Course 2",
                    "due_at": "2023-12-17T18:59:59Z",
                    "html_url": "test_html_url_2"
                },
            },
            "2023-12-09T10:59:59Z",
            "2023-12-11T10:59:59Z",
            1
        ),
        (
            {
                "12345": {
                    "due_at": "2023-12-10T10:59:59Z",
                    "html_url": "test_html_url_1"
                },
                "67890": {
                    "name": "Test Course 2",
                    "due_at": "2023-12-10T18:59:59Z",
                    "html_url": "test_html_url_2"
                },
            },
            "2023-12-09T10:59:59Z",
            "2023-12-11T10:59:59Z",
            2
        ),
        (
            {
                "12345": {
                    "name": "Test Course 1",
                    "due_at": "2023-12-10T10:59:59Z",
                    "html_url": "test_html_url_1"
                },
                "67890": {
                    "name": "Test Course 2",
                    "due_at": "2023-12-10T18:59:59Z",
                },
            },
            "2023-12-09T10:59:59Z",
            "2023-12-11T10:59:59Z",
            2
        ),
        (
            {
                "12345": {
                    "name": "Test Course 1",
                    "due_at": "2023-12-10T10:59:59Z",
                    "html_url": "test_html_url_1"
                },
                "67890": {
                    "name": "Test Course 2",
                    "due_at": "2023-12-10T18:59:59Z",
                    "html_url": "",
                },
            },
            "2023-12-09T10:59:59Z",
            "2023-12-11T10:59:59Z",
            2
        ),
    ]
)
async def test_async_get_events(
    hass: HomeAssistant,
    assignment_data: dict,
    start: str,
    end: str,
    output_length: int
) -> None:
    coordinator = MagicMock()
    coordinator.configure_mock(data={ASSIGNMENTS_KEY: assignment_data})

    canvas_calendar = CanvasCalendarEntity(hass, coordinator, "test_entity_id")
    start_date = canvas_calendar.parse_date(start)
    end_date = canvas_calendar.parse_date(end)
    event_list = await canvas_calendar.async_get_events(hass, start_date, end_date)
    assert len(event_list) == output_length
    for event in event_list:
        assert event.summary != ""
        assert event.description != ""