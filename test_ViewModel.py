from ViewModel import TodoListViewModel
from trello_utils import Card, cardComparator, ISO_TIMESTAMP_FORMAT
from trello_utils import CARD_DONE_STATUS, CARD_TODO_STATUS, CARD_DOING_STATUS
from datetime import datetime

test_list = [
    Card(
        '1',
        'name1',
        CARD_TODO_STATUS,
        '2020-09-01T15:22:10.424Z'
    ),
    Card(
        '2',
        'name2',
        CARD_TODO_STATUS,
        '2020-09-01T15:22:10.424Z'
    ),
    Card(
        '3',
        'name3',
        CARD_DONE_STATUS,
        '2020-09-01T15:22:10.424Z'
    ),
    Card(
        '4',
        'name4',
        CARD_DOING_STATUS,
        '2020-09-01T15:22:10.424Z'
    ),
    Card(
        '5',
        'done today',
        CARD_DONE_STATUS,
        datetime.now().strftime(ISO_TIMESTAMP_FORMAT)
    )
]


def test_items_returns_all():
    view_model = TodoListViewModel(test_list)
    assert len(view_model.items) == 5


def test_items_todo_returns_only_todo_items():
    view_model = TodoListViewModel(test_list)
    result = list(view_model.items_todo)
    result.sort(key=cardComparator)
    assert len(result) == 2
    assert result[0].id == '1'
    assert result[1].id == '2'


def test_items_done_returns_only_done_items():
    view_model = TodoListViewModel(test_list)
    result = list(view_model.items_done)
    result.sort(key=cardComparator)
    assert len(result) == 2
    assert result[0].id == '3'
    assert result[1].id == '5'


def test_items_doing_returns_only_doing_items():
    view_model = TodoListViewModel(test_list)
    result = list(view_model.items_doing)
    result.sort(key=cardComparator)
    assert len(result) == 1
    assert result[0].id == '4'


def test_items_done_today_returns_items_completed_today():
    view_model = TodoListViewModel(test_list)
    result = list(view_model.items_done_today)
    result.sort(key=cardComparator)
    assert len(result) == 1
    assert result[0].id == '5'
