# Blog-API

## Overview
This is a robust RESTful API built with **FastAPI** and **MySQL** for a blogging platform. It manages Authors and Posts with a strong focus on backend best practices, including data integrity and query optimization.

This project was built to satisfy strict backend requirements:
* **One-to-Many Relationships:** Implementation of `Author` -> `Posts` relationship.
* **Cascade Deletes:** Deleting an author automatically removes all their associated posts to maintain data integrity.
* **N+1 Query Optimization:** Utilizes SQLAlchemy's `joinedload` to fetch related data in a single query, preventing performance bottlenecks.
* **Data Validation:** Uses Pydantic schemas for strict request/response validation.

---

## Technology Stack
* **Framework:** FastAPI
* **Database:** MySQL (8.0+)
* **ORM:** SQLAlchemy
* **Driver:** PyMySQL
* **Validation:** Pydantic
* **Server:** Uvicorn

---

## Setup & Installation

### 1. Prerequisites
* Python 3.8 or higher
* MySQL Server installed and running

### 2. Clone and Environment Setup
Open your terminal and run the following commands:

```bash
# 1. Create a project directory (if you haven't already)
mkdir blog_project
cd blog_project

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy pymysql pydantic email-validator
```

### 4. Database Configuration
Log in to your MySQL server and create the database:

```SQL
CREATE DATABASE blog_db;
```

Open database.py and update the SQLALCHEMY_DATABASE_URL with your credentials:
```Python

# Format: mysql+pymysql://<username>:<password>@localhost/blog_db
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:YourPassword@localhost/blog_db"
```
**(Note: If your password contains special characters like '@', use urllib.parse.quote_plus to encode it).**

### 5. Run the Application
Start the server with hot-reloading:
```bash
uvicorn main:app --reload
```

## API Documentation

You can access the interactive **Swagger UI** at:

(https://documenter.getpostman.com/view/50502181/2sB3dSR9Hg)

Below is a summary of the available endpoints.

---

## Author Endpoints

### **1. Create Author**
**URL:** `POST /authors`  
**Description:** Registers a new author. The email must be unique.

#### Request Body (JSON)

```json
{
  "name": "Sudheer",
  "email": "sudheer@example.com"
}
```
#### Response (200 OK):

```json
{
  "name": "Sudheer",
  "email": "sudheer@example.com",
  "id": 1
}
```

---

### **2. Get All Authors**
**URL:** `GET /authors`
**Description:** Retrieve a list of all authors.

### **3. Get Single Author**
**URL:** `GET /authors/{id}`
**Description:** Get details of a specific author. Returns 404 if not found.

### **4. Update Author**
**URL:** `PUT /authors/{id}`
Request Body:

```json
{
  "name": "Sudheer Updated",
  "email": "sudheer.email@example.com"
}
```

### **5. Delete Author (Cascade)**
**URL:** `DELETE /authors/{id}`
**Description:** Deletes the author AND automatically deletes all their blog posts.

#### Response: { "message": "Author and associated posts deleted" }

### **6. Get Posts by Author**
**URL:** `GET /authors/{id}/posts`
**Description:** Retrieve all posts written by a specific author.

## Post Endpoints
### **1. Create Post**
**URL:** `POST /posts`
**Description:** Create a new post. Requires a valid author_id.

#### Request Body:

```json
{
  "title": "My First Blog",
  "content": "Content of the blog post...",
  "author_id": 1
}
```
#### Response (200 OK):

```json
{
  "title": "My First Blog",
  "content": "Content of the blog post...",
  "id": 1,
  "author_id": 1
}
```

### **2. Get All Posts**
**URL:** `GET /posts`
**Optional Filter:** GET /posts?author_id=1

### **3. Get Single Post (Detailed)**
**URL:** `GET /posts/{id}`
**Description:** Retrieves a post and includes the nested Author object (solving N+1 problem).

##### Response:

```json
{
  "title": "My First Blog",
  "content": "Content...",
  "id": 1,
  "author_id": 1,
  "author": {
    "name": "Sudheer",
    "email": "sudheer@example.com",
    "id": 1
  }
}
```

### **4. Update Post**
**URL:** `PUT /posts/{id}`

#### Request Body:

```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

### **5. Delete Post**
**URL:** `DELETE /posts/{id}`
**Response:** { "message": "Post deleted" }

## Database Schema & ERD

The database contains two tables: **authors** and **posts**, connected by a **one-to-many relationship**  
(one author can have many posts).

---

## Schema Details

### **Authors Table**
- `id` — Primary Key (Integer, Auto-increment)  
- `name` — String (Not Null)  
- `email` — String (Unique, Not Null)  
- **Relationship:** One Author → Many Posts  

---

### **Posts Table**
- `id` — Primary Key (Integer, Auto-increment)  
- `title` — String (Not Null)  
- `content` — Text (Not Null)  
- `author_id` — Foreign Key referencing `authors.id`  
- **Constraint:** `ON DELETE CASCADE` (Deleting an author deletes all their posts)  

---

```mermaid
erDiagram
    AUTHORS ||--|{ POSTS : has

    AUTHORS {
        int id PK
        string name
        string email
    }

    POSTS {
        int id PK
        string title
        text content
        int author_id FK
    }
```

## Testing (Postman)

A **Postman_collection.json** file is included in this repository.

### How to Use:

1. Open **Postman**.
2. Click **Import → Upload Files**.
3. Select **Postman_collection.json**.
4. Run the requests in the following order to verify functionality:

   1. **Create Author**  
   2. **Create Post** (requires an existing Author ID)  
   3. **Get Single Post** (verifies nested author–post relationship)  
   4. **Delete Author** (verifies `ON DELETE CASCADE` behavior)
