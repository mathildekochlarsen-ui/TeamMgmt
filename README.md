# Team Management System

A full-stack application for managing students and teams, built with Flask backend and React frontend.

## Project Structure

```
TeamMgmt/
├── TeamApi.py              # Flask API backend
├── repo.py                 # MongoDB repository class
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── frontend/              # React frontend application
    ├── public/
    ├── src/
    ├── package.json
    └── README.md
```

## Features

### Backend (Flask API)
- RESTful API for students and teams management
- Swagger documentation at `/apidocs`
- CORS enabled for frontend communication
- In-memory storage (can be extended to use MongoDB via repo.py)

### Frontend (React)
- Modern, responsive UI
- Student management (CRUD operations)
- Team creation and member assignment
- Real-time updates
- Clean, professional design

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Installation & Setup

### Backend Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask API:
   ```bash
   python TeamApi.py
   ```

   The API will start on `http://localhost:5000`

3. Access Swagger documentation:
   Open `http://localhost:5000/apidocs` in your browser

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## API Endpoints

### Students
- `GET /students` - Get all students
- `GET /students/<id>` - Get student by ID
- `POST /students` - Create new student
  ```json
  {
    "name": "John Doe",
    "age": 22,
    "email": "john@example.com"
  }
  ```
- `PUT /students/<id>` - Update student
- `DELETE /students/<id>` - Delete student

### Teams
- `GET /teams` - Get all teams
- `POST /teams` - Create new team
  ```json
  {
    "name": "Team Alpha"
  }
  ```
- `POST /teams/<id>/add_member` - Add student to team
  ```json
  {
    "student_id": 1
  }
  ```

## Usage

1. Start the backend API (Flask)
2. Start the frontend application (React)
3. Navigate to `http://localhost:3000`
4. Use the UI to:
   - Add, edit, and delete students
   - Create teams
   - Add students to teams

## Development

### Backend Development
- The API uses in-memory storage by default
- To use MongoDB, modify `TeamApi.py` to use the `MongoDBRepo` class from `repo.py`
- API documentation is automatically generated with Swagger

### Frontend Development
- Built with Create React App
- Uses functional components and React Hooks
- API calls are centralized in `src/services/api.js`
- Styling is done with vanilla CSS

## Future Enhancements

- Persistent database storage (MongoDB integration)
- User authentication
- Team editing and deletion
- Remove members from teams
- Student search and filtering
- Bulk operations
- Data export functionality

## Technologies Used

### Backend
- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- Flasgger - Swagger documentation
- PyMongo - MongoDB driver (optional)

### Frontend
- React - UI library
- JavaScript (ES6+)
- CSS3
- Fetch API for HTTP requests

## License

This project is created for educational purposes.
