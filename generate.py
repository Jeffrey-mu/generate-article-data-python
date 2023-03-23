import requests
import json
from config import OPENAI_API_KEY


def openai_stream(title) -> str:
    print(title)
    payload = dict()
    payload['model'] = 'gpt-3.5-turbo'
    payload['max_tokens'] = 1500
    payload['messages'] = [
        {
            "role": "system",
            "content": "From now on, you are a blogger who is good at producing blog articles in any field. You need to follow the instructions to guide me in writing articles"
        },
        {
            "role": "system",
            "content": "When you need to add an image, please use the img tag and fill in the src attribute https://source.unsplash.com/600x400/? <PUT YOUR QUERY HERE>"
        },
        {"role": "user",
         "content": f"Generate a set of \"{title}\" outline values Only return secondary headings, and add a serial number"},
    ]

    response = get_request(payload)
    titles = response.json()["choices"][0]['message']['content']
    print(titles)
    title_list = titles.split("\n")
    title_list = [s for s in title_list if
                  s and not s.startswith(' ') and not s.startswith('Sure') and not s.startswith('-') and s[0].isdigit()]
    print(title_list)
    title_list = title_list
    response_item_docx = ""
    for title in title_list:
        newpayload = payload
        payload['max_tokens'] = 500
        payload['messages'] = [
            {
                "role": "system",
                "content": "From now on, you are a blogger who is good at producing blog articles in any field. You need to follow the instructions to guide me in writing articles"
            },
            {
                "role": "system",
                "content": "When you need to add an image, please use the img tag and fill in the src attribute https://source.unsplash.com/600x400/? <PUT YOUR QUERY HERE>"
            },
            {"role": "user",
             "content": f"Generate a set of \"{title}\" outline values Only return secondary headings, which can be separated by commas"},
            {"role": "assistant",
             "content": f"{titles}"},
            {"role": "user", "content": f"expands {titles} and add a picture based on the title"},
            {"role": "user", "content": f"Document structure has paragraph breaks like h1 and h2."}
        ]
        print(newpayload)
        print(title)

        response_item = get_request(newpayload).json()["choices"][0]['message']['content']
        print(response_item)
        response_item_docx += response_item
    print(title_list)
    try:
        return response_item_docx
    except (KeyError, IndexError):
        return ""


def get_request(payload):
    base_path = 'https://api.openai.com'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    response = requests.post(base_path + "/v1/chat/completions", headers=headers, data=json.dumps(payload))
    return response
