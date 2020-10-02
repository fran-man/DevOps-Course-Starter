from trello_utils import CARD_DONE_STATUS, CARD_TODO_STATUS, CARD_DOING_STATUS, ISO_TIMESTAMP_FORMAT
from datetime import date


def is_done_today(card):
    dt_today = date.today()
    today_start = dt_today.strftime(ISO_TIMESTAMP_FORMAT)
    today_end = dt_today.replace(day=dt_today.day + 1).strftime(ISO_TIMESTAMP_FORMAT)
    return (card.status == CARD_DONE_STATUS) \
           and (today_start <= card.last_modified) \
           and (today_end > card.last_modified)


def is_done_before_day(card):
    dt_today = date.today()
    today_start = dt_today.strftime(ISO_TIMESTAMP_FORMAT)
    return (card.status == CARD_DONE_STATUS) \
           and (card.last_modified < today_start)


class TodoListViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def items_todo(self):
        todo_items = list(filter(lambda x: x.status == CARD_TODO_STATUS, self._items))
        return todo_items

    @property
    def items_done(self):
        done_items = list(filter(lambda x: x.status == CARD_DONE_STATUS, self._items))
        return done_items

    @property
    def items_doing(self):
        doing_items = list(filter(lambda x: x.status == CARD_DOING_STATUS, self._items))
        return doing_items

    @property
    def items_done_all(self):
        done_items = list(filter(lambda x: x.status == CARD_DONE_STATUS, self._items))
        return done_items

    @property
    def items_done_today(self):
        done_today_items = list(filter(lambda x: is_done_today(x), self._items))
        return done_today_items

    @property
    def items_done_before_today(self):
        done_items = list(filter(lambda x: is_done_before_day(x), self._items))
        return done_items
