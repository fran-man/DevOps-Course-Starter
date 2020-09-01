import os
import requests

TRELLO_KEY = os.environ.get('TRELLO_KEY')
TRELLO_TKN = os.environ.get('TRELLO_TKN')

TRELLO_BOARD = '5f48fa1737fa77134ffe1e17'
TRELLO_TODO_LIST = '5f48fa17b70abe80f7f0942d'
TRELLO_DONE_LIST = '5f48fa17d5f15e744c86a725'
TRELLO_URL_BASE = 'https://api.trello.com/1/'

LOCAL_CARDS = []


def trimCardsList(trello_cards):
    for card in trello_cards:
        updateOrAddCard(Card(
            card['id'],
            card['name'],
            getCardStatus(card['id'])
        ))
    return LOCAL_CARDS


def getCardStatus(card_id):
    params = {'key': TRELLO_KEY, 'token': TRELLO_TKN}
    board_name = requests.get(TRELLO_URL_BASE + 'cards/' + card_id + '/list', data=params).json()['name']
    return 'Done!' if board_name == 'Done' else 'To-do'


class Card:
    def __init__(self, id, name, status):
        self.id = id
        self.status = status
        self.name = name


def updateOrAddCard(card):
    result = filter(lambda x: x.id == card.id, LOCAL_CARDS)
    if len(result) > 0:
        result[0].status = card.status
        result[0].name = card.name
    else:
        LOCAL_CARDS.append(card)
