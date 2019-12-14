import vk
import json

vk_api = vk.API(vk.Session(access_token="0152bbbc0152bbbc0152bbbc04013f4323001520152bbbc5c995c1692c36bf31fb38a5d"))
groupid = 189740662
groupDomain = "redfederust"


def get_members_that_liked_post(postid):
    first = vk_api.likes.getList(type="post", owner_id=-groupid, item_id=postid, filter="likes", offset=0, friends_only=0, count=1000,  v=5.92)

    data  = first["items"]
    count = first["count"] // 1000

    for i in range(1, count + 1):
        data = data + vk_api.likes.getList(type="post", owner_id=-groupid, item_id=postid, filter="likes", offset=i*1000, friends_only=0, count=1000,  v=5.92)["items"]
    return data


def get_all_posts():
    first = vk_api.wall.get(domain="redfederust", filter="owner", extended=1, offset=0, count=100,  v=5.92)

    # data  = first["items"]
    # count = first["count"] // 100
    #
    # for i in range(1, count + 1):
    #     data = data + vk_api.wall.get(owner_id=-groupid, filter="owner", offset=i*1000, friends_only=0, count=100,  v=5.92)["items"]
    return first




# print('here is a list of memberships that likes post...')
# print(get_members_that_liked_post(25))

# print(get_all_posts())