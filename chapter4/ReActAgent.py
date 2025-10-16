class ReActAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        """
        初始化 ReAct 智能体。
        """

        self.llm_client = llm_client
        self.tools_executor = tool_executor
        self.max_steps = max_steps
        self.history = []
    
    # 智能体的入口
    def run(self, question: str):
        """
        运行 ReAct 智能体，处理问题并返回答案。
        """
        self.history = [] #每次运行时重置历史记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"---第 {current_step} 步---")

            #1. 格式化提示词
            # 获取工具描述
            tools_desc = self.tools_executor.getAvailableTools()
            # 获取历史记录
            history_str = "\n".join(self.history)
            # 为提示词模板提供 格式化参数
            prompt = REACT_PROMPT_TEMPLATE.format(tools=tools_desc, history=history_str, question=question)

            #2. 调用LLM进行思考
            messages = [{'role':'user','content':prompt}]
            response_text = self.llm_client.think(messages=messages)
        
            if not response_text:
                print("错误： LLM 没有返回响应")
                break
        
            # 3. 解析LLM的输出
            thought, action = self._parse_output(response_text)
            if thought:
                print(f"思考: {thought}")
        
            if not action:
                print("警告：未能解析出有效的Action，流程终止。")
                break
        
            # 4. 执行Action
            if action.startsWith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"最终答案: {final_answer}")
                return final_answer
            
            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                # 处理无效的Action格式
                continue
            print(f"🎬 行动Action: {tool_name}[{tool_input}]")
            tool_function = self.tools_executor.getTool(tool_name)
            if not tool_function:
                observation = f"错误：未找到名为 '{tool_name}' 的工具。"
            else:
                #调用真实工具
                observation = tool_function(tool_input)
                print(f"👀 观察: {observation}")
            
            # 将本轮的Action和Observation添加到历史记录中
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

            # 循环结束
            print("已达到最大步数，流程终止。")
            return None
        
    def _parse_output(self, text:str):
        """
        解析LLM的输出，提取Thought和Action。
        """
        # 提前文本中的thought、action内容
        thought_match = re.search(r"Thought: (.*)", text)
        action_match = re.search(r"Action: (.*)", text)
        # 如果找到匹配 (thought_match 不为 None)，thought_match.group(1) 获取捕获组的内容，.strip() 去除首尾空白字符
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        
        return thought, action

    def _parse_action(self, action_text: str):
        """
        解析Action字符串，提取工具名称和参数。
        """
        match = re.match(r"(\w+)\[(.*)\]", action_text)
        if match:
            return match.group(1), match.group(2)
        return None, None
