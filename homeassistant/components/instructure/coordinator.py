from datetime import timedelta
import logging

import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import ANNOUNCEMENTS_KEY, ASSIGNMENTS_KEY, CONVERSATIONS_KEY
from .canvas_api import CanvasAPI

_LOGGER = logging.getLogger(__name__)


class CanvasUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for the Canvas integration."""

    def __init__(self, hass, entry: ConfigEntry, api: CanvasAPI):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Canvas Sensor",
            update_interval=timedelta(seconds=30),
        )
        self.config_entry = entry
        self.api = api
        self.update_entities = None
        self.selected_courses = entry.options["courses"]

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        courses = self.selected_courses
        course_ids = courses.keys()

        try:
            async with async_timeout.timeout(10):
                assignments = await self.api.async_get_assignments(course_ids)
                announcements = await self.api.async_get_announcements(course_ids)
                conversations = await self.api.async_get_conversations()

                # TODO - filtering
                new_data = {
                    ASSIGNMENTS_KEY: assignments,
                    ANNOUNCEMENTS_KEY: announcements,
                    CONVERSATIONS_KEY: conversations,
                }

                old_data = self.data or {} #maybe put self.data={} in __init__()
                self.data = new_data

                if self.update_entities:
                    for data_type in new_data.keys():
                        self.update_entities(
                            data_type,
                            new_data.get(data_type, {}),
                            old_data.get(data_type, {}),
                        )

                return new_data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
