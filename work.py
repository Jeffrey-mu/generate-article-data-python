import utils
from db.query import query_data_by_id
import generate_v2 as generate
import json


def auto_work():
    data_list = utils.read_elsx(".")
    for item in data_list:
        id = item["样式参考id"]
        print(item["Topic（话题）"], "开启获取数据")
        consult = query_data_by_id(id)[0]
        # consult["content"] = utils.stringEncodingFun(consult["content"])
        result_data = generate.openai_stream(item["Topic（话题）"], consult)
        # result_data["data_type"] = item["数据类型"]
        # result_data["data_second_type"] = item["二级数据"]
        with open('./data/data_json/' + str(item["生成文本序号"]) + '.json', 'w') as f:
            f.write(result_data)


# auto_work()

def auto_work_to_docx():
    data_list = utils.read_elsx("./chatgpt内容生成id(1) copy.xlsx")
    for item in data_list:
        path = f'./data_json/{item["生成文本序号"]}.json'
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        # text = re.sub(r'\n\n', '<br />', text)
        obj = json.loads(text)
        utils.format_html(obj, './data/ai_data/' + str(item["生成文本序号"]) + '.docx')
        print(obj['title'])


# auto_work_to_docx()


def test_v2():
    data_list = utils.read_elsx("./测试话题.xlsx")
    print("开始运行")
    for item in data_list:
        print(item['Topic（话题）'])
        try:
            result_data = generate.openai_stream(item['Topic（话题）'])
            print(result_data)
            with open('./data/test/data_json/' + item['Topic（话题）'] + '.html', 'w') as f:
                f.write(result_data)
            utils.format_html(result_data, './data/ai_data/v2/' + item['Topic（话题）'] + '.docx')
        except Exception as e:
            # 处理异常
            print(f"任务 发生异常：{e}")
            continue
        finally:
            print('finally')


test_v2()
