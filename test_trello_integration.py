import os

from flask import json

import pytest
from bson.objectid import ObjectId
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
    monkeypatch.setattr('pymongo.MongoClient', mock_mongo)
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


class MockMongoCollection:
    def __init__(self, name):
        self.name = name

    def find(self):
        print(self.name)
        return [{
            '_id': ObjectId('607ebb23beec53b28f23b194'),
            'name': self.name,
            'dateLastActivity': '2021-04-20T13:51:44.000000'
        }]


def mock_mongo(*args, **kwargs):
    return {'DevopsEx': {'to_do': MockMongoCollection('card1'),
                         'doing': MockMongoCollection('card2'),
                         'done_items': MockMongoCollection('card3')
                         }}


def example_repsponse():
    with open('cards_example_response.json', 'r') as file:
        content = file.read()
    return json.loads(content)
