import streamlit as st
from openai import OpenAI

# 1. 基础配置（必须在第一行）
st.set_page_config(page_title="小红书标题助手", page_icon="📝")

# 2. 注入所有 CSS 样式（黑底白字、蓝色按钮、隐藏所有 Streamlit 官方装饰）
st.markdown(
    """
    <style>
    /* 全局背景与文字颜色 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* 输入框样式定制 */
    .stTextInput input {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #444444 !important;
        border-radius: 8px !important;
    }

    /* 蓝色主按钮样式 */
    div.stButton > button {
        background-color: #1E5494 !important;
        color: #FFFFFF !important;
        font-weight: bold;
        border: none !important;
        border-radius: 8px;
        width: 100%;
        height: 3em;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #2866AD !important;
        border: none !important;
    }

    /* 彻底隐藏：页脚、全屏按钮、工具栏、顶部 Header */
    footer {visibility: hidden; height: 0px;}
    header {visibility: hidden;}
    .stAppToolbar {visibility: hidden; display: none;}
    [data-testid="stStatusWidget"] {visibility: hidden; display: none;}
    
    /* 移除页面多余间距，让布局更紧凑 */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. 初始化 DeepSeek 客户端
# 请确保在 Streamlit Cloud 的 Secrets 中配置了 DEEPSEEK_API_KEY
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com"
)

# 4. 业务逻辑界面
st.title("🚀 AI爆款标题生成器")

product_name = st.text_input("你的产品名称是什么？", placeholder="例如：养生壶")

if st.button("一键生成爆款"):
    if product_name:
        with st.spinner('AI 正在为您深度定制爆款标题...'):
            try:
                # 调用 DeepSeek 接口
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
                st.markdown("---")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"生成失败，请检查网络或配置：{e}")
    else:
        st.warning("请先输入产品名称哦！")
