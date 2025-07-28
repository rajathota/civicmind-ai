# 🔌 CivicMind AI Integrations Guide

Comprehensive guide for integrating CivicMind AI with external systems, APIs, and civic technology platforms.

## 📋 Table of Contents

1. [🏛️ Government API Integrations](#️-government-api-integrations)
2. [📱 311 System Integration](#-311-system-integration)
3. [🗺️ GIS and Mapping Services](#️-gis-and-mapping-services)
4. [📊 Open Data Portals](#-open-data-portals)
5. [🔗 Webhook and Event Systems](#-webhook-and-event-systems)
6. [📧 Communication Platforms](#-communication-platforms)
7. [🏠 Property and Housing Data](#-property-and-housing-data)
8. [🚨 Emergency Services](#-emergency-services)
9. [💳 Payment and Permit Systems](#-payment-and-permit-systems)
10. [📈 Analytics and Reporting](#-analytics-and-reporting)

---

## 🏛️ **Government API Integrations**

### **City API Framework**

Create a standardized framework for connecting to municipal APIs:

```python
# civicmind/integrations/city_api.py

from typing import Dict, Any, List, Optional
import requests
import asyncio
from abc import ABC, abstractmethod

class BaseCityAPI(ABC):
    """Base class for municipal API integrations"""
    
    def __init__(self, city_name: str, api_key: str, base_url: str):
        self.city_name = city_name
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_authentication()
    
    def _setup_authentication(self):
        """Setup API authentication headers"""
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"CivicMind-AI/1.0 ({self.city_name})"
        })
    
    @abstractmethod
    async def get_departments(self) -> List[Dict[str, Any]]:
        """Get list of city departments with contact information"""
        pass
    
    @abstractmethod
    async def submit_service_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a service request to the city"""
        pass
    
    @abstractmethod
    async def get_service_request_status(self, request_id: str) -> Dict[str, Any]:
        """Get the status of a service request"""
        pass
    
    async def get_contact_info(self, department: str) -> Optional[Dict[str, Any]]:
        """Get contact information for a specific department"""
        departments = await self.get_departments()
        for dept in departments:
            if department.lower() in dept.get("name", "").lower():
                return dept
        return None


class SacramentoAPI(BaseCityAPI):
    """Sacramento-specific API integration"""
    
    def __init__(self, api_key: str):
        super().__init__(
            "Sacramento", 
            api_key, 
            "https://api.cityofsacramento.org/v1"
        )
    
    async def get_departments(self) -> List[Dict[str, Any]]:
        """Get Sacramento city departments"""
        response = await self._make_request("GET", "/departments")
        return response.get("departments", [])
    
    async def submit_service_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit 311 request to Sacramento"""
        payload = {
            "service_code": self._map_to_service_code(request_data["category"]),
            "description": request_data["description"],
            "location": request_data["location"],
            "citizen_info": request_data.get("citizen_info", {}),
            "priority": request_data.get("priority", "medium")
        }
        
        response = await self._make_request("POST", "/service_requests", payload)
        return response
    
    async def get_service_request_status(self, request_id: str) -> Dict[str, Any]:
        """Get status of Sacramento service request"""
        response = await self._make_request("GET", f"/service_requests/{request_id}")
        return response
    
    def _map_to_service_code(self, category: str) -> str:
        """Map CivicMind categories to Sacramento service codes"""
        mapping = {
            "parking": "PARK001",
            "noise": "NOIS001",
            "infrastructure": "INFR001",
            "permits": "PERM001",
            "environmental": "ENVR001"
        }
        return mapping.get(category, "GENR001")
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make authenticated API request"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise CityAPIException(f"API request failed: {str(e)}")


class CityAPIException(Exception):
    """Custom exception for city API errors"""
    pass
```

### **Multi-City API Manager**

```python
# civicmind/integrations/city_manager.py

class CityAPIManager:
    """Manages multiple city API integrations"""
    
    def __init__(self):
        self.city_apis = {}
        self._register_default_cities()
    
    def _register_default_cities(self):
        """Register default city API integrations"""
        # Register cities with available APIs
        self.register_city("Sacramento", SacramentoAPI)
        self.register_city("San Francisco", SanFranciscoAPI)
        self.register_city("Los Angeles", LosAngelesAPI)
    
    def register_city(self, city_name: str, api_class: type):
        """Register a new city API"""
        self.city_apis[city_name.lower()] = api_class
    
    def get_city_api(self, location: str, api_key: str) -> Optional[BaseCityAPI]:
        """Get appropriate city API based on location"""
        city = self._extract_city_from_location(location)
        if city in self.city_apis:
            return self.city_apis[city](api_key)
        return None
    
    def _extract_city_from_location(self, location: str) -> str:
        """Extract city name from location string"""
        # Simple implementation - can be enhanced with geocoding
        location_lower = location.lower()
        for city in self.city_apis.keys():
            if city in location_lower:
                return city
        return None
```

---

## 📱 **311 System Integration**

### **Generic 311 Integration**

```python
# civicmind/integrations/three11.py

from typing import Dict, Any, List
import requests
from datetime import datetime

class Three11Integration:
    """Integration with 311 service request systems"""
    
    def __init__(self, endpoint_url: str, api_key: str = None):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"
    
    async def submit_request(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new 311 service request"""
        
        request_payload = {
            "service_code": self._categorize_service_code(issue_data["description"]),
            "description": issue_data["description"],
            "lat": issue_data.get("latitude"),
            "long": issue_data.get("longitude"),
            "address_string": issue_data.get("location"),
            "email": issue_data.get("citizen_info", {}).get("email"),
            "first_name": issue_data.get("citizen_info", {}).get("first_name"),
            "last_name": issue_data.get("citizen_info", {}).get("last_name"),
            "phone": issue_data.get("citizen_info", {}).get("phone"),
            "media_url": issue_data.get("image_url"),
            "requested_datetime": datetime.now().isoformat()
        }
        
        response = self.session.post(
            f"{self.endpoint_url}/requests.json",
            json=request_payload
        )
        response.raise_for_status()
        return response.json()
    
    async def get_request_status(self, service_request_id: str) -> Dict[str, Any]:
        """Get the status of a service request"""
        response = self.session.get(
            f"{self.endpoint_url}/requests/{service_request_id}.json"
        )
        response.raise_for_status()
        return response.json()
    
    async def search_requests(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for existing service requests"""
        params = {
            "jurisdiction_id": filters.get("jurisdiction"),
            "service_code": filters.get("service_code"),
            "start_date": filters.get("start_date"),
            "end_date": filters.get("end_date"),
            "status": filters.get("status", "open")
        }
        
        response = self.session.get(
            f"{self.endpoint_url}/requests.json",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def _categorize_service_code(self, description: str) -> str:
        """Map issue description to 311 service code"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["pothole", "road", "street", "pavement"]):
            return "street_maintenance"
        elif any(word in description_lower for word in ["noise", "loud", "music"]):
            return "noise_complaint"
        elif any(word in description_lower for word in ["parking", "car", "vehicle"]):
            return "parking_violation"
        elif any(word in description_lower for word in ["trash", "garbage", "litter"]):
            return "sanitation"
        elif any(word in description_lower for word in ["water", "leak", "pipe"]):
            return "water_utility"
        else:
            return "general_inquiry"


# SeeClickFix Integration
class SeeClickFixIntegration(Three11Integration):
    """Integration with SeeClickFix platform"""
    
    def __init__(self, api_key: str):
        super().__init__("https://seeclickfix.com/api/v2", api_key)
    
    async def submit_request(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit issue to SeeClickFix"""
        payload = {
            "issue": {
                "summary": issue_data["description"][:100],  # SeeClickFix has title length limit
                "description": issue_data["description"],
                "lat": issue_data.get("latitude"),
                "lng": issue_data.get("longitude"),
                "address": issue_data.get("location"),
                "category": self._map_to_scf_category(issue_data.get("category"))
            }
        }
        
        response = self.session.post(
            f"{self.endpoint_url}/issues",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def _map_to_scf_category(self, category: str) -> str:
        """Map CivicMind categories to SeeClickFix categories"""
        mapping = {
            "parking": "Parking",
            "infrastructure": "Street Light Out",
            "environmental": "Other Environmental Issue",
            "noise": "Noise Issue"
        }
        return mapping.get(category, "Other")
```

---

## 🗺️ **GIS and Mapping Services**

### **Google Maps Integration**

```python
# civicmind/integrations/mapping.py

import googlemaps
from typing import Dict, Any, List, Tuple

class MappingService:
    """Integration with mapping and geocoding services"""
    
    def __init__(self, google_api_key: str):
        self.gmaps = googlemaps.Client(key=google_api_key)
    
    async def geocode_address(self, address: str) -> Dict[str, Any]:
        """Convert address to coordinates and location data"""
        try:
            result = self.gmaps.geocode(address)
            if result:
                location = result[0]
                return {
                    "formatted_address": location["formatted_address"],
                    "latitude": location["geometry"]["location"]["lat"],
                    "longitude": location["geometry"]["location"]["lng"],
                    "city": self._extract_city(location["address_components"]),
                    "county": self._extract_county(location["address_components"]),
                    "state": self._extract_state(location["address_components"]),
                    "zip_code": self._extract_zip(location["address_components"]),
                    "place_id": location["place_id"]
                }
        except Exception as e:
            raise MappingException(f"Geocoding failed: {str(e)}")
        
        return None
    
    async def reverse_geocode(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Convert coordinates to address information"""
        try:
            result = self.gmaps.reverse_geocode((latitude, longitude))
            if result:
                return self.geocode_address(result[0]["formatted_address"])
        except Exception as e:
            raise MappingException(f"Reverse geocoding failed: {str(e)}")
        
        return None
    
    async def find_nearby_places(self, latitude: float, longitude: float, 
                                place_type: str, radius: int = 1000) -> List[Dict[str, Any]]:
        """Find nearby places of interest"""
        try:
            result = self.gmaps.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                type=place_type
            )
            
            places = []
            for place in result.get("results", []):
                places.append({
                    "name": place.get("name"),
                    "address": place.get("vicinity"),
                    "rating": place.get("rating"),
                    "types": place.get("types", []),
                    "place_id": place.get("place_id"),
                    "distance": self._calculate_distance(
                        latitude, longitude,
                        place["geometry"]["location"]["lat"],
                        place["geometry"]["location"]["lng"]
                    )
                })
            
            return sorted(places, key=lambda x: x["distance"])
        except Exception as e:
            raise MappingException(f"Places search failed: {str(e)}")
    
    async def get_civic_locations(self, latitude: float, longitude: float) -> Dict[str, List]:
        """Find nearby civic locations (city hall, police, etc.)"""
        civic_types = [
            "city_hall", "police", "fire_station", "courthouse", 
            "library", "post_office", "hospital"
        ]
        
        civic_locations = {}
        for place_type in civic_types:
            locations = await self.find_nearby_places(
                latitude, longitude, place_type, radius=5000
            )
            civic_locations[place_type] = locations[:3]  # Top 3 closest
        
        return civic_locations
    
    def _extract_city(self, address_components: List[Dict]) -> str:
        """Extract city from address components"""
        for component in address_components:
            if "locality" in component["types"]:
                return component["long_name"]
        return ""
    
    def _extract_county(self, address_components: List[Dict]) -> str:
        """Extract county from address components"""
        for component in address_components:
            if "administrative_area_level_2" in component["types"]:
                return component["long_name"]
        return ""
    
    def _extract_state(self, address_components: List[Dict]) -> str:
        """Extract state from address components"""
        for component in address_components:
            if "administrative_area_level_1" in component["types"]:
                return component["short_name"]
        return ""
    
    def _extract_zip(self, address_components: List[Dict]) -> str:
        """Extract ZIP code from address components"""
        for component in address_components:
            if "postal_code" in component["types"]:
                return component["long_name"]
        return ""
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in miles"""
        from math import radians, cos, sin, asin, sqrt
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 3959  # Radius of earth in miles
        
        return c * r


class MappingException(Exception):
    """Custom exception for mapping service errors"""
    pass
```

### **ArcGIS Integration**

```python
# civicmind/integrations/arcgis.py

from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from typing import Dict, Any, List

class ArcGISIntegration:
    """Integration with ArcGIS for government GIS data"""
    
    def __init__(self, portal_url: str = None, username: str = None, password: str = None):
        if portal_url and username and password:
            self.gis = GIS(portal_url, username, password)
        else:
            self.gis = GIS()  # Anonymous access to public data
    
    async def search_government_data(self, location: str, data_type: str) -> List[Dict[str, Any]]:
        """Search for government data layers by location and type"""
        search_query = f"{location} {data_type} government"
        
        items = self.gis.content.search(
            query=search_query,
            item_type="Feature Layer",
            max_items=10
        )
        
        datasets = []
        for item in items:
            datasets.append({
                "title": item.title,
                "description": item.description,
                "url": item.url,
                "owner": item.owner,
                "created": item.created,
                "modified": item.modified,
                "tags": item.tags
            })
        
        return datasets
    
    async def get_zoning_info(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Get zoning information for a specific location"""
        # This would connect to local government zoning layers
        try:
            # Search for zoning feature layers
            zoning_layers = self.gis.content.search(
                query="zoning",
                item_type="Feature Layer"
            )
            
            if zoning_layers:
                layer = FeatureLayer(zoning_layers[0].url)
                
                # Query for the specific point
                query_result = layer.query(
                    geometry={"x": longitude, "y": latitude, "spatialReference": {"wkid": 4326}},
                    spatial_rel="esriSpatialRelIntersects",
                    return_geometry=False,
                    out_fields="*"
                )
                
                if query_result.features:
                    feature = query_result.features[0]
                    return {
                        "zoning_code": feature.attributes.get("ZONE_CODE"),
                        "zoning_description": feature.attributes.get("ZONE_DESC"),
                        "permitted_uses": feature.attributes.get("PERMITTED_USES"),
                        "restrictions": feature.attributes.get("RESTRICTIONS")
                    }
        except Exception as e:
            raise GISException(f"Zoning query failed: {str(e)}")
        
        return {}
    
    async def get_parcel_info(self, address: str) -> Dict[str, Any]:
        """Get parcel/property information"""
        # Connect to assessor's parcel data
        try:
            parcel_layers = self.gis.content.search(
                query="parcel assessor property",
                item_type="Feature Layer"
            )
            
            if parcel_layers:
                layer = FeatureLayer(parcel_layers[0].url)
                
                # Search by address
                query_result = layer.query(
                    where=f"ADDRESS LIKE '%{address}%'",
                    return_geometry=False,
                    out_fields="*"
                )
                
                if query_result.features:
                    feature = query_result.features[0]
                    return {
                        "parcel_number": feature.attributes.get("APN"),
                        "owner": feature.attributes.get("OWNER"),
                        "assessed_value": feature.attributes.get("ASSESSED_VAL"),
                        "property_type": feature.attributes.get("PROP_TYPE"),
                        "land_use": feature.attributes.get("LAND_USE"),
                        "square_footage": feature.attributes.get("SQ_FT")
                    }
        except Exception as e:
            raise GISException(f"Parcel query failed: {str(e)}")
        
        return {}


class GISException(Exception):
    """Custom exception for GIS service errors"""
    pass
```

---

## 📊 **Open Data Portals**

### **CKAN Data Portal Integration**

```python
# civicmind/integrations/open_data.py

import requests
from typing import Dict, Any, List

class OpenDataPortal:
    """Integration with CKAN-based open data portals"""
    
    def __init__(self, portal_url: str, api_key: str = None):
        self.portal_url = portal_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers["Authorization"] = api_key
    
    async def search_datasets(self, query: str, tags: List[str] = None) -> List[Dict[str, Any]]:
        """Search for datasets in the open data portal"""
        params = {
            "q": query,
            "rows": 20
        }
        
        if tags:
            params["fq"] = " OR ".join([f"tags:{tag}" for tag in tags])
        
        response = self.session.get(
            f"{self.portal_url}/api/3/action/package_search",
            params=params
        )
        response.raise_for_status()
        
        data = response.json()
        return data["result"]["results"]
    
    async def get_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific dataset"""
        response = self.session.get(
            f"{self.portal_url}/api/3/action/package_show",
            params={"id": dataset_id}
        )
        response.raise_for_status()
        
        return response.json()["result"]
    
    async def get_resource_data(self, resource_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get data from a specific resource"""
        params = {
            "resource_id": resource_id,
            "limit": limit
        }
        
        response = self.session.get(
            f"{self.portal_url}/api/3/action/datastore_search",
            params=params
        )
        response.raise_for_status()
        
        data = response.json()
        return data["result"]["records"]
    
    async def get_civic_datasets(self, city: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get civic-relevant datasets for a city"""
        civic_categories = {
            "budget": ["budget", "finance", "spending"],
            "permits": ["permit", "license", "inspection"],
            "crime": ["crime", "police", "safety", "incident"],
            "traffic": ["traffic", "transportation", "parking"],
            "zoning": ["zoning", "planning", "land use"],
            "elections": ["election", "voting", "campaign"],
            "demographics": ["census", "population", "demographics"]
        }
        
        civic_data = {}
        for category, tags in civic_categories.items():
            query = f"{city} {category}"
            datasets = await self.search_datasets(query, tags)
            civic_data[category] = datasets[:5]  # Top 5 results per category
        
        return civic_data


# Socrata Open Data API Integration
class SocrataIntegration:
    """Integration with Socrata-powered open data portals"""
    
    def __init__(self, domain: str, app_token: str = None):
        self.domain = domain
        self.app_token = app_token
        self.session = requests.Session()
        
        if app_token:
            self.session.headers["X-App-Token"] = app_token
    
    async def query_dataset(self, dataset_id: str, query_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query a Socrata dataset"""
        url = f"https://{self.domain}/resource/{dataset_id}.json"
        
        params = query_params or {}
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def search_by_location(self, dataset_id: str, latitude: float, longitude: float, 
                                radius_miles: float = 1.0) -> List[Dict[str, Any]]:
        """Search dataset by geographic location"""
        # Convert miles to meters for Socrata
        radius_meters = radius_miles * 1609.34
        
        params = {
            "$where": f"within_circle(location, {latitude}, {longitude}, {radius_meters})"
        }
        
        return await self.query_dataset(dataset_id, params)
    
    async def get_recent_records(self, dataset_id: str, days: int = 30, 
                                date_field: str = "date") -> List[Dict[str, Any]]:
        """Get recent records from a dataset"""
        from datetime import datetime, timedelta
        
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        params = {
            "$where": f"{date_field} >= '{since_date}'"
        }
        
        return await self.query_dataset(dataset_id, params)
```

---

## 🔗 **Webhook and Event Systems**

### **Webhook Handler**

```python
# civicmind/integrations/webhooks.py

from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import Dict, Any, Callable, List
import hmac
import hashlib
from datetime import datetime

class WebhookManager:
    """Manages incoming webhooks from external systems"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.handlers = {}
        self.secret_keys = {}
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup webhook endpoints"""
        
        @self.app.post("/webhooks/{source}")
        async def receive_webhook(source: str, data: Dict[str, Any], 
                                background_tasks: BackgroundTasks):
            """Receive webhook from external source"""
            
            if source not in self.handlers:
                raise HTTPException(status_code=404, detail="Webhook source not found")
            
            # Verify webhook signature if secret key is configured
            if source in self.secret_keys:
                if not self._verify_signature(source, data):
                    raise HTTPException(status_code=401, detail="Invalid signature")
            
            # Process webhook in background
            background_tasks.add_task(self._process_webhook, source, data)
            
            return {"status": "received", "timestamp": datetime.now().isoformat()}
    
    def register_handler(self, source: str, handler: Callable, secret_key: str = None):
        """Register a webhook handler for a specific source"""
        self.handlers[source] = handler
        if secret_key:
            self.secret_keys[source] = secret_key
    
    async def _process_webhook(self, source: str, data: Dict[str, Any]):
        """Process webhook data with registered handler"""
        try:
            handler = self.handlers[source]
            await handler(data)
        except Exception as e:
            # Log error and potentially send to error tracking
            print(f"Webhook processing error for {source}: {str(e)}")
    
    def _verify_signature(self, source: str, data: Dict[str, Any]) -> bool:
        """Verify webhook signature"""
        # Implementation depends on the webhook source's signature method
        # This is a basic example
        secret = self.secret_keys[source]
        signature = data.get("signature", "")
        payload = data.get("payload", "")
        
        expected_signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)


# Example webhook handlers
async def handle_311_update(data: Dict[str, Any]):
    """Handle updates from 311 system"""
    request_id = data.get("service_request_id")
    status = data.get("status")
    
    # Update local database with 311 status change
    # Notify citizen if they requested updates
    # Update agent knowledge with resolution outcome


async def handle_city_data_update(data: Dict[str, Any]):
    """Handle updates from city data systems"""
    dataset = data.get("dataset")
    change_type = data.get("change_type")
    
    # Update vector store with new city data
    # Refresh agent knowledge bases
    # Trigger retraining if needed


async def handle_payment_notification(data: Dict[str, Any]):
    """Handle payment notifications for permits/fines"""
    payment_id = data.get("payment_id")
    amount = data.get("amount")
    status = data.get("status")
    
    # Update permit application status
    # Send confirmation to citizen
    # Update agent context for future interactions
```

---

## 📧 **Communication Platforms**

### **Email Integration**

```python
# civicmind/integrations/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any, Optional
import jinja2

class EmailService:
    """Email service for sending notifications and updates"""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates/email")
        )
    
    async def send_issue_confirmation(self, recipient: str, issue_data: Dict[str, Any]):
        """Send confirmation email when issue is submitted"""
        template = self.template_env.get_template("issue_confirmation.html")
        
        html_content = template.render(
            issue_id=issue_data["id"],
            description=issue_data["description"],
            location=issue_data["location"],
            recommendations=issue_data["recommendations"],
            contacts=issue_data["contacts"],
            next_steps=issue_data["next_steps"]
        )
        
        await self._send_email(
            recipient=recipient,
            subject=f"CivicMind AI: Your Issue #{issue_data['id']} - Confirmation",
            html_content=html_content
        )
    
    async def send_status_update(self, recipient: str, issue_id: str, status: str, details: str):
        """Send status update for an ongoing issue"""
        template = self.template_env.get_template("status_update.html")
        
        html_content = template.render(
            issue_id=issue_id,
            status=status,
            details=details,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        await self._send_email(
            recipient=recipient,
            subject=f"CivicMind AI: Update on Issue #{issue_id}",
            html_content=html_content
        )
    
    async def send_community_digest(self, recipients: List[str], location: str, digest_data: Dict[str, Any]):
        """Send weekly community digest"""
        template = self.template_env.get_template("community_digest.html")
        
        html_content = template.render(
            location=location,
            week_ending=digest_data["week_ending"],
            total_issues=digest_data["total_issues"],
            resolved_issues=digest_data["resolved_issues"],
            top_issues=digest_data["top_issues"],
            success_stories=digest_data["success_stories"]
        )
        
        for recipient in recipients:
            await self._send_email(
                recipient=recipient,
                subject=f"CivicMind AI: Weekly Digest for {location}",
                html_content=html_content
            )
    
    async def _send_email(self, recipient: str, subject: str, html_content: str, attachments: List[str] = None):
        """Send email with optional attachments"""
        msg = MIMEMultipart()
        msg["From"] = self.username
        msg["To"] = recipient
        msg["Subject"] = subject
        
        msg.attach(MIMEText(html_content, "html"))
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {file_path.split('/')[-1]}",
                )
                msg.attach(part)
        
        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)


# SMS Integration using Twilio
class SMSService:
    """SMS service for urgent notifications"""
    
    def __init__(self, account_sid: str, auth_token: str, phone_number: str):
        from twilio.rest import Client
        self.client = Client(account_sid, auth_token)
        self.phone_number = phone_number
    
    async def send_urgent_alert(self, recipient: str, message: str):
        """Send urgent SMS alert"""
        self.client.messages.create(
            body=message,
            from_=self.phone_number,
            to=recipient
        )
    
    async def send_issue_update(self, recipient: str, issue_id: str, status: str):
        """Send SMS update for issue status"""
        message = f"CivicMind AI Update: Issue #{issue_id} status changed to '{status}'. Check your email for details."
        
        self.client.messages.create(
            body=message,
            from_=self.phone_number,
            to=recipient
        )
```

---

This integrations guide provides a comprehensive framework for connecting CivicMind AI with external systems. Each integration can be customized and extended based on your specific municipal needs and available APIs.
