import utils
from db.query import query_data_by_id
import generate_v2 as generate
import json
from log.index import info, error
import threading
from config import project_path


def auto_work():
    data_list = utils.read_excel(".")
    for item in data_list:
        id = item["样式参考id"]
        info(item["Topic（话题）"], "开启获取数据")
        consult = query_data_by_id(id)[0]
        # consult["content"] = utils.stringEncodingFun(consult["content"])
        result_data = generate.get_article(item["Topic（话题）"], consult)
        # result_data["data_type"] = item["数据类型"]
        # result_data["data_second_type"] = item["二级数据"]
        with open(project_path + '/data/data_json/' + str(item["生成文本序号"]) + '.json', 'w') as f:
            f.write(result_data)


def auto_work_to_docx():
    data_list = utils.read_excel("./测试话题.xlsx")
    for item in data_list[20: 24]:
        path = f'{project_path}/data_json/{item["生成文本序号"]}.json'
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        # text = re.sub(r'\n\n', '<br />', text)
        obj = json.loads(text)
        utils.format_html(obj, './data/ai_data/' + str(item["生成文本序号"]) + '.docx')
        info(obj['title'])


def start_task():
    data_list = utils.read_excel(project_path + "/文章测试话题.xlsx")
    info("开始运行")
    for item in data_list[20: 24]:
        try:
            t = threading.Thread(target=worker, args=(item,))
            t.start()
        except Exception as e:
            # 处理异常
            error(f"线程错误：{e}")
            continue


file_path = 'v4'


def worker(data):
    info(data['Topic（话题）'])
    try:
        result_data = generate.get_article(data['Topic（话题）'])
        info(f"标题{data['Topic（话题）']}内容长度： {len(result_data)}")
        with open(project_path + '/data/test/' + file_path + '/' + data['Topic（话题）'] + '.html', 'w') as f:
            f.write(result_data)
        utils.format_html(result_data, project_path + '/data/ai_data/' + file_path + '/' + data['Topic（话题）'] + '.docx')
    except Exception as e:
        # 处理异常
        error(f"{data['Topic（话题）']}写入docx发生错误：{e}")
    finally:
        info('finally')


start_task()
