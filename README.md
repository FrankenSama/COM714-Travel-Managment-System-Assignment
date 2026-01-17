# Travel Management System - Solent Trips

A comprehensive Python-based Travel Management System developed for Solent University's COM714 Software Design & Development module.

## 📋 Project Overview

This system digitizes the entire trip lifecycle for Solent Trips, replacing manual paperwork with an automated platform that streamlines communication between staff and travellers while providing centralized management of all trip aspects.

## ✨ Features

### User Management
- **Role-Based Access Control**: Three-tier hierarchy (Administrator → Trip Manager → Trip Coordinator)
- **Secure Authentication**: SHA-256 password hashing
- **User CRUD Operations**: Create, view, update, and delete users

### Trip Management
- Complete trip lifecycle management
- Trip coordinator assignment
- Trip status tracking (active/inactive)
- Multiple traveller assignments per trip

### Financial Management
- Automated invoice generation from trip costs
- Payment tracking with multiple payment methods
- Balance calculations and payment history
- Invoice status management

### Reporting & Analytics
- Trip statistics with visualizations
- Financial summaries and trends
- Traveller demographics analysis
- Revenue trend analysis over time

### Trip Leg System
- Detailed transportation segment management
- Support for multiple transport modes (Flight, Train, Bus, Taxi, Ship)
- Leg types (Accommodation, Point of Interest, Transfer)
- Cost tracking per leg
- Automated itinerary generation

## 🛠️ Technology Stack

- **Python 3.8+**
- **Standard Libraries**:
  - `json` - Data persistence
  - `datetime` - Date/time handling
  - `hashlib` - Password hashing
  - `enum` - Type-safe enumerations
  - `os` - File path operations
- **Visualization**:
  - `matplotlib` - Chart generation for reports
  - `numpy` - Data processing

## 📁 Project Structure

```
COM714_Travel_System/
├── main.py                 # Main application entry point
├── models.py              # Domain models and business entities
├── auth.py                # Authentication and authorization
├── data_manager.py        # Data persistence layer (JSON)
├── report_generator.py    # Report generation with matplotlib
├── data/                  # JSON data storage
│   ├── users.json
│   ├── travellers.json
│   ├── trips.json
│   └── invoices.json
├── reports/               # Generated report visualizations
├── tests/                 # Unit tests
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/FrankenSama/COM714_Travel_System.git
cd COM714_Travel_System
```

2. **Install dependencies**
```bash
pip install matplotlib numpy
```

3. **Run the application**
```bash
python main.py
```

## 🔐 Default Login Credentials

**Administrator Account:**
- Username: `admin`
- Password: `admin123`

> ⚠️ **Important**: Change the default administrator password after first login in a production environment.

## 📖 User Guide

### Administrator Functions
- Create and manage Trip Managers
- View all system invoices
- Generate comprehensive reports
- Access all Trip Coordinator functions

### Trip Manager Functions
- Create and manage Trip Coordinators
- Generate total invoices for trips
- Access all Trip Coordinator functions

### Trip Coordinator Functions
- Manage trips (CRUD operations)
- Manage travellers
- Create and manage trip legs
- Assign/remove travellers to/from trips
- Generate itineraries
- Handle payments and invoices

## 🏗️ Architecture

The system follows a **three-layer architecture**:

1. **Presentation Layer**: Console-based menu system with role-specific interfaces
2. **Business Logic Layer**: Object-oriented domain models and controllers
3. **Data Access Layer**: JSON file persistence with serialization/deserialization

### Design Principles Applied
- **Encapsulation**: Each class manages its own data
- **Inheritance**: User role hierarchy
- **Separation of Concerns**: Clear separation between UI, business logic, and data
- **Single Responsibility**: Each class has a focused purpose
- **Composition over Inheritance**: Object relationships

## 🎨 UML Design

The system was designed using the **ICONIX process** with three key UML diagrams:

1. **Class Diagram**: Shows the object-oriented structure including:
   - User inheritance hierarchy
   - Trip composition relationships
   - Enumeration types

2. **Use Case Diagram**: Documents all system functionalities by actor role

3. **Robustness Diagram**: Details the "Generate Itinerary" use case showing:
   - Boundary objects (UI)
   - Controller objects (business logic)
   - Entity objects (data models)

## 🧪 Testing

Run the test suite:
```bash
python -m unittest discover tests
```

### Testing Coverage
- Unit tests for authentication
- Cost calculation validation
- Data serialization/deserialization
- Invoice and payment processing
- Trip leg management

## 📊 Report Types

The system generates four types of visualizations:

1. **Trip Statistics**: Distribution of trips per coordinator with status breakdown
2. **Financial Summary**: Revenue overview, payment methods, top invoices
3. **Traveller Statistics**: Age distribution and demographics
4. **Revenue Trends**: Monthly revenue and trip count trends

Reports are saved as PNG files in the `reports/` directory.

## 🔒 Security Features

- **Password Hashing**: SHA-256 encryption for all passwords
- **Role-Based Access Control**: Hierarchical permission system
- **Session Management**: Secure user authentication and logout
- **Data Validation**: Input validation and error handling

## 🐛 Known Limitations

- **No Database**: Uses JSON files (not suitable for concurrent access)
- **Console Interface**: Limited to command-line interaction
- **No Real Payments**: Payment processing is simulated
- **Single-User Session**: One user can be logged in at a time

## 🔮 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Web-based interface (Django/Flask)
- [ ] Multi-user concurrent access
- [ ] Real payment gateway integration
- [ ] Email notifications
- [ ] Advanced analytics and predictive trends
- [ ] Export functionality (PDF reports, CSV data)
- [ ] API for third-party integrations

## 👨‍💻 Author

**Octavio Silva**
- MSc Computer Engineering
- Solent University (2024-2025)
- Module: COM714 - Software Design & Development

## 📄 License

This project is developed as part of university coursework for Solent University.

## 🙏 Acknowledgments

- Module Leader: Daniel Olabanji
- Solent University School of Science and Engineering
- Python Software Foundation
- Matplotlib Development Team

**Last Updated**: January 2025

**Version**: 1.1.0