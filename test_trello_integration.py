import os

from flask import json
from unittest.mock import patch, MagicMock

import pytest
import requests
from dotenv import find_dotenv, load_dotenv

import app


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')

    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    test_app.testing = True

    with test_app.test_client() as client:
        yield client


def test_example(client, monkeypatch):
    monkeypatch.setattr(requests, 'get', lambda url, data: mock_get(url))
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
    assert 'card1' in response.data.decode('utf-8')
    assert 'card2' in response.data.decode('utf-8')


class MockedCardsResponse:
    @staticmethod
    def json():
        with open('cards_example_response.json', 'r') as file:
            content = file.read()
        return json.loads(content)


class MockedListResponse:
    @staticmethod
    def json():
        with open('list_example.json', 'r') as file:
            content = file.read()
        return json.loads(content)


def mock_get(url):
    if url.endswith('/cards'):
        return MockedCardsResponse()
    elif url.endswith('/list'):
        return MockedListResponse()


def example_repsponse():
    with open('cards_example_response.json', 'r') as file:
        content = file.read()
    return json.loads(content)
