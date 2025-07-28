from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import mysql.connector
from db_config import get_db_connection
import json
import uvicorn

app = FastAPI(title="Tofico Analyzer API", version="1.0.0")

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
    criteria: Dict[str, float]

class LocationUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    criteria: Optional[Dict[str, float]] = None

class CriteriaCreate(BaseModel):
    id: str
    name: str
    weight: float
    type: str  # 'benefit' or 'cost'

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Tofico Analyzer API",
        "status": "running",
        "endpoints": ["/locations", "/criteria", "/docs"]
    }

# LOCATIONS ENDPOINTS
@app.get("/locations")
def get_locations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM locations")
        locations = cursor.fetchall()
        
        # Convert JSON string back to dict
        for location in locations:
            if isinstance(location['criteria'], str):
                location['criteria'] = json.loads(location['criteria'])
        
        cursor.close()
        conn.close()
        return locations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/locations/{location_id}")
def get_location(location_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
        location = cursor.fetchone()
        
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        # Convert JSON string back to dict
        if isinstance(location['criteria'], str):
            location['criteria'] = json.loads(location['criteria'])
        
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
        # Validasi criteria (0-100)
        for key, value in location.criteria.items():
            if not (0 <= value <= 100):
                raise HTTPException(status_code=400, detail=f"Criteria '{key}' must be between 0-100")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO locations (name, address, latitude, longitude, criteria) 
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            location.name,
            location.address,
            location.latitude,
            location.longitude,
            json.dumps(location.criteria)
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get the created location
        location_id = cursor.lastrowid
        cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
        new_location = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "id": new_location[0],
            "name": new_location[1],
            "address": new_location[2],
            "latitude": new_location[3],
            "longitude": new_location[4],
            "criteria": json.loads(new_location[5])
        }
    except HTTPException:
        raise
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
        if location.criteria is not None:
            # Validasi criteria
            for key, value in location.criteria.items():
                if not (0 <= value <= 100):
                    raise HTTPException(status_code=400, detail=f"Criteria '{key}' must be between 0-100")
            updates.append("criteria = %s")
            values.append(json.dumps(location.criteria))
        
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        values.append(location_id)
        query = f"UPDATE locations SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        # Get updated location
        cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
        updated_location = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return {
            "id": updated_location[0],
            "name": updated_location[1],
            "address": updated_location[2],
            "latitude": updated_location[3],
            "longitude": updated_location[4],
            "criteria": json.loads(updated_location[5])
        }
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
        cursor.execute("SELECT * FROM criteria")
        criteria = cursor.fetchall()
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
