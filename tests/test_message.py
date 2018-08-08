import pytest

from hangouts_helper.message import Message


def test_basic_text_message():
    message = Message(text='hello')
    assert message.output() == {'text': 'hello'}
