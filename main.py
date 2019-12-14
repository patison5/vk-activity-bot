from vk_api.bot_longpoll import  VkBotLongPoll, VkBotEventType
from functions import  writeOrUpdateFile, readFromFile, getMemberFromFile
from vkRequests import  get_members_that_liked_post
from prettytable import PrettyTable
import json
import vk_api
import time

vk = vk_api.VkApi(token="b46013bc0945e81e73c84c6cceb1896dfb39dc53b2ad280ce7be624d364d2eca43306c01fc1d91a2c5c94")
vk._auth_token()
vk.get_api()

longpoll = VkBotLongPoll(vk, 189740662)

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

members = []

members.append({
    'id': 170877706,
    'score': 42,
    'likes': [25, 12],
    'comments': {'25': 5, '12': 2},        # в 25 посту 5 комментариев
    'reposts': [25, 12],
    'adminDecision': 10,
})
members.append({
    'id': 270877234,
    'score': 42,
    'likes': [25, 12],
    'comments': {'25': 5, '12': 2},        # в 25 посту 5 комментариев
    'reposts': [25, 12],
    'adminDecision': 10,
})

writeOrUpdateFile(members)

# data = readFromFile()

# testMember = getMemberFromFile(170877706)
# if testMember:
#     print(testMember)
# else:
#     print("no member found")

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.WALL_REPLY_NEW:
                print("Got new comment under post..")
                print(f'User: {event.object.from_id}')
                print(f'Body: {event.object}')

            if event.type == VkBotEventType.WALL_REPOST:
                print("Someone reposted our post!!!!")
                print(f'User: {event.object.from_id}')
                print(f'Body: {event.object}')

            if event.type == VkBotEventType.POLL_VOTE_NEW:
                print("Someone vote...")
                print(f'User: {event.object.from_id}')
                print(f'Body: {event.object}')

            if event.type == VkBotEventType.GROUP_JOIN:
                print("we got new membership!")
                print(event.object.user_id)

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
