"""Tests config."""

from unittest import mock

import pytest

from resideo import config


def test_creatingAConfigCreatesValidConfig():
    """Tests that creating a configuration succedes."""
    config.Config(faceRecognition={mock.sentinel.str: mock.sentinel.bool})


def test_creatingAConfigWithWrongKeyWordErrors():
    """Tests that creating a configuration with incorrect keyword errors."""
    with pytest.raises(AttributeError):
        config.Config(badArg=mock.sentinel.arg)
