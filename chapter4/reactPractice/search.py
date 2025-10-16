from ddgs import ddgs
    # 这里使用的ddgs
def search(query: str) -> str:
        """
        网页搜索引擎根据。
        使用DuckDuckGo 来搜索并返回排名前3的结果摘要。
        """
        print(f"搜索查询: {query}")
        try:
            # 使用with上下文管理器处理ddgs
            with ddgs() as ddgs:
                # max_results 控制返回结果的数量
                # ddgs.text(query, max_results=3) 返回一个生成器，用于迭代搜索结果，需要被迭代才会获取实际数据
                # for r in ...  遍历生成器的每个元素
                # 列表推导式（快速生成列表） [expression for item in iterable] ，示例：numbers = [i for i in range(5)] --- numbers = [0, 1, 2, 3, 4]
                results = [r for r in ddgs.text(query, max_results=3)]
            if not results:
                # not是运算符，类似于非 ，整体就是results为假（None、False、0、(空字符串), [] (空列表), () (空元组), {} (空字典)、set()空集合、自定义对象的特殊情况），
                return f"对不起，没有找到关于 '{query}' 的信息。"

            # 将结果格式化为对LLM友好的字符串
            result_strings =[]
            #  enumerate 返回一个枚举对象，生成(index, value)对
            for i, result in enumerate(results):
                result_strings.append(f"[{i+1}] {result['title']}\n{result['body']}")
            return "\n\n".join(result_strings)

        except Exception as e:
            return f"搜索过程中出现错误: {e}"