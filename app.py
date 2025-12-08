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
    page_title="Rizz Me Up by Dinh Nguyen",
    page_icon="💘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Soft Playful Theme ---
st.markdown("""
<style>
    /* Import Google Fonts - Be Vietnam Pro (optimized for Vietnamese) */
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles - Mesh Gradient Background */
    .stApp {
        font-family: 'Be Vietnam Pro', sans-serif;
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
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    
    /* Hide Streamlit toolbar/header completely */
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    .stDeployButton {display: none !important;}
    div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* Reduce top padding in main container */
    .st-emotion-cache-1w723zb {
        padding: 2rem 1rem 10rem !important;
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
        margin-top: -5rem;
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
        background: linear-gradient(145deg, rgba(255,107,157,0.08) 0%, rgba(255,138,101,0.05) 100%) !important;
        border: 2px dashed rgba(255, 107, 157, 0.5) !important;
        border-radius: 24px !important;
        padding: 2.5rem 2rem !important;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #ff6b9d !important;
        background: linear-gradient(145deg, rgba(255,107,157,0.12) 0%, rgba(255,138,101,0.08) 100%) !important;
        transform: scale(1.01);
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.2);
    }
    
    .stFileUploader label {
        color: #e0e0e0 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.3px;
    }
    
    /* Style the drag text */
    .stFileUploader [data-testid="stFileUploaderDropzone"] p {
        color: #aaa !important;
        font-size: 0.95rem !important;
    }
    
    /* Hide the default ugly text and replace with styled version */
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 180px !important;
        cursor: pointer !important;
        background: linear-gradient(145deg, rgba(255,107,157,0.08) 0%, rgba(196,69,105,0.05) 100%) !important;
        border: 2px dashed rgba(255,107,157,0.4) !important;
        border-radius: 24px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #ff6b9d !important;
        background: linear-gradient(145deg, rgba(255,107,157,0.12) 0%, rgba(196,69,105,0.08) 100%) !important;
        transform: scale(1.01) !important;
        box-shadow: 0 10px 30px rgba(255, 107, 157, 0.2) !important;
    }
    
    /* Hide ALL default content inside dropzone */
    .stFileUploader [data-testid="stFileUploaderDropzone"] > div,
    .stFileUploader [data-testid="stFileUploaderDropzone"] span,
    .stFileUploader [data-testid="stFileUploaderDropzone"] button,
    .stFileUploader [data-testid="stFileUploaderDropzone"] small,
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }
    
    /* Show custom content via pseudo-elements */
    .stFileUploader [data-testid="stFileUploaderDropzone"]::before {
        content: "📸" !important;
        display: block !important;
        font-size: 3.5rem !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"]::after {
        content: "Đang kẹt ko biết nói gì? Cứu bồ điiii\\A Up ảnh chat (Eng/Viet) - Hỗ trợ PNG, JPG, JPEG" !important;
        display: block !important;
        white-space: pre-wrap !important;
        text-align: center !important;
        color: #ddd !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        line-height: 1.8 !important;
    }
    
    /* Hide the small text under uploader */
    .stFileUploader small {
        display: none !important;
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
    
    /* Image with overlay container */
    .image-with-overlay {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .image-caption {
        text-align: center;
        color: #aaa;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* X delete button positioned over image */
    .delete-overlay-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 100;
        background: rgba(0, 0, 0, 0.6);
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.3);
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
        backdrop-filter: blur(4px);
        text-decoration: none;
    }
    
    .delete-overlay-btn:hover {
        background: rgba(255, 60, 60, 0.9);
        border-color: rgba(255, 255, 255, 0.5);
        transform: scale(1.1);
    }
    
    /* Center the delete button below image */
    .image-with-overlay + div + div [data-testid="stButton"],
    [data-testid="column"] .image-with-overlay ~ div [data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
    }
    
    .image-with-overlay ~ div [data-testid="stButton"] button {
        background: transparent !important;
        color: #ff6b9d !important;
        border: 1px solid rgba(255, 107, 157, 0.3) !important;
        border-radius: 20px !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.9rem !important;
        box-shadow: none !important;
    }
    
    .image-with-overlay ~ div [data-testid="stButton"] button:hover {
        background: rgba(255, 107, 157, 0.15) !important;
        border-color: #ff6b9d !important;
    }
    
    /* Delete button wrapper - centered on all devices */
    .delete-btn-wrapper {
        display: flex !important;
        justify-content: center !important;
        width: 100%;
    }
    
    /* Delete button - small and centered */
    [data-testid="column"]:nth-child(3) [data-testid="stButton"] button {
        background: transparent !important;
        color: #ff6b9d !important;
        border: 1px solid rgba(255, 107, 157, 0.4) !important;
        border-radius: 20px !important;
        padding: 0.3rem 0.8rem !important;
        font-size: 0.8rem !important;
        max-width: 80px !important;
        min-width: 50px !important;
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
        gap: 1rem;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    .stRadio > div > label {
        background: rgba(30, 30, 50, 0.8) !important;
        border: 2px solid rgba(255, 107, 157, 0.4) !important;
        border-radius: 25px !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        color: #ffffff !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        white-space: nowrap;
    }
    
    .stRadio > div > label span,
    .stRadio > div > label p,
    .stRadio > div > label div {
        color: #ffffff !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #ff6b9d !important;
        background: rgba(255, 107, 157, 0.15) !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 157, 0.2);
    }
    
    .stRadio > div > label[data-checked="true"],
    .stRadio > div > label[data-baseweb="radio"]:has(input:checked) {
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
    
    /* Spinner text color */
    .stSpinner > div > div {
        color: white !important;
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

# --- Main Content ---
st.markdown('<h1 class="hero-title" style="text-align: center;">💘 Rizz Me Up 💘</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle" style="text-align: center;">Rep là dính • thính là say/slay</p>', unsafe_allow_html=True)

# --- Settings Row ---
st.markdown('<div style="text-align: center; color: white;"><b>🎯 Đối tượng mục tiêu</b></div>', unsafe_allow_html=True)

# Center the radio buttons
_, center_col, _ = st.columns(3)
with center_col:
    target = st.radio(
        "Chọn đối tượng",
        ["👩 Tán Gái", "👨 Tán Trai"],
        label_visibility="collapsed",
        horizontal=True
    )

st.markdown("")  # Spacing

# Initialize session state
if 'uploaded_file_data' not in st.session_state:
    st.session_state.uploaded_file_data = None

# Show uploader only when no file is stored
if st.session_state.uploaded_file_data is None:
    uploaded_file = st.file_uploader(
        "Upload",
        type=['png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )
    
    # Store file data when uploaded
    if uploaded_file is not None:
        st.session_state.uploaded_file_data = uploaded_file.read()
        st.rerun()

# Display uploaded image if exists
if st.session_state.uploaded_file_data is not None:
    # Load image from session state
    from io import BytesIO
    import base64
    
    image = Image.open(BytesIO(st.session_state.uploaded_file_data))
    
    # Convert image to base64 for HTML embedding
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    # Use columns to constrain image width (center column only)
    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        # Combined HTML structure with image and clickable overlay X button
        st.markdown(f'''
        <div class="image-with-overlay">
            <img src="data:image/png;base64,{img_base64}" style="width: 100%; max-height: 300px; object-fit: contain; border-radius: 12px;">
            <div class="image-caption">📱 Ảnh chat của bạn</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Delete button - narrower center column
    _, _, center_btn, _, _ = st.columns(5)
    with center_btn:
        if st.button("🗑️ Xóa", key="delete_image", use_container_width=True):
            st.session_state.uploaded_file_data = None
            st.rerun()
    
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
                    clean_target = target.split(" ")[-1] if " " in target else target
                    
                    # Construct Prompt with JSON output for ALL styles
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
                    
                    Goal: Generate 4 distinct reply options for EACH of the 4 styles below. That's 24 total replies.
                    
                    Styles to generate:
                    1. Thả thính 💋 (Pickup lines & Flirty)
                    2. Hài hước & Lầy lội 😂 (Funny & Playful)
                    3. Ngọt ngào 🍯 (Sweet & Romantic)
                    4. Táo bạo 🔥 (Bold & Flirty)
                    5. Mysterious 🌙 (Mysterious & Intriguing)
                    6. Lãng mạn 🌹 (Romantic & Poetic)
                    7. Playboy/Playgirl 😏 (Confident & Charming)
                    8. Lạnh lùng boy/girl 🧊 (Cool & Mysterious)
                    
                    Each reply should:
                    - Flow naturally from the entire conversation, not just the last message
                    - Reference previous topics or jokes if appropriate
                    - Match the energy and vibe of the conversation
                    - Be tailored to the partner's apparent personality and interests
                    
                    ⚠️ GEN Z VIBE CHECK (QUAN TRỌNG):
                    - Dùng ngôn ngữ Gen Z tự nhiên (teencode nhẹ, slang phổ biến như: ultr, tr, khum, j z tr, vãi, ủa alo, chấn động, slay, keo lì, mlem...)
                    - KHÔNG dùng văn phong ChatGPT/AI cứng nhắc. Phải giống người thật nhắn tin.
                    - KHÔNG viết hoa đầu câu nếu không cần thiết (lowercase aesthetic).
                    - Dùng emoji hợp lý, không spam emoji cũ kỹ (như 😄, 👍). Dùng emoji kiểu Gen Z (💀, 😭, 🤡, 💅, ✨, 🥹).
                    - Văn phong ngắn gọn, súc tích, không sến súa (trừ khi là style sến).
                    
                    ⚠️ CRITICAL LANGUAGE RULE - THIS IS MANDATORY:
                    - VIETNAMESE conversation = 100% Vietnamese output. EVERY SINGLE WORD must be in Vietnamese.
                    - ENGLISH conversation = 100% English output. Every word in English.
                    - DO NOT mix languages (trừ slang tiếng Anh phổ biến).
                    - Use natural slang and texting style that matches the conversation.
                    
                    IMPORTANT: You MUST respond in this EXACT JSON format only, no other text:
                    {{
                        "analysis": "Tóm tắt ngắn gọn cuộc trò chuyện (VIẾT BẰNG NGÔN NGỮ CỦA CUỘC TRÒ CHUYỆN)",
                        "styles": [
                            {{
                                "style_name": "Thả thính �",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }},
                            {{
                                "style_name": "Hài hước & Lầy lội 😂",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }},
                            {{
                                "style_name": "Ngọt ngào 🍯",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }},
                            {{
                                "style_name": "Táo bạo 🔥",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }},
                            {{
                                "style_name": "Mysterious �",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }},
                            {{
                                "style_name": "Lãng mạn 🌹",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }},
                            {{
                                "style_name": "Playboy/Playgirl �",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }},
                            {{
                                "style_name": "Lạnh lùng boy/girl 🧊",
                                "replies": ["reply1", "reply2", "reply3", "reply4"]
                            }}
                        ]
                    }}
                    """
                    
                    def render_response_cards(response_text):
                        """Parse JSON response and render beautiful cards for all styles"""
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
                            
                            # Style colors
                            style_colors = {
                                "Hài hước & Lầy lội 😂": "#FFD700",
                                "Ngọt ngào 🍯": "#FF69B4",
                                "Táo bạo 🔥": "#FF4500",
                                "Mysterious 🌙": "#6A5ACD",
                                "Lãng mạn 🌹": "#E91E63",
                                "Playboy/Playgirl 😏": "#FF1493",
                                "Thả thính 💋": "#DC143C",
                                "Lạnh lùng boy/girl 🧊": "#00CED1"
                            }
                            
                            # Render each style section
                            for style_data in data.get('styles', []):
                                style_name = style_data.get('style_name', '')
                                replies = style_data.get('replies', [])
                                color = style_colors.get(style_name, "#ff6b9d")
                                
                                # Style header
                                style_header = f'''<div style="background: linear-gradient(135deg, {color}22, {color}11); border: 2px solid {color}66; border-radius: 16px; padding: 1rem 1.2rem; margin: 1.5rem 0 1rem 0;"><h3 style="color: {color}; margin: 0; font-size: 1.3rem; font-weight: 700;">{style_name}</h3></div>'''
                                st.markdown(style_header, unsafe_allow_html=True)
                                
                                # Render replies for this style
                                for i, reply in enumerate(replies):
                                    reply_html = f'''<div style="background: rgba(255, 255, 255, 0.04); border-left: 3px solid {color}; padding: 0.8rem 1rem; margin-bottom: 0.6rem; border-radius: 8px;"><span style="color: {color}; font-weight: 600; font-size: 1rem;">Option {i+1}:</span> <span style="color: #eee; font-size: 1.2rem;">{reply}</span></div>'''
                                    st.markdown(reply_html, unsafe_allow_html=True)
                            
                            return True
                        except Exception as parse_err:
                            print(f"JSON parse error: {parse_err}")
                            # Fallback to markdown display
                            st.markdown(response_text)
                            return False
                    
                    # Attempt generation
                    try:
                        # Try default model first
                        default_model = 'gemini-2.0-flash-exp'
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
    # No image uploaded - the upload card above is already visible
    pass

# Footer
st.markdown("""
<div class="footer-text">
    💕 Having fun by Dinh Nguyen 💕<br/>
    <span style="font-size: 0.9rem;">Góp ý hoặc donate qua Facebook</span>
    <a href="https://www.facebook.com/dinhnp" target="_blank" style="
        display: inline-block;
        background: linear-gradient(135deg, #1877f2 0%, #3b5998 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        margin-left: 0.3rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(24, 119, 242, 0.3);
    ">Dinh Nguyen</a> <br/>
    <span style="font-size: 0.9rem;">App không lưu trữ hình ảnh upload của bạn</span>
</div>
""", unsafe_allow_html=True)
