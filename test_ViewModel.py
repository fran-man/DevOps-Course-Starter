from ViewModel import TodoListViewModel
from trello_utils import Card, cardComparator
from trello_utils import CARD_DONE_STATUS, CARD_TODO_STATUS


def test_items_returns_all():
    test_list = ["something", "something1", "something2"]
    view_model = TodoListViewModel(test_list)
    assert len(view_model.items) == 3


def test_items_todo_returns_only_todo_items():
    test_list = [
        Card(
            '1',
            'name1',
            CARD_TODO_STATUS
        ),
        Card(
            '2',
            'name2',
            CARD_TODO_STATUS
        ),
        Card(
            '3',
            'name3',
            CARD_DONE_STATUS
        )
    ]
    view_model = TodoListViewModel(test_list)
    result = list(view_model.items_todo)
    result.sort(key=cardComparator)
    assert len(result) == 2
    assert result[0].id == '1'
    assert result[1].id == '2'
