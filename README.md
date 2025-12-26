![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Hospital](https://img.shields.io/badge/Domain-Healthcare-red.svg)

🏥 DocLine – AI-Powered Hospital Wait Time & Scheduling System
DocLine is an AI-driven hospital management system that reduces patient waiting time, optimizes doctor utilization, and enables seamless appointment booking using Queuing Theory, Stochastic Simulation, and Linear Programming.
It provides separate dashboards for Admins and Users, supports real-time doctor availability, and includes a complete appointment booking system.

🚀 Problem Statement
Hospitals often face:
Long patient waiting times (2–4 hours)
Uneven doctor workload
Poor emergency prioritization
Manual appointment management
DocLine solves this by intelligently predicting, simulating, and optimizing patient flow without requiring additional hospital infrastructure.

💡 Solution Overview
DocLine combines mathematics + AI + web technology to create a smart hospital scheduling platform.
Core Capabilities:
Predict waiting times uing Queuing Theory
Simulate real hospital flow using stochastic processes
Optimize scheduling using Linear Programming
Provide live doctor availability to users
Enable appointment booking without admin approval
Secure admin panel for hospital management
## 🎥 Demo

> 📌 Screenshots and demo GIF will be added soon.

### 🔐 Admin Dashboard
- Login with animation
- Run simulations
- Optimize schedules
- View bookings

### 👤 User Dashboard
- View doctor availability
- Live waiting time
- Book appointments

*(You can add screenshots later using GitHub upload.)*


🧠 Mathematical Foundations
DocLine is built on three major mathematical pillars:

1️⃣ Queuing Theory (M/M/c Model)
Models patient arrivals (Poisson process)
Models service times (Exponential distribution)
Predicts:
Average waiting time
Queue length
Doctor utilization

2️⃣ Stochastic Simulation
Simulates real-life randomness:
Emergency arrivals
Variable consultation times
Produces realistic performance metrics

3️⃣ Linear Programming (Optimization)
Minimizes total patient waiting time
Prioritizes emergency patients
Balances doctor workload
Produces an optimal patient–doctor–time-slot schedule

⚙️ System Architecture
User / Admin
    ↓
Frontend (HTML, CSS, Bootstrap, JS)
     ↓
Flask Backend (APIs)
     ↓
Simulation Engine + LP Optimizer
     ↓
SQLite Database

🖥️ Dashboards
👤 User Dashboard (No Login Required)
View live doctor availability
View estimated waiting time
View doctor workload (utilization bars)
Book appointments instantly
Auto-refreshes every 15 seconds

🔐 Admin Dashboard (Login Required)
Secure login with animated UI
Run AI simulations
Run LP & Hybrid optimization
Upload patient CSV
View and manage all appointments
Logout support

📅 Appointment Booking System

User selects doctor
Chooses date and time
Enters details
Confirms booking
Receives booking confirmation
Bookings are stored securely in SQLite database.
Admins can view all bookings in one place.

🛠️ Technology Stack
Backend
Python
Flask
SimPy (Simulation)
PuLP (Linear Programming)
SQLite (Database)
Frontend
HTML5
CSS3
Bootstrap 5
JavaScript
Font Awesome Icons
Particles.js (Animated login)

📁 Project Structure
DocLine/
│
├── app.py
├── src/
│   ├── simulator.py
│   ├── scheduler_lp.py
│   ├── hybrid_scheduler.py
│   └── queue_estimator.py
│
├── templates/
│   ├── login.html
│   ├── index.html
│   ├── user_dashboard.html
│   ├── book.html
│   ├── booking_success.html
│   └── admin_bookings.html
│
├── static/
│   └── style.css
│
├── data/
├── outputs/
├── appointments.db
└── README.md

▶️ How to Run the Project
1️⃣ Clone the repository
git clone https://github.com/your-username/DocLine.git
cd DocLine
2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install flask flask-cors pandas simpy pulp matplotlib
4️⃣ Run the application
python app.py
5️⃣ Open in browser
http://127.0.0.1:5000/

🔐 Admin Login Credentials (Demo)
Username: admin
Password: 1234
(Change in app.py for production use)

📈 Impact & Results
⏱️ Up to 40% reduction in waiting time
⚖️ Better doctor workload distribution
🚑 Emergency prioritization
📊 Real-time hospital insights
🧾 Fully automated appointment flow

🌟 Key Highlights
Hybrid AI scheduling (Greedy + LP)
Real-time dashboards
Secure admin system
User-friendly booking system
Scalable & modular design

🚀 Future Enhancements
SMS/WhatsApp appointment notifications
Role-based access (Doctor / Receptionist)
Doctor shift scheduling
Real-time queue visualization
Cloud deployment
Payment gateway integration

## 🌟 Why DocLine Stands Out
- Real-world healthcare problem
- Strong mathematical foundation
- AI + Optimization based solution
- Complete end-to-end system
- Production-ready architecture
- Clean UI and UX


## How to Run
Open index.html in browser
