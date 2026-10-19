import io
import os
import json
from typing import List, Dict, Any
import streamlit as st
import google.generativeai as genai
from PIL import Image
import docx
import pypdf

# ==========================================
# 1. PAN-INDIA MULTI-LANGUAGE & GEOGRAPHY DATA
# ==========================================

LANGUAGES = {
    "English": "English",
    "Hindi": "हिंदी (Hindi)",
    "Bengali": "বাংলা (Bengali)",
    "Telugu": "తెలుగు (Telugu)",
    "Marathi": "मराठी (Marathi)",
    "Tamil": "தமிழ் (Tamil)",
    "Urdu": "اردو (Urdu)",
    "Gujarati": "ગુજરાતી (Gujarati)",
    "Kannada": "ಕನ್ನಡ (Kannada)",
    "Malayalam": "മലയാളം (Malayalam)",
    "Odia": "ଓଡ଼ିଆ (Odia)",
    "Punjabi": "ਪੰਜਾਬੀ (Punjabi)",
    "Assamese": "অসমীয়া (Assamese)",
    "Sanskrit": "संस्कृतम् (Sanskrit)",
    "Kashmiri": "कॉशुर (Kashmiri)",
    "Konkani": "कोंकणी (Konkani)",
    "Manipuri": "মৈতৈলোন্ (Manipuri)",
    "Nepali": "नेपाली (Nepali)",
    "Sindhi": "سنڌي (Sindhi)",
    "Maithili": "मैथिली (Maithili)",
    "Dogri": "डोगरी (Dogri)",
    "Santali": "संताली (Santali)"
}

INDIA_STATES_UT = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", 
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", 
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
    "Uttar Pradesh", "Uttarakhand", "West Bengal", 
    "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", 
    "Delhi NCR", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

HEALTHCARE_CATEGORIES = {
    "Diagnostic & Imaging Centers": [
        "CT Scan Centers", 
        "MRI Diagnostic Labs", 
        "Sonography / Ultrasound Centers", 
        "X-Ray Imaging Labs", 
        "PET Scan & Advanced Nuclear Imaging", 
        "Pathology & Full Body Blood Testing Labs"
    ],
    "Specialized Hospitals & Clinical Depts": [
        "Neurology & Neurosurgery", 
        "Urology & Nephrology", 
        "Cardiology & Heart Care", 
        "Dermatology & Skin Specialists", 
        "Orthopedics & Joint Replacement", 
        "Pediatrics & Neonatology", 
        "Oncology (Cancer Treatment)", 
        "Gastroenterology", 
        "Ophthalmology (Eye Care)", 
        "Gynecology & Obstetrics"
    ],
    "Government & Public Health Infrastructure": [
        "AIIMS & Central Government Institutes", 
        "State Government Medical Colleges & General Hospitals", 
        "District Civil Hospitals & Community Health Centers (CHC/PHC)", 
        "ESIC & Indian Railways Hospitals", 
        "Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP) Kendra (Generic Medicines)"
    ],
    "Essential Emergency & Support Services": [
        "24/7 Blood Banks (Multi-Group)", 
        "Ambulance Services (Advanced Life Support / ICU)", 
        "Poison Control & Toxicological Centers"
    ]
}

# ==========================================
# 2. GEMINI 3.8 FLASH AI ENGINE SETUP
# ==========================================

def get_gemini_model():
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3.8-flash')

def analyze_medicine(med_name: str, language: str) -> dict:
    model = get_gemini_model()
    if not model:
        return {"error": "Gemini API Key is missing. Please configure GEMINI_API_KEY in Streamlit Secrets."}

    prompt = f"""
    You are an expert clinical pharmacologist. Analyze the medical item '{med_name}'.
    Provide the response strictly as a valid JSON object with these exact keys (written entirely in {language}):
    - "item_name": The standardized name of the medicine/syrup/tablet/cream/syringe.
    - "composition": Active ingredients, chemical salts, and concentrations.
    - "primary_uses": What medical conditions or symptoms it treats.
    - "manufacturer_provider": Typical manufacturer types or providers.
    - "side_effects_warnings": Potential adverse reactions, side effects, and allergy warnings.
    - "dosage_storage": Standard usage guidelines and storage instructions.
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

def analyze_prescription_multimodal(content_input, input_type: str, language: str) -> str:
    model = get_gemini_model()
    if not model:
        return "Gemini API Key missing. Please configure secrets."

    prompt = f"""
    You are an expert medical AI assistant. Analyze the provided prescription document or image.
    Extract all mentioned medicines, dosages, and instructions, and provide a detailed analysis in {language} covering:
    1. List of identified medications and compositions.
    2. Primary therapeutic purpose of each medication.
    3. Important safety warnings, possible side effects, or cross-interactions.
    4. General dosage compliance advice.
    """

    try:
        if input_type == "image":
            response = model.generate_content([content_input, prompt])
        else:
            full_prompt = f"{prompt}\n\nPrescription Content:\n{content_input}"
            response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Prescription Analysis Error: {e}"

def fetch_directory_results(state: str, location_query: str, category: str, subcategory: str, language: str) -> str:
    model = get_gemini_model()
    if not model:
        return "Gemini API Key missing. Please configure secrets."

    prompt = f"""
    Act as a verified medical infrastructure directory and health locator in India.
    Find and list authentic real-world or standard major healthcare facilities, hospitals, or centers for:
    - Specific Location (City / Taluka / Village): {location_query}, State/UT: {state}, India
    - Category: {category} -> {subcategory}
    
    Note: If '{location_query}' is a small town, taluka, or village, find the nearest specialized hospitals, civil/government health centers, or diagnostic hubs serving this region.
    
    Provide the output in Markdown format completely translated in the language '{language}', detailing:
    1. Names of prominent hospitals/centers/labs or nearest government health infrastructure matching this category.
    2. Typical addresses, contact helplines, and availability details.
    3. Government subsidy / insurance info (e.g. Ayushman Bharat / PMJAY eligibility if applicable).
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Directory Fetch Error: {e}"

