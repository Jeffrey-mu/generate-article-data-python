import random

list = {
    "name": '123',
    "content": [
        {
            "name": "123"
        },
        {
            "name": "123213"
        }
    ]
}

for item in list['content']:
    item['name'] = "jaca"
print(list)
token = random.randrange(200, 300)
print(token)
print(token)
