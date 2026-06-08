from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from llm_setup import get_tongyi_llm
from network_tools import ping, traceroute, nslookup, check_port, get_local_network_info


def create_network_diagnosis_agent():
    llm = get_tongyi_llm(temperature=0.0)
    
    tools = [
        Tool(
            name="ping",
            func=lambda x: ping(x),
            description="用于测试与目标主机的连接性。输入应为要ping的主机名或IP地址。"
        ),
        Tool(
            name="traceroute",
            func=lambda x: traceroute(x),
            description="用于追踪数据包到目标主机的路由路径。输入应为目标主机名或IP地址。"
        ),
        Tool(
            name="nslookup",
            func=lambda x: nslookup(x),
            description="用于查询域名的DNS解析记录。输入应为要查询的域名。"
        ),
        Tool(
            name="check_port",
            func=lambda x: check_port(x.split(':')[0], int(x.split(':')[1])) if ':' in x else "请使用格式: host:port",
            description="用于检查目标主机的指定端口是否开放。输入格式应为: host:port"
        ),
        Tool(
            name="get_local_network_info",
            func=lambda x: get_local_network_info(),
            description="用于获取本地网络接口信息，无需输入参数。"
        )
    ]
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # 使用 LangChain 标准的 ReAct 提示模板
    prompt = PromptTemplate.from_template("""你是一个专业的网络故障诊断工程师。你的任务是帮助用户诊断和解决网络问题。

你可以使用以下工具来帮助诊断:
{tools}

使用以下格式:

Question: 输入的问题
Thought: 思考需要做什么
Action: 选择工具，应该是 [{tool_names}] 中的一个
Action Input: 工具的输入
Observation: 工具的输出
... (这个 Thought/Action/Action Input/Observation 可以重复 N 次)
Thought: 现在我知道最终答案了
Final Answer: 问题的最终答案

开始!

聊天历史:
{chat_history}

Question: {input}
Thought: {agent_scratchpad}""")
    
    agent = create_react_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return agent_executor


def main():
    print("=" * 60)
    print("网络故障诊断智能系统")
    print("=" * 60)
    print("输入 'exit' 或 'quit' 退出程序\n")
    
    agent = create_network_diagnosis_agent()
    
    while True:
        try:
            user_input = input("\n请描述您的网络问题: ").strip()
            
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("感谢使用，再见！")
                break
            
            if not user_input:
                continue
            
            print("\n正在分析中...\n")
            result = agent.invoke({"input": user_input})
            print("\n" + "=" * 60)
            print("诊断结果:")
            print(result["output"])
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n感谢使用，再见！")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")


if __name__ == "__main__":
    main()
