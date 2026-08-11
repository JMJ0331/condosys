# CONDOSYS - API Testing Guide

## 🚀 Quick Start

### 1. Start Development Server
```bash
cd c:\Users\JMJ\Desktop\condosys\backend
.\venv\Scripts\python manage.py runserver 0.0.0.0:8000
```

Server runs at: `http://localhost:8000`

### 2. Access Django Admin
```
URL: http://localhost:8000/admin/
Email: admin@condosys.com
Password: admin123
```

---

## 📋 API Endpoints Reference

### Authentication (POST)
```
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "admin@condosys.com",
  "password": "admin123"
}

Response:
{
  "message": "Login successful",
  "user": {
    "id": "...",
    "email": "admin@condosys.com",
    "full_name": "Admin Test",
    "role": "admin",
    "status": "active",
    "is_active": true,
    "created_at": "2026-08-11T..."
  }
}
```

### Structure - Gardens (GET/POST)
```
GET /api/v1/structure/gardens/
GET /api/v1/structure/gardens/{id}/
POST /api/v1/structure/gardens/

POST body:
{
  "name": "Conjunto Nuevo",
  "location": "Bogotá",
  "description": "Descripción opcional",
  "is_active": true
}
```

### Structure - Buildings (GET/POST)
```
GET /api/v1/structure/buildings/
GET /api/v1/structure/buildings/?garden={garden_id}
POST /api/v1/structure/buildings/

POST body:
{
  "garden": "{garden_id}",
  "name": "Edificio A",
  "number_of_floors": 10,
  "description": "Edificio residencial",
  "is_active": true
}
```

### Structure - Apartments (GET/POST)
```
GET /api/v1/structure/apartments/
GET /api/v1/structure/apartments/?building={building_id}
GET /api/v1/structure/apartments/?status=occupied
GET /api/v1/structure/apartments/{id}/
POST /api/v1/structure/apartments/

POST body:
{
  "building": "{building_id}",
  "number": "101",
  "floor": 1,
  "area_m2": 85.5,
  "type": "apartment",
  "status": "empty",
  "is_active": true
}
```

### Residents (GET/POST)
```
GET /api/v1/residents/
GET /api/v1/residents/?apartment={apt_id}
POST /api/v1/residents/

POST body:
{
  "user": "{user_id}",
  "apartment": "{apartment_id}",
  "role_in_apartment": "owner",
  "move_in_date": "2026-01-01",
  "emergency_contact": "Juan Pérez",
  "emergency_phone": "+5715555555"
}
```

### Payments (GET/POST)
```
GET /api/v1/payments/
GET /api/v1/payments/?status=pending
GET /api/v1/payments/?apartment={apt_id}
GET /api/v1/payments/charge-types/

POST /api/v1/payments/
{
  "apartment": "{apartment_id}",
  "charge_type": "{charge_type_id}",
  "amount": 250000.00,
  "invoice_date": "2026-08-11",
  "due_date": "2026-08-25",
  "status": "pending",
  "payment_method": "transfer"
}
```

### Incidents (GET/POST)
```
GET /api/v1/incidents/incidents/
GET /api/v1/incidents/incidents/?status=new
GET /api/v1/incidents/incidents/{id}/
POST /api/v1/incidents/incidents/

POST body:
{
  "apartment": "{apartment_id}",
  "reported_by": "{user_id}",
  "category": "plumbing",
  "priority": "high",
  "title": "Fuga de agua",
  "description": "Hay fuga en el baño",
  "status": "new"
}
```

### Incidents History (GET)
```
GET /api/v1/incidents/history/
GET /api/v1/incidents/history/?incident={incident_id}
```

### Visitors (GET/POST/PATCH)
```
GET /api/v1/visitors/
GET /api/v1/visitors/?status=pending
POST /api/v1/visitors/

POST body:
{
  "apartment": "{apartment_id}",
  "registered_by": "{user_id}",
  "name": "Juan Pérez",
  "document": "12345678",
  "phone": "+5715551234",
  "reason": "Visita familiar",
  "type": "family",
  "scheduled_entry": "2026-08-12T14:00:00Z",
  "scheduled_exit": "2026-08-12T18:00:00Z",
  "status": "pending"
}
```

### Reservations (GET/POST/PATCH)
```
GET /api/v1/reservations/
GET /api/v1/reservations/?status=requested
GET /api/v1/reservations/common-areas/

POST /api/v1/reservations/
{
  "common_area": "{area_id}",
  "reserved_by": "{user_id}",
  "start_time": "2026-08-15T10:00:00Z",
  "end_time": "2026-08-15T14:00:00Z",
  "reason": "Fiesta familiar",
  "expected_guests": 25,
  "status": "requested"
}

PATCH /api/v1/reservations/{id}/
{
  "status": "approved",
  "approved_by": "{manager_user_id}"
}
```

