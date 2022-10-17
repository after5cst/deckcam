"""
conftest.py
"""
import pytest


@pytest.fixture
def streamdeck_url():
    return "http://127.0.0.1:8888"
