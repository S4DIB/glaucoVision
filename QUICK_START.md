# 🚀 Quick Start Guide - Glaucoma Detection AI

## ⚡ Get Running in 5 Minutes

### **Option 1: One-Click Start (Windows)**
1. **Double-click** `start_system.bat`
2. **Wait** for the API server to start
3. **Open a new terminal** and run:
   ```bash
   cd glaucoma_detection
   npm install
   npm run dev
   ```
4. **Open your browser** to `http://localhost:3000`

### **Option 2: Manual Start**
1. **Start the API server**:
   ```bash
   python api_server.py
   ```
2. **In a new terminal, start the frontend**:
   ```bash
   cd glaucoma_detection
   npm install
   npm run dev
   ```
3. **Open your browser** to `http://localhost:3000`

## 🎯 What You'll See

- **Professional Medical Interface**: Clean, modern design that looks like expensive commercial software
- **Image Upload**: Drag-and-drop retinal fundus images
- **Clinical Data Forms**: Organized input fields for all medical parameters
- **AI Analysis**: Real-time glaucoma detection with confidence scores
- **Professional Results**: Beautiful presentation of diagnosis and recommendations

## 🔧 System Requirements

- **Python 3.8+** with required packages (see requirements.txt)
- **Node.js 18+** for the frontend
- **Your existing AI models** (densenet121.pth, late_fusion_model.pkl)

## 🌟 Key Features

✅ **Professional UI/UX** - Looks like $10K+ commercial software  
✅ **Responsive Design** - Works on all devices  
✅ **Real-time AI Analysis** - Instant glaucoma detection  
✅ **Clinical Data Integration** - Combines imaging + clinical parameters  
✅ **Beautiful Animations** - Smooth, professional interactions  
✅ **Error Handling** - User-friendly error messages  
✅ **Modern Architecture** - Scalable and maintainable  

## 🚨 Troubleshooting

### **API Server Won't Start**
- Check if port 5000 is available
- Ensure all Python packages are installed: `pip install -r requirements.txt`
- Verify your model files exist in the `models/` folder

### **Frontend Won't Start**
- Ensure Node.js 18+ is installed
- Run `npm install` in the `glaucoma_detection` folder
- Check if port 3000 is available

### **Connection Errors**
- Ensure both API server (port 5000) and frontend (port 3000) are running
- Check browser console for CORS errors
- Verify the API server is accessible at `http://localhost:5000`

## 📱 Using the System

1. **Upload Image**: Drag a retinal fundus image or click to browse
2. **Enter Clinical Data**: Fill in the medical parameters
3. **Analyze**: Click "Analyze Retinal Image"
4. **View Results**: Get professional diagnosis with confidence scores
5. **Follow Recommendations**: Review AI-generated medical guidance

## 🎉 You're Ready!

Your glaucoma detection system now has a **professional, enterprise-grade frontend** that rivals commercial medical software. The system maintains all your existing AI functionality while providing a beautiful, responsive, and professional user interface.

---

**Need Help?** Check `PROJECT_OVERVIEW.md` for detailed documentation or run `python test_system.py` to verify everything is working correctly.
