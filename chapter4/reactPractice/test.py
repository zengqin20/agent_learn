from ToolExecutor import ToolExecutor
from search import search
# 将search工具注册到工具箱中
if __name__ == "__main__":
    # 1.初始化工具执行器
    tool_executor = ToolExecutor()

    # 2.注册搜索工具
    tool_executor.registerTool(
        "Search",
        "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。",
        search
    )

    # 3. 打印可用的工具
    print("\n ----------可用的工具----------:")
    print(tool_executor.getAvailableTools())

    # 4. 智能体的Action问题
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"
    
    tool_function = tool_executor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察Observation----")
        print(observation)
    else:
        print(f"错误：未找到名为 '{tool_name}' 的工具。")

