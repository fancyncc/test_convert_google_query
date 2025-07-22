import time
import openai


def get_query(query, streaming_flg=True, max_retries=5):
    # 设置 DeepSeek API 相关信息
    openai.api_base = "https://api.deepseek.com"
    openai.api_key = "sk-123456"

    # 提示
    system_prompt = (
        "你是一个学术搜索优化专家。你的任务是将用户输入的自然语言需求，转换为适合在 Google Scholar 中检索学术文献的英文搜索语句。\n"
        "要求如下：\n"
        "1. 输出不少于两条 Google Scholar 检索语句；\n"
        "2. 每条语句应使用英文表达，尽量保留用户输入中的核心关键词；\n"
        "3. 可添加关键词限定（如 \"review\"、\"systematic review\"、\"application\" 等）；\n"
        "4. 可使用引号 \"\"、AND、OR来提高检索质量；\n"
        "5. 各个检索语句之间请用中文分号 `；` 分隔；\n"
        "6. 请使用英文、保留核心关键词、必要时添加双引号和限定词（如 review、application）\n"
        "7. 只输出最终的检索语句，不要解释。\n"
        "请将自然语言请求转换为可以在 Google Scholar 中粘贴使用的英文检索语句，包含以下特征：精准关键词（用引号）、限定字段（如 intitle: 或 inauthor: 可选）、可包含 AND、OR、site:可选添加关键词如 \"systematic review\" 或 \"meta-analysis\""
    )

    # 传入'scontent'和'ucontent'
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]


    for attempt in range(max_retries +1):
        try:
            start_time = time.time()
            # model = ”deepseek-r1“
            response = openai.ChatCompletion.create(
                model="deepseek-reasoner",
                messages=messages,
                stream=streaming_flg
            )
            msg = None
            if streaming_flg:  # 流式响应标识
                msg, response = process_streaming_response(response)
            else:
                if not response.choices:
                    raise ValueError("No choices return from API.")
                msg = response.choices[0].message['content']

            # 成功获取到消息，则返回结果
            if msg:
                end_time = time.time()
                print(f"耗时:{end_time - start_time:.2f}s    GPT output: {msg}")
                time.sleep(3)
                return msg, response

        except Exception as err:
            print(f'OpenAI API Error: {str(err)}')
            if attempt < max_retries:
                print(f"Retrying... (Attempt {attempt + 1} of {max_retries})")
                time.sleep(2 ** (attempt + 2))  # 使用指数退避策略延迟重试（延迟时间为 2^(attempt + 2) 秒）。

            else:
                print(f"请求出错: {err}")
                return

# 流式输出结果
def process_streaming_response(response):
    llist = []
    msg = ""
    for i in response:
        if len(i['choices']) != 0:
            delta = i['choices'][0]['delta']
            content = delta.get('content', None)
            if content is not None:
                msg += content
        else:
            continue

    def generator(llist):
        for i in llist:
            yield i

    return msg, generator(llist)


# 示例用法
# if __name__ == "__main__":
#     natural_input = input("输入自然语言搜索描述：")
#     google_query = get_query(natural_input)
#     print(f"Google 搜索语句: {google_query}")

