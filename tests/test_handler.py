import pytest
from pytest_mock import mocker

from enum import Enum

from hangouts_helper.handler import HangoutsChatHandler, EventType, SpaceType


@pytest.fixture
def handler(mocker):
    from enum import Enum
    class ActionMethod(Enum):
        TEST_ACTION = 'TEST_ACTION'
    m = mocker.patch('hangouts_helper.api.HangoutsChatAPI._initialize_api')
    m.return_value = mocker.Mock()
    handler = HangoutsChatHandler()
    handler.ActionMethod = ActionMethod
    return handler

@pytest.fixture
def create_event():

    def _create_event(event_type='MESSAGE', space_type='DM',
                      user_type='HUMAN', message_text=None,
                      action_method=None, action_parameters=None):
        event = {
            "type": event_type,
            "eventTime": '2018-08-04T01:36:33.832895Z',
            "token": 'yxsTv7uVsnr5BL1qecnig8sMLLulF5RvC0nTrw2yZCE=',
            "responseUrl": 'http://www.example.com',
            "threadKey": 'thread1',
            "configCompleteRedirectUrl": 'https://chat.google.com/api/bot_config_complete?token=abc123',
            "user": {
                "name": 'users/111998962929502904878',
                "displayName": 'Bob Dylan',
                "type": user_type
            },
            "space": {
                "name": 'spaces/AAAA9UbUwi8',
                "type": space_type,
                "displayName": 'My Chat'
            }
        }
        if message_text is not None:
            event.update({'message': {'text': message_text}})
        if action_method is not None:
            action_data = {'actionMethodName': action_method}
            if action_parameters is not None:
                action_data.update({'parameters': action_parameters})
            event.update({'action': action_data})
        return event
    return _create_event

@pytest.mark.parametrize("space_type", [SpaceType.ROOM, SpaceType.DIRECT_MESSAGE])
def test_handle_added_to_space(mocker, handler, create_event, space_type):
    event = create_event(event_type='ADDED_TO_SPACE', space_type=space_type.value)
    mocker.patch.object(HangoutsChatHandler, 'handle_added_to_space')
    handler.handle_chat_event(event)
    handler.handle_added_to_space.assert_called_once_with(space_type, event)

@pytest.mark.parametrize("space_type", [SpaceType.ROOM, SpaceType.DIRECT_MESSAGE])
def test_handle_removed_from_space(mocker, handler, create_event, space_type):
    space_type_str = space_type.value  # create_event expects string value
    event = create_event(event_type='REMOVED_FROM_SPACE', space_type=space_type_str)
    mocker.patch.object(HangoutsChatHandler, 'handle_removed_from_space')
    handler.handle_chat_event(event)
    handler.handle_removed_from_space.assert_called_once_with(space_type, event)

def test_handle_message(mocker, handler, create_event):
    event = create_event(event_type='MESSAGE', message_text='Hello')
    mocker.patch.object(HangoutsChatHandler, 'handle_message')
    handler.handle_chat_event(event)
    handler.handle_message.assert_called_once_with('Hello', event)

def test_handle_card_clicked(mocker, handler, create_event):
    action_method_name = 'TEST_ACTION'
    action_parameters = [
        {'key': 'key1', 'value': 'value1'},
        {'key': 'key2', 'value': 'value2'}
    ]
    event = create_event(event_type='CARD_CLICKED', action_method=action_method_name,
                         action_parameters=action_parameters)
    mocker.patch.object(HangoutsChatHandler, 'handle_card_clicked')
    handler.handle_chat_event(event)
    expected_parameters = {
        'key1': 'value1',
        'key2': 'value2'
    }
    handler.handle_card_clicked.assert_called_once_with(
        handler.ActionMethod.TEST_ACTION,
        expected_parameters,
        event)

def test_parse_action_parameters(handler):
    parameters = [
        {
            'key': 'key1',
            'value': 'value1'
        },
        {
            'key': 'key2',
            'value': 'value2'
        }
    ]
    expected = {
        'key1': 'value1',
        'key2': 'value2'
    }
    assert handler._parse_action_parameters(parameters) == expected

def test_exception_during_event_handling(mocker, handler, create_event):
    event = create_event(event_type='MESSAGE', message_text='Hello')
    mocker.patch.object(HangoutsChatHandler, 'handle_message')
    mocker.patch.object(HangoutsChatHandler, 'handle_exception')
    handler.handle_message.side_effect = Exception
    handler.handle_chat_event(event)
    handler.handle_exception.call_count == 1

