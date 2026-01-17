# 🌍 COM714 Travel Management System – Solent Trips

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![JSON](https://img.shields.io/badge/Data-JSON-lightgrey)
![License](https://img.shields.io/badge/License-Academic-informational)
![GitHub](https://img.shields.io/badge/GitHub-Repository-brightgreen)

A comprehensive **Python-based Travel Management System** developed for **Solent University’s COM714 – Software Design & Development** module.  
The system replaces manual trip administration with a fully digitized platform for managing users, trips, finances, and analytical reporting.

---

## 📊 Project Highlights

| Aspect | Technologies Used | Key Features |
|------|------------------|--------------|
| **Application** | Python 3.8+ | Modular design, OOP, role-based menus |
| **Data Management** | JSON | Persistent storage, serialization |
| **Security** | SHA-256 | Secure authentication, RBAC |
| **Analytics** | Matplotlib, NumPy | Visual reports & trend analysis |
| **Design** | UML (ICONIX) | Class, Use Case & Robustness diagrams |

---

## 🎯 Learning Outcomes Demonstrated

### 1. Object-Oriented Design
- Inheritance-based user hierarchy  
- Encapsulation of business rules  
- Composition for trip and leg structures  
- Clear separation of responsibilities  

### 2. Software Architecture
- Three-layer architecture  
- Separation of concerns  
- Scalable and maintainable structure  

### 3. Secure Application Development
- Password hashing with SHA-256  
- Role-based access control  
- Session handling and validation  

### 4. Data Processing & Reporting
- Cost aggregation and invoice generation  
- Financial summaries  
- Traveller demographic analysis  
- Revenue trend visualizations  

---

## 🔍 Core Features

### 👤 User Management
- Three-tier role hierarchy  
  **Administrator → Trip Manager → Trip Coordinator**
- Secure login system  
- Full CRUD operations for users  

### 🧳 Trip Management
- Complete trip lifecycle handling  
- Trip coordinator assignment  
- Trip status tracking (active / inactive)  
- Multiple traveller assignments  

### 💰 Financial Management
- Automated invoice generation  
- Payment tracking (multiple methods)  
- Balance calculations  
- Invoice status management  

### 🗺️ Trip Leg System
- Multi-leg itinerary support  
- Transport modes: Flight, Train, Bus, Taxi, Ship  
- Leg types: Accommodation, Transfer, Point of Interest  
- Cost tracking per leg  
- Automated itinerary generation  

### 📈 Reporting & Analytics
- Trip statistics by coordinator  
- Financial summaries  
- Traveller age demographics  
- Revenue trends over time  

---

## 🧱 System Architecture

Presentation Layer (Console UI)  
- Role-based menus  

Business Logic Layer  
- User management  
- Trip & traveller management  
- Financial processing  

Data Access Layer  
- JSON file persistence  

### Design Principles Applied
- Encapsulation  
- Inheritance  
- Single Responsibility Principle  
- Separation of Concerns  
- Composition over Inheritance  

---

## 📁 Project Structure

COM714_Travel_System/  
├── main.py  
├── models.py  
├── auth.py  
├── data_manager.py  
├── report_generator.py  
├── data/  
│   ├── users.json  
│   ├── travellers.json  
│   ├── trips.json  
│   └── invoices.json  
├── reports/  
├── tests/  
└── README.md  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+  
- pip  

### Installation
git clone https://github.com/FrankenSama/COM714_Travel_System.git  
cd COM714_Travel_System  
pip install matplotlib numpy  
python main.py  

---

## 🔐 Default Login Credentials

**Administrator**  
- Username: `admin`  
- Password: `admin123`  

⚠️ Change the default password immediately in any production scenario.

---

## 👥 User Roles & Permissions

### Administrator
- Manage Trip Managers  
- View all invoices  
- Generate full system reports  
- Full system access  

### Trip Manager
- Manage Trip Coordinators  
- Generate trip-level invoices  
- Access coordinator functions  

### Trip Coordinator
- Manage trips and travellers  
- Create trip legs and itineraries  
- Handle invoices and payments  

---

## 🧪 Testing

Run all tests using:  
python -m unittest discover tests  

### Coverage Includes
- Authentication logic  
- Cost calculations  
- JSON serialization  
- Invoice and payment processing  
- Trip leg management  

---

## 📊 Generated Report Types

1. Trip Statistics  
2. Financial Summary  
3. Traveller Statistics  
4. Revenue Trends  

Reports are saved as PNG files in the `reports/` directory.

---

## 🔒 Security Features

- SHA-256 password hashing  
- Role-based access control  
- Input validation  
- Controlled session management  

---

## 🐛 Known Limitations

- JSON storage (no concurrent access)  
- Console-based UI  
- Simulated payment processing  
- Single-user session  

---

## 🔮 Future Enhancements

- Database integration (SQLite / PostgreSQL)  
- Web interface (Flask / Django)  
- Multi-user concurrent access  
- Real payment gateway  
- Email notifications  
- PDF / CSV export  
- REST API  

---

## 📚 Academic Context

- **Module:** COM714 – Software Design & Development  
- **University:** Solent University  
- **Programme:** MSc Computer Engineering  
- **Academic Year:** 2024–2025  
- **Tutor:** Daniel Olabanji  

---

## 👨‍💻 Author

**Octavio Silva**  
MSc Computer Engineering  
Solent University  
GitHub: **@FrankenSama**

---

## 📄 License

Developed as part of academic coursework for Solent University.

---

## 🙏 Acknowledgments

- Solent University – School of Science & Engineering  
- Python Software Foundation  
- Matplotlib Development Team  

---

**Last Updated:** January 2025  
**Version:** 1.1.0
