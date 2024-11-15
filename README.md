# SpyCat Agency API

This is a Django REST API application for managing SpyCats, Missions, and Targets in a spy agency. The API allows you to create, read, update, and delete SpyCats, Missions, and Targets, with restrictions to prevent modifying or deleting items that are already assigned or completed.

## Requirements

- Python 3.x
- Django 4.x+
- Django Rest Framework
- Poetry (for dependency management)
- Postman (for API testing)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd spy-cat-agency
```

### 2. Set up the Virtual Environment with Poetry

```bash

poetry install
poetry shell
```

### 3. Run Migrations

Apply the database migrations to set up the necessary tables.

```bash

python manage.py migrate
```

### 4. Run the Development Server

```bash

python manage.py runserver
```

Now, the API should be accessible at <http://127.0.0.1:8000/>.

### 5. Api endpoints

Can be acessed in SCA.postman_collection.json
