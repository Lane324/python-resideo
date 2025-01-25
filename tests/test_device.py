"""Tests device."""

import datetime
from unittest import mock

import pytest
import requests

from resideo import device


@pytest.fixture
def mockThermostat() -> device.Thermostat:
    """Creates mock Thermostat object."""
    oauthToken = mock.sentinel.oauthToken
    refreshToken = mock.sentinel.refreshToken
    apiKey = mock.sentinel.apiKey
    locationId = mock.sentinel.locationId
    accessToken = mock.sentinel.accessToken
    deviceID = mock.sentinel.deviceID

    return device.Thermostat(
        oauthToken=oauthToken,
        refreshToken=refreshToken,
        apiKey=apiKey,
        locationId=locationId,
        accessToken=accessToken,
        deviceID=deviceID,
    )


def test_creatingDeviceSuccedes():
    """Tests creating a Device succedes."""
    oauthToken = mock.sentinel.oauthToken
    refreshToken = mock.sentinel.refreshToken
    apiKey = mock.sentinel.apiKey
    locationId = mock.sentinel.locationId
    accessToken = mock.sentinel.accessToken

    device.Device(
        oauthToken=oauthToken,
        refreshToken=refreshToken,
        apiKey=apiKey,
        locationId=locationId,
        accessToken=accessToken,
    )


def test_creatingThermostatSuccedes(mockThermostat: device.Thermostat):
    """Tests creating a Thermostat succedes."""
    assert isinstance(mockThermostat, device.Thermostat)


def test_creatingThermostatWithWrongKeyWordErrors():
    """Tests creating a Thermostat succedes."""
    oauthToken = mock.sentinel.oauthToken
    refreshToken = mock.sentinel.refreshToken
    apiKey = mock.sentinel.apiKey
    locationId = mock.sentinel.locationId
    accessToken = mock.sentinel.accessToken

    with pytest.raises(AttributeError):
        device.Thermostat(
            oauthToken=oauthToken,
            refreshToken=refreshToken,
            apiKey=apiKey,
            locationId=locationId,
            accessToken=accessToken,
            badArg=mock.sentinel.arg,
        )


def test_creatingThermostatConvertsDatetime():
    """Tests creating a Thermostat converts deviceRegistrationDate to datetime."""
    oauthToken = mock.sentinel.oauthToken
    refreshToken = mock.sentinel.refreshToken
    apiKey = mock.sentinel.apiKey
    locationId = mock.sentinel.locationId
    accessToken = mock.sentinel.accessToken
    date = datetime.datetime.now().isoformat()

    thermostat = device.Thermostat(
        oauthToken=oauthToken,
        refreshToken=refreshToken,
        apiKey=apiKey,
        locationId=locationId,
        accessToken=accessToken,
        deviceRegistrationDate=date,
    )

    assert isinstance(thermostat.deviceRegistrationDate, datetime.datetime)


def test_settingTempMakesCorrectApiCall(mockThermostat: device.Thermostat, monkeypatch):
    """Tests that setting the thermostat temp and mode makes correct request."""
    mockRequests = mock.create_autospec(requests)
    monkeypatch.setattr(device, "requests", mockRequests)

    mode = "Cool"
    temp = 70
    headers = {
        "Authorization": f"Bearer {mockThermostat.accessToken}",
        "Content-Type": "application/json",
    }

    json_data = {
        "mode": mode,
        "autoChangeoverActive": True,
        "heatSetpoint": 66,
        "coolSetpoint": temp,
        "thermostatSetpointStatus": "TemporaryHold",
    }
    params = {
        "apikey": mockThermostat.apiKey,
        "locationId": mockThermostat.locationId,
    }

    mockThermostat.setTemp(temp=temp, mode=mode)

    assert mockRequests.post.call_count == 1
    mockRequests.post.assert_called_once_with(
        f"https://api.honeywellhome.com/v2/devices/thermostats/{mockThermostat.deviceID}",
        params=params,
        headers=headers,
        json=json_data,
    )


def test_changingThermostatToInvalidModeErrors(mockThermostat: device.Thermostat, monkeypatch):
    """Tests changing the mode to a mode that does not exists raises error."""
    mockRequests = mock.create_autospec(requests)
    monkeypatch.setattr(device, "requests", mockRequests)

    mode = mock.sentinel.mode

    with pytest.raises(ValueError):
        mockThermostat.setTemp(temp=70, mode=mode)
