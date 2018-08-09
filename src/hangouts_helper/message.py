from enum import Enum
from collections import Iterable


class ImageStyle(Enum):
    IMAGE = 'IMAGE'  # square
    AVATAR = 'AVATAR'  # circular


class Icon(Enum):
    AIRPLANE = 'AIRPLANE'
    BOOKMARK = 'BOOKMARK'
    BUS = 'BUS'
    CAR = 'CAR'
    CLOCK = 'CLOCK'
    CONFIRMATION_NUMBER_ICON = 'CONFIRMATION_NUMBER_ICON'
    DESCRIPTION = 'DESCRIPTION'
    DOLLAR = 'DOLLAR'
    EMAIL = 'EMAIL'
    EVENT_SEAT = 'EVENT_SEAT'
    FLIGHT_ARRIVAL = 'FLIGHT_ARRIVAL'
    FLIGHT_DEPARTURE = 'FLIGHT_DEPARTURE'
    HOTEL = 'HOTEL'
    HOTEL_ROOM_TYPE = 'HOTEL_ROOM_TYPE'
    INVITE = 'INVITE'
    MAP_PIN = 'MAP_PIN'
    MEMBERSHIP = 'MEMBERSHIP'
    MULTIPLE_PEOPLE = 'MULTIPLE_PEOPLE'
    PERSON = 'PERSON'
    PHONE = 'PHONE'
    RESTAURANT_ICON = 'RESTAURANT_ICON'
    SHOPPING_CART = 'SHOPPING_CART'
    STAR = 'STAR'
    STORE = 'STORE'
    TICKET = 'TICKET'
    TRAIN = 'TRAIN'
    VIDEO_CAMERA = 'VIDEO_CAMERA'
    VIDEO_PLAY = 'VIDEO_PLAY'


class ResponseType(Enum):
    TYPE_UNSPECIFIED = 'TYPE_UNSPECIFIED'
    NEW_MESSAGE = 'NEW_MESSAGE'
    UPDATE_MESSAGE = 'UPDATE_MESSAGE'
    REQUEST_CONFIG = 'REQUEST_CONFIG'


class OnClickMixin:
    def add_link(self, url):
        self.link = True
        self.link_url = url
        return self

    def add_action(self, action_method, parameters=None):
        self.action = True
        self.action_method = action_method
        self.action_parameters = parameters
        return self

    def _update_on_click(self, widget):
        link = getattr(self, 'link', False)
        action = getattr(self, 'action', False)
        if link:
            data = {
                'openLink': {
                    'url': self.link_url
                }}
        elif action:
            action_data = {'actionMethodName': self.action_method.value}
            if self.action_parameters:
                action_data.update({
                    'parameters': [{'key': k, 'value': v} for k, v in self.action_parameters.items()]
                })
            data = {'action': action_data}
        if link or action:
            on_click = {'onClick': data}
            widget.update(on_click)


class Message:
    ResponseType = ResponseType

    def __init__(self, *cards, **kwargs):
        self.cards = list(cards)
        self.response_type = kwargs.get('response_type')
        self.response_url = kwargs.get('response_url')
        self.text = kwargs.get('text')

    def add_card(self, card):
        self.cards.append(card)

    def output(self):
        message = {}
        if self.cards:
            message.update({
                'cards': [c.output() for c in self.cards]
            })
        if self.text is not None:
            message.update({'text': self.text})
        if self.response_type is not None:
            response_type = {'type': self.response_type.value}
            if self.response_type == ResponseType.REQUEST_CONFIG:
                response_type.update({'url': self.response_url})
            message.update({'responseType': response_type})
        return message


class CardAction(OnClickMixin):
    def __init__(self, label):
        self.action_label = label

    def output(self):
        card_action = {'actionLabel': self.action_label}
        self._update_on_click(card_action)
        return card_action


