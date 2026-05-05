"""
Configuration settings for the Handwritten Notes Converter
"""

# Supported image formats
SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'webp', 'bmp']

# Maximum image size (pixels on longest side)
MAX_IMAGE_SIZE = 2048

# API endpoints
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Model configurations
MODELS = {
    "llama_4_scout": {
        "name": "meta-llama/llama-4-scout-17b-16e-instruct",
        "max_tokens": 4000,
        "temperature": 0.1
    },
    "llama_4_maverick": {
        "name": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "max_tokens": 4000,
        "temperature": 0.1
    }
}

# Language codes and names
LANGUAGES = {
    "auto": "Auto-detect",
    "en": "English",
    "es": "Spanish", 
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi"
}

# Conversion prompt template
CONVERSION_PROMPT = """
Please analyze this handwritten note image and convert it to editable text. Follow these requirements:

1. Preserve the original language of the text (detect automatically if language hint is 'auto', otherwise prioritize {language_hint})
2. Maintain the structure and formatting as much as possible
3. For tables: Convert to markdown table format
4. For mathematical equations: Use LaTeX notation wrapped in $ for inline math and $$ for display math
5. For diagrams/figures: Describe them in [FIGURE: description] format
6. Preserve bullet points, numbering, and indentation
7. If text is in multiple languages, preserve each language as written
8. For unclear text, use [UNCLEAR: best_guess] format

Please provide the output in the following JSON format:
{{
    "detected_language": "language_code",
    "converted_text": "the_converted_text_here",
    "has_tables": true/false,
    "has_equations": true/false,
    "has_figures": true/false,
    "confidence": 0.0-1.0,
    "notes": "any additional notes about the conversion"
}}
"""