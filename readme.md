# Vacation Rental Management System

A comprehensive Django-based web application for managing vacation rental properties with advanced search capabilities, filtering options, and an intuitive admin interface.

## Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Custom Management Commands](#custom-management-commands)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Admin Panel](#admin-panel)

---

## Features

### Client-Facing Features
- **Property Listing**: Browse all available vacation rental properties with pagination
- **Advanced Search**: Search properties by location with real-time autocomplete suggestions
- **Smart Filters**: Filter properties by type, number of bedrooms, and price range
- **Property Details**: View comprehensive property information including images, amenities, and location
- **Responsive Design**: Mobile-friendly interface for seamless browsing on any device

### Admin Features
- **Complete CRUD Operations**: Create, Read, Update, and Delete properties
- **Inline Image Management**: Upload and manage multiple property images within the property form
- **Bulk Import**: Import properties from CSV files using custom management command
- **Location Management**: Manage property locations separately for better data organization
- **Admin Dashboard**: Full-featured Django admin interface with custom configurations

### Technical Features
- **RESTful API**: Custom API endpoint for location autocomplete
- **PostgreSQL Database**: Robust relational database with proper foreign key relationships
- **Image Upload**: Django ImageField for efficient image handling
- **Pagination**: Built-in Django pagination for better performance
- **CSV Import**: Custom management command for bulk property import

---

## System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.8 or higher
- **PostgreSQL**: Version 13 or higher
- **Docker**: (Optional) For containerized PostgreSQL
- **Storage**: Minimum 500MB free space for media files
- **RAM**: Minimum 2GB recommended

---

## Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Database**: PostgreSQL 13+
- **ORM**: Django ORM
- **Image Processing**: Pillow

### Frontend
- **Template Engine**: Django Templates
- **Styling**: Custom CSS 
- **JavaScript**:  For interaction

### Development Tools
- **Virtual Environment**: Python venv
- **Database Adapter**: psycopg2-binary

---

## 🗄 Database Schema

### Tables Overview

The application uses three main models (tables):

#### 1. **Location** (`properties_location`)
Stores location information for properties.

| Field      | Type         | Description                    |
|------------|--------------|--------------------------------|
| id         | Integer (PK) | Primary key                    |
| city       | VARCHAR(100) | City name                      |
| state      | VARCHAR(100) | State/Province name            |
| country    | VARCHAR(100) | Country name                   |
| address    | TEXT         | Full street address            |
| zip_code   | VARCHAR(20)  | Postal/ZIP code (nullable)     |

#### 2. **Property** (`properties_property`)
Main table for vacation rental properties.

| Field            | Type          | Description                              |
|------------------|---------------|------------------------------------------|
| id               | Integer (PK)  | Primary key                              |
| name             | VARCHAR(200)  | Property name                            |
| description      | TEXT          | Detailed property description            |
| property_type    | VARCHAR(50)   | Type (apartment/house/villa/cottage/cabin)|
| bedrooms         | Integer       | Number of bedrooms                       |
| bathrooms        | Integer       | Number of bathrooms                      |
| max_guests       | Integer       | Maximum guest capacity                   |
| price_per_night  | Decimal(10,2) | Nightly rental price                     |
| location_id      | Integer (FK)  | Foreign key to Location                  |
| created_at       | DateTime      | Record creation timestamp                |
| updated_at       | DateTime      | Last update timestamp                    |

#### 3. **Image** (`properties_image`)
Stores property images with many-to-one relationship.

| Field       | Type          | Description                    |
|-------------|---------------|--------------------------------|
| id          | Integer (PK)  | Primary key                    |
| property_id | Integer (FK)  | Foreign key to Property        |
| image       | ImageField    | Image file path                |
| caption     | VARCHAR(200)  | Image caption (nullable)       |
| uploaded_at | DateTime      | Upload timestamp               |

### Relationships
- **Property → Location**: Many-to-One (Each property belongs to one location)
- **Image → Property**: Many-to-One (Each property can have multiple images)

### Database Connection Details

```
Database Engine: PostgreSQL
Database Name: pythondb
Username: postgres
Password: postgres
Host: localhost
Port: 5432
```

---

## Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd django-vacation-rental-w3e
```

### Step 2: Set Up PostgreSQL Database

```bash
# Pull PostgreSQL image
docker pull postgres:latest

# Run PostgreSQL container
docker run --name postgres-vacation \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=pythondb \
  -p 5432:5432 \
  -d postgres:latest

# Verify container is running
docker ps
```

### Step 3: Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages from requirements.txt
pip install -r requirements.txt
```

**requirements.txt content:**
```
Django==4.2.7
psycopg2-binary==2.9.9
Pillow==10.1.0
```

### Step 5: Run Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### Step 6: Create Superuser for Admin Access

**IMPORTANT**: The setup script's automatic superuser creation may not work. You must create the superuser manually.

```bash
# Create superuser manually
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com  (press Enter to skip)
Password: admin123
Password (again): admin123
```

**Note**: When typing the password, nothing will appear on screen - this is normal. Just type and press Enter.

---

## Configuration

### Database Configuration

The database settings are configured in `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pythondb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Media Files Configuration

```python
# Media Files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static Files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## Run the Application quickly

### 1. Clone the project
```bash
git clone <-repo-url>
cd vacation_rental
```

### 2. Docker PostgreSQL run 
```bash
docker run --name postgres-vacation \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=pythondb \
  -p 5432:5432 -d postgres:latest
```

### 3. Database backup import 
```bash
./import_database.sh
```

### 4. Python setup 
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Server 
```bash
python manage.py runserver
```

### Access the Application

- **Frontend**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Admin Credentials**: 
  - Username: `admin`
  - Password: `admin` (or what you set during superuser creation)

---

## Usage

### For End Users (Clients)

