# 🚀 Setup Guide - Tofico Analyzer

## 📋 Prerequisites
- Python 3.8+
- MySQL Server
- ngrok account (free)

## 🔧 Backend Setup

### 1. Environment Configuration
\`\`\`bash
# Edit .env file
DB_HOST=localhost
DB_NAME=tofico_analyzer
DB_USER=root
DB_PASSWORD=your_mysql_password  # ⚠️ GANTI INI
DB_PORT=3306
PORT=8000
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements_normalized.txt
\`\`\`

### 3. Setup Database
\`\`\`bash
python setup_normalized_db.py
\`\`\`

### 4. Start Backend Server
\`\`\`bash
python main_normalized.py
\`\`\`
✅ Server akan berjalan di: `http://localhost:8000`

## 🌐 Ngrok Setup

### 1. Install ngrok
- Download dari: https://ngrok.com/download
- Extract dan add to PATH

### 2. Start ngrok tunnel
\`\`\`bash
ngrok http 8000
\`\`\`

### 3. Copy ngrok URL
\`\`\`
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
\`\`\`
📋 Copy URL: `https://abc123.ngrok-free.app`

## 🌍 Frontend Setup

### 1. Update API URL
Edit `script.js` line 3:
\`\`\`javascript
const API_BASE_URL = "https://abc123.ngrok-free.app"  // ⚠️ GANTI INI
\`\`\`

### 2. Upload to GitHub Pages
- Upload semua file frontend ke repository
- Enable GitHub Pages di settings

## ✅ Testing

### 1. Test Backend
\`\`\`bash
curl http://localhost:8000/health
curl http://localhost:8000/locations
\`\`\`

### 2. Test ngrok
\`\`\`bash
curl https://your-ngrok-url.ngrok-free.app/health
\`\`\`

### 3. Test Frontend
- Buka website di browser
- Check browser console untuk errors
- Test CRUD operations

## 🐛 Troubleshooting

### Error: "Unexpected token '<'"
❌ **Problem**: Frontend mendapat HTML instead of JSON
✅ **Solution**: 
1. Pastikan backend berjalan di port 8000
2. Pastikan ngrok forward ke port 8000
3. Update API_BASE_URL di script.js

### Error: "CORS policy"
❌ **Problem**: CORS blocked
✅ **Solution**: Backend sudah include CORS middleware

### Error: "Connection refused"
❌ **Problem**: Backend tidak berjalan
✅ **Solution**: 
1. Check MySQL server running
2. Check .env configuration
3. Run `python main_normalized.py`

### Error: "Database connection failed"
❌ **Problem**: MySQL connection issue
✅ **Solution**:
1. Check MySQL server status
2. Verify .env credentials
3. Create database manually if needed

## 📊 API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `GET /locations` - All locations
- `GET /criteria` - All criteria
- `GET /evaluations` - All evaluations
- `GET /docs` - Swagger UI

## 🎯 Success Checklist

- [ ] MySQL server running
- [ ] .env configured correctly
- [ ] Dependencies installed
- [ ] Database setup completed
- [ ] Backend running on port 8000
- [ ] ngrok tunnel active
- [ ] Frontend API_BASE_URL updated
- [ ] Frontend uploaded to GitHub Pages
- [ ] All CRUD operations working

🎉 **Ready to use!**
