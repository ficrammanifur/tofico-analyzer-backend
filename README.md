# Tofico Analyzer Backend - Simple Version

Backend FastAPI sederhana untuk Sistem Pendukung Keputusan Tofico Analyzer.

## 🚀 Quick Start

### 1. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Setup Database
\`\`\`bash
# Pastikan MySQL sudah running
# Ganti password di db_config.py sesuai MySQL Anda

python setup_db.py
\`\`\`

### 3. Run Server
\`\`\`bash
python main.py
\`\`\`

Server berjalan di: \`http://localhost:8000\`

## 📝 Configuration

Edit \`db_config.py\`:
\`\`\`python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'tofico_dss',
    'user': 'root',
    'password': 'your_mysql_password',  # Ganti ini
    'charset': 'utf8mb4'
}
\`\`\`

## 🌐 API Endpoints

### Locations
- \`GET /locations\` - Ambil semua lokasi
- \`GET /locations/{id}\` - Ambil lokasi by ID
- \`POST /locations\` - Tambah lokasi baru
- \`PUT /locations/{id}\` - Update lokasi
- \`DELETE /locations/{id}\` - Hapus lokasi

### Criteria
- \`GET /criteria\` - Ambil semua kriteria
- \`POST /criteria\` - Tambah kriteria baru
- \`DELETE /criteria/{id}\` - Hapus kriteria

### Utility
- \`GET /\` - Info API
- \`GET /health\` - Health check
- \`GET /docs\` - Swagger UI

## 🔧 Ngrok Setup

\`\`\`bash
# Install ngrok dari https://ngrok.com
ngrok http 8000
\`\`\`

Copy URL ngrok dan gunakan di frontend:
\`\`\`javascript
const API_URL = "https://abc123.ngrok-free.app";
\`\`\`

## 📊 Sample Data

Database otomatis terisi dengan:
- 3 lokasi sample (Jakarta, Bandung, Surabaya)
- 5 kriteria default (populationDensity, accessibility, dll)

## 🛠️ Testing

\`\`\`bash
# Test API
curl http://localhost:8000/locations

# Atau buka Swagger UI
# http://localhost:8000/docs
\`\`\`

## 📁 File Structure

\`\`\`
├── main.py          # FastAPI app dengan semua endpoints
├── db_config.py     # Konfigurasi database MySQL
├── setup_db.py     # Script setup database
├── requirements.txt # Dependencies
└── README.md       # Dokumentasi
\`\`\`

Versi simple ini menggabungkan semua fungsi dalam 3 file utama untuk kemudahan penggunaan!
\`\`\`
