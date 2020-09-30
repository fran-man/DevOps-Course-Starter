from trello_utils import CARD_DONE_STATUS, CARD_TODO_STATUS


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
