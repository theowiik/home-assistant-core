"""Test the canvas config flow."""
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant import config_entries
from homeassistant.components.instructure.config_flow import CannotConnect, InvalidAuth
from homeassistant.components.instructure.const import DOMAIN, HOST_PREFIX, ACCESS_TOKEN, CONF_COURSES
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from tests.test_util.aiohttp import AiohttpClientMocker

from pytest_httpx import HTTPXMock # add aioresponse to requirements!

TEST_ACCESS_TOKEN = "test_access_token"
TEST_HOST_PREFIX = "chalmers"

pytestmark = pytest.mark.usefixtures("mock_setup_entry")

@pytest.mark.asyncio
async def test_sucessful_flow(
    hass: HomeAssistant,
    httpx_mock: HTTPXMock
) -> None:
    """Test the successful config flow from start to finish."""
    httpx_mock.add_response(
        method="GET",
        url=f"https://{TEST_HOST_PREFIX}.instructure.com/api/v1/courses?",
        headers={"Authorization": f"Bearer {TEST_ACCESS_TOKEN}"},
        status_code=200,
        json={"test_response_key": "test_response_value"}
    )

    httpx_mock.add_response(
        method="GET",
        url=f"https://{TEST_HOST_PREFIX}.instructure.com/api/v1/courses?per_page=50",
        headers={"Authorization": f"Bearer {TEST_ACCESS_TOKEN}"},
        status_code=200,
        json=[
            {
            "name": "Test Course 1",
            "id": 12345,
            },
            {
            "name": "Test Course 2",
            "id": 67890,
            },
        ]
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER}
    )

    assert result["step_id"] == "user"
    assert result["type"] == "form"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            HOST_PREFIX: TEST_HOST_PREFIX,
            ACCESS_TOKEN: TEST_ACCESS_TOKEN,
        }
    )
    assert result["step_id"] == "courses"
    assert result["type"] == "form"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input= {
            CONF_COURSES: ["Test Course 1", "Test Course 2"]
        }
    )
    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "Canvas"
    assert "data" in result
    assert result["data"][HOST_PREFIX] == TEST_HOST_PREFIX
    assert result["data"][ACCESS_TOKEN] == TEST_ACCESS_TOKEN
    assert "options" in result
    assert CONF_COURSES in result["options"]
    assert result["options"][CONF_COURSES] == {
        12345: "Test Course 1",
        67890: "Test Course 2",
    }


# async def test_form(hass: HomeAssistant, mock_setup_entry: AsyncMock) -> None:
#     """Test we get the form."""
#     result = await hass.config_entries.flow.async_init(
#         DOMAIN, context={"source": config_entries.SOURCE_USER}
#     )
#     assert result["type"] == FlowResultType.FORM
#     assert result["errors"] is None

#     with patch(
#         "homeassistant.components.instructure.config_flow.PlaceholderHub.authenticate",
#         return_value=True,
#     ):
#         result2 = await hass.config_entries.flow.async_configure(
#             result["flow_id"],
#             {
#                 "host": "1.1.1.1",
#                 "username": "test-username",
#                 "password": "test-password",
#             },
#         )
#         await hass.async_block_till_done()

#     assert result2["type"] == FlowResultType.CREATE_ENTRY
#     assert result2["title"] == "Name of the device"
#     assert result2["data"] == {
#         "host": "1.1.1.1",
#         "username": "test-username",
#         "password": "test-password",
#     }
#     assert len(mock_setup_entry.mock_calls) == 1


# async def test_form_invalid_auth(hass: HomeAssistant) -> None:
#     """Test we handle invalid auth."""
#     result = await hass.config_entries.flow.async_init(
#         DOMAIN, context={"source": config_entries.SOURCE_USER}
#     )

#     with patch(
#         "homeassistant.components.instructure.config_flow.PlaceholderHub.authenticate",
#         side_effect=InvalidAuth,
#     ):
#         result2 = await hass.config_entries.flow.async_configure(
#             result["flow_id"],
#             {
#                 "host": "1.1.1.1",
#                 "username": "test-username",
#                 "password": "test-password",
#             },
#         )

#     assert result2["type"] == FlowResultType.FORM
#     assert result2["errors"] == {"base": "invalid_auth"}


# async def test_form_cannot_connect(hass: HomeAssistant) -> None:
#     """Test we handle cannot connect error."""
#     result = await hass.config_entries.flow.async_init(
#         DOMAIN, context={"source": config_entries.SOURCE_USER}
#     )

#     with patch(
#         "homeassistant.components.instructure.config_flow.PlaceholderHub.authenticate",
#         side_effect=CannotConnect,
#     ):
#         result2 = await hass.config_entries.flow.async_configure(
#             result["flow_id"],
#             {
#                 "host": "1.1.1.1",
#                 "username": "test-username",
#                 "password": "test-password",
#             },
#         )

#     assert result2["type"] == FlowResultType.FORM
#     assert result2["errors"] == {"base": "cannot_connect"}
