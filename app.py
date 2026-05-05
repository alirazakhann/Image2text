import streamlit as st
import base64
from PIL import Image, ImageEnhance, ImageFilter
import io
import requests
import json
from typing import Optional, Dict, Any
import os
from datetime import datetime
import time
from config import *

# Configure Streamlit page
st.set_page_config(
    page_title="Handwritten Notes Converter",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

class HandwritingConverter:
    """
    Advanced handwriting to text converter using vision-language models
    """
    
    def __init__(self):
        self.supported_formats = SUPPORTED_FORMATS
        
    def encode_image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
    
    def enhance_image(self, image: Image.Image, enhance_contrast: bool = True, 
                     enhance_sharpness: bool = True) -> Image.Image:
        """Enhance image quality for better recognition"""
        if enhance_contrast:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
        
        if enhance_sharpness:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
        return image
    
    def preprocess_image(self, image: Image.Image, enhance: bool = False) -> Image.Image:
        """Preprocess image for better recognition"""
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Enhance if requested
        if enhance:
            image = self.enhance_image(image)
        
        # Resize if too large
        if max(image.size) > MAX_IMAGE_SIZE:
            ratio = MAX_IMAGE_SIZE / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def convert_with_groq_vision(self, image: Image.Image, api_key: str, 
                               model_name: str, language_hint: str = "auto", 
                               enhance_image: bool = False) -> Dict[str, Any]:
        """
        Convert handwritten notes using Groq Vision models
        """
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image, enhance_image)
            base64_image = self.encode_image_to_base64(processed_image)
            
            # Prepare the prompt
            prompt = CONVERSION_PROMPT.format(language_hint=language_hint)
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": MODELS[list(MODELS.keys())[0]]["max_tokens"],
                "temperature": MODELS[list(MODELS.keys())[0]]["temperature"]
            }
            
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse JSON response
                try:
                    # Extract JSON from the response (in case there's extra text)
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = content[start_idx:end_idx]
                        parsed_result = json.loads(json_str)
                        return {
                            "success": True,
                            "result": parsed_result,
                            "raw_response": content
                        }
                    else:
                        raise json.JSONDecodeError("No JSON found", content, 0)
                except json.JSONDecodeError:
                    # Fallback: return raw content
                    return {
                        "success": True,
                        "result": {
                            "detected_language": "unknown",
                            "converted_text": content,
                            "has_tables": False,
                            "has_equations": False,
                            "has_figures": False,
                            "confidence": 0.8,
                            "notes": "Raw response (JSON parsing failed)"
                        },
                        "raw_response": content
                    }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Conversion error: {str(e)}"
            }

