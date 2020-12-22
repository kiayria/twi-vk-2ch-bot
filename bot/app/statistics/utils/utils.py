from app import db


def get_stat(chat_id, api=None):
    user = db.get_user(chat_id)
    if user is None or api not in ('twitter', 'vk', 'dvach'):
        return
    if api is None:
        dicts = [
            user['data']['twitter']['statistics'],
            user['data']['vk']['statistics'],
            user['data']['dvach']['statistics'],
        ]
        sum_dict = dict()
        for d in dicts:
            for k, v in d.items():
                if k in sum_dict:
                    sum_dict[k] += v
                else:
                    sum_dict[k] = v
    else:
        sum_dict = user['data'][api]['statistics']

    if len(sum_dict) == 0:
        return None

    top_reversed_keys = sorted(sum_dict, key=sum_dict.get, reverse=True)
    if len(top_reversed_keys) > 10:
        top_reversed_keys = top_reversed_keys[:10]

    return {k: sum_dict[k] for k in top_reversed_keys}
