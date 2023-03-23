from flask import Flask, request, render_template
import generate

app = Flask(__name__)


@app.route('/ai-generate', methods=['GET'])
async def ai_generate():
    try:
        title = request.args['title']
        prompts = request.args['prompts']
        print(generate.openai_stream(title, prompts))
        return {"title": title + prompts}
        result = generate.openai_stream(title, prompts)
        return result
    except Exception as e:
        return e


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True, port=8083, host='0.0.0.0')  # 默认127.0.0.1:5000，这里修改了地址和端口
