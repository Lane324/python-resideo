import datetime
import inspect
from typing import Literal

import requests

import resideo


class Device:
    """
    Contains data about a device.
    """

    baseUrl: str = resideo.BASE_URL
    oauthToken: str
    refreshToken: str
    apiKey: str
    locationId: str
    accessToken: str

    def __init__(
        self,
        oauthToken: str,
        refreshToken: str,
        apiKey: str,
        locationId: str,
        accessToken: str,
    ):
        self.oauthToken = oauthToken
        self.refreshToken = refreshToken
        self.apiKey = apiKey
        self.locationId = locationId
        self.accessToken = accessToken


class Thermostat(Device):
    """
    Contains data about a thermostat.
    """

    displayedOutdoorHumidity: int
    vacationHold: dict[str, bool]
    currentSchedulePeriod: dict[str, str]
    scheduleCapabilities: dict[str, list[str] | bool]
    scheduleType: dict[str, str]
    changeSource: dict[str, str]
    scheduleStatus: str
    allowedTimeIncrements: int
    settings: dict[
        str,
        bool
        | dict[str, int]
        | dict[str, str | int | bool]
        | dict[str, list[str] | dict[str, str] | dict[str, bool]],
    ]
    deviceOsVersion: str
    deviceClass: str
    deviceType: str
    deviceID: str
    deviceInternalID: int
    userDefinedDeviceName: str
    name: str
    isAlive: bool
    isUpgrading: bool
    isProvisioned: bool
    macID: str
    deviceSettings: dict
    service: dict[str, str]
    deviceRegistrationDate: datetime.datetime
    dataSyncStatus: str
    deviceSerialNo: str
    units: str
    indoorTemperature: int
    outdoorTemperature: int
    allowedModes: list[str]
    deadband: int
    hasDualSetpointStatus: bool
    minHeatSetpoint: int
    maxHeatSetpoint: int
    minCoolSetpoint: int
    maxCoolSetpoint: int
    changeableValues: dict[str, str | int]
    operationStatus: dict[str, str | bool]
    deviceModel: str

    def __init__(
        self,
        oauthToken: str,
        refreshToken: str,
        apiKey: str,
        locationId: str,
        accessToken: str,
        **kwargs,
    ):
        super().__init__(
            oauthToken=oauthToken,
            refreshToken=refreshToken,
            apiKey=apiKey,
            locationId=locationId,
            accessToken=accessToken,
        )
        for key, value in kwargs.items():
            if inspect.get_annotations(type(self)).get(key) == datetime.datetime:
                setattr(
                    self, key, datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                )
            elif key not in inspect.get_annotations(type(self)):
                raise AttributeError
            else:
                setattr(self, key, value)

    def setTemp(self, temp: int, mode: Literal["Heat", "Cool"]):
        """Sets temp."""
        possibleModes = ("Heat", "Cool")
        if mode not in possibleModes:
            raise ValueError(
                f"Invalide mode of {mode}. Must be {possibleModes[0]} or {possibleModes[1]}."
            )
        if not self.deviceType == "Thermostat":
            raise ValueError("Device is not a thermostat.")

        headers = {
            "Authorization": f"Bearer {self.accessToken}",
            "Content-Type": "application/json",
        }

        json_data = {
            "mode": mode,
            "autoChangeoverActive": True,
            "heatSetpoint": temp if mode == "Heat" else 66,
            "coolSetpoint": temp if mode == "Cool" else 74,
            "thermostatSetpointStatus": "TemporaryHold",
        }
        params = {
            "apikey": self.apiKey,
            "locationId": self.locationId,
        }

        response = requests.post(
            f"https://api.honeywellhome.com/v2/devices/thermostats/{self.deviceID}",
            params=params,
            headers=headers,
            json=json_data,
        )
