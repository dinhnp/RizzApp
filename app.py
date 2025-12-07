import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Rizz - Trợ Lý Cưa Cẩm",
    page_icon="💘",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Soft Playful Theme ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles - Mesh Gradient Background */
    .stApp {
        font-family: 'Nunito', sans-serif;
        background-color: #0f0c29;
        overflow: hidden;
    }

    /* Animated Mesh Gradient Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
        z-index: -2;
    }

    .stApp::after {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 50% 50%, rgba(76, 29, 149, 0.4), transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(219, 39, 119, 0.4), transparent 40%),
            radial-gradient(circle at 20% 80%, rgba(14, 165, 233, 0.4), transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(249, 115, 22, 0.4), transparent 40%);
        filter: blur(60px);
        animation: meshMove 20s ease-in-out infinite alternate;
        z-index: -1;
        pointer-events: none;
    }

    @keyframes meshMove {
        0% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(-5%, 5%) rotate(5deg); }
        50% { transform: translate(5%, -5%) rotate(-5deg); }
        75% { transform: translate(-5%, -5%) rotate(5deg); }
        100% { transform: translate(5%, 5%) rotate(0deg); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    
    /* Custom Header - Playful gradient */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8a65 50%, #ffb347 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #aaa;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 3px dashed rgba(255, 107, 157, 0.4) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #ff6b9d !important;
        background: rgba(255, 107, 157, 0.1) !important;
        transform: scale(1.02);
    }
    
    .stFileUploader label {
        color: #ccc !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        letter-spacing: 0.5px;
    }
    
    /* Primary Button - Playful & Bouncy */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8a65 100%);
        color: white;
        font-weight: 800;
        font-size: 1.3rem;
        padding: 1.2rem 2.5rem;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        box-shadow: 0 8px 25px rgba(255, 107, 157, 0.4);
        text-transform: none;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 15px 35px rgba(255, 107, 157, 0.5);
        background: linear-gradient(135deg, #ff8a9e 0%, #ff9a75 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.01);
    }
    
    /* Sidebar Styling - Dark & Clean */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #252533 0%, #1e1e2a 100%);
        border-right: 1px solid rgba(255, 107, 157, 0.2);
    }
    
    /* Sidebar Typography */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #e0e0e0 !important;
        font-weight: 600;
        font-size: 1.15rem !important;
        letter-spacing: 0.3px;
    }

    [data-testid="stSidebar"] h5 {
        color: #ffffff !important;
        font-weight: 800;
        font-size: 1.4rem !important;
        margin-bottom: 1.2rem !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 0.5px;
    }
    
    [data-testid="stSidebar"] .stMarkdown p {
        font-size: 1.1rem !important;
    }
    
    /* Sidebar Title */
    .sidebar-title {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8a65 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Selectbox - Beautiful Dropdown */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 107, 157, 0.3) !important;
        border-radius: 15px !important;
        color: #eee !important;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #ff6b9d !important;
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.2);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #ff6b9d !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.2);
    }
    
    /* Radio buttons - Pill style */
    .stRadio > div {
        gap: 0.6rem;
        flex-direction: column;
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 2px solid rgba(255, 107, 157, 0.3) !important;
        border-radius: 15px !important;
        padding: 0.8rem 1.2rem !important;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        color: #ddd !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #ff6b9d !important;
        background: rgba(255, 107, 157, 0.15) !important;
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(255, 107, 157, 0.2);
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff8a65 100%) !important;
        border-color: #ff6b9d !important;
        color: white !important;
    }
    
    /* Success/Info/Warning/Error boxes */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border: 2px solid #28a745 !important;
        border-radius: 15px !important;
        color: #155724 !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #e7f3ff 0%, #cce5ff 100%) !important;
        border: 2px solid #17a2b8 !important;
        border-radius: 15px !important;
        color: #0c5460 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%) !important;
        border: 2px solid #ffc107 !important;
        border-radius: 15px !important;
        color: #856404 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
        border: 2px solid #dc3545 !important;
        border-radius: 15px !important;
        color: #721c24 !important;
    }
    
    /* Image styling */
    .stImage {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        border: 3px solid rgba(255, 107, 157, 0.3);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #ff6b9d !important;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #999;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 2px dashed #ffe4ec;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #ffb6c1, transparent);
        margin: 1.5rem 0;
        border-radius: 2px;
    }
    
    /* Cards container for results */
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 5px 20px rgba(255, 107, 157, 0.1);
        border: 2px solid #ffe4ec;
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.15);
        border-color: #ffb6c1;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Cài đặt</div>', unsafe_allow_html=True)
    
    st.markdown("##### 🎭 Phong cách trả lời")
    style = st.selectbox(
        "Chọn style",
        ["Hài hước & Lầy lội 😂", "Lạnh lùng boy/girl 🧊", "Ngọt ngào 🍯", "Táo bạo 🔥"],
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("##### 🎯 Đối tượng mục tiêu")
    target = st.radio(
        "Chọn đối tượng",
        ["👩 Tán Bạn Gái", "👨 Tán Bạn Trai"],
        label_visibility="collapsed"
    )
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem;">
        Made with 💕 by AI<br/>
        <span style="color: #ff6b9d;">v2.0</span>
    </div>
    """, unsafe_allow_html=True)

# --- Main Content ---
st.markdown('<h1 class="hero-title">💘 Rizz Master</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Upload screenshot tin nhắn • Nhận gợi ý trả lời cực dính</p>', unsafe_allow_html=True)

# File uploader with custom styling
uploaded_file = st.file_uploader(
    "📸 Kéo thả hoặc click để upload ảnh chat",
    type=['png', 'jpg', 'jpeg'],
    help="Hỗ trợ PNG, JPG, JPEG"
)

if uploaded_file is not None:
    # Display image with rounded corners - constrained size
    image = Image.open(uploaded_file)
    
    # Use columns to constrain image width (center column only)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image(image, caption='📱 Ảnh chat của bạn', use_container_width=True)
    
    st.markdown("")  # Spacing
    
    if st.button("✨ RIZZ ME UP! ✨", use_container_width=True):
        if not api_key:
            st.error("⚠️ Vui lòng thêm GEMINI_API_KEY vào file .env!")
        else:
            try:
                with st.spinner("🔮 Đang phân tích và tạo Rizz lines..."):
                    # Configure Gemini
                    genai.configure(api_key=api_key)
                    
                    # Clean style and target for prompt
                    clean_style = style.split(" ")[0] if " " in style else style
                    clean_target = target.split(" ")[-1] if " " in target else target
                    
                    # Construct Prompt with JSON output
                    prompt = f"""
                    Role: You are an expert dating coach and conversation analyst specializing in "Rizz" and Gen Z dating culture. You are highly skilled at reading social dynamics and crafting the perfect responses.
                    
                    Task: 
                    1. READ THE ENTIRE CONVERSATION in the screenshot carefully from top to bottom
                    2. DETECT THE LANGUAGE of the conversation (English or Vietnamese)
                    3. Identify who is the user (usually on the right/blue bubbles) and who is the partner (on the left)
                    4. Understand the CONTEXT and FLOW of the conversation - what topics have been discussed, the tone, the energy
                    5. Analyze the partner's personality, interests, and communication style based on their messages
                    6. Note any hints, inside jokes, or opportunities that can be used in the reply
                    
                    Context:
                    - User's Goal: {clean_target}
                    - Desired Reply Style: {clean_style}
                    
                    Goal: Generate 3 distinct, CONTEXT-AWARE reply options that:
                    - Flow naturally from the entire conversation, not just the last message
                    - Reference previous topics or jokes if appropriate
                    - Match the energy and vibe of the conversation
                    - Are tailored to the partner's apparent personality and interests
                    - Use the selected style ({clean_style}) effectively
                    
                    ⚠️ CRITICAL LANGUAGE RULE - THIS IS MANDATORY:
                    - VIETNAMESE conversation = 100% Vietnamese output. EVERY SINGLE WORD must be in Vietnamese. Analysis in Vietnamese. Replies in Vietnamese. Explanations in Vietnamese. NO ENGLISH AT ALL.
                    - ENGLISH conversation = 100% English output. Every word in English.
                    - DO NOT mix languages. DO NOT write "The conversation is in Vietnamese" in English. Write it in Vietnamese: "Cuộc trò chuyện..."
                    - Use natural slang and texting style that matches the conversation.
                    
                    IMPORTANT: You MUST respond in this EXACT JSON format only, no other text:
                    {{
                        "analysis": "Tóm tắt cuộc trò chuyện (VIẾT BẰNG NGÔN NGỮ CỦA CUỘC TRÒ CHUYỆN): chủ đề chính, vibe, tính cách đối phương, cơ hội rizz",
                        "options": [
                            {{"reply": "Câu trả lời", "explanation": "Giải thích ngắn gọn (CÙNG NGÔN NGỮ)"}},
                            {{"reply": "Câu trả lời", "explanation": "Giải thích ngắn gọn (CÙNG NGÔN NGỮ)"}},
                            {{"reply": "Câu trả lời", "explanation": "Giải thích ngắn gọn (CÙNG NGÔN NGỮ)"}}
                        ]
                    }}
                    """
                    
                    def render_response_cards(response_text):
                        """Parse JSON response and render beautiful cards"""
                        import json
                        import re
                        
                        # Try to extract JSON from the response
                        try:
                            # Find JSON in the response
                            json_match = re.search(r'\{[\s\S]*\}', response_text)
                            if json_match:
                                data = json.loads(json_match.group())
                            else:
                                raise ValueError("No JSON found")
                            
                            # Render analysis
                            analysis_html = f'''<div style="background: rgba(255, 255, 255, 0.08); border-left: 4px solid #ff6b9d; padding: 1.5rem; border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);"><div style="color: #ff6b9d; font-weight: 800; margin-bottom: 0.8rem; font-size: 1.3rem; letter-spacing: 0.5px;">📊 Phân tích tình huống</div><div style="color: #ddd; font-size: 1.15rem; line-height: 1.7;">{data.get('analysis', '')}</div></div>'''
                            st.markdown(analysis_html, unsafe_allow_html=True)
                            
                            # Render each option as a card
                            colors = ["#ff6b9d", "#ff8a65", "#ffb347"]
                            
                            for i, option in enumerate(data.get('options', [])):
                                reply_text = option.get('reply', '')
                                explanation = option.get('explanation', '')
                                color = colors[i]
                                
                                card_html = f'''<div style="background: rgba(255, 255, 255, 0.06); border: 2px solid rgba(255, 107, 157, 0.25); border-radius: 16px; padding: 1rem 1.2rem; margin-bottom: 1rem; position: relative; overflow: hidden; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);"><div style="position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, #ff6b9d, #ff8a65, #ffb347);"></div><div style="margin-bottom: 0.8rem; margin-top: 0.3rem;"><span style="background: linear-gradient(135deg, {color} 0%, #ff8a65 100%); color: white; font-weight: 700; font-size: 0.85rem; padding: 0.4rem 1rem; border-radius: 20px; box-shadow: 0 3px 8px rgba(255, 107, 157, 0.25);">Option {i+1}</span></div><div style="color: #fff; font-size: 1.15rem; line-height: 1.5; margin-bottom: 0.8rem; padding: 0.8rem 1rem; background: rgba(255, 107, 157, 0.1); border-radius: 12px; border-left: 4px solid {color}; font-weight: 600;">"{reply_text}"</div><div style="color: #bbb; font-size: 0.95rem; font-style: italic; display: flex; align-items: flex-start; gap: 0.5rem;"><span style="color: {color};">💡</span>{explanation}</div></div>'''
                                st.markdown(card_html, unsafe_allow_html=True)
                            
                            return True
                        except Exception as parse_err:
                            print(f"JSON parse error: {parse_err}")
                            # Fallback to markdown display
                            st.markdown(response_text)
                            return False
                    
                    # Attempt generation
                    try:
                        # Try default model first
                        default_model = 'gemini-1.5-flash'
                        model = genai.GenerativeModel(default_model)
                        response = model.generate_content([prompt, image])
                        
                        st.success("🎉 Đã có hàng! Chọn câu nào dính câu đó nha 😉")
                        st.markdown("")
                        render_response_cards(response.text)
                        
                    except Exception as e:
                        print(f"Error with default model: {e}")
                        
                        if "404" in str(e) and "not found" in str(e):
                            # Silently switch to fallback model                            
                            # Get available models
                            available_models = []
                            try:
                                for m in genai.list_models():
                                    if 'generateContent' in m.supported_generation_methods:
                                        available_models.append(m.name)
                            except Exception as list_err:
                                print(f"Error listing models: {list_err}")
                            
                            # Smart fallback selection
                            fallback_model_name = None
                            
                            for m in available_models:
                                if 'gemini-2.0-flash' in m and 'exp' not in m:
                                    fallback_model_name = m
                                    break
                            
                            if not fallback_model_name:
                                for m in available_models:
                                    if 'gemini-1.5-flash' in m:
                                        fallback_model_name = m
                                        break

                            if not fallback_model_name:
                                for m in available_models:
                                    if 'flash' in m:
                                        fallback_model_name = m
                                        break
                                        
                            if not fallback_model_name:
                                for m in available_models:
                                    if 'pro' in m: 
                                        fallback_model_name = m
                                        break
                            
                            if fallback_model_name:
                                try:
                                    model = genai.GenerativeModel(fallback_model_name)
                                    response = model.generate_content([prompt, image])
                                    st.success("🎉 Đã có hàng!")
                                    st.markdown("")
                                    render_response_cards(response.text)
                                except Exception as fallback_err:
                                    st.error(f"❌ Lỗi: {str(fallback_err)}")
                            else:
                                st.error("❌ Không tìm thấy model phù hợp")
                        else:
                            st.error(f"❌ Đã xảy ra lỗi: {str(e)}")
                            st.info("💡 Hãy kiểm tra lại API Key")
            
            except Exception as e:
                st.error(f"❌ Lỗi không mong muốn: {str(e)}")

else:
    # Empty state with attractive design
    st.markdown("""
    <div style="
        text-align: center;
        padding: 1rem 1rem;
        background: linear-gradient(145deg, rgba(255,107,157,0.05) 0%, rgba(196,69,105,0.05) 100%);
        border: 2px dashed rgba(255,107,157,0.3);
        border-radius: 20px;
        margin: 1rem 0;
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
        <div style="color: #e0e0e0; font-size: 1.2rem; margin-bottom: 0.5rem;">
            Chưa có ảnh nào được upload
        </div>
        <div style="color: #888; font-size: 0.95rem;">
            Hãy upload ảnh chụp màn hình đoạn chat để bắt đầu
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-text">
    💕 Được tạo bởi AI • Phiên bản 2.0<br/>
    <small>Sử dụng Gemini AI để phân tích và gợi ý</small>
</div>
""", unsafe_allow_html=True)
