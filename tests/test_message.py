import os
import pytest

from hangouts_helper.message import (Message, Card, CardHeader, Section,
    Image, KeyValue, ButtonList, TextButton)


@pytest.fixture
def pizza_bot_message():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    import json
    with open(os.path.join(test_dir, 'pizza_bot_example.json')) as f:
        example_json = f.read()
    return json.loads(example_json)

def test_text_message():
    message = Message(text='hello')
    assert message.output() == {'text': 'hello'}

def test_request_config():
    message = Message.request_config('https://example.com')
    expected = {
        'actionResponse': {
            'type': 'REQUEST_CONFIG',
            'url': 'https://example.com'
        }
    }
    assert message.output() == expected

def test_add_link():
    button = TextButton(text='OPEN ORDER').add_link(url='https://example.com/orders/...')
    expected = {
        'textButton': {
            'text': 'OPEN ORDER',
            'onClick': {
                'openLink': {
                    'url': 'https://example.com/orders/...'
                }
            }
        }
    }
    assert button.output() == expected

def test_add_action():
    from enum import Enum
    class ActionMethod(Enum):
        TEST_METHOD = 'TEST_METHOD'
    parameters = {'param1': 'value1', 'param2': 'value2'}
    button = TextButton(text='OPEN ORDER').add_action(
        action_method=ActionMethod.TEST_METHOD,
        parameters=parameters)
    expected = {
        'textButton': {
            'text': 'OPEN ORDER',
            'onClick': {
                'action': {
                    'actionMethodName': 'TEST_METHOD',
                    'parameters': [{
                        'key': 'param1',
                        'value': 'value1'
                    },
                    {
                        'key': 'param2',
                        'value': 'value2'
                    }]
                }
            }
        }
    }
    assert button.output() == expected

def test_pizza_bot_full_example(pizza_bot_message):
    message = Message()
    message.add_card(
        Card(
            CardHeader(
                title='Pizza Bot Customer Support',
                subtitle='pizzabot@example.com',
                image_url='https://goo.gl/aeDtrS'),
        Section(
            KeyValue(top_label='Order No.', content='12345'),
            KeyValue(top_label='Status', content='In Delivery')),
        Section(
            'Location',
            Image(image_url='https://maps.googleapis.com/...')),
        Section(
            ButtonList(
                TextButton(text='OPEN ORDER').add_link(url='https://example.com/orders/...')))))

    assert message.output() == pizza_bot_message
