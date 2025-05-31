#!/usr/bin/env python3

import os
import subprocess
import sys


def install_tesseract():
    """Install Tesseract OCR if not already installed."""
    try:
        import pytesseract

        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR is already installed")
        return True
    except Exception:
        print("❌ Tesseract OCR not found")

        system = sys.platform
        if system == "darwin":  # macOS
            print("📦 Installing Tesseract via Homebrew...")
            try:
                subprocess.run(["brew", "install", "tesseract"], check=True)
                print("✅ Tesseract installed successfully")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install Tesseract. Please install Homebrew first.")
                print("   Visit: https://brew.sh/")
                return False
        elif system.startswith("linux"):
            print("📦 Please install Tesseract manually:")
            print("   Ubuntu/Debian: sudo apt-get install tesseract-ocr")
            print("   CentOS/RHEL: sudo yum install tesseract")
            return False
        elif system == "win32":
            print("📦 Please install Tesseract manually:")
            print("   Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            return False
        else:
            print(f"❌ Unsupported system: {system}")
            return False


def install_requirements():
    """Install Python requirements."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False


def create_directories():
    """Create necessary directories."""
    directories = ["data", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")


def main():
    print("🎬 Setting up Glimpsify...")
    print("=" * 50)

    # Install Tesseract
    if not install_tesseract():
        print(
            "\n❌ Setup failed. Please install Tesseract manually and run setup again."
        )
        return 1

    # Install Python requirements
    if not install_requirements():
        print("\n❌ Setup failed. Please check your internet connection and try again.")
        return 1

    # Create directories
    create_directories()

    print("\n" + "=" * 50)
    print("🎉 Setup complete! You can now use Glimpsify:")
    print("\n📋 Quick start:")
    print("   python main.py --input youtube --url 'YOUR_YOUTUBE_URL'")
    print("\n📚 For more options:")
    print("   python main.py --help")

    return 0


if __name__ == "__main__":
    sys.exit(main())
