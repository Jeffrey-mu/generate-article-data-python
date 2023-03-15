import requests
import json


def openai_stream(title, consult, prompts="") -> str:
    OPENAI_API_KEY = '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'
    payload = dict()
    sample_data = consult
    payload['model'] = 'gpt-3.5-turbo'
    payload['messages'] = [
            {
                "role": "user", "content": 'Write an outline for a blog post about "The Topic" Turn it into an article with each of the headings above'
            },
            {
                "role": "user",
                "content": f"Please generate an article about {sample_data['title']} for me Data Type user_name title main_title subtitle Time Keyword score description content is required"
            },
            {
                "role": "assistant",
                "content": f'{sample_data}'
            },
            {
                "role": "user",
                "content": "Please generate an article for me Data Type user_name title main_title subtitle time Keyword score description content is required return my json datatype"
            },
            {
                "role": "user",
                "content": "The following description mainly optimizes content in json format"
            },
            {
                "role": "user", "content": 'Write an outline for a blog post about "The Topic" Expand on "H2 Headline"'
            },
            {
                "role": "user", "content": 'Create an outline for an essay "The Topic" Please write the Introduction of "H2 Headline"'
            },
            {
                "role": "user", "content": 'Write an outline for a blog post about "The Topic" Turn this into an essay'
            },
            {
                "role": "user", "content": 'Write an outline for a blog post about "The Topic" write a paragraph for each point and include headings so it is sectioned like an essay'
            },
            { "role": "user", "content": "Please return my article according to the content I sent" },
            { "role": "user", "content": " return my json datatype" },
            ]
    if not prompts:
        prompts_list = []
    else:
        prompts_list =  list(map(lambda x: {"role": "user", "content": x}, prompts.split(',')))
    payload['messages'] = payload['messages'] + prompts_list
    payload['messages'].append({ "role": "user", "content": title })
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(payload))
    stream = response.json()
    try:
        return stream["choices"][0]['message']['content']
    except (KeyError, IndexError):
        return ""