def main():
    st.title("📝 Handwritten Notes to Editable Text Converter")
    st.markdown("Convert handwritten notes to editable text using Groq's fast vision models")
    
    # Add deployment info
    if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
        st.success("🌐 Running on Streamlit Cloud with configured API key!")
    
    # Initialize converter
    converter = HandwritingConverter()
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Model selection
    model_options = [
        ("groq_llama_90b_vision", "Llama 3.2 90B Vision (Best Quality)"),
        ("groq_llama_vision", "Llama 3.2 11B Vision (Balanced)"),
        ("groq_llava", "LLaVA 1.5 7B (Fast)")
    ]
    
    # Model selection
    model_options = [
        ("llama_4_scout", "Llama 4 Scout (Balanced - Fast & Efficient)"),
        ("llama_4_maverick", "Llama 4 Maverick (Advanced - Multimodal & Multilingual)")
    ]
    
    model_choice = st.sidebar.selectbox(
        "Choose Groq Vision Model",
        options=[key for key, name in model_options],
        format_func=lambda x: dict(model_options)[x],
        help="Select the Groq vision model for conversion"
    )
    
    # API key input
    # Check if API key is in secrets (for Streamlit Cloud)
    default_api_key = ""
    if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
        default_api_key = st.secrets['GROQ_API_KEY']
    
    api_key = st.sidebar.text_input(
        "Groq API Key",
        value=default_api_key,
        type="password",
        help="Enter your Groq API key from https://console.groq.com/"
    )
    
    if not api_key and not default_api_key:
        st.sidebar.info("💡 Get your free Groq API key at https://console.groq.com/")
        st.sidebar.markdown("**For deployment:** Add your API key to Streamlit Cloud secrets as `GROQ_API_KEY`")
    
    # Language hint
    language_options = [(code, name) for code, name in LANGUAGES.items()]
    language_hint = st.sidebar.selectbox(
        "Language Hint",
        options=[code for code, name in language_options],
        format_func=lambda x: LANGUAGES[x],
        help="Hint for the expected language (auto-detect if 'auto')"
    )
    
    # Image enhancement options
    st.sidebar.subheader("🎨 Image Enhancement")
    enhance_image = st.sidebar.checkbox(
        "Enhance image quality",
        value=False,
        help="Apply contrast and sharpness enhancement"
    )
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=converter.supported_formats,
            help="Upload an image of handwritten notes"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Image info
            st.info(f"📊 Image: {image.size[0]}x{image.size[1]} pixels, Format: {image.format}")
    
    with col2:
        st.header("📝 Converted Text")
        
        if uploaded_file is not None and api_key:
            if st.button("🚀 Convert to Text", type="primary"):
                start_time = time.time()
                
                with st.spinner("Converting handwritten notes with Groq..."):
                    # Get model name from selection
                    model_name = MODELS[model_choice]["name"]
                    
                    # Perform conversion
                    result = converter.convert_with_groq_vision(
                        image, api_key, model_name, language_hint, enhance_image
                    )
                    
                    processing_time = time.time() - start_time
                    
                    if result["success"]:
                        data = result["result"]
                        
                        # Display results
                        st.success(f"✅ Conversion completed in {processing_time:.1f} seconds!")
                        
                        # Metadata
                        col_meta1, col_meta2, col_meta3, col_meta4 = st.columns(4)
                        with col_meta1:
                            lang_code = data.get("detected_language", "Unknown")
                            lang_name = LANGUAGES.get(lang_code, lang_code)
                            st.metric("Language", lang_name)
                        with col_meta2:
                            st.metric("Confidence", f"{data.get('confidence', 0):.1%}")
                        with col_meta3:
                            features = []
                            if data.get("has_tables"): features.append("Tables")
                            if data.get("has_equations"): features.append("Equations") 
                            if data.get("has_figures"): features.append("Figures")
                            st.metric("Features", ", ".join(features) if features else "Text only")
                        with col_meta4:
                            st.metric("Processing Time", f"{processing_time:.1f}s")
                        
                        # Converted text
                        st.subheader("Converted Text")
                        converted_text = data.get("converted_text", "")
                        st.text_area("", converted_text, height=300, key="converted_text")
                        
                        # Download options
                        col_dl1, col_dl2 = st.columns(2)
                        
                        with col_dl1:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"converted_notes_{timestamp}.txt"
                            st.download_button(
                                "💾 Download as Text File",
                                converted_text,
                                filename,
                                "text/plain"
                            )
                        
                        with col_dl2:
                            # Create markdown version with metadata
                            model_display_name = dict(model_options)[model_choice]
                            markdown_content = f"""# Converted Handwritten Notes

**Conversion Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Detected Language:** {lang_name}
**Confidence:** {data.get('confidence', 0):.1%}
**Processing Time:** {processing_time:.1f} seconds
**Model Used:** {model_display_name}

---

{converted_text}

---
*Converted using Handwritten Notes Converter with Groq*
"""
                            md_filename = f"converted_notes_{timestamp}.md"
                            st.download_button(
                                "📄 Download as Markdown",
                                markdown_content,
                                md_filename,
                                "text/markdown"
                            )
                        
                        # Additional notes
                        if data.get("notes"):
                            st.info(f"ℹ️ Notes: {data['notes']}")
                        
                        # Show raw response in expander for debugging
                        if "raw_response" in result:
                            with st.expander("🔍 View Raw AI Response"):
                                st.text(result["raw_response"])
                            
                    else:
                        st.error(f"❌ Conversion failed: {result['error']}")
                        
                        # Show troubleshooting tips
                        st.markdown("""
                        **Troubleshooting Tips:**
                        - Verify your Groq API key is correct and has sufficient credits
                        - Ensure the image is clear and well-lit
                        - Try enhancing the image quality option
                        - Check your internet connection
                        - Try Llama 4 Maverick for complex documents with multiple languages
                        - Try Llama 4 Scout for faster processing of simpler documents
                        """)
        
        elif uploaded_file is not None and not api_key:
            st.warning("⚠️ Please enter your Groq API key in the sidebar to proceed")
        elif not uploaded_file:
            st.info("👆 Upload an image to get started")
    
    # Instructions
    st.markdown("---")
    st.header("📋 How to Use")
    
    col_inst1, col_inst2, col_inst3 = st.columns(3)
    
    with col_inst1:
        st.markdown("""
        **1. Setup**
        - Choose your preferred Groq vision model
        - Enter your Groq API key
        - Select language hint (optional)
        """)
    
    with col_inst2:
        st.markdown("""
        **2. Upload**
        - Upload clear image of handwritten notes
        - Supported: PNG, JPG, JPEG, WebP, BMP
        - Max recommended: 2048px
        """)
    
    with col_inst3:
        st.markdown("""
        **3. Convert**
        - Click "Convert to Text"
        - Review the results
        - Download as text or markdown file
        """)
    
    # Features
    st.header("✨ Features")
    
    feature_cols = st.columns(4)
    
    with feature_cols[0]:
        st.markdown("""
        **🌍 Multi-language**
        - Auto-detect language
        - Preserve original text
        - Support for 13+ languages
        """)
    
    with feature_cols[1]:
        st.markdown("""
        **📊 Tables & Structure**
        - Convert to Markdown tables
        - Preserve formatting
        - Maintain hierarchy
        """)
    
    with feature_cols[2]:
        st.markdown("""
        **🧮 Math Equations**
        - LaTeX notation
        - Inline and display math
        - Complex formulas
        """)
    
    with feature_cols[3]:
        st.markdown("""
        **⚡ Llama 4 Power**
        - Latest Groq models
        - Enhanced vision capabilities
        - Multimodal understanding
        """)
    
    # Model details
    st.header("🔍 Model Details")
    
    col_model1, col_model2 = st.columns(2)
    
    with col_model1:
        st.subheader("🚀 Llama 4 Scout")
        st.markdown("""
        - **Speed**: 460+ tokens/second
        - **Best for**: General purpose, fast processing
        - **Strengths**: Summarization, reasoning, code
        - **Use case**: Quick note conversion
        """)
    
    with col_model2:
        st.subheader("🎯 Llama 4 Maverick")
        st.markdown("""
        - **Capability**: Advanced multimodal
        - **Best for**: Complex documents
        - **Strengths**: Multilingual, detailed analysis
        - **Use case**: Complex handwritten notes
        """)
    
    # Model comparison
    st.header("🤖 Model Comparison")
    
    model_comparison = {
        "Model": ["Llama 4 Scout", "Llama 4 Maverick"],
        "Speed": ["🌟🌟🌟🌟🌟", "🌟🌟🌟🌟"],
        "Quality": ["🌟🌟🌟🌟", "🌟🌟🌟🌟🌟"],
        "Specialization": ["General purpose", "Multimodal & Multilingual"],
        "Best For": ["Fast processing", "Complex documents"]
    }
    
    st.table(model_comparison)

if __name__ == "__main__":
    main()