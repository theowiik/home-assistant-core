from homeassistant.core import CoreState, HomeAssistant
from unittest.mock import MagicMock

import pytest

from homeassistant.components.instructure.config_flow import get_courses_names
from homeassistant.components.instructure.calendar import CanvasCalendarEntity

from homeassistant.components.instructure.const import DOMAIN, HOST_PREFIX, ACCESS_TOKEN, CONF_COURSES, ASSIGNMENTS_KEY
from homeassistant.core import HomeAssistant

from pytest_httpx import HTTPXMock # add HTTPXMock to requirements!
from tests.common import MockConfigEntry, patch

# async def test_async_setup_entry(hass: HomeAssistant) -> None:
#     """Test async_setup_entry."""
#     assert hass.state is CoreState.running
#     entry = MockConfigEntry(
#         domain=DOMAIN,
#         data={
#             HOST_PREFIX: "chalmers",
#             ACCESS_TOKEN: "test_access_token",
#         },
#         options={
#             CONF_COURSES: {
#                 "12345": "Test Course 1",
#                 "67890": "Test Course 2"
#             }
#         },
#         title="Canvas"
#     )

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