-- Insert sample criteria
INSERT INTO criteria (id, name, weight, type) VALUES
('populationDensity', 'Kepadatan Penduduk', 0.25, 'benefit'),
('accessibility', 'Aksesibilitas', 0.20, 'benefit'),
('competition', 'Tingkat Persaingan', 0.15, 'cost'),
('rentCost', 'Biaya Sewa', 0.20, 'cost'),
('marketPotential', 'Potensi Pasar', 0.20, 'benefit')
ON DUPLICATE KEY UPDATE
name = VALUES(name),
weight = VALUES(weight),
type = VALUES(type);

-- Insert sample locations
INSERT INTO locations (name, address, latitude, longitude) VALUES
('Jakarta Pusat', 'Jl. MH Thamrin No. 1, Menteng, Jakarta Pusat, DKI Jakarta 10310', -6.19440000, 106.82290000),
('Bandung', 'Jl. Asia Afrika No. 146, Sumur Bandung, Kota Bandung, Jawa Barat 40112', -6.91750000, 107.61910000),
('Surabaya', 'Jl. Pemuda No. 31-37, Embong Kaliasin, Genteng, Surabaya, Jawa Timur 60271', -7.25750000, 112.75210000)
ON DUPLICATE KEY UPDATE
name = VALUES(name),
address = VALUES(address),
latitude = VALUES(latitude),
longitude = VALUES(longitude);

-- Insert sample evaluations
INSERT INTO evaluations (location_id, criteria_id, value) VALUES
-- Jakarta Pusat
(1, 'populationDensity', 85),
(1, 'accessibility', 90),
(1, 'competition', 60),
(1, 'rentCost', 40),
(1, 'marketPotential', 88),

-- Bandung
(2, 'populationDensity', 75),
(2, 'accessibility', 80),
(2, 'competition', 70),
(2, 'rentCost', 70),
(2, 'marketPotential', 82),

-- Surabaya
(3, 'populationDensity', 80),
(3, 'accessibility', 85),
(3, 'competition', 65),
(3, 'rentCost', 60),
(3, 'marketPotential', 85)
ON DUPLICATE KEY UPDATE
value = VALUES(value);
