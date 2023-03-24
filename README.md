# generate-article-data-python
- 基于gpt-3.5-turbo 模型开发内容生成
在 config.py 脚本中添加 `OPENAI_API_KEY `
```py
OPENAI_API_KEY = '您的key'
```

调用 `generate_v2.openai_stream()`方法 参数为需要生成内容话题 返回完整的具有大纲段落的内容

[预览文章](https://jeffrey-mu.github.io/generate-article-data-python/)