### Maintenance Orders (GET/POST/PATCH)
```
GET /api/v1/maintenance/
GET /api/v1/maintenance/?status=scheduled
POST /api/v1/maintenance/

POST body:
{
  "apartment": "{apartment_id}",
  "assigned_to": "{maintenance_user_id}",
  "type": "preventive",
  "description": "Mantenimiento preventivo",
  "scheduled_date": "2026-08-15",
  "estimated_cost": 50000.00,
  "status": "scheduled"
}
```

### Communications (GET/POST)
```
GET /api/v1/communications/
GET /api/v1/communications/?target_type=general
POST /api/v1/communications/

POST body:
{
  "garden": "{garden_id}",
  "sender": "{user_id}",
  "title": "Anuncio importante",
  "body": "Se suspenderá el servicio de agua",
  "target_type": "general",
  "is_published": true
}
```

### Notifications (GET/PATCH)
```
GET /api/v1/notifications/
GET /api/v1/notifications/?is_read=false
PATCH /api/v1/notifications/{id}/
{
  "is_read": true
}
```

### Chat Messages (GET/POST)
```
GET /api/v1/chat/
GET /api/v1/chat/?receiver={user_id}
GET /api/v1/chat/?group_name={group_name}
POST /api/v1/chat/

POST body (private message):
{
  "sender": "{user_id}",
  "receiver": "{user_id}",
  "message": "Hola, ¿cómo estás?"
}

POST body (group message):
{
  "sender": "{user_id}",
  "group_name": "mantenimiento",
  "message": "Recordatorio: reunión a las 3pm"
}
```

---

## 🧪 Testing with cURL

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@condosys.com","password":"admin123"}'
```

### Get Gardens
```bash
curl http://localhost:8000/api/v1/structure/gardens/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Create Apartment
```bash
curl -X POST http://localhost:8000/api/v1/structure/apartments/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{
    "building": "building-uuid",
    "number": "101",
    "floor": 1,
    "area_m2": 85.5,
    "type": "apartment",
    "status": "empty"
  }'
```

---

## 🔐 Permission Classes

The following permission classes are configured:

- **IsAdmin**: Solo administradores
- **IsManager**: Administradores o gerentes
- **IsResident**: Solo residentes
- **IsResidentOrManager**: Residentes, gerentes o admins
- **IsMaintenance**: Personal de mantenimiento
- **IsSecurity**: Personal de seguridad

These can be applied to individual ViewSets for authorization control.

---

## 🌐 WebSocket Endpoints

### Chat (Private)
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/user-id/');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Mensaje recibido:', data);
};
```

### Group Chat
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/group/group-name/');
```

### Notifications
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/notifications/user-id/');
```

---

## 📊 Database Models & Relationships

```
Garden (1) ---- (n) Building
           \---- (n) Apartment
           \---- (n) CommonArea
           \---- (n) Communication

Building (1) ---- (n) Apartment
                   \---- (n) Resident
                   \---- (n) Payment
                   \---- (n) Incident
                   \---- (n) Visitor
                   \---- (n) MaintenanceOrder

User (1) ---- (1) Resident
      (1) ---- (n) Incident (reported_by, assigned_to)
      (1) ---- (n) Visitor (registered_by, authorized_by)
      (1) ---- (n) Reservation (reserved_by, approved_by)
      (1) ---- (n) ChatMessage (sender, receiver)
      (1) ---- (n) Notification
      (1) ---- (n) Communication (sender)

Apartment (1) ---- (n) Resident
            \---- (n) Payment
            \---- (n) Incident
            \---- (n) Visitor
            \---- (n) MaintenanceOrder
```

---

## ✅ Test Checklist

- [ ] Login endpoint works
- [ ] Can get/create Gardens
- [ ] Can get/create Buildings
- [ ] Can get/create Apartments
- [ ] Can create Residents
- [ ] Can create Payments
- [ ] Can report Incidents
- [ ] Can register Visitors
- [ ] Can create Reservations
- [ ] Can create Maintenance Orders
- [ ] Can post Communications
- [ ] WebSocket chat connects
- [ ] Notifications work

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Missing Dependencies
```bash
pip install -r requirements.txt
pip install channels channels-redis
pip install django-cors-headers
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 127.0.0.1:8001
```

---

**Status**: Phase 2 Complete - All Endpoints Ready for Testing
**Last Updated**: 2026-08-11
