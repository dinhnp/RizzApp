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

# --- Custom CSS for Premium Dark Theme ---
# --- Custom CSS for Premium Theme ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Outfit', sans-serif;
        background: #0f0c29;  /* fallback for old browsers */
        background: -webkit-linear-gradient(to right, #24243e, #302b63, #0f0c29);  /* Chrome 10-25, Safari 5.1-6 */
        background: linear-gradient(to right, #24243e, #302b63, #0f0c29); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 850px;
    }
    
    /* Custom Header */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #ff9966, #ff5e62);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        text-shadow: 0 10px 30px rgba(255, 94, 98, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #e0e0e0;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        opacity: 0.8;
    }
    
    /* Upload Area */
    .upload-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
    }
    
    .upload-container:hover {
        border-color: #ff9966;
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    /* Style the file uploader */
    .stFileUploader > div > div {
        background: transparent !important;
    }
    
    .stFileUploader label {
        color: #fff !important;
        font-size: 1.1rem;
    }
    
    /* Primary Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff9966 0%, #ff5e62 100%);
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        padding: 1rem 2rem;
        border: none;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(255, 94, 98, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 35px rgba(255, 94, 98, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(1px);
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    /* Sidebar Title */
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #ff9966, #ff5e62);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Style Selector Cards */
    .style-option {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        transition: all 0.2s ease;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        color: #fff;
    }
    
    /* Image styling */
    .stImage {
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #ff9966 !important;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: rgba(255,255,255,0.4);
        font-size: 0.9rem;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Radio buttons styling */
    .stRadio > div {
        gap: 0.8rem;
    }
    
    .stRadio > div > label {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        transition: all 0.2s ease;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        color: white;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 2rem 0;
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
    
    # Status indicator
    if api_key:
        st.success("✅ API Key đã kết nối")
    else:
        st.error("❌ Chưa có API Key")
    
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
    # Display image with rounded corners
    image = Image.open(uploaded_file)
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
                            analysis_html = f'''<div style="background: rgba(255,255,255,0.05); border-left: 4px solid #ff9966; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.1);"><div style="color: #ff9966; font-weight: 700; margin-bottom: 0.5rem; font-size: 1.1rem; letter-spacing: 0.5px; text-transform: uppercase;">📊 Phân tích tình huống</div><div style="color: #e0e0e0; font-size: 1.05rem; line-height: 1.6;">{data.get('analysis', '')}</div></div>'''
                            st.markdown(analysis_html, unsafe_allow_html=True)
                            
                            # Render each option as a card
                            icons = ["�", "�", "✨"]
                            colors = ["#ff9966", "#ff5e62", "#ff9966"]
                            
                            for i, option in enumerate(data.get('options', [])):
                                reply_text = option.get('reply', '')
                                explanation = option.get('explanation', '')
                                color = colors[i]
                                icon = icons[i]
                                
                                card_html = f'''<div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 1.5rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; transition: all 0.3s ease; box-shadow: 0 10px 30px rgba(0,0,0,0.1);"><div style="position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #ff9966, #ff5e62);"></div><div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;"><span style="background: linear-gradient(135deg, #ff9966 0%, #ff5e62 100%); color: white; font-weight: 700; font-size: 0.9rem; padding: 0.4rem 1rem; border-radius: 30px; box-shadow: 0 5px 15px rgba(255, 94, 98, 0.3);">Option {i+1}</span><span style="font-size: 1.4rem;">{icon}</span></div><div style="color: #fff; font-size: 1.25rem; line-height: 1.5; margin-bottom: 1rem; padding: 1rem 1.2rem; background: rgba(255,255,255,0.05); border-radius: 12px; border-left: 3px solid #ff9966; font-weight: 500;">"{reply_text}"</div><div style="color: rgba(255,255,255,0.6); font-size: 0.95rem; font-style: italic; display: flex; align-items: flex-start; gap: 0.6rem;"><span style="color: #ff9966;">💡</span>{explanation}</div></div>'''
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
        padding: 3rem 2rem;
        background: linear-gradient(145deg, rgba(255,107,157,0.05) 0%, rgba(196,69,105,0.05) 100%);
        border: 2px dashed rgba(255,107,157,0.3);
        border-radius: 20px;
        margin: 2rem 0;
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
