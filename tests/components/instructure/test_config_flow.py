"""Test the canvas config flow."""
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant import config_entries
from homeassistant.components.instructure.config_flow import get_courses_names
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

async def test_flow_with_invalid_auth_failure(
    hass: HomeAssistant,
    httpx_mock: HTTPXMock
) -> None:
    """Test flow with connection failure."""
    httpx_mock.add_response(
        method="GET",
        url=f"https://{TEST_HOST_PREFIX}.instructure.com/api/v1/courses?",
        headers={"Authorization": f"Bearer {TEST_ACCESS_TOKEN}"},
        status_code=401,
        json={"test_response_key": "test_response_value"}
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
    assert result["step_id"] == "user"
    assert result["type"] == "form"

@pytest.mark.parametrize(
    "mock_config_data, expected_output",
    [
        (
            {
                HOST_PREFIX: TEST_HOST_PREFIX,
                ACCESS_TOKEN: TEST_ACCESS_TOKEN
            },
            {
                "Test Course 1": 12345,
                "Test Course 2": 67890,
            }
        ),
    ]
)
async def test_get_courses_names_with_valid_access_token(httpx_mock: HTTPXMock, mock_config_data: dict, expected_output: dict):
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

    assert await get_courses_names(mock_config_data) == expected_output

@pytest.mark.parametrize(
    "mock_config_data, expected_output",
    [
        (
            {
                HOST_PREFIX: TEST_HOST_PREFIX,
                ACCESS_TOKEN: TEST_ACCESS_TOKEN
            },
            {
                "Test Course 1": 12345,
                "Test Course 2": 67890,
            }
        ),
    ]
)
async def test_get_courses_names_with_invalid_access_token(httpx_mock: HTTPXMock, mock_config_data: dict, expected_output: dict):
    httpx_mock.add_response(
        method="GET",
        url=f"https://{TEST_HOST_PREFIX}.instructure.com/api/v1/courses?per_page=50",
        headers={"Authorization": f"Bearer {TEST_ACCESS_TOKEN}"},
        status_code=401,
        json=[]
    )

    assert await get_courses_names(mock_config_data) == {}
