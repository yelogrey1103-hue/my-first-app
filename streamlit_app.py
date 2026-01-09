import streamlit as st
from openai import OpenAI # DeepSeek 使用 OpenAI 的库即可兼容

st.set_page_config(page_title="DeepSeek爆款助手", page_icon="💰")

# 从 Secrets 中安全获取 API Key
api_key = st.secrets["DEEPSEEK_API_KEY"]

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com" # 务必指向 DeepSeek 的服务器
)

st.title("🚀 DeepSeek 爆款标题生成器")
product_name = st.text_input("你的产品名称是什么？", placeholder="例如：养生壶")

if st.button("一键生成爆款"):
    if product_name:
        with st.spinner('DeepSeek 正在疯狂思考中...'):
            try:
                # 调用 DeepSeek 接口
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个小红书爆款文案专家，擅长使用情绪化词汇和Emoji。"},
                        {"role": "user", "content": f"请为产品『{product_name}』写3个不同风格的小红书带货标题。"}
                    ],
                    stream=False
                )
                
                # 显示结果
                result = response.choices[0].message.content
                st.success("✅ 生成成功！")
                st.markdown(result)
                
            except Exception as e:
                st.error(f"出错了：{e}")
    else:
        st.warning("请先输入产品名称哦！")
