import os
import requests

TRELLO_KEY = os.environ.get('TRELLO_KEY')
TRELLO_TKN = os.environ.get('TRELLO_TKN')

TRELLO_BOARD = '5f48fa1737fa77134ffe1e17'
TRELLO_TODO_LIST = '5f48fa17b70abe80f7f0942d'
TRELLO_DONE_LIST = '5f48fa17d5f15e744c86a725'
TRELLO_URL_BASE = 'https://api.trello.com/1/'

def trimCardsList(list_of_cards):
    trimmed_result = []
    for card in list_of_cards:
        trimmed_result.append({
            'name': card['name'],
            'status': getCardStatus(card['id']),
            'id': card['id']
        })
    return trimmed_result

def getCardStatus(card_id):
    params = {'key': TRELLO_KEY, 'token': TRELLO_TKN}
    board_name = requests.get(TRELLO_URL_BASE + 'cards/' + card_id + '/list', data=params).json()['name']
    return 'Done!' if board_name == 'Done' else 'To-do'