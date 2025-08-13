#!/usr/bin/env python3
"""
Universal Glaucoma Detection System Startup Script
This script works on ANY PC after cloning from GitHub.
It automatically handles all dependencies and setup.
"""

import subprocess
import sys
import time
import os
import platform
from pathlib import Path

def print_banner():
    """Print the system banner."""
    print("=" * 70)
    print("🏥 Glaucoma Detection AI - Universal Startup System")
    print("=" * 70)
    print(f"🖥️  Operating System: {platform.system()} {platform.release()}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_node_js():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js version: {version}")
            return True
        else:
            print("❌ Node.js not found!")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found!")
        print("   Please install Node.js from: https://nodejs.org/")
        return False

def check_npm():
    """Check if npm is installed."""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ npm version: {version}")
            return True
        else:
            print("❌ npm not found!")
            return False
    except FileNotFoundError:
        print("❌ npm not found!")
        return False

def install_python_dependencies():
    """Install Python dependencies."""
    print("\n🐍 Installing Python dependencies...")
    
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Python dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install Python dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing Python dependencies: {e}")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies."""
    print("\n🎨 Installing frontend dependencies...")
    
    frontend_dir = Path("glaucoma_detection")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Install dependencies
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Frontend dependencies installed successfully!")
            os.chdir("..")  # Go back to root
            return True
        else:
            print(f"❌ Failed to install frontend dependencies: {result.stderr}")
            os.chdir("..")  # Go back to root
            return False
    except Exception as e:
        print(f"❌ Error installing frontend dependencies: {e}")
        os.chdir("..")  # Go back to root
        return False

def check_model_files():
    """Check if AI model files exist."""
    print("\n🤖 Checking AI model files...")
    
    models_dir = Path("models")
    if not models_dir.exists():
        print("❌ Models directory not found!")
        return False
    
    required_models = ["densenet121.pth", "late_fusion_model.pkl"]
    missing_models = []
    
    for model in required_models:
        model_path = models_dir / model
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"✅ {model} ({size_mb:.1f} MB)")
        else:
            print(f"❌ {model} - MISSING!")
            missing_models.append(model)
    
    if missing_models:
        print(f"\n⚠️  Missing models: {', '.join(missing_models)}")
        print("   Please ensure all model files are present in the models/ directory")
        return False
    
    return True

def start_api_server():
    """Start the Flask API server."""
    print("\n🚀 Starting Glaucoma Detection API Server...")
    
    try:
        # Start the Flask server
        process = subprocess.Popen([
            sys.executable, 'api_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the server is running
        if process.poll() is None:
            print("✅ API Server started successfully!")
            print("🌐 API available at: http://localhost:5000")
            print("🔍 Health check: http://localhost:5000/api/health")
            return process
        else:
            stdout, stderr = process.communicate()
            print("❌ Failed to start API server:")
            print(stderr.decode())
            return None
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def print_frontend_instructions():
    """Print instructions for starting the frontend."""
    print("\n" + "=" * 70)
    print("🎨 FRONTEND SETUP INSTRUCTIONS")
    print("=" * 70)
    print("1. Open a NEW terminal/command prompt")
    print("2. Navigate to the frontend directory:")
    print("   cd glaucoma_detection")
    print("3. Start the development server:")
    print("   npm run dev")
    print("4. Open your browser and go to: http://localhost:3000")
    print("=" * 70)

def print_success_message():
    """Print success message."""
    print("\n" + "=" * 70)
    print("🎉 SYSTEM READY! 🎉")
    print("=" * 70)
    print("✅ Python dependencies: Installed")
    print("✅ Frontend dependencies: Installed")
    print("✅ AI models: Verified")
    print("✅ API server: Running on port 5000")
    print("\n🚀 Next step: Start the frontend in a new terminal!")
    print("=" * 70)

def main():
    """Main function to start the system."""
    print_banner()
    
    # Check system requirements
    print("\n🔍 Checking system requirements...")
    
    if not check_python_version():
        sys.exit(1)
    
    if not check_node_js():
        sys.exit(1)
    
    if not check_npm():
        sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies!")
        sys.exit(1)
    
    if not install_frontend_dependencies():
        print("❌ Failed to install frontend dependencies!")
        sys.exit(1)
    
    # Check model files
    if not check_model_files():
        print("❌ AI model files are missing!")
        sys.exit(1)
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        print("❌ Failed to start API server!")
        sys.exit(1)
    
    # Print instructions
    print_frontend_instructions()
    print_success_message()
    
    try:
        print("\n🔄 API Server is running. Press Ctrl+C to stop...")
        
        # Keep the server running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down API server...")
        api_process.terminate()
        api_process.wait()
        print("✅ API Server stopped.")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
