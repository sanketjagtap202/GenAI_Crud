# FastAPI + MongoDB User CRUD Application

## 1. Prerequisites
- Python 3.10+
- MongoDB running locally or a MongoDB Atlas connection string
- Postman

## 2. Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

For Linux/macOS:
```bash
source venv/bin/activate
cp .env.example .env
```

Edit `.env` if MongoDB is not local.

## 3. Start MongoDB
Local MongoDB default URL:
`mongodb://localhost:27017`

The database and `users` collection are created when the application first writes data. A unique index is created for `employee_id`.

## 4. Start API

```bash
uvicorn app.main:app --reload
```

Open Swagger:
`http://127.0.0.1:8000/docs`

Health check:
`GET http://127.0.0.1:8000/health`

## 5. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/users` | Create user |
| GET | `/api/users` | Get all users |
| GET | `/api/users/{user_id}` | Get one user |
| PUT | `/api/users/{user_id}` | Update user |
| DELETE | `/api/users/{user_id}` | Delete user |
| POST | `/api/users/{user_id}/profile-photo` | Upload/replace photo |
| PUT | `/api/users/{user_id}/profile-photo` | Update/replace photo |

## 6. Postman testing
Import `postman/User_CRUD_API.postman_collection.json` into Postman. Set collection variable `base_url` to `http://127.0.0.1:8000`.

Recommended sequence:
1. Create User
2. Upload Profile Photo using the returned `user_id`
3. Get Users
4. Get User
5. Update User
6. Update Profile Photo
7. Delete User

For file upload use Body -> form-data -> key `file` -> type File.

## 7. Data model
Example MongoDB document:
```json
{
  "user_name": "Rahul Sharma",
  "address": "Pune, Maharashtra",
  "employee_id": "EMP1001",
  "salary": 65000,
  "gender": "Male",
  "joining_date": "2025-01-15",
  "active_status": true,
  "profile_photo": "uploads/OBJECTID_UUID.jpg"
}
```

MongoDB also adds `_id` automatically.

## 8. Error handling
- 400: invalid ObjectId, invalid image type, empty update
- 404: user not found
- 409: duplicate employee ID
- 413: image exceeds configured size
- 422: FastAPI/Pydantic request validation error

## 9. Architecture
Postman -> FastAPI route -> Pydantic validation -> MongoDB / file system -> JSON response

Profile photo flow:
Postman multipart/form-data -> FastAPI UploadFile -> validation -> save to `uploads/` -> store file path in MongoDB -> response contains `profile_photo` path.
