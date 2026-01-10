import streamlit as st
from openai import OpenAI

# 1. 基础配置
st.set_page_config(page_title="小红书标题助手", page_icon="📝")

# 2. 注入优化后的 CSS (按钮改为蓝色)
st.markdown(
    """
    <style>
    /* 全局背景 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* 文字颜色 */
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

    /* 关键修改：按钮改为蓝色样式 */
    .stButton>button {
        background-color: #1E5494 !important; /* 深蓝色，匹配你的截图 */
        color: #FFFFFF !important;
        font-weight: bold;
        border: none !important;
        border-radius: 8px;
        width: 100%;
        height: 3em;
        transition: all 0.3s ease;
    }

    /* 按钮悬停效果 */
    .stButton>button:hover {
        background-color: #2866AD !important; /* 略亮的蓝色 */
        border: none !important;
        transform: scale(1.01);
    }

    /* 隐藏多余组件 */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. 初始化客户端
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
                        {"role": "system", "content": "你是一个小红书爆款文案专家，擅长捕捉用户情绪，使用抓人眼球的词汇和Emoji。"},
                        {"role": "user", "content": f"请为产品『{product_name}』写3个不同风格的小红书带货标题，要求包含Emoji，且具有极强的点击欲望。"}
                    ],
                    stream=False
                )
                
                result = response.choices[0].message.content
                st.success("✅ 爆款已就绪！")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"生成失败：{e}")
    else:
        st.warning("请先输入产品名称哦！")
