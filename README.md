# Event Management System

A Python-based web application for managing events, registrations, and approvals with separate user and admin roles.

## Features

### For Users
- Submit event proposals for approval
- View approved events
- Register for events
- Input validation for all form submissions

### For Admins
- Submit events (directly goes to pending)
- View all approved events
- Approve or reject pending event submissions
- View all user registrations
- Admin authentication for secure access

## Technologies Used
- Python 3
- Gradio (for web interface)
- CSV file-based data storage

## File Structure
- `final.py` - Main application code
- `events.csv` - Stores approved events
- `pending_events.csv` - Stores events waiting for admin approval
- `registrations.csv` - Stores user registrations for events

## Data Structure

### Events (events.csv & pending_events.csv)
- Event Name
- Date (DD-MM-YYYY)
- Time (HH:MM)
- Venue
- Organizer Name
- Organizer Phone
- Organizer Email

### Registrations (registrations.csv)
- User Name
- User Email
- User Phone
- Event Name

## Setup and Installation

1. Clone the repository
```
git clone https://github.com/yourusername/event-management-system.git
cd event-management-system
```

2. Install required packages
```
pip install gradio
```

3. Run the application
```
python final.py
```

4. Open your browser and navigate to the URL shown in the terminal (typically http://127.0.0.1:7860)

## Usage

### User Mode
1. Select "User" role on the homepage
2. Click "Login" to access user dashboard
3. Use tabs to:
   - Submit event proposals
   - View approved events
   - Register for events

### Admin Mode
1. Select "Admin" role on the homepage
2. Enter admin credentials:
   - Username: admin
   - Password: 123
3. Click "Login" to access admin dashboard
4. Use tabs to:
   - Submit events
   - View approved events
   - Approve pending events
   - View user registrations

## Input Validation
The system includes comprehensive validation for:
- Required fields
- Date format (DD-MM-YYYY) and future dates only
- Time format (HH:MM in 24-hour format)
- Email format
- Phone number format (10-15 digits)
- Event existence (for registrations)

## Security Notes
- Default admin credentials (admin/123) should be changed in production
- CSV file storage should be replaced with a proper database for production use

## Future Improvements
- Database integration
- User authentication
- Event categorization
- Event capacity limits
- Email notifications
- Admin user management
- Event cancellation functionality
