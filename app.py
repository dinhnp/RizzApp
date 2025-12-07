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
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    
    /* Custom Header */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 50%, #ff6b9d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #a0a0a0;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Upload Area */
    .upload-container {
        background: linear-gradient(145deg, rgba(255,107,157,0.1) 0%, rgba(196,69,105,0.1) 100%);
        border: 2px dashed rgba(255,107,157,0.4);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .upload-container:hover {
        border-color: rgba(255,107,157,0.8);
        background: linear-gradient(145deg, rgba(255,107,157,0.15) 0%, rgba(196,69,105,0.15) 100%);
    }
    
    /* Style the file uploader */
    .stFileUploader > div > div {
        background: transparent !important;
    }
    
    .stFileUploader label {
        color: #e0e0e0 !important;
    }
    
    /* Primary Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255,107,157,0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(255,107,157,0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Response Cards */
    .response-card {
        background: linear-gradient(145deg, rgba(40,40,50,0.9) 0%, rgba(30,30,40,0.9) 100%);
        border: 1px solid rgba(255,107,157,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .response-card:hover {
        border-color: rgba(255,107,157,0.5);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(255,107,157,0.15);
    }
    
    .response-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.8rem;
    }
    
    .response-number {
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
    }
    
    .response-text {
        color: #e8e8e8;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 0.8rem;
    }
    
    .response-explanation {
        color: #888;
        font-size: 0.9rem;
        font-style: italic;
        padding-left: 1rem;
        border-left: 2px solid rgba(255,107,157,0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(25,25,35,1) 0%, rgba(15,15,25,1) 100%);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    
    /* Sidebar Title */
    .sidebar-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #ff6b9d;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Style Selector Cards */
    .style-option {
        background: rgba(255,107,157,0.1);
        border: 1px solid rgba(255,107,157,0.2);
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .style-option:hover {
        background: rgba(255,107,157,0.2);
        border-color: rgba(255,107,157,0.4);
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess {
        background: linear-gradient(135deg, rgba(46,204,113,0.2) 0%, rgba(39,174,96,0.2) 100%);
        border: 1px solid rgba(46,204,113,0.4);
        border-radius: 12px;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(52,152,219,0.2) 0%, rgba(41,128,185,0.2) 100%);
        border: 1px solid rgba(52,152,219,0.4);
        border-radius: 12px;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(241,196,15,0.2) 0%, rgba(243,156,18,0.2) 100%);
        border: 1px solid rgba(241,196,15,0.4);
        border-radius: 12px;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(231,76,60,0.2) 0%, rgba(192,57,43,0.2) 100%);
        border: 1px solid rgba(231,76,60,0.4);
        border-radius: 12px;
    }
    
    /* Image styling */
    .stImage {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #ff6b9d !important;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #666;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .footer-text a {
        color: #ff6b9d;
        text-decoration: none;
    }
    
    /* Radio buttons styling */
    .stRadio > div {
        gap: 0.5rem;
    }
    
    .stRadio > div > label {
        background: rgba(255,107,157,0.1);
        border: 1px solid rgba(255,107,157,0.2);
        border-radius: 10px;
        padding: 0.6rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255,107,157,0.2);
        border-color: rgba(255,107,157,0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(40,40,50,0.8);
        border: 1px solid rgba(255,107,157,0.3);
        border-radius: 10px;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,107,157,0.5), transparent);
        margin: 1.5rem 0;
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
st.markdown('<h1 class="hero-title">💘 AI Rizz Master</h1>', unsafe_allow_html=True)
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
    
    if st.button("✨ Gợi ý câu trả lời Rizz", use_container_width=True):
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
                    Role: You are a Vietnamese dating expert and conversation analyst specializing in "Rizz" and Gen Z dating culture. You are highly skilled at reading social dynamics and crafting the perfect responses.
                    
                    Task: 
                    1. READ THE ENTIRE CONVERSATION in the screenshot carefully from top to bottom
                    2. Identify who is the user (usually on the right/blue bubbles) and who is the partner (on the left)
                    3. Understand the CONTEXT and FLOW of the conversation - what topics have been discussed, the tone, the energy
                    4. Analyze the partner's personality, interests, and communication style based on their messages
                    5. Note any hints, inside jokes, or opportunities that can be used in the reply
                    
                    Context:
                    - User's Goal: {clean_target}
                    - Desired Reply Style: {clean_style}
                    
                    Goal: Generate 3 distinct, CONTEXT-AWARE reply options that:
                    - Flow naturally from the entire conversation, not just the last message
                    - Reference previous topics or jokes if appropriate
                    - Match the energy and vibe of the conversation
                    - Are tailored to the partner's apparent personality and interests
                    - Use the selected style ({clean_style}) effectively
                    
                    Language Rule: Output ONLY in natural Vietnamese. Use slang (teencode, Gen Z terms) appropriately. Sound like a real person texting, not a robot.
                    
                    IMPORTANT: You MUST respond in this EXACT JSON format only, no other text:
                    {{
                        "analysis": "Tóm tắt ngắn gọn về cuộc trò chuyện: bao gồm chủ đề chính, tone/vibe của conversation, tính cách của đối phương, và cơ hội để rizz (2-3 câu)",
                        "options": [
                            {{"reply": "Câu trả lời thực tế", "explanation": "Giải thích ngắn gọn tại sao câu này phù hợp với context"}},
                            {{"reply": "Câu trả lời thực tế", "explanation": "Giải thích ngắn gọn tại sao câu này phù hợp với context"}},
                            {{"reply": "Câu trả lời thực tế", "explanation": "Giải thích ngắn gọn tại sao câu này phù hợp với context"}}
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
                            analysis_html = f'''<div style="background: linear-gradient(135deg, rgba(255,107,157,0.15) 0%, rgba(196,69,105,0.15) 100%); border-left: 4px solid #ff6b9d; padding: 1rem 1.5rem; border-radius: 0 12px 12px 0; margin-bottom: 1.5rem;"><div style="color: #ff6b9d; font-weight: 600; margin-bottom: 0.3rem;">📊 Phân tích</div><div style="color: #e0e0e0; font-size: 1rem;">{data.get('analysis', '')}</div></div>'''
                            st.markdown(analysis_html, unsafe_allow_html=True)
                            
                            # Render each option as a card
                            icons = ["💬", "💭", "💫"]
                            colors = ["#ff6b9d", "#c44569", "#a03050"]
                            
                            for i, option in enumerate(data.get('options', [])):
                                reply_text = option.get('reply', '')
                                explanation = option.get('explanation', '')
                                color = colors[i]
                                icon = icons[i]
                                
                                card_html = f'''<div style="background: linear-gradient(145deg, rgba(40,40,50,0.95) 0%, rgba(30,30,40,0.95) 100%); border: 1px solid {color}40; border-radius: 16px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; position: relative; overflow: hidden;"><div style="position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, {color}, transparent);"></div><div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem;"><span style="background: linear-gradient(135deg, {color} 0%, {color}cc 100%); color: white; font-weight: 700; font-size: 0.85rem; padding: 0.35rem 0.9rem; border-radius: 20px;">Option {i+1}</span><span style="font-size: 1.2rem;">{icon}</span></div><div style="color: #f5f5f5; font-size: 1.15rem; line-height: 1.6; margin-bottom: 0.8rem; padding: 0.8rem 1rem; background: rgba(255,107,157,0.08); border-radius: 10px; border-left: 3px solid {color};">"{reply_text}"</div><div style="color: #999; font-size: 0.9rem; font-style: italic; display: flex; align-items: flex-start; gap: 0.5rem;"><span style="color: {color};">💡</span>{explanation}</div></div>'''
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
                            st.warning(f"⏳ Đang chuyển sang model khác...")
                            
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
