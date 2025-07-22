# Google Scholar Query Generator

该代码通过调用 DeepSeek API，将自然查询语言（中文）转换为可以在 Google Scholar 中使用的英文检索语句。



## 一、功能简介

- 输入自然语言（中文）描述的问题
- 输出不少于两条英文 Google Scholar 检索语句
- 支持 AND、OR、引号、限定词（如 `"systematic review"`）
- 支持流式输出
- 内置重试机制，防止网络出错



## 二、使用方法

1. 环境要求

   - Python 3.7+
   - `openai`包

2. 安装依赖

   ```python
   pip install openai==0.28
   ```

3. 设置API KEY

   ```python
   openai.api_key = "your-api-key"
   ```

4. 运行

   ```
   python test_convert_google_query.py
   ```

   根据提示输入自然语言描述，例如：

   ```
   输入自然语言搜索描述：AI在护理中提高模型准确性与系统安全的研究
   ```

   输出示例：

   ```python
   耗时:69.35s    GPT output: "artificial intelligence" AND "nursing" AND "model accuracy" AND "system safety"；"artificial intelligence" AND "nursing" AND ("model accuracy" OR "system safety") AND "systematic review"
   ```

5. 文件说明

   ```
   test_convert_google_query.py   # 主程序
   README.md          # 项目说明（本文件）
   ```

6. 注意事项

   - 代码中使用的 DeepSeek API（类似 OpenAI API），需要自己申请 API Key 
   - 流式输出（streaming）为默认开启，如需关闭可在 `get_query()` 中修改 `streaming_flg=False`。 
