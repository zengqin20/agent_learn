import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict


# 加载 .env 文件中的环境变量
load_dotenv()

class HelloAgentsLLM:
    def __init__(self, model: str =None, api_key: str = None, base_url: str =None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。

        :param model: 模型 ID，默认值为 None。
        :param api_key: API 密钥，默认值为 None。
        :param base_url: 基础 URL，默认值为 None。
        :param timeout: 超时时间，默认值为 None。
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = api_key or os.getenv("LLM_API_KEY")
        baseUrl = base_url or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        # 检查列表中所有元素是否都不为空
        if not all([self.model, self.api_key, self.base_url]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")
        
        # 定义客户端client，用于与大语言模型进行交互
        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)
        
        """
        # -> str  返回类型注解，def 函数名(参数) -> 返回值类型:， 指定函数返回值的类型（字符串）
        # message: List[Dict[str, str]] 类型注解
        [
            {"role": "system", "content": "你是一个助手"},
            {"role": "user", "content": "写一段代码"}
        ]  # 符合 List[Dict[str, str]]
        """
        def think(self, message: List[Dict[str, str]], temperature: float = 0)-> str:
            """
            调用大语言模型进行思考，并返回其响应。

            :param message: 包含消息的列表，每个消息是一个字典，包含 'role' 和 'content' 键。
            :param temperature: 温度参数，用于控制生成文本的随机性，默认值为 0。
            :return: 模型生成的文本。
            """
            print(f"正在调用 {self.model} 模型")
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=message,
                    temperature=temperature,
                    stream=True
                )

                # 处理流式响应
                print(' 大模型响应成功：')
                collected_content = []
                for chunk in response:
                    content = chunk.choices[0].delta.content or ""
                    print(content, end="" ,flush=True)
                    collected_content.append(content)
                print() #在流式输出后结束换行
                return "".join(collected_content)
            except Exception as e:
                # Exception 是所有异常的基类，几乎所有的错误类型都继承自它
                print(f"调用大模型时出错: {e}")
                return ""


# ---客户端使用示例---
"""
Python 的特殊惯用法，用来区分"直接运行"和"被导入"两种情况
__name__ 是一个内置变量，
当模块被直接运行时(python hello_agents.py, print(__name__))，__name__ 的值为 "__main__"；
当模块被导入时(# 如果在另一个文件中：import hello_agents print(__name__)  # 输出：hello_agents（文件名）)，__name__ 的值为模块的名称。
"""
if __name__ == '__main__':
    try: 
        llmClient = HelloAgentsLLM()
        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]

        print("-- 调用 LLM --")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("LLM 响应:\n", responseText)
    except ValueError as e:
           # ValueError 是当传入的参数类型错误时触发的异常
           print(e)