# Tofico Analyzer Backend - Normalized Database Version

Backend FastAPI dengan struktur database normalized untuk Sistem Pendukung Keputusan Tofico Analyzer.

## 🗄️ Database Structure

### Tabel Utama:
- **`locations`** - Data lokasi (id, name, address, coordinates)
- **`criteria`** - Kriteria penilaian (id, name, weight, type)  
- **`evaluations`** - Nilai penilaian (location_id, criteria_id, value)
- **`calculation_results`** - Cache hasil perhitungan (opsional)

## 🚀 Quick Start

### 1. Environment Setup
\`\`\`bash
# Copy dan edit file .env
cp .env.example .env

# Edit .env sesuai konfigurasi MySQL Anda:
DB_HOST=localhost
DB_NAME=tofico_analyzer
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_PORT=3306
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements_normalized.txt
\`\`\`

### 3. Setup Database
\`\`\`bash
python setup_normalized_db.py
\`\`\`

### 4. Run Server
\`\`\`bash
python main_normalized.py
\`\`\`

Server berjalan di: \`http://localhost:8000\`

## 🌐 API Endpoints

### Locations
- \`GET /locations\` - Ambil semua lokasi dengan evaluasi
- \`GET /locations/{id}\` - Ambil lokasi by ID dengan evaluasi
- \`POST /locations\` - Tambah lokasi baru
- \`PUT /locations/{id}\` - Update lokasi
- \`DELETE /locations/{id}\` - Hapus lokasi

### Criteria
- \`GET /criteria\` - Ambil semua kriteria
- \`POST /criteria\` - Tambah kriteria baru
- \`PUT /criteria/{id}\` - Update kriteria
- \`DELETE /criteria/{id}\` - Hapus kriteria

### Evaluations (NEW!)
- \`GET /evaluations\` - Ambil semua evaluasi dengan detail
- \`PUT /evaluations\` - Update nilai evaluasi spesifik
- \`DELETE /evaluations/{location_id}/{criteria_id}\` - Hapus evaluasi

### Utility
- \`GET /\` - Info API
- \`GET /health\` - Health check
- \`GET /docs\` - Swagger UI

## 📊 Sample API Usage

### Menambah Lokasi Baru
\`\`\`bash
curl -X POST "http://localhost:8000/locations" \\
-H "Content-Type: application/json" \\
-d '{
  "name": "Yogyakarta",
  "address": "Jl. Malioboro No. 1, Yogyakarta",
  "latitude": -7.7956,
  "longitude": 110.3695
}'
\`\`\`

### Update Evaluasi
\`\`\`bash
curl -X PUT "http://localhost:8000/evaluations" \\
-H "Content-Type: application/json" \\
-d '{
  "location_id": 1,
  "criteria_id": "populationDensity",
  "value": 90
}'
\`\`\`

### Menambah Kriteria Baru
\`\`\`bash
curl -X POST "http://localhost:8000/criteria" \\
-H "Content-Type: application/json" \\
-d '{
  "id": "transportation",
  "name": "Transportasi",
  "weight": 0.15,
  "type": "benefit"
}'
\`\`\`

## 🔧 Ngrok Setup

\`\`\`bash
# Install ngrok dari https://ngrok.com
ngrok http 8000
\`\`\`

Copy URL ngrok dan gunakan di frontend:
\`\`\`javascript
const API_URL = "https://abc123.ngrok-free.app";
\`\`\`

## ✅ Keuntungan Normalized Schema

### 1. **Data Integrity**
- Foreign key constraints
- Cascade delete otomatis
- Data validation di database level

### 2. **Flexibility & Scalability**
- Mudah menambah/hapus kriteria
- Struktur yang dapat berkembang
- Performance optimal dengan indexing

### 3. **Better Maintenance**
- Query yang lebih efisien
- Backup/restore yang lebih baik
- Mudah dikelola dan diupdate

## 🛠️ Testing

\`\`\`bash
# Test API
curl http://localhost:8000/locations
curl http://localhost:8000/criteria
curl http://localhost:8000/evaluations

# Atau buka Swagger UI
# http://localhost:8000/docs
\`\`\`

## 📁 File Structure

\`\`\`
├── main_normalized.py              # FastAPI app dengan normalized schema
├── db_config_normalized.py         # Konfigurasi database dengan .env
├── setup_normalized_db.py          # Script setup database
├── .env                           # Environment variables
├── requirements_normalized.txt     # Dependencies
├── scripts/
│   ├── create_database_normalized.sql
│   └── seed_data_normalized.sql
└── README_normalized.md           # Dokumentasi
\`\`\`

## 🔄 Migration dari Versi Lama

Jika Anda menggunakan versi JSON sebelumnya, data dapat dimigrasikan dengan script khusus.

Versi normalized ini memberikan struktur yang lebih **professional**, **scalable**, dan **maintainable**! 🎉
\`\`\`
