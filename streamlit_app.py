import streamlit as st
from openai import OpenAI

# 1. 基础配置
st.set_page_config(page_title="小红书标题助手", page_icon="📝")

# 2. 加强版 CSS (黑色背景、蓝色按钮、隐藏页脚/全屏)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    .stTextInput input {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
    }

    /* 主生成按钮：蓝色 */
    div.stButton > button:first-child {
        background-color: #1E5494 !important;
        color: #FFFFFF !important;
        font-weight: bold;
        border: none !important;
        border-radius: 8px;
        width: 100%;
        height: 3em;
    }

    /* 重置按钮样式：透明带边框 */
    .reset-button > button {
        background-color: transparent !important;
        color: #888888 !important;
        border: 1px solid #444444 !important;
        font-size: 0.8em !important;
        height: 2.5em !important;
        margin-top: 15px !important;
    }

    /* 彻底隐藏底部装饰 */
    footer {visibility: hidden; height: 0px;}
    header {visibility: hidden;}
    .stAppToolbar {visibility: hidden; display: none;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none;}
    
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

# 定义重置逻辑
def reset_content():
    st.session_state["product_input"] = ""
    st.session_state["result_output"] = ""

# 初始化 session_state
if "product_input" not in st.session_state:
    st.session_state["product_input"] = ""
if "result_output" not in st.session_state:
    st.session_state["result_output"] = ""

# 4. 界面布局
# 使用 columns 让标题和清除按钮并排
col1, col2 = st.columns([4, 1])

with col1:
    st.title("🚀 AI爆款标题生成器")

with col2:
    # 放置清除按钮
    st.markdown('<div class="reset-button">', unsafe_allow_html=True)
    if st.button("清除"):
        reset_content()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 输入框绑定 session_state
product_name = st.text_input(
    "你的产品名称是什么？", 
    value=st.session_state["product_input"],
    placeholder="例如：养生壶",
    key="input_field"
)

if st.button("一键生成爆款"):
    if product_name:
        st.session_state["product_input"] = product_name # 保存输入
        with st.spinner('AI 正在为您深度定制爆款标题...'):
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个小红书爆款文案专家，擅长捕捉用户情绪，使用抓人眼球的词汇和Emoji。"},
                        {"role": "user", "content": f"请为产品『{product_name}』写3个不同风格的小红书带货标题，要求包含Emoji，且具有极强的点击欲望。"}
                    ],
                    stream=False
                )
                
                st.session_state["result_output"] = response.choices[0].message.content
                st.success("✅ 爆款已就绪！")
                
            except Exception as e:
                st.error(f"生成失败：{e}")
    else:
        st.warning("请先输入产品名称哦！")

# 显示结果
if st.session_state["result_output"]:
    st.markdown("---")
    st.markdown(st.session_state["result_output"])
