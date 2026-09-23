import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# ==========================================
# 1. 网页界面基础设置
# ==========================================
st.set_page_config(page_title="A+ Page AI Generator", layout="wide", page_icon="🚀")
st.title("🚀 亚马逊 A+ 页面自动化生成系统 (v2.0)")
st.markdown("基于 Google Gemini API 与 Nano Banana Pro 渲染引擎")

# ==========================================
# 2. 侧边栏：配置 API Key (安全输入，不泄露)
# ==========================================
with st.sidebar:
    st.header("⚙️ 系统配置")
    user_api_key = st.text_input("请输入 Google AI Studio API Key:", type="password")
    nano_banana_key = st.text_input("请输入 Nano Banana Pro API Key:", type="password")
    st.warning("注：API Key 仅在当前网页运行，刷新后即焚，绝不保存在服务器。")

# ==========================================
# 3. 主界面：输入区 (对应你的第一步)
# ==========================================
st.header("📦 第一步：输入产品信息与参考视觉")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 产品基础档案")
    product_name = st.text_input("产品名称 (如：便携式充气户外床垫)")
    core_features = st.text_area("排名前三的核心卖点 (USP)")
    target_audience = st.text_input("目标人群与场景 (如：北美蓝领, 周末露营)")
    pain_points = st.text_area("竞品痛点 (如：半夜漏气塌陷)")
    brand_style = st.text_input("品牌调性与视觉风格 (如：硬核户外风)")

with col2:
    st.subheader("2. 上传参考 A+ 页面长图")
    uploaded_file = st.file_uploader("支持 JPG, PNG 格式", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="已上传参考图", use_column_width=True)

# ==========================================
# 4. 核心处理引擎：调用 Google Gemini (对应你的第二步)
# ==========================================
st.header("🧠 第二步：AI 智能拆解与生成")

if st.button("🚀 一键生成 7 屏 A+ 蓝图"):
    if not user_api_key:
        st.error("请先在左侧输入 Google API Key！")
    elif uploaded_file is None:
        st.error("请上传一张参考 A+ 页面长图！")
    else:
        with st.spinner("正在调用 Google Gemini 1.5 Pro 解析图像与重写文案..."):
            try:
                # 配置 Google API
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-1.5-pro') # 使用多模态模型
                
                # 组合发给大模型的超级 Prompt
                prompt = f"""
                你是一个顶级的亚马逊 A+ 页面视觉总监和文案大师。
                请结合我提供的产品信息和上传的图片，为我生成一套 7 屏的 A+ 页面蓝图。
                
                【产品信息】
                名称: {product_name}
                卖点: {core_features}
                人群: {target_audience}
                痛点: {pain_points}
                风格: {brand_style}
                
                【任务要求】
                请将输出拆解为 7 屏 (Screen 1 到 Screen 7)。
                每一屏必须包含：1. 英文主标题，2. 英文副标题，3. 排版建议，4. 发给 Nano Banana Pro 的生图关键词(英文)。
                """
                
                # 请求 Google AI Studio
                response = model.generate_content([prompt, image])
                
                st.success("✅ 解析成功！以下是生成的 7 屏蓝图：")
                st.markdown(response.text)
                
                # ==========================================
                # 5. Nano Banana Pro 对接端口 (模拟发送)
                # ==========================================
                st.info("🍌 系统已就绪，准备将指令发送给 Nano Banana Pro 进行生图和排版合成...")
                if st.button("将指令发送给 Nano Banana Pro (渲染)"):
                    st.success("指令发送成功！等待图像渲染返回...")
                    
            except Exception as e:
                st.error(f"生成失败，错误信息：{e}")
