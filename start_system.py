#!/usr/bin/env python3
"""
Glaucoma Detection System Startup Script
This script starts the Flask API server for the glaucoma detection system.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required Python packages are installed."""
    package_checks = [
        ('flask', 'flask'),
        ('flask_cors', 'flask_cors'),
        ('torch', 'torch'),
        ('torchvision', 'torchvision'),
        ('PIL', 'pillow'),  # PIL is the import name, pillow is the package name
        ('numpy', 'numpy')
    ]
    missing_packages = []
    
    for import_name, package_name in package_checks:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def start_api_server():
    """Start the Flask API server."""
    print("🚀 Starting Glaucoma Detection API Server...")
    
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
    print("\n" + "="*60)
    print("🎨 FRONTEND SETUP INSTRUCTIONS")
    print("="*60)
    print("1. Open a new terminal/command prompt")
    print("2. Navigate to the frontend directory:")
    print("   cd glaucoma_detection")
    print("3. Install dependencies (if not already done):")
    print("   npm install")
    print("4. Start the development server:")
    print("   npm run dev")
    print("5. Open your browser and go to: http://localhost:3000")
    print("="*60)

def main():
    """Main function to start the system."""
    print("🏥 Glaucoma Detection AI System")
    print("="*40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start API server
    api_process = start_api_server()
    if not api_process:
        sys.exit(1)
    
    # Print frontend instructions
    print_frontend_instructions()
    
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
