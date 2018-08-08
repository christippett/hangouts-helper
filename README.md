Hangouts Chat Utils
=============================================================

[![PyPI version](https://img.shields.io/pypi/v/hangouts-chat-util.svg)](https://pypi.python.org/pypi/hangouts-chat-util)
[![Build status](https://img.shields.io/travis/christippett/hangouts-chat-util.svg)](https://travis-ci.org/christippett/hangouts-chat-util)
[![Coverage](https://img.shields.io/coveralls/github/christippett/hangouts-chat-util.svg)](https://coveralls.io/github/christippett/hangouts-chat-util?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/hangouts-chat-util.svg)](https://pypi.python.org/pypi/hangouts-chat-util)
[![Github license](https://img.shields.io/github/license/christippett/hangouts-chat-util.svg)](https://github.com/christippett/hangouts-chat-util)

Description
===========

Helper Python classes for handling and responding to Hangouts Chat events.

Installation
============

Install with `pip`:

``` bash
pip install hangouts-chat-util
```

Message Components
=====

This library contains several component classes to assist with constructing a Hangouts Chat message.
- `Message`
- `Section`
- `Card`
- `CardAction`
- `CardHeader`
- `TextParagraph`
- `KeyValue`
- `Image`
- `ButtonList`
- `ImageButton`
- `TextButton`

Example
-------

Using the [**Pizza Bot**](https://developers.google.com/hangouts/chat/reference/message-formats/cards#full_example_pizza_bot) example from the official Hangouts Chat API documentation, this is how you'd construct the same message using the components above.

```python
from hangouts_chat.message import (Message, Card, CardHeader, Section,
    Image, KeyValue, ButtonList, TextButton)

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
```

The raw message output is available from `message.output()`. After converting to JSON, the message looks like this:

```javascript
{
    "cards": [
        {
            "header": {
                "imageUrl": "https://goo.gl/aeDtrS",
                "subtitle": "pizzabot@example.com",
                "title": "Pizza Bot Customer Support"
            },
            "sections": [
                {
                    "widgets": [
                        {
                            "keyValue": {
                                "content": "12345",
                                "topLabel": "Order No."
                            }
                        },
                        {
                            "keyValue": {
                                "content": "In Delivery",
                                "topLabel": "Status"
                            }
                        }
                    ]
                },
                {
                    "header": "Location",
                    "widgets": [
                        {
                            "image": {
                                "imageUrl": "https://maps.googleapis.com/..."
                            }
                        }
                    ]
                },
                {
                    "widgets": [
                        {
                            "buttons": [
                                {
                                    "textButton": {
                                        "onClick": {
                                            "openLink": {
                                                "url": "https://example.com/orders/..."
                                            }
                                        },
                                        "text": "OPEN ORDER"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```

Chat Handler
============

The library also includes a class to help with handling incoming chat events. The methods contained in `HangoutsChatHandler` correspond to the different event types you can expect to receive. Each method should return a message response.

Example
-------

```python
from enum import Enum

from hangouts_chat.handler import HangoutsChatHandler, SpaceType
from hangouts_chat.message import Message


class ActionMethod(Enum):
    BUTTON_CLICKED = 'BUTTON_CLICKED'


class MyHangoutsChatHandler(HangoutsChatHandler):
    ActionMethod = ActionMethod

    def handle_added_to_space(self, space_type, event):
        if space_type == SpaceType.DM:
            return Message(text="Thanks DM'ing me!")
        elif space_type == SpaceType.ROOM:
            return Message(text="Thanks adding me to your room!")

    def handle_message(self, message, event):
        return Message(text="Thanks for your message!")

    def handle_card_clicked(self, action_method, action_parameters, event):
        if action_method == ActionMethod.BUTTON_CLICKED:
            return Message(text="I've processed your button click!")

    def handle_removed_from_space(self, event):
        pass

```

A Flask app that repsonds to Hangouts Chat events might look like:

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    event = request.json
    handler = MyHangoutsChatHandler()
    response_message = handler.handle_event(event)
    return jsonify(response_message.output())

```

TODO
====
- Add examples for each component type in README
- Document and add examples for adding OnClick events to widgets
- Document Enums (`SpaceType`, `EventType`, `ActionMethod`, `Icon`, `ImageStyle`, `ResponseType`)
- Document usage scenarios for `HangoutsChatHandler`
- Add methods for interacting with Hangouts Chat API to `HangoutsChatHandler`
