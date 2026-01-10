import streamlit as st
from openai import OpenAI

# 1. 必须是第一行 Streamlit 命令，修改了页面标签名称
st.set_page_config(page_title="小红书标题助手", page_icon="📝")

# 2. 注入 CSS (黑底白字样式)
st.markdown(
    """
    <style>
    /* 全局背景设为黑色，文字设为白色 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* 强制所有标题和段落显示为白色 */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* 输入框样式定制：深灰背景+白字 */
    .stTextInput input {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #444444 !important;
    }

    /* 按钮样式定制：白底黑字 */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
    }

    /* 隐藏顶部和底部修饰 */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# 3. 初始化客户端 (确保 Secrets 中已配置 DEEPSEEK_API_KEY)
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com"
)

# 4. 业务逻辑 (已更新文案)
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
                st.markdown(result)
                
            except Exception as e:
                st.error(f"生成失败，请检查网络或配置：{e}")
    else:
        st.warning("请先输入产品名称哦！")
