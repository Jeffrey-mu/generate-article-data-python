import requests
import json
import random
from config import OPENAI_API_KEY
from log.index import info, error
def openai_stream(title) -> str:
    payload = dict()
    payload['model'] = 'gpt-3.5-turbo'
    payload['max_tokens'] = 1500
    payload['messages'] = [
        {
            "role": "system",
            "content": """
                To write an essay titled "title", first you should write an outline with many paragraphs.
                Expand each outline after you write the outline, including small outlines, adding more detail,
                examples, or explanations to expand each idea. Document structure has paragraph breaks like h1 and h2.
                format requirement
                Your essay should be between 1000 and 1200 words
                add a picture for each paragraph
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
        html_data = ''
        info(json_data['content'])
        for item in json_data["content"]:
            try:
                info('优化段落:', item['p'])
                embroidery_data = embroidery(item['p']).json()["choices"][0]['message']['content']
                info('优化段落block')
                info(embroidery_data)
                info('优化段落end')
                item['p'] = embroidery_data
                html_data += f"{get_value('h1', item)}{get_value('h2', item)}{get_value('ul', item)}{get_value('p', item)}<img src='{get_value('img', item)}' /> <br>"
            except Exception as e:
                # 处理异常
                error(f"任务 发生异常：{e}")
                continue
            finally:
                info('finally')
        return html_data
    except (KeyError, IndexError):
        return ""


def get_value(key, obj):
    if key in obj:
        if key == 'ul':
            lis = ''
            for item in obj[key]:
                lis += f'<li>{item}</li>'
            return f"<{key}>{lis}</{key}>"
        return f"<{key}>{obj[key]}</{key}>"
    else:
        return ''


def embroidery(title) -> str:
    token = random.randrange(200, 300)
    payload = dict()
    payload['model'] = 'gpt-3.5-turbo'
    payload['max_tokens'] = 350
    payload['messages'] = [
        {
            "role": "system",
            "content": """
               You need to polish and increase the number of words based on the article I wear；
               Don't go back Anyway Conclusion；
               the returned content must be html code;
               Ensure the integrity of the article and do not truncate it;
               add appropriate images based on the content
            """
        },
        {
            "role": "system",
            "content": "When you need to add an image, please use the img tag and fill in the src attribute https://source.unsplash.com/600x400/? <PUT YOUR QUERY HERE>"
        }, {
            "role": "system",
            "content": "you don't need to list outline titles, just optimize the content and divide it into paragraphs"
        },
        {"role": "user",
         "content": f" \"{title}\"The optimization field p has a word count of {token} words and use html tags to decorate the content"},
    ]
    try:
        response = get_request(payload)
        info(response)
        return response
    except (KeyError, IndexError):
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
