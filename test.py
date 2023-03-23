import random

list = {
    "name": '123',
}

value = list.get('age', list.get('s', '2'))
print(value)
