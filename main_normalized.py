from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import mysql.connector
from db_config_normalized import get_db_connection
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Tofico Analyzer API - Normalized", version="2.0.0")

# CORS untuk ngrok dan GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class LocationCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CriteriaCreate(BaseModel):
    id: str
    name: str
    weight: float
    type: str  # 'benefit' or 'cost'

class CriteriaUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = None
    type: Optional[str] = None

class EvaluationUpdate(BaseModel):
    location_id: int
    criteria_id: str
    value: int

class LocationWithEvaluations(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    criteria: Dict[str, int]

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Tofico Analyzer API - Normalized Version",
        "status": "running",
        "version": "2.0.0",
        "endpoints": ["/locations", "/criteria", "/evaluations", "/docs"]
    }

# LOCATIONS ENDPOINTS
@app.get("/locations")
def get_locations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get locations with their evaluations
        query = """
        SELECT 
            l.id, l.name, l.address, l.latitude, l.longitude,
            e.criteria_id, e.value
        FROM locations l
        LEFT JOIN evaluations e ON l.id = e.location_id
        ORDER BY l.id, e.criteria_id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Group evaluations by location
        locations = {}
        for row in results:
            location_id = row['id']
            if location_id not in locations:
                locations[location_id] = {
                    'id': row['id'],
                    'name': row['name'],
                    'address': row['address'],
                    'latitude': float(row['latitude']) if row['latitude'] else 0,
                    'longitude': float(row['longitude']) if row['longitude'] else 0,
                    'criteria': {}
                }
            
            if row['criteria_id']:
                locations[location_id]['criteria'][row['criteria_id']] = row['value']
        
        cursor.close()
        conn.close()
        return list(locations.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/locations/{location_id}")
def get_location(location_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get location
        cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
        location = cursor.fetchone()
        
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        # Get evaluations for this location
        cursor.execute("SELECT criteria_id, value FROM evaluations WHERE location_id = %s", (location_id,))
        evaluations = cursor.fetchall()
        
        location['criteria'] = {eval['criteria_id']: eval['value'] for eval in evaluations}
        location['latitude'] = float(location['latitude']) if location['latitude'] else 0
        location['longitude'] = float(location['longitude']) if location['longitude'] else 0
        
        cursor.close()
        conn.close()
        return location
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/locations")
def create_location(location: LocationCreate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO locations (name, address, latitude, longitude) 
        VALUES (%s, %s, %s, %s)
        """
        values = (location.name, location.address, location.latitude, location.longitude)
        
        cursor.execute(query, values)
        conn.commit()
        
        location_id = cursor.lastrowid
        
        # Get the created location
        cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
        new_location = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "id": new_location[0],
            "name": new_location[1],
            "address": new_location[2],
            "latitude": float(new_location[3]) if new_location[3] else 0,
            "longitude": float(new_location[4]) if new_location[4] else 0,
            "criteria": {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/locations/{location_id}")
def update_location(location_id: int, location: LocationUpdate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if location exists
        cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Location not found")
        
        # Build update query dynamically
        updates = []
        values = []
        
        if location.name is not None:
            updates.append("name = %s")
            values.append(location.name)
        if location.address is not None:
            updates.append("address = %s")
            values.append(location.address)
        if location.latitude is not None:
            updates.append("latitude = %s")
            values.append(location.latitude)
        if location.longitude is not None:
            updates.append("longitude = %s")
            values.append(location.longitude)
        
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(location_id)
        query = f"UPDATE locations SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        # Return updated location
        return get_location(location_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/locations/{location_id}")
def delete_location(location_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if location exists
        cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Location not found")
        
        cursor.execute("DELETE FROM locations WHERE id = %s", (location_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"message": "Location deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CRITERIA ENDPOINTS
@app.get("/criteria")
def get_criteria():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM criteria ORDER BY name")
        criteria = cursor.fetchall()
        
        # Convert weight to float
        for criterion in criteria:
            criterion['weight'] = float(criterion['weight'])
        
        cursor.close()
        conn.close()
        return criteria
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/criteria")
def create_criteria(criteria: CriteriaCreate):
    try:
        # Validasi weight (0-1)
        if not (0 <= criteria.weight <= 1):
            raise HTTPException(status_code=400, detail="Weight must be between 0-1")
        
        # Validasi type
        if criteria.type not in ['benefit', 'cost']:
            raise HTTPException(status_code=400, detail="Type must be 'benefit' or 'cost'")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO criteria (id, name, weight, type) VALUES (%s, %s, %s, %s)"
        values = (criteria.id, criteria.name, criteria.weight, criteria.type)
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "id": criteria.id,
            "name": criteria.name,
            "weight": criteria.weight,
            "type": criteria.type
        }
    except mysql.connector.IntegrityError:
        raise HTTPException(status_code=400, detail="Criteria ID already exists")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/criteria/{criteria_id}")
def update_criteria(criteria_id: str, criteria: CriteriaUpdate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if criteria exists
        cursor.execute("SELECT * FROM criteria WHERE id = %s", (criteria_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Criteria not found")
        
        # Build update query dynamically
        updates = []
        values = []
        
        if criteria.name is not None:
            updates.append("name = %s")
            values.append(criteria.name)
        if criteria.weight is not None:
            if not (0 <= criteria.weight <= 1):
                raise HTTPException(status_code=400, detail="Weight must be between 0-1")
            updates.append("weight = %s")
            values.append(criteria.weight)
        if criteria.type is not None:
            if criteria.type not in ['benefit', 'cost']:
                raise HTTPException(status_code=400, detail="Type must be 'benefit' or 'cost'")
            updates.append("type = %s")
            values.append(criteria.type)
        
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(criteria_id)
        query = f"UPDATE criteria SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get updated criteria
        cursor.execute("SELECT * FROM criteria WHERE id = %s", (criteria_id,))
        updated_criteria = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "id": updated_criteria[0],
            "name": updated_criteria[1],
            "weight": float(updated_criteria[2]),
            "type": updated_criteria[3]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/criteria/{criteria_id}")
def delete_criteria(criteria_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if criteria exists
        cursor.execute("SELECT * FROM criteria WHERE id = %s", (criteria_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Criteria not found")
        
        cursor.execute("DELETE FROM criteria WHERE id = %s", (criteria_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": "Criteria deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# EVALUATIONS ENDPOINTS
@app.get("/evaluations")
def get_evaluations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            e.location_id, e.criteria_id, e.value,
            l.name as location_name,
            c.name as criteria_name, c.type as criteria_type
        FROM evaluations e
        JOIN locations l ON e.location_id = l.id
        JOIN criteria c ON e.criteria_id = c.id
        ORDER BY l.name, c.name
        """
        cursor.execute(query)
        evaluations = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return evaluations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/evaluations")
def update_evaluation(evaluation: EvaluationUpdate):
    try:
        # Validasi value (0-100)
        if not (0 <= evaluation.value <= 100):
            raise HTTPException(status_code=400, detail="Value must be between 0-100")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if location and criteria exist
        cursor.execute("SELECT * FROM locations WHERE id = %s", (evaluation.location_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Location not found")
        
        cursor.execute("SELECT * FROM criteria WHERE id = %s", (evaluation.criteria_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Criteria not found")
        
        # Insert or update evaluation
        query = """
        INSERT INTO evaluations (location_id, criteria_id, value) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE value = VALUES(value)
        """
        values = (evaluation.location_id, evaluation.criteria_id, evaluation.value)
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            "location_id": evaluation.location_id,
            "criteria_id": evaluation.criteria_id,
            "value": evaluation.value,
            "message": "Evaluation updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/evaluations/{location_id}/{criteria_id}")
def delete_evaluation(location_id: int, criteria_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if evaluation exists
        cursor.execute("SELECT * FROM evaluations WHERE location_id = %s AND criteria_id = %s", 
                      (location_id, criteria_id))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Evaluation not found")
        
        cursor.execute("DELETE FROM evaluations WHERE location_id = %s AND criteria_id = %s", 
                      (location_id, criteria_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"message": "Evaluation deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/health")
def health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))  # Ganti dari 5000 ke 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
