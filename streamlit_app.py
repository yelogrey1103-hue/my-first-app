import streamlit as st
from openai import OpenAI

# 1. 基础配置
st.set_page_config(page_title="小红书标题助手", page_icon="📝")

# 2. 加强版 CSS 注入（强制消除底部 Built with Streamlit 和 Fullscreen）
st.markdown(
    """
    <style>
    /* 全局黑色背景 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* 输入框样式 */
    .stTextInput input {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
    }

    /* 蓝色主按钮 */
    div.stButton > button {
        background-color: #1E5494 !important;
        color: #FFFFFF !important;
        font-weight: bold;
        border: none !important;
        border-radius: 8px;
        width: 100%;
        height: 3em;
    }

    /* --- 核心修改：彻底强制消除底部元素 --- */
    /* 隐藏页脚信息和链接 */
    footer {
        visibility: hidden !important;
        height: 0px !important;
        display: none !important;
    }
    
    /* 隐藏包含 Fullscreen 的顶部工具栏（对于 Streamlit 1.30+） */
    header {
        visibility: hidden !important;
        display: none !important;
    }

    /* 针对最新版 Streamlit 的工具栏容器 */
    .stAppToolbar, [data-testid="stStatusWidget"], .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* 强制移除页面底部容器的间距 */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. 初始化 DeepSeek 客户端
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com"
)

# 4. 界面逻辑
st.title("🚀 AI爆款标题生成器")
product_name = st.text_input("你的产品名称是什么？", placeholder="例如：养生壶")

if st.button("一键生成爆款"):
    if product_name:
        with st.spinner('AI 正在为您深度定制爆款标题...'):
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个小红书爆款文案专家。"},
                        {"role": "user", "content": f"请为产品『{product_name}』写3个不同风格的小红书带货标题，包含Emoji。"}
                    ],
                    stream=False
                )
                
                result = response.choices[0].message.content
                st.success("✅ 爆款已就绪！")
                st.markdown("---")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"生成失败：{e}")
    else:
        st.warning("请先输入产品名称哦！")
