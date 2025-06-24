# Todo Web Application

A modern, full-featured todo application built with Django and MongoDB. This application provides user authentication, full CRUD functionality for tasks, and a beautiful, responsive web interface.

## Features

- **User Authentication**: Register and login functionality using MongoDB
- **Full CRUD Operations**: Create, Read, Update, Delete tasks
- **Task Management**: 
  - Title and description
  - Due dates
  - Completion status
  - User-specific tasks (private)
- **Modern UI**: Clean, responsive design with smooth animations
- **MongoDB Integration**: NoSQL database for all data storage
- **Real-time Updates**: AJAX-powered interactions without page reloads

## Prerequisites

Before running this application, make sure you have the following installed:

1. **Python 3.8+**
2. **MongoDB** (local installation or MongoDB Atlas)
3. **pip** (Python package manager)

## Installation & Setup

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd todo-web

# Or download and extract the project files
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. MongoDB Setup

#### Option A: Local MongoDB Installation

1. **Download and Install MongoDB Community Server**
   - Visit [MongoDB Download Center](https://www.mongodb.com/try/download/community)
   - Download the appropriate version for your operating system
   - Follow the installation instructions

2. **Start MongoDB Service**
   
   **Windows:**
   ```bash
   # MongoDB should start automatically as a service
   # If not, you can start it manually:
   net start MongoDB
   ```
   
   **macOS/Linux:**
   ```bash
   sudo systemctl start mongod
   # or
   brew services start mongodb-community
   ```

#### Option B: MongoDB Atlas (Cloud)

1. **Create MongoDB Atlas Account**
   - Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account
   - Create a new cluster

2. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string

3. **Update Database Configuration**
   - Open `todo_project/settings.py`
   - Replace the MongoDB connection with your Atlas connection string:
   ```python
   mongoengine.connect(
       db='todo_db',
       host='your-atlas-connection-string'
   )
   ```

### 4. Configure the Application

1. **Update Database Settings** (if using local MongoDB)
   
   The application is already configured for local MongoDB. If you need to change the database name or connection details, edit `todo_project/settings.py`:
   
   ```python
   mongoengine.connect(
       db='todo_db',  # Change database name here
       host='localhost',
       port=27017
   )
   ```

### 5. Run the Application

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage

### 1. Registration
- Visit the application homepage
- Click "Register" to create a new account
- Fill in your username and password (minimum 8 characters)
- You'll be automatically logged in after registration

### 2. Login
- If you already have an account, click "Login"
- Enter your username and password
- You'll be redirected to your task dashboard

### 3. Managing Tasks

#### Create a Task
- Click "Add New Task" or "Create Your First Task"
- Fill in the task details:
  - **Title** (required): Brief description of the task
  - **Description** (optional): Detailed information about the task
  - **Due Date** (optional): When the task should be completed
- Click "Create Task"

#### View Tasks
- All your tasks are displayed on the main dashboard
- Tasks are shown in cards with all relevant information
- Completed tasks are visually distinguished (grayed out with strikethrough)

#### Edit a Task
- Click the "Edit" button on any task
- A modal will open with the current task details
- Make your changes and click "Save Changes"

#### Mark Task as Complete
- Click the "Complete" button on any task
- The task will be marked as completed
- Click "Undo" to mark it as incomplete again

#### Delete a Task
- Click the "Delete" button on any task
- Confirm the deletion in the popup dialog
- The task will be permanently removed

## Project Structure

```
todo-web/
├── todo_project/          # Django project settings
│   ├── settings.py        # Application configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── tasks/                # Main application
│   ├── models.py         # MongoDB User & Task models
│   ├── views.py          # Custom auth + CRUD views
│   ├── urls.py           # App URL routing
│   └── templates/        # HTML templates
│       └── tasks/
│           ├── base.html      # Base template with styling
│           ├── home.html      # Welcome page
│           ├── login.html     # Login page
│           ├── register.html  # Registration page
│           ├── task_list.html # Main dashboard
│           └── create_task.html # Create task form
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MongoDB with mongoengine ODM
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Authentication**: Custom session-based authentication with MongoDB
- **Styling**: Custom CSS with modern design principles

## Security Features

- **User Authentication**: Custom MongoDB-based authentication system
- **CSRF Protection**: Built-in Django CSRF protection
- **User Isolation**: Each user can only access their own tasks
- **Input Validation**: Server-side validation for all inputs
- **Secure Headers**: Django security middleware enabled
- **Password Hashing**: Secure password storage using Django's hashing

## Customization

### Styling
- All styles are in `tasks/templates/tasks/base.html`
- The design uses a modern gradient background with glassmorphism effects
- Colors and styling can be easily modified in the CSS section

### Database
- The application uses MongoDB for all data storage
- User and Task schemas can be extended in `tasks/models.py`
- Additional fields can be added to both User and Task models

### Features
- New views can be added in `tasks/views.py`
- URL patterns are defined in `tasks/urls.py`
- Templates can be extended or modified in the `templates/` directory

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check if the connection string is correct
   - Verify network connectivity (for Atlas)

2. **Port Already in Use**
   - Change the port: `python manage.py runserver 8001`
   - Or kill the process using the port

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

4. **Template Errors**
   - Ensure all template files are in the correct directory structure
   - Check for syntax errors in HTML templates

### Getting Help

If you encounter issues:
1. Check the Django debug page for detailed error information
2. Verify MongoDB is running and accessible
3. Check the console for Python error messages
4. Ensure all dependencies are properly installed

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests. 
