import utils
from db.query import query_data_by_id
import generate
import json

def auto_work():
  data_list = utils.read_elsx('./chatgpt内容生成id(1).xlsx')
  for item in data_list:
    id = item['样式参考id']
    consult = query_data_by_id(id)[0]
    print(item['Topic（话题）'])
    result = generate.openai_stream(item['Topic（话题）'], consult)
    result_data = json.loads(result)
    result_data['data_type'] = item['数据类型']
    result_data['data_second_type'] = item['二级数据']
    utils.format_html(json.loads(result_data), item['生成文本序号'])
    # print(result_data)
auto_work()
