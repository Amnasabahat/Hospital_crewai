import streamlit as st
from agents import process_complaint
from test_cases import sample_inputs
import json
from datetime import datetime
import time

# Custom CSS for unique styling
def apply_custom_styles():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit header and navbar */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #0f172a;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Card styling - Dark mode adaptive */
    .input-card, .result-card {
        background: var(--background-color, white);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid var(--border-color, rgba(230, 230, 230, 0.8));
        transition: all 0.3s ease;
        color: var(--text-color, #374151);
    }
    
    .input-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text-color, #374151);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Input styling - Enhanced for consistency */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        font-size: 1rem;
        padding: 1.2rem;
        transition: all 0.3s ease;
        min-height: 50px ;
        resize: vertical;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox styling - Dark mode compatible */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        min-height: 60px !important;
        background: var(--background-color, white);
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        padding: 0.5rem 1rem;
    }

    .stSelectbox > div > div:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    /* Dark mode adaptive selectbox text */
    .stSelectbox [data-baseweb="select"] {
        border: none !important;
        color: var(--text-color) !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        color: var(--text-color) !important;
        background: transparent !important;
    }
    
    .stSelectbox [data-baseweb="select"] [role="option"] {
        color: var(--text-color) !important;
        background: var(--background-color, white) !important;
    }
    
    .stSelectbox [data-baseweb="select"] [role="option"]:hover {
        background: var(--secondary-background-color, #f0f0f0) !important;
    }
    
    /* Radio button styling - Dark mode compatible */
    .stRadio {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 2rem 0 !important;
        min-height: 10px!important;
        box-shadow: none !important;
    }
    
    .stRadio > div {
        flex-direction: row !important;
        gap: 2rem !important;
        align-items: stretch !important;
        justify-content: center !important;
        width: 100% !important;
        display: flex !important;
        padding: 0 !important;
    }
    .stRadio > div {
    display: flex !important;
    justify-content: center !important;
    gap: 2rem !important;
    flex-wrap: wrap !important;
    width: 100% !important;
}

    
    .stRadio label {
        background: var(--background-color, white) !important;
        padding: 1rem 1.5rem !important;
        border-radius: 10px !important;
        border: 2px solid #e5e7eb !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        text-align: center !important;
        flex: 1 !important;
        min-width: 900px !important;
        min-height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08) !important;
        color: var(--text-color, #374151) !important;
    }

    .stRadio label:hover {
        border-color: #667eea !important;
        background: rgba(102, 126, 234, 0.05) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.15) !important;
    }

   .stRadio [aria-checked="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-weight: 700 !important;
}

    .stRadio input[type="radio"] {
        display: none !important;
    }
    /* Process button */
    .process-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 2rem auto;
        display: block;
        width: fit-content;
    }
    
    .process-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
    }
    
    /* Status indicators - Dark mode adaptive */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
    }
    
    /* Processing animation - Dark mode adaptive */
    .processing-container {
        text-align: center;
        padding: 3rem 2rem;
        background: var(--processing-bg-light, linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%));
        border-radius: 15px;
        margin: 2rem 0;
        border: 2px solid var(--processing-border-light, #fcd34d);
    }
    
    .processing-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--processing-title-light, #92400e);
        margin-bottom: 1rem;
    }
    
    .processing-text {
        color: var(--processing-text-light, #a16207);
        font-size: 1.1rem;
    }
    
    /* Results styling - FIXED for dark mode */
    .final-output {
        background: var(--final-output-bg, linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%));
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #8b5cf6;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
        color: var(--final-output-color, #581c87);
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.1);
    }
    
    .agent-step {
        background: var(--secondary-background-color, #f9fafb);
        border: 1px solid var(--border-color, #e5e7eb);
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        font-size: 1rem;
        line-height: 1.5;
        color: var(--text-color, #374151);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .agent-header {
        font-weight: 600;
        color: var(--text-color, #374151);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Download button */
    .download-section {
        margin-top: 2rem;
        text-align: center;
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.3);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(5, 150, 105, 0.4);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Stats card styling - Match input text area dimensions */
    .stats-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
        padding: 1.8rem 1.5rem; 
        border-radius: 12px; 
        border: 2px solid #a7f3d0; 
        text-align: center;
        margin: 1rem 0;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .stats-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
    }
    
    .stats-number {
        font-size: 2rem; 
        font-weight: bold; 
        color: #065f46;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        color: #047857; 
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Dark mode variables - Streamlit automatically sets these */
    :root {
        --text-color: #262730;
        --background-color: #ffffff;
        --secondary-background-color: #f0f2f6;
        --border-color: rgba(230, 230, 230, 0.8);
        --final-output-bg: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
        --final-output-color: #581c87;
        --processing-bg-light: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%);
        --processing-border-light: #fcd34d;
        --processing-title-light: #92400e;
        --processing-text-light: #a16207;
    }
    
    /* Dark mode overrides */
    [data-theme="dark"] {
        --text-color: #fafafa;
        --background-color: #0e1117;
        --secondary-background-color: #262730;
        --border-color: rgba(255, 255, 255, 0.1);
        --final-output-bg: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        --final-output-color: #c4b5fd;
        --processing-bg-light: linear-gradient(135deg, #451a03 0%, #78350f 100%);
        --processing-border-light: #f59e0b;
        --processing-title-light: #fbbf24;
        --processing-text-light: #f59e0b;
    }
    
    /* Force dark mode styling for Streamlit components */
    [data-theme="dark"] .final-output {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%) !important;
        color: #c4b5fd !important;
        border-left-color: #a78bfa !important;
    }
    
    [data-theme="dark"] .processing-container {
        background: linear-gradient(135deg, #451a03 0%, #78350f 100%) !important;
        border-color: #f59e0b !important;
    }
    
    [data-theme="dark"] .processing-title {
        color: #fbbf24 !important;
    }
    
    [data-theme="dark"] .processing-text {
        color: #f59e0b !important;
    }
    
    [data-theme="dark"] .agent-step {
        background: #262730 !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: #fafafa !important;
    }
    
    [data-theme="dark"] .agent-header {
        color: #fafafa !important;
    }
    
    [data-theme="dark"] .card-title {
        color: #fafafa !important;
    }
    
    [data-theme="dark"] .input-card,
    [data-theme="dark"] .result-card {
        background: #0e1117 !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: #fafafa !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }
        
        .main-container {
            margin: 0.5rem;
            padding: 1.5rem;
        }
        
        .process-button {
            width: 100%;
            padding: 1rem;
        }
        
        .stRadio > div {
            flex-direction: column !important;
            gap: 1.5rem !important;
        }
        
        .stRadio label {
            max-width: 100% !important;
            width: 100% !important;
            margin: 0 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Page configuration
    st.set_page_config(
        page_title="🏥 Hospital Crew AI",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom styles
    apply_custom_styles()
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🏥 Hospital Crew AI</h1>
        <p class="subtitle">Intelligent Healthcare Complaint Processing System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats section
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <div class="stats-number">98.5%</div>
            <div class="stats-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%); border: 2px solid #fcd34d;">
            <div class="stats-number" style="color: #92400e;">2.3s</div>
            <div class="stats-label" style="color: #a16207;">Avg Response Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card" style="background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); border: 2px solid #a5b4fc;">
            <div class="stats-number" style="color: #3730a3;">24/7</div>
            <div class="stats-label" style="color: #4338ca;">Available</div>
        </div>
        """, unsafe_allow_html=True)
    
   
    st.markdown('<div class="input-box-wrapper">', unsafe_allow_html=True)
    # Provider selection dropdown
    provider = st.selectbox("🤖 Select AI Provider", ["OpenAI", "Groq"], index=1)
    provider_key = provider.lower()  # 'openai' or 'groq'

    # Radio options (without that extra box)
    input_mode = st.selectbox(
    "📋 Select Input Method",
    ["Direct Input", "Pre-configured Cases"],
    key="input_mode"
    )

    # Input area
    if input_mode == "Direct Input":
        user_input = st.text_area(
            "✍️ Enter Your Healthcare Concern",
            height=120,
            placeholder="Please describe your healthcare concern...",
            help="Provide a detailed description of your healthcare facility concern"
        )
    else:
        user_input = st.selectbox(
            "📋 Select from Sample Cases",
            sample_inputs,
            help="Choose from pre-configured healthcare scenarios for demonstration"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced process button
    if st.button("🚀 Process Complaint", type="primary", use_container_width=False):
        if not user_input or not user_input.strip():
            st.markdown("""
            <div class="status-warning">
                ⚠️ Please enter a complaint before submitting
            </div>
            """, unsafe_allow_html=True)
        else:
            # Processing animation
            st.markdown("""
            <div class="processing-container">
                <div class="processing-title">🔄 Processing Your Complaint</div>
                <div class="processing-text">Our AI crew is analyzing your request and generating a solution...</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress indication
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            try:
                # Process the complaint with default provider
                with st.spinner("🤖 AI agents are working..."):
                    result = process_complaint(user_input, provider=provider_key)
                
                progress_bar.empty()
                
                # Success message
                st.balloons()
                st.markdown("""
                <div class="status-success">
                    ✅ Complaint processed successfully! 
                </div>
                """, unsafe_allow_html=True)
                
                # Results section
                st.markdown("""
                <div class="result-card">
                    <h3 class="card-title">📋 Processing Results</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Final output with enhanced styling
                st.markdown("### 🎯 Final Recommendation")
                st.markdown(f"""
                <div class="final-output">
                    {result["final"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Agent steps
                st.markdown("### 🔄 Processing Steps")
                
                for i, step in enumerate(result["steps"], 1):
                    # Determine status icon
                    status_icon = "✅" if step.get("status") == "completed" else "🔄"
                    agent_icon = "🤖" if "agent" in step.get("agent", "").lower() else "👨‍⚕️"
                    
                    with st.expander(f"{status_icon} Step {i}: {agent_icon} {step['agent']}", expanded=False):
                        st.markdown(f"""
                        <div class="agent-step">
                            <div class="agent-header">
                                {agent_icon} <strong>{step['agent']}</strong>
                                <span style="color: #10b981; font-size: 0.9rem;">● {step.get('status', 'completed')}</span>
                            </div>
                            <div style="margin-top: 0.5rem;">
                                {step["output"]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                

                # Create download data with timestamp
                download_data = {
                    "timestamp": datetime.now().isoformat(),
                    "provider": provider_key,
                    "complaint": user_input,
                    "result": result
                }
                
                json_data = json.dumps(download_data, indent=2)
                filename = f"hospital_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    st.download_button(
                        "📄 Download Detailed Report",
                        data=json_data,
                        file_name=filename,
                        mime="application/json",
                        help="Download complete processing report as JSON file"
                    )
                
                # Feedback section
                st.markdown("---")
                st.markdown("### 💭 How was this response?")
                st.select_slider(
                    "Rate the quality:",
                    options=["Poor", "Fair", "Good", "Great", "Excellent"],
                    value="Good"
                )
                st.info(f"🤖 Provider: {provider}")
                
            except Exception as e:
                progress_bar.empty()
                st.markdown(f"""
                <div class="status-warning">
                    ❌ Error processing complaint: {str(e)}<br>
                    Please try again or contact system administrator.
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()