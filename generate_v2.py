import requests
import json
import random
from config import OPENAI_API_KEY
from log.index import info, error
from utils import revise_html
import re


def openai_stream(title) -> str:
    payload = dict()
    payload['model'] = 'gpt-3.5-turbo'
    payload['max_tokens'] = 1500
    payload['messages'] = [
        {
            "role": "system",
            "content": """
                To write an essay titled "title", first you should write an outline with many paragraphs.；
                Expand each outline after you write the outline, including small outlines, adding more detail,；
                examples, or explanations to expand each idea. Document structure has paragraph breaks like h1 and h2.
                format requirement；
                Your essay should be between 1000 and 1200 words；
                add a picture for each paragraph；
                The last paragraph must summarize the article in 150-200 words
            """
        },
        {
            "role": "system",
            "content": "When you need to add an image, please use the img tag and fill in the src attribute https://source.unsplash.com/600x400/? <PUT YOUR QUERY HERE>"
        },
        {"role": "user", "content": f"the returned content must be html code"},
        {"role": "user",
         "content": f"When h1 appears at the top of the article, the paragraph structure needs to be h2 p img, and no other tags need to appear"},
        {"role": "user", "content":
            """
            Return Structure Reference：
               {
                  title: '',
                  keywords: '',
                  description: '',
                  content: [
                    {
                      h1: 'xxx',
                      h2: 'xxx',
                      p: 'xxx',
                      img: '',
                    }
                  ]
                }
            """},
        {"role": "user",
         "content": f"To write an essay titled  \"{title}\""},
    ]
    try:
        response = get_request(payload)
        response_item_docx = response.json()["choices"][0]['message']['content']
        info(response)
        json_data = json.loads(response_item_docx)
        html_data = f"<p>title: {json_data['title']}</p><p>description: {json_data['description']}</p><p>keywords: {json_data['keywords']}</p>"
        info(json_data['content'])
        # 结论不做优化
        for item in json_data["content"][0: len(json_data["content"]) - 1]:

            try:
                info('优化段落:' + item['p'])
                params = f"Revisit the content based on the {item.get('h2', item.get('h1', ''))},content:{item['p']}"
                # params = f"Revisit the content based on the {item.get('h2', item.get('h1', ''))},content:{item['p']}"
                # embroidery_data = embroidery(item.get('h2', item.get('h1', '')), item['p']).json()["choices"][0]['message']['content']
                embroidery_data = revise_html(embroidery(params).json()["choices"][0]['message']['content'])
                item['p'] = embroidery_data
                # html_data += f"{get_value('h1', item)}{get_value('h2', item)}{get_value('ul', item)}<div  class='purple'>{get_value('p', item)}</div><div  class='green'>{embroidery_data}</div><img src='{get_value('img', item)}' /> <br>"
                html_data += f"{get_value('h1', item)}{get_value('h2', item)}{get_value('ul', item)}<div  class='green'>{embroidery_data}</div><img src='{get_value('img', item, False)}' /> <br>"

            except Exception as e:
                # 处理异常
                error(f"任务 发生异常：{e}")
                continue
            finally:
                info('finally')
        item = json_data["content"][len(json_data["content"]) - 1]
        html_data += f"{get_value('h1', item)}{get_value('h2', item)}{get_value('ul', item)}{get_value('p', item)}<img src='{get_value('img', item, False)}' />"
        return html_data
    except (KeyError, IndexError):
        return ""


def get_value(key, obj, format=True):
    if key in obj:
        if key == 'ul':
            lis = ''
            for item in obj[key]:
                lis += f'<li>{item}</li>'
            return f"<{key}>{lis}</{key}>"
        if format:
            return f"<{key}>{obj[key]}</{key}>"
        else:
            return f"<{obj[key]}"
    else:
        return ''


def embroidery(title, count=2) -> str:
    token = random.randrange(200, 300)
    payload = dict()
    payload['model'] = 'gpt-3.5-turbo'
    payload['max_tokens'] = 350
    payload['temperature'] = 0.5
    payload['messages'] = [
        {
            "role": "system",
            "content": """
               You need to polish and increase the number of words based on the article I wear；
               the returned content must be html code;
               Ensure the integrity of the article and do not truncate it;
               add appropriate images based on the content
            """
        },
        {
            "role": "system",
            "content": "When you need to add an image, please use the img tag and fill in the src attribute https://source.unsplash.com/600x400/? <PUT YOUR QUERY HERE>"
        },
        {
            "role": "system",
            "content": "you don't need to list outline titles, just optimize the content and divide it into paragraphs"
        },
        {
            "role": "system",
            "content": "There is no need to summarize the content at the end of the article"
        },
        {"role": "user",
         "content": f" \"{title}\"The optimization word count of {token} words and use html tags to decorate the content and there is no need for the h2 h1 title to appear"},
        # {"role": "user",
        #  "content": f"""
        #     First, determine the title of the article that needs to be optimized as {title}.
        #     What needs to be optimized is {content};
        #     For specific operations, consider adding some relevant information, supplementing details, providing arguments,
        #     and other methods to expand the content of the article until the number of words reaches{token}.
        #     Can't return h2 Title Title needs to start from h3
        #     and use html tags to decorate the content
        #  """},
    ]
    try:
        response = get_request(payload)
        info("优化结果" + response.json()["choices"][0]['message']['content'])
        return response
    except (KeyError, IndexError):
        if count >= 0:
            embroidery(title, count - 1)
            info("优化失败，重新优化")
        else:
            return ""


def get_request(payload):
    base_path = 'https://api.openai.com'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    try:
        response = requests.post(base_path + "/v1/chat/completions", headers=headers, data=json.dumps(payload))
        return response
    except (KeyError, IndexError):
        return ""
