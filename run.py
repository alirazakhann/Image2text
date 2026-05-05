#!/usr/bin/env python3
"""
Launcher script for the Handwritten Notes Converter
API_KEY=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
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        ('streamlit', 'streamlit'),
        ('Pillow', 'PIL'),
        ('requests', 'requests')
    ]
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 Starting Handwritten Notes Converter...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found in current directory")
        sys.exit(1)
    
    print("✅ All dependencies found")
    print("🌐 Starting Streamlit server...")
    print("📝 Open your browser to http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        # Run streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()