def ai_symptom_triage(symptoms: str, language: str) -> str:
    model = get_gemini_model()
    if not model:
        return "API Key missing in secrets."

    prompt = f"""
    Analyze the patient's symptoms: "{symptoms}".
    Provide preliminary guidance in {language} on:
    1. Potential underlying issues or specialty department to consult.
    2. Whether this requires urgent/emergency hospital care or home care.
    3. Recommended initial questions to ask a doctor.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return str(e)

# ==========================================
# 3. NEXT-GEN ULTRA GLASSMORPHISM CSS STYLING
# ==========================================

def inject_glassmorphism_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background: radial-gradient(circle at 10% 20%, #030712 0%, #0b1329 50%, #020617 100%) !important;
        background-attachment: fixed !important;
        color: #f1f5f9 !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(3, 7, 18, 0.9) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(56, 189, 248, 0.12) !important;
    }

    div.glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 20px !important;
        padding: 28px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 16px 40px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    div.glass-card:hover {
        border-color: rgba(56, 189, 248, 0.35) !important;
        box-shadow: 0 20px 50px 0 rgba(14, 165, 233, 0.15), inset 0 1px 0 0 rgba(255, 255, 255, 0.2) !important;
    }

    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
    }

    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.25) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px 26px !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.4) !important;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%) !important;
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.6) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px !important;
        color: #94a3b8 !important;
        padding: 10px 18px !important;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%) !important;
        border: 1px solid #38bdf8 !important;
        color: #f8fafc !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. MAIN APPLICATION INTERFACE
# ==========================================

def main():
    st.set_page_config(page_title="NovaMed | Next-Gen Medical Suite", page_icon="🩺", layout="wide")
    inject_glassmorphism_css()

    with st.sidebar:
        st.markdown("### 🇮🇳 Multi-Language Engine")
        selected_lang_key = st.selectbox("Select Regional Language", list(LANGUAGES.keys()))
        chosen_language = LANGUAGES[selected_lang_key]
        
        st.markdown("<hr style='border-color: rgba(56, 189, 248, 0.15);'>", unsafe_allow_html=True)
        st.markdown("### ⚡ About NovaMed")
        st.markdown(
            "<p style='color: #94a3b8; font-size: 13px; line-height: 1.6;'>"
            "NovaMed is an enterprise-grade AI medical intelligence platform powered by <b>Google Gemini 3.8 Flash</b>, "
            "delivering universal drug analysis, pan-India geo-hospital directories, live maps, AI triage, and multimodal prescription scanning."
            "</p>", 
            unsafe_allow_html=True
        )

    st.markdown("""
        <div class="glass-card" style="border-left: 6px solid #38bdf8;">
            <h1 style="margin: 0; font-size: 34px; font-weight: 800; background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                NovaMed 🩺
            </h1>
            <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 16px; font-weight: 500;">
                Next-Gen AI Medical Intelligence & Pan-India Healthcare Infrastructure Directory (Gemini 3.8 Flash)
            </p>
        </div>
    """, unsafe_allow_html=True)

    tab_pharmacy, tab_directory, tab_triage, tab_scanner = st.tabs([
        "💊 Smart Pharmacy Inspector", 
        "🗺️ Geo-Medical Locator & Maps", 
        "🤖 AI Symptom Triage", 
        "📂 Multimodal Prescription Scanner"
    ])

    with tab_pharmacy:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💊 Universal Drug & Medical Item Inspector")
        st.write("Enter any medicine, tablet, syrup, cream, syringe, or medical supply name below:")
        
        med_input = st.text_input("Medicine / Item Name", placeholder="e.g. Paracetamol, Azithromycin syrup, Betadine cream, Insulin syringe...")
        
        if st.button("🔍 Analyze Medical Item"):
            if not med_input.strip():
                st.warning("Please enter a valid medical item name.")
            else:
                with st.spinner(f"Analyzing in {chosen_language}..."):
                    result = analyze_medicine(med_input, chosen_language)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success(f"Analysis Complete for: **{result.get('item_name', med_input)}**")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**🧪 Composition & Salts:**\n{result.get('composition', 'N/A')}")
                            st.markdown(f"**🎯 Primary Uses:**\n{result.get('primary_uses', 'N/A')}")
                            st.markdown(f"**🏭 Manufacturer / Provider:**\n{result.get('manufacturer_provider', 'N/A')}")
                        with col2:
                            st.markdown(f"**⚠️ Side Effects & Warnings:**\n{result.get('side_effects_warnings', 'N/A')}")
                            st.markdown(f"**📦 Dosage & Storage:**\n{result.get('dosage_storage', 'N/A')}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_directory:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🗺️ Pan-India Location-Aware Healthcare Directory & Google Maps")
        st.write("Select your State/UT, type your specific **City, Taluka, or Village**, and view the integrated Google Map alongside the healthcare directory.")

        c1, c2 = st.columns(2)
        with c1:
            selected_state = st.selectbox("Select State / UT", INDIA_STATES_UT)
        with c2:
            location_query = st.text_input("City / Taluka / Village Name", placeholder="e.g. Solapur, Akkalkot, Jowla, Pune...")

        c3, c4 = st.columns(2)
        with c3:
            selected_category = st.selectbox("Healthcare Category", list(HEALTHCARE_CATEGORIES.keys()))
        with c4:
            available_subcats = HEALTHCARE_CATEGORIES.get(selected_category, [])
            selected_subcategory = st.selectbox("Specific Requirement / Specialty", available_subcats)

        if st.button("🚀 Fetch Pan-India Directory & Load Map"):
            if not location_query.strip():
                st.warning("Please enter your City, Taluka, or Village name.")
            else:
                st.markdown(f"### 📍 Google Maps View: {location_query}, {selected_state}")
                map_query = f"{location_query}, {selected_state}, India".replace(" ", "+")
                map_embed_url = f"https://maps.google.com/maps?q={map_query}&output=embed"
                
                st.markdown(
                    f'<iframe src="{map_embed_url}" width="100%" height="400" style="border:0; border-radius:14px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);" allowfullscreen="" loading="lazy"></iframe>',
                    unsafe_allow_html=True
                )

                with st.spinner(f"Querying verified healthcare directory for {location_query}, {selected_state}..."):
                    directory_report = fetch_directory_results(selected_state, location_query, selected_category, selected_subcategory, chosen_language)
                    st.markdown(directory_report)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_triage:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🤖 AI Symptom Triage Assistant")
        st.write("Describe your symptoms to receive initial guidance on which medical specialist or department to consult.")
        
        symptoms_text = st.text_area("Describe Symptoms", placeholder="e.g., Persistent headache, mild fever, and joint fatigue for 3 days...")
        if st.button("💡 Run Symptom Triage"):
            if not symptoms_text.strip():
                st.warning("Please describe your symptoms.")
            else:
                with st.spinner("Evaluating clinical indicators..."):
                    triage_result = ai_symptom_triage(symptoms_text, chosen_language)
                    st.markdown(triage_result)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scanner:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📂 Multimodal Prescription Scanner & OCR")
        st.write("Upload a prescription document (**PDF, Word, PNG, JPG, or JPEG**) for instant AI analysis.")
        
        uploaded_file = st.file_uploader("Upload Prescription File or Image", type=["pdf", "docx", "png", "jpg", "jpeg"])
        
        if uploaded_file:
            file_bytes = uploaded_file.read()
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith((".png", ".jpg", ".jpeg")):
                image = Image.open(io.BytesIO(file_bytes))
                st.image(image, caption="Uploaded Prescription Image", use_column_width=True)
                
                if st.button("⚡ Analyze Prescription Image"):
                    with st.spinner("Processing image via Gemini Multimodal OCR..."):
                        analysis_report = analyze_prescription_multimodal(image, "image", chosen_language)
                        st.markdown(analysis_report)
            
            else:
                rx_text = ""
                try:
                    if file_name.endswith(".pdf"):
                        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                        for page in reader.pages:
                            rx_text += (page.extract_text() or "") + "\n"
                    elif file_name.endswith(".docx"):
                        doc = docx.Document(io.BytesIO(file_bytes))
                        rx_text = "\n".join([p.text for p in doc.paragraphs if p.text])
                    
                    st.text_area("Extracted Document Text", value=rx_text, height=140)
                    
                    if st.button("⚡ Analyze Document Text"):
                        if not rx_text.strip():
                            st.warning("No readable text found in the document.")
                        else:
                            with st.spinner("Analyzing document text..."):
                                analysis_report = analyze_prescription_multimodal(rx_text, "text", chosen_language)
                                st.markdown(analysis_report)
                except Exception as e:
                    st.error(f"Error parsing prescription file: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
