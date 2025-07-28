-- Membuat database
CREATE DATABASE IF NOT EXISTS tofico_analyzer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tofico_analyzer;

-- Tabel Lokasi
CREATE TABLE IF NOT EXISTS locations (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  address TEXT,
  latitude DECIMAL(10,8),
  longitude DECIMAL(11,8),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_coordinates (latitude, longitude)
);

-- Tabel Kriteria
CREATE TABLE IF NOT EXISTS criteria (
  id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  weight DECIMAL(5,3) NOT NULL CHECK (weight >= 0 AND weight <= 1),
  type ENUM('benefit', 'cost') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name)
);

-- Tabel Penilaian
CREATE TABLE IF NOT EXISTS evaluations (
  location_id INT,
  criteria_id VARCHAR(50),
  value INT NOT NULL CHECK (value >= 0 AND value <= 100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
  FOREIGN KEY (criteria_id) REFERENCES criteria(id) ON DELETE CASCADE,
  PRIMARY KEY (location_id, criteria_id)
);

-- Tabel untuk menyimpan hasil perhitungan (opsional, untuk caching)
CREATE TABLE IF NOT EXISTS calculation_results (
  id INT PRIMARY KEY AUTO_INCREMENT,
  location_id INT,
  algorithm VARCHAR(10) NOT NULL,
  score DECIMAL(10,6) NOT NULL,
  rank_position INT NOT NULL,
  calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
  INDEX idx_algorithm (algorithm),
  INDEX idx_calculated_at (calculated_at)
);
