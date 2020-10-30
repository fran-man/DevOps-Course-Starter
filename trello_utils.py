import os
import requests

TRELLO_KEY = os.environ.get('TRELLO_KEY')
TRELLO_TKN = os.environ.get('TRELLO_TKN')

DEFAULT_PARAMS = {'key': TRELLO_KEY, 'token': TRELLO_TKN}

TRELLO_BOARD = os.environ.get('TRELLO_BOARD')
TRELLO_URL_BASE = 'https://api.trello.com/1/'

ISO_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

CARD_DONE_STATUS = 'Done!'
CARD_TODO_STATUS = 'To-do'
CARD_DOING_STATUS = 'Doing'

def mapTrelloCardsToLocalRepresentation(trello_cards):
    card_list = []
    for card in trello_cards:
        card_list.append(Card(
            card['id'],
            card['name'],
            getCardStatus(card['id']),
            card['dateLastActivity']
        ))
    card_list.sort(key=cardComparator)
    print(card_list)
    return card_list


def cardComparator(c):
    return 1 if c.status == CARD_DONE_STATUS else 0


def cardComparatorId(c):
    return int(c.id)


def cardComparatorTimestamp(c):
    return c.last_modified


def getCardStatus(card_id):
    params = {'key': TRELLO_KEY, 'token': TRELLO_TKN}
    list_name = requests.get(TRELLO_URL_BASE + 'cards/' + card_id + '/list', data=params).json()['name']
    if list_name == 'Done':
        return CARD_DONE_STATUS
    elif list_name == 'Doing':
        return CARD_DOING_STATUS
    else:
        return CARD_TODO_STATUS


class Card:
    def __init__(self, id, name, status, last_modified):
        self.id = id
        self.status = status
        self.name = name
        self.last_modified = last_modified

