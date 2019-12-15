from vk_api.bot_longpoll import  VkBotLongPoll, VkBotEventType
from functions import updateCurrentMember
from vkRequests import  get_members_that_liked_post
from prettytable import PrettyTable
import json
import vk_api
import time

vk = vk_api.VkApi(token="b46013bc0945e81e73c84c6cceb1896dfb39dc53b2ad280ce7be624d364d2eca43306c01fc1d91a2c5c94")
vk._auth_token()
vk.get_api()

longpoll = VkBotLongPoll(vk, 189740662, wait=25)

keyboard = {
    "one_time": False,
    "buttons": [
        [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Красный"
                },
                "color": "negative"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Зелёный"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Синий"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Белый"
                },
                "color": "secondary"
            }
        ]
    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

updateCurrentMember(1, {'key': 'adminDecision', 'value': 10}, 1)
updateCurrentMember(2, {'key': 'adminDecision', 'value': 10}, 1)
updateCurrentMember(3, {'key': 'adminDecision', 'value': 10}, 1)

for i in range(100):
    updateCurrentMember(i, {'key': 'adminDecision', 'value': 10}, 1)

while True:
    try:
        for event in longpoll.listen():

            if event.type == VkBotEventType.WALL_REPLY_NEW or event.type == VkBotEventType.WALL_REPLY_RESTORE:
                print(f'Body: {event.object}')
                updateCurrentMember(event.object.from_id, {'key': 'comments', 'value': event.object.post_id}, 1)

            if event.type == VkBotEventType.WALL_REPLY_DELETE:
                print(f'Body: {event.object}')
                updateCurrentMember(event.object.deleter_id, {'key': 'comments', 'value': event.object.post_id}, -1)

            if event.type == VkBotEventType.WALL_REPOST:
                print(f'Body: {event.object}')
                updateCurrentMember(event.object.from_id, {'key': 'reposts', 'value': event.object.post_id}, 1)

            if event.type == VkBotEventType.POLL_VOTE_NEW:
                print(f'Body: {event.object}')
                updateCurrentMember(event.object.user_id, {'key': 'votes', 'value': event.object.poll_id}, 1)

            if event.type == VkBotEventType.GROUP_JOIN:
                print("we got new membership!")
                print(event.object.user_id)
                updateCurrentMember(event.object.user_id, {'key': 'adminDecision', 'value': 10}, 1)

            if event.type == VkBotEventType.MESSAGE_NEW:
                print("Got new message from subscriber")
                print(f'Он пишет: {event.object.message["text"]}')

                vk.method("messages.send", {"peer_id": event.object.message['from_id'], "message": "Новые кнопки",
                                                    "keyboard": keyboard, "random_id": 0})

            if event.type == VkBotEventType.MESSAGE_REPLY:
                print("I'm writing new message...")
                print(f'Он пишет: {event.object["text"]}')
                print(f'Он пишет: {event.object["peer_id"]}')

            # print(event)
            print("\n")

    except Exception as E:
        print(E)
        time.sleep(10)


        print('\n')
