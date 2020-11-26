from helpers import *


class Widget:
    def __init__(self, sender="default"):
        self.sender = sender
        self.service_id = pytest.service_id
        self.session_id = pytest.session_id

    def send_message(self, text):
        return my_request(method="POST",
                          url=URLs.api + "/" + self.service_id + "/" + self.session_id + "/messages",
                          payload={"ts": ts(),
                                   "sender": self.sender,
                                   "text": text,
                                   "senderPayload": {}})

    def click_button(self, button_name, buttons):
        for button in buttons['buttons']:
            if button['text'] == button_name:
                button_payload = button['payload']

        return my_request(method="POST",
                          url=URLs.api + "/" + self.service_id + "/" + self.session_id + "/messages",
                          payload={"ts": ts(),
                                   "sender": self.sender,
                                   "text": "",
                                   "senderPayload": {},
                                   "replyToMessage": pytest.last_message_id,
                                   "payload": {
                                       "inlineButtonSrcMessageId": buttons['id'],
                                       "inlineButtonPayload": button_payload,
                                       "clicked": "true"
                                   }})
