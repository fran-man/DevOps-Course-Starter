import os

TRELLO_KEY = os.environ.get('TRELLO_KEY')
TRELLO_TKN = os.environ.get('TRELLO_TKN')

MONGO_PASS = os.environ.get('MONGO_PASS')

DEFAULT_PARAMS = {'key': TRELLO_KEY, 'token': TRELLO_TKN}

TRELLO_BOARD = os.environ.get('TRELLO_BOARD')
TRELLO_URL_BASE = 'https://api.trello.com/1/'

ISO_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

CARD_DONE_STATUS = 'Done!'
CARD_TODO_STATUS = 'To-do'
CARD_DOING_STATUS = 'Doing'

MONGO_LIST_DONE = 'done_items'
MONGO_LIST_DOING = 'doing'
MONGO_LIST_TODO = 'to_do'

def mapTrelloCardsToLocalRepresentation(cards):
    all_card_list = []
    for status, status_list in cards.items():
        for card in status_list:
            all_card_list.append(Card(
                str(card['_id']),
                card['name'],
                getCardStatusFromListName(status),
                card['dateLastActivity']
            ))
    all_card_list.sort(key=cardComparator)
    print(all_card_list)
    return all_card_list


def cardComparator(c):
    return 1 if c.status == CARD_DONE_STATUS else 0


def cardComparatorId(c):
    return int(c.id)


def cardComparatorTimestamp(c):
    return c.last_modified


def getCardStatusFromListName(list_name):
    if list_name == MONGO_LIST_DONE:
        return CARD_DONE_STATUS
    elif list_name == MONGO_LIST_DOING:
        return CARD_DOING_STATUS
    else:
        return CARD_TODO_STATUS


class Card:
    def __init__(self, id, name, status, last_modified):
        self.id = id
        self.status = status
        self.name = name
        self.last_modified = last_modified

