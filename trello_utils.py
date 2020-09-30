import os
import requests

TRELLO_KEY = os.environ.get('TRELLO_KEY')
TRELLO_TKN = os.environ.get('TRELLO_TKN')

TRELLO_BOARD = '5f48fa1737fa77134ffe1e17'
TRELLO_TODO_LIST = '5f48fa17b70abe80f7f0942d'
TRELLO_DONE_LIST = '5f48fa17d5f15e744c86a725'
TRELLO_URL_BASE = 'https://api.trello.com/1/'

CARD_DONE_STATUS = 'Done!'
CARD_TODO_STATUS = 'To-do'
CARD_DOING_STATUS = 'Doing'

def mapTrelloCardsToLocalRepresentation(trello_cards):
    card_list = []
    for card in trello_cards:
        card_list.append(Card(
            card['id'],
            card['name'],
            getCardStatus(card['id'])
        ))
    card_list.sort(key=cardComparator)
    print(card_list)
    return card_list


def cardComparator(c):
    return 1 if c.status == CARD_DONE_STATUS else 0


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
    def __init__(self, id, name, status):
        self.id = id
        self.status = status
        self.name = name