class Card:
    def __init__(self, *components):
        self.card_actions = list()
        self.sections = list()
        self.header = None
        for component in components:
            if isinstance(component, CardHeader) and self.header is None:
                self.header = component
            elif isinstance(component, Section):
                self.sections.append(component)
            elif isinstance(component, CardAction):
                self.card_actions.append(component)

    def add_section(self, section):
        self.sections.append(section)

    def add_action(self, action):
        self.card_actions.append(action)

    def output(self):
        sections = [s.output() for s in self.sections]
        card = {'sections': sections}
        if self.header:
            header = self.header.output()
            card.update({'header': header})
        if self.card_actions:
            card_actions = [a.output() for a in self.card_actions]
            card.update({'cardActions': card_actions})
        return card


class Section:
    def __init__(self, *widgets):
        self.widgets = list(widgets)
        self.header = None
        if self.widgets and isinstance(self.widgets[0], str):
            self.header = self.widgets.pop(0)

    def add_widget(self, widget):
        self.widgets.append(widget)

    def output(self):
        widgets = [w.output() for w in self.widgets]
        section = {'widgets': widgets}
        if self.header is not None:
            section.update({'header': self.header})
        return section


class ButtonList:
    def __init__(self, *buttons):
        self.buttons = list(buttons)

    def add_button(self, button):
        self.buttons.append(button)

    def output(self):
        buttons = [b.output() for b in self.buttons]
        return {'buttons': buttons}


class CardHeader:
    ImageStyle = ImageStyle

    def __init__(self, title, subtitle, image_url=None, image_style=None):
        self.title = title
        self.subtitle = subtitle
        self.image_url = image_url
        self.image_style = image_style

    def output(self):
        header = {
            'title': self.title,
            'subtitle': self.subtitle
        }
        if self.image_url is not None:
            header.update({'imageUrl': self.image_url})
        if self.image_style is not None:
            header.update({'imageStyle': self.image_style.value})
        return header


class TextParagraph:
    def __init__(self, text):
        self.text = text

    def output(self):
        text_paragraph = {'text': self.text}
        return {'textParagraph': text_paragraph}


class KeyValue(OnClickMixin):
    Icon = Icon

    def __init__(self, content, top_label=None, bottom_label=None, icon=None, icon_url=None, button=None):
        self.top_label = top_label
        self.content = content
        self.bottom_label = bottom_label
        self.icon = icon
        self.icon_url = icon_url
        self.button = button

    def output(self):
        key_value = {'content': self.content}
        if '\n' in self.content:
            key_value.update({'contentMultiline': True})
        if self.top_label is not None:
            key_value.update({'topLabel': self.top_label})
        if self.bottom_label is not None:
            key_value.update({'bottomLabel': self.bottom_label})
        if self.button is not None:
            key_value.update({'button': self.button})
        if self.icon is not None:
            key_value.update({'icon': self.icon.value})
        elif self.icon_url is not None:
            key_value.update({'iconUrl': self.icon_url})
        self._update_on_click(key_value)
        return {'keyValue': key_value}


class Image(OnClickMixin):
    def __init__(self, image_url, aspect_ratio=None):
        self.image_url = image_url
        self.aspect_ratio = aspect_ratio

    def output(self):
        image = {'imageUrl': self.image_url}
        if self.aspect_ratio is not None:
            image.update({'aspectRatio': self.icon_url})
        self._update_on_click(image)
        return {'image': image}


class ImageButton(OnClickMixin):
    Icon = Icon

    def __init__(self, icon=None, icon_url=None, name=None):
        self.icon_url = icon_url
        self.icon = icon
        self.name = name

    def output(self):
        if self.icon is not None:
            button = {'icon': self.icon.value}
        elif self.icon_url is not None:
            button = {'iconUrl': self.icon_url}
        if self.name is not None:
            button = {'name': self.name}
        self._update_on_click(button)
        return {'imageButton': button}


class TextButton(OnClickMixin):
    Icon = Icon

    def __init__(self, text):
        self.text = text

    def output(self):
        button = {'text': self.text}
        self._update_on_click(button)
        return {'textButton': button}


