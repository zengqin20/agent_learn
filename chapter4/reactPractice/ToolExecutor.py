from typing import Dict, Any

class ToolExecutor:
    """
    一个工具执行器，负责管理和执行工具。
    """
    def __init__(self) :
        # 定义所有工具
        self.tools: Dict[str, Dict[str, Any]] = {}
    def registerTool(self,name:str, description:str, func:callable):
        """
        向工具箱中注册一个新工具
        """
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def getTool(self, name:str) -> callable:
        """
        根据名称获取一个工具的执行函数。
        """
        # 链式调用，get name的时候，如果没找到，返回空字典{}作为默认值
        return self.tools.get(name, {}).get("func")

    def getAvailableTools(self) -> str:
        """
        获取所有已注册工具的名称列表。
        """
        # 列表推导式和字符串连接
        # self.tools.items() - 遍历字典的键值对
        return "\n".join([
            f"-{name}: {info['description']}"
            for name, info in self.tools.items()
        ])
