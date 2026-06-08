import streamlit as st
from network_diagnosis import create_network_diagnosis_agent

# 页面配置
st.set_page_config(
    page_title="网络故障诊断智能系统",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session state
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 侧边栏
with st.sidebar:
    st.title("🌐 网络故障诊断智能系统")
    st.markdown("---")
    
    st.subheader("📋 可用工具")
    st.markdown("""
    - `ping` - 测试主机连通性
    - `traceroute` - 追踪路由路径
    - `nslookup` - DNS 查询
    - `check_port` - 端口检测 (格式: host:port)
    - `get_local_network_info` - 获取本地网络信息
    """)
    
    st.markdown("---")
    
    if st.button("🔄 初始化 Agent"):
        with st.spinner("正在初始化诊断系统..."):
            try:
                st.session_state.agent = create_network_diagnosis_agent()
                st.success("✅ 系统初始化成功！")
            except Exception as e:
                st.error(f"❌ 初始化失败: {str(e)}")
                st.info("请确保已在 .env 文件中配置了 DASHSCOPE_API_KEY")

# 主页面
st.title("🌐 网络故障诊断智能系统")
st.markdown("---")

# 欢迎信息
if not st.session_state.agent:
    st.info("👋 欢迎使用网络故障诊断智能系统！")
    st.warning("⚠️ 请先在侧边栏初始化系统")
else:
    # 显示聊天历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 输入框
    if prompt := st.chat_input("请描述您的网络问题..."):
        # 添加用户消息到历史
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 生成回答
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("🤔 正在分析问题..."):
                try:
                    # 调用 agent
                    result = st.session_state.agent.invoke({"input": prompt})
                    full_response = result["output"]
                except Exception as e:
                    full_response = f"❌ 发生错误: {str(e)}"
            
            message_placeholder.markdown(full_response)
        
        # 添加助手响应到历史
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# 页脚
st.markdown("---")
st.caption("💡 提示: 您可以问诸如 '为什么我访问不了 google.com？'、'帮我检查 github.com 的连通性' 等问题")