#### 1. Browse Properties
- Navigate to the home page
- View all available properties in a grid layout
- Use pagination to browse through multiple pages

#### 2. Filter Properties
- Use the filter form to narrow down results:
  - **Property Type**: apartment, house, villa, cottage, cabin
  - **Bedrooms**: 1, 2, 3, 4+
  - **Price Range**: Set minimum and maximum price

#### 3. Search by Location
- Enter a location in the search bar
- Select from autocomplete suggestions
- View search results on a separate page

#### 4. View Property Details
- Click on any property card
- View complete property information
- See all available images
- Check pricing and amenities

### For Administrators

#### 1. Access Admin Panel
- Navigate to `/admin/`
- Login with admin credentials

#### 2. Manage Properties
- **Add Property**: Click "Add Property" button
- **Edit Property**: Click on property name
- **Delete Property**: Select properties and choose delete action
- **Add Images**: Use inline image formsets within property form

#### 3. Manage Locations
- Create and manage location data separately
- Link properties to locations

---

## Custom Management Commands

### Import Properties from CSV

The application includes a custom management command to bulk import properties from CSV files.

#### CSV File Location

The CSV file should be placed in the **project root directory** with the name `property.csv`.

```
vacation_rental/
├── property.csv        ← Place your CSV file here
├── manage.py
├── config/
├── properties/
└── ...
```

#### CSV File Format

Create a CSV file with the following columns:

```csv
name,description,property_type,bedrooms,bathrooms,max_guests,price_per_night,city,state,country,address,zip_code,image_urls
```

**Column Descriptions:**
- `name`: Property name (required)
- `description`: Detailed description (required)
- `property_type`: One of: apartment, house, villa, cottage, cabin (required)
- `bedrooms`: Number of bedrooms (integer, required)
- `bathrooms`: Number of bathrooms (integer, required)
- `max_guests`: Maximum guests (integer, required)
- `price_per_night`: Nightly price (decimal, required)
- `city`: City name (required)
- `state`: State/Province (required)
- `country`: Country name (required)
- `address`: Full address (optional)
- `zip_code`: Postal code (optional)
- `image_urls`: Pipe-separated image URLs (optional, leave empty if no internet)

#### Example CSV Row

```csv
Oceanfront Paradise,Luxurious villa with pool,villa,5,4,12,580.00,Malibu,California,USA,2850 Pacific Coast Highway,90265,
```

#### Import Command

```bash
# Make sure you're in the project directory

# Activate virtual environment
source venv/bin/activate

# Import from project root (property.csv)
python manage.py import_properties property.csv

# Or import from any other location with full path
python manage.py import_properties /path/to/your/property.csv
```

#### Import Process
1. Reads CSV file line by line
2. Creates or retrieves location records
3. Creates property records
4. Downloads and saves images (if URLs provided and internet available)
5. Handles errors gracefully (continues on image download failures)
6. Displays progress and summary

**Note**: If you don't have internet connection or want to skip images, leave the `image_urls` column empty in the CSV file. You can add images later through the admin panel.

---

## Project Structure

```
vacation_rental/
│
├── property.csv                # CSV file for importing properties
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
├── README.md                   # This file
│
├── config/                     # Django project configuration
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── properties/                 # Main application
│   ├── migrations/            # Database migrations
│   ├── management/            # Custom management commands
│   │   └── commands/
│   │       └── import_properties.py
│   ├── templates/             # HTML templates
│   │   └── properties/
│   │       ├── property_list.html
│   │       ├── search_results.html
│   │       └── property_detail.html
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py
│   ├── models.py             # Database models (3 models)
│   ├── tests.py
│   ├── urls.py               # App URL patterns
│   └── views.py              # View functions
│
├── templates/                 # Base templates
│   └── base.html             # Base template
│
├── static/                    # Static files (CSS, JS)
│   ├── css/
│   └── js/
│
├── media/                     # User-uploaded files
│   └── property_images/      # Property images
│
└── venv/                      # Virtual environment (not in git)
```

---

## API Endpoints

### Public Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | Property listing page | `page`, `type`, `bedrooms`, `min_price`, `max_price` |
| `/search/` | GET | Search results page | `location`, `page` |
| `/property/<id>/` | GET | Property detail page | `id` (path parameter) |
| `/api/locations/` | GET | Location autocomplete API | `query` (min 2 chars) |

### API Response Example

**Location Autocomplete** (`/api/locations/?query=miami`)

```json
{
  "locations": [
    {
      "city": "Miami",
      "state": "Florida",
      "country": "USA",
      "display": "Miami, Florida, USA"
    }
  ]
}
```

---

## Admin Panel

### Admin Interface Features

#### Property Admin
- **List View**: 
  - Display: name, type, bedrooms, bathrooms, price, location, creation date
  - Filters: property type, bedrooms, bathrooms
  - Search: name, description, location city
  
- **Edit View**:
  - Fieldsets: Basic Information, Property Details, Location, Timestamps
  - Inline Image Management: Add/edit/delete images within property form
  - Read-only fields: created_at, updated_at

#### Location Admin
- **List View**: city, state, country, zip code
- **Filters**: country, state
- **Search**: city, state, country

#### Image Admin
- **List View**: property, caption, upload date
- **Filters**: upload date
- **Search**: property name, caption

### Admin Customizations
- Tabular inline for images
- Custom fieldsets for better organization
- Verbose admin list displays
- Comprehensive search and filter options

---


## Quick Start Guide

### Complete Setup from Scratch

```bash
# 1. Navigate to project directory
# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser
# Username: admin
# Password: admin

# 6. Import data (if property.csv exists in root)
python manage.py import_properties property.csv

# 7. Run server
python manage.py runserver
```

```bash
# Access application
# Frontend: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
```
