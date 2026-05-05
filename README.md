# Handwritten Notes to Editable Text Converter

A modern Streamlit application that converts handwritten notes into editable text format while preserving tables, figures, and mathematical equations. This solution uses Groq's ultra-fast vision models for superior speed and accuracy compared to traditional OCR.

## 🌟 Features

- **Ultra-Fast Processing**: Powered by Groq's LPU (Language Processing Unit) technology
- **Multiple Vision Models**: Choose from Llama 3.2 90B, 11B, or LLaVA 7B models
- **Multi-language Support**: Auto-detects and preserves original language (13+ languages supported)
- **Structure Preservation**: Maintains formatting, bullet points, numbering, and indentation
- **Table Conversion**: Converts handwritten tables to Markdown format
- **Mathematical Equations**: Converts math to LaTeX notation ($ for inline, $$ for display)
- **Figure Description**: Describes diagrams and figures in structured format
- **Cost-Effective**: Groq's competitive pricing for high-quality results
- **User-friendly Interface**: Clean, intuitive Streamlit interface

## 🌐 Live Demo

**🚀 Try it now:** [Deploy your own version to Streamlit Cloud](DEPLOYMENT_GUIDE.md)

## 🚀 Quick Start

### Local Development

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser to `http://localhost:8501`

### Cloud Deployment

Deploy to Streamlit Cloud in minutes:

1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Add your Groq API key to secrets
5. Deploy!

See the complete [Deployment Guide](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📖 Usage

1. **Setup**: 
   - Choose your preferred Groq vision model:
     - **Llama 3.2 90B Vision**: Best quality for complex documents
     - **Llama 3.2 11B Vision**: Balanced performance and speed
     - **LLaVA 1.5 7B**: Fastest processing for simple documents
   - Enter your Groq API key in the sidebar
   - Optionally select a language hint

2. **Upload Image**:
   - Upload a clear image of handwritten notes
   - Supported formats: PNG, JPG, JPEG, WebP, BMP
   - Recommended max size: 2048px on longest side

3. **Convert**:
   - Click "Convert to Text" button
   - Wait for processing (usually 5-15 seconds with Groq's speed)
   - Review and download the converted text

## 🔧 Configuration

### Groq API Key

**Getting Started:**
- Sign up at [Groq Console](https://console.groq.com/)
- Create an API key in your dashboard
- Groq offers competitive pricing and fast inference speeds
- Free tier available for testing

### Model Selection Guide

| Model | Best For | Speed | Quality | Cost |
|-------|----------|-------|---------|------|
| Llama 3.2 90B Vision | Complex documents, detailed analysis | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Higher |
| Llama 3.2 11B Vision | General use, balanced performance | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Medium |
| LLaVA 1.5 7B | Quick processing, simple documents | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Lower |

### Language Support

The application supports auto-detection and conversion for:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)

## 📝 Output Format

The converter provides structured output including:

- **Detected Language**: Automatically identified language code
- **Converted Text**: Clean, editable text with preserved formatting
- **Feature Detection**: Identifies presence of tables, equations, figures
- **Confidence Score**: AI model's confidence in the conversion
- **Additional Notes**: Any relevant conversion notes

### Special Formatting

- **Tables**: Converted to Markdown table format
- **Math Equations**: LaTeX notation (`$inline$` or `$$display$$`)
- **Figures**: Described as `[FIGURE: description]`
- **Unclear Text**: Marked as `[UNCLEAR: best_guess]`

## 🎯 Best Practices

### Image Quality
- Use good lighting and avoid shadows
- Ensure text is clearly visible and not blurred
- Avoid extreme angles or distortion
- Higher resolution images generally work better

### Handwriting Tips
- Clear, legible handwriting works best
- Avoid overlapping text or drawings
- Ensure adequate spacing between lines
- Dark ink on light background is optimal

## 🔒 Privacy & Security

- Images are processed via API calls to OpenAI or Anthropic
- No images are stored locally by this application
- Review the privacy policies of your chosen AI provider
- Consider data sensitivity when using cloud-based AI services

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Image Processing**: PIL (Python Imaging Library)
- **AI Models**: OpenAI GPT-4 Vision or Anthropic Claude Vision
- **Output**: Structured JSON with converted text

### Dependencies
- `streamlit`: Web application framework
- `Pillow`: Image processing library
- `requests`: HTTP client for API calls

## 📊 Comparison with OCR

| Feature | Traditional OCR | This Solution (Groq) |
|---------|----------------|----------------------|
| Language Detection | Limited | Excellent |
| Handwriting Recognition | Poor | Excellent |
| Structure Preservation | Basic | Advanced |
| Math Equations | Not supported | LaTeX format |
| Table Recognition | Limited | Markdown format |
| Context Understanding | None | High |
| Processing Speed | Slow | Ultra-fast (Groq LPU) |
| Cost | Variable | Competitive |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is open source. Please ensure you comply with Groq's terms of service.

## ⚠️ Limitations

- Requires internet connection for Groq API calls
- Processing time: 5-30 seconds depending on model and image complexity
- API usage costs apply (Groq offers competitive pricing)
- Very poor handwriting may still be challenging to convert
- Extremely complex diagrams may not be fully captured

## 🆘 Troubleshooting

**Common Issues:**

1. **API Key Error**: Ensure your Groq API key is valid and has sufficient credits
2. **Image Too Large**: Resize images to under 2048px on the longest side
3. **Slow Processing**: Try the LLaVA 7B model for faster results
4. **Poor Results**: Try the Llama 90B model for better quality or enhance image quality

**Getting Help:**
- Check the error messages in the application
- Verify your Groq API key and credits at [Groq Console](https://console.groq.com/)
- Ensure image quality meets recommendations
- Try different models for comparison