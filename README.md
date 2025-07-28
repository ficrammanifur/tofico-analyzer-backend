<h1 align="center"># 🏢 Tofico Analyzer Backend</h1>
<p align="center"><em>FastAPI-based Decision Support System for Optimal Location Selection</em></p>

---

A robust backend API for the Tofico Analyzer Decision Support System that helps businesses determine the best locations for their operations using Multi-Criteria Decision Making (MCDM) algorithms.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📊 Database Schema](#-database-schema)
- [🌐 API Documentation](#-api-documentation)
- [🧮 Algorithms](#-algorithms)
- [🔧 Configuration](#-configuration)
- [📱 Frontend Integration](#-frontend-integration)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

The Tofico Analyzer Backend is a comprehensive API solution designed to support decision-making processes for location selection. It implements two powerful MCDM algorithms:

- **SAW (Simple Additive Weighting)** - Linear aggregation method
- **WP (Weighted Product)** - Multiplicative aggregation method

The system evaluates multiple locations against various criteria such as population density, accessibility, competition level, rental costs, and market potential to provide data-driven recommendations.

---

## ✨ Features

### 🏗️ **Core Functionality**
- ✅ **Multi-Criteria Decision Making** using SAW and WP algorithms
- ✅ **RESTful API** with comprehensive CRUD operations
- ✅ **Normalized Database Schema** for optimal performance
- ✅ **Real-time Calculations** with caching support
- ✅ **Data Validation** with Pydantic models

### 🔧 **Technical Features**
- ✅ **FastAPI Framework** with automatic OpenAPI documentation
- ✅ **MySQL Database** with foreign key constraints
- ✅ **Environment Configuration** with .env support
- ✅ **CORS Support** for cross-origin requests
- ✅ **Error Handling** with detailed HTTP responses
- ✅ **Database Migrations** with SQL scripts

### 📊 **Data Management**
- ✅ **Location Management** - Add, update, delete locations
- ✅ **Criteria Management** - Configure evaluation criteria
- ✅ **Evaluation System** - Score locations against criteria
- ✅ **Result Caching** - Store calculation results for performance

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Framework** | FastAPI | 0.104+ |
| **Language** | Python | 3.8+ |
| **Database** | MySQL | 8.0+ |
| **ORM** | Raw SQL | - |
| **Validation** | Pydantic | 2.5+ |
| **Server** | Uvicorn | 0.24+ |
| **Environment** | python-dotenv | 1.0+ |

---

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0+
- pip (Python package manager)

### 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tofico-analyzer-backend.git
   cd tofico-analyzer-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_normalized.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Setup database**
   ```bash
   python setup_normalized_db.py
   ```

6. **Run the server**
   ```bash
   python main_normalized.py
   ```

🎉 **Server will be running at:** `http://localhost:8000`

---

### 🔍 **Verify Installation**

```bash
# Test API health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

---

## 📊 Database Schema

### 🗄️ **Tables Overview**

```sql
-- Locations table
CREATE TABLE locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Criteria table
CREATE TABLE criteria (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    weight DECIMAL(5,3) NOT NULL CHECK (weight >= 0 AND weight <= 1),
    type ENUM('benefit', 'cost') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Evaluations table
CREATE TABLE evaluations (
    location_id INT,
    criteria_id VARCHAR(50),
    value INT NOT NULL CHECK (value >= 0 AND value <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
    FOREIGN KEY (criteria_id) REFERENCES criteria(id) ON DELETE CASCADE,
    PRIMARY KEY (location_id, criteria_id)
);

-- Calculation results cache (optional)
CREATE TABLE calculation_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    location_id INT,
    algorithm VARCHAR(10) NOT NULL,
    score DECIMAL(10,6) NOT NULL,
    rank_position INT NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE
);
```

### 🔗 **Relationships**

- `locations` ← **1:N** → `evaluations`
- `criteria` ← **1:N** → `evaluations`
- `locations` ← **1:N** → `calculation_results`

## 🌐 API Documentation

### 📍 **Base URL**
```
http://localhost:8000
```

### 🔑 **Authentication**
Currently, no authentication is required. All endpoints are publicly accessible.

### 📋 **Endpoints Overview**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Interactive API documentation |

#### 🏢 **Locations**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/locations` | Get all locations with evaluations |
| `GET` | `/locations/{id}` | Get specific location |
| `POST` | `/locations` | Create new location |
| `PUT` | `/locations/{id}` | Update location |
| `DELETE` | `/locations/{id}` | Delete location |

#### ⚙️ **Criteria**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/criteria` | Get all criteria |
| `POST` | `/criteria` | Create new criteria |
| `PUT` | `/criteria/{id}` | Update criteria |
| `DELETE` | `/criteria/{id}` | Delete criteria |

#### 📊 **Evaluations**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/evaluations` | Get all evaluations |
| `PUT` | `/evaluations` | Update evaluation value |
| `DELETE` | `/evaluations/{location_id}/{criteria_id}` | Delete evaluation |

### 📝 **Request/Response Examples**

#### **Create Location**
```bash
curl -X POST "http://localhost:8000/locations" \
-H "Content-Type: application/json" \
-d '{
  "name": "Jakarta Selatan",
  "address": "Jl. Sudirman No. 1, Jakarta Selatan",
  "latitude": -6.2297,
  "longitude": 106.8261
}'
```

#### **Create Criteria**
```bash
curl -X POST "http://localhost:8000/criteria" \
-H "Content-Type: application/json" \
-d '{
  "id": "transportation",
  "name": "Transportasi",
  "weight": 0.15,
  "type": "benefit"
}'
```

#### **Update Evaluation**
```bash
curl -X PUT "http://localhost:8000/evaluations" \
-H "Content-Type: application/json" \
-d '{
  "location_id": 1,
  "criteria_id": "transportation",
  "value": 85
}'
```

---

## 🧮 Algorithms

### 🏆 **SAW (Simple Additive Weighting)**

**Formula:** `Vi = Σ(wj × rij)`

**Steps:**
1. **Normalize** decision matrix
2. **Calculate** preference values
3. **Rank** alternatives

**Normalization:**
- **Benefit criteria:** `rij = Xij / max(Xij)`
- **Cost criteria:** `rij = min(Xij) / Xij`

### 🥈 **WP (Weighted Product)**

**Formula:** `Si = Π(Xij^wj)`, `Vi = Si / Σ(Si)`

**Steps:**
1. **Determine** relative weights
2. **Calculate** S values
3. **Calculate** preference values
4. **Rank** alternatives

**Weight adjustment:**
- **Benefit criteria:** `+wj`
- **Cost criteria:** `-wj`

### 📊 **Example Calculation**

Given data:
- Jakarta: [85, 90, 60, 40, 88]
- Bandung: [75, 80, 70, 70, 82]
- Surabaya: [80, 85, 65, 60, 85]

**SAW Results:**
1. Jakarta: 1.000
2. Surabaya: 0.888
3. Bandung: 0.828

**WP Results:**
1. Jakarta: 0.380
2. Surabaya: 0.335
3. Bandung: 0.285

---

## 🔧 Configuration

### 📄 **Environment Variables (.env)**

```env
# Database Configuration
DB_HOST=localhost
DB_NAME=tofico_analyzer
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_PORT=3306
```

### Server Configuration
PORT=8000
DEBUG=True

### Optional: External API Keys
MAPS_API_KEY=your_google_maps_key

### ⚙️ **Database Configuration**

Edit `db_config_normalized.py` for advanced database settings:

```python
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'tofico_analyzer'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'autocommit': True
}
```

---

## 📝 License
<p align="center">
  <a href="https://github.com/ficrammanifur/ficrammanifur/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT" />
  </a>
</p>

<p align="centre"><a href="#tofico-analyzer-backend">↑ RETURN</a></p>
