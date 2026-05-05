#!/usr/bin/env python3
"""
Setup script for the Handwritten Notes Converter
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_sample_image():
    """Create a sample image for testing"""
    try:
        from demo import save_sample_image
        save_sample_image()
        print("✅ Sample image created!")
    except Exception as e:
        print(f"⚠️  Could not create sample image: {e}")

def main():
    """Main setup function"""
    print("🔧 Setting up Handwritten Notes Converter...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create sample image
    create_sample_image()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Get a Groq API key from https://console.groq.com/")
    print("   - Sign up for free tier or choose a paid plan")
    print("   - Create an API key in your dashboard")
    print("2. Run the application: python run.py")
    print("3. Choose your preferred Groq vision model:")
    print("   - Llama 3.2 90B Vision: Best quality for complex documents")
    print("   - Llama 3.2 11B Vision: Balanced performance for general use")
    print("   - LLaVA 1.5 7B: Fastest processing for simple documents")
    print("4. Upload an image and start converting!")
    print("\n💡 Tip: Use 'sample_handwritten_notes.png' to test the converter")
    print("⚡ Advantage: Groq's LPU technology provides ultra-fast processing!")

if __name__ == "__main__":
    main()