# college-event-management-system
College Event Management System — Python Django + MySQL
# 🎓 CEMS — College Event Management System

### Student Dashboard (Streamlit App)

CEMS (College Event Management System) is a modern **Streamlit-based student dashboard** that allows students to browse, register, and manage college events. It also provides AI-based event recommendations, certificates, and notifications.

---

## 🚀 Features

* 🔐 Student Login (demo authentication)
* 🏠 Interactive Dashboard
* 🎉 Browse & Register for Events
* 📋 Manage Registrations
* 🏅 Download Certificates
* 🔔 Notification Center
* 👤 Student Profile Management
* 🤖 AI-Based Event Recommendations
* 📊 Student Statistics
* 🎨 Modern Dark UI with Custom CSS

---

## 📁 Project Structure

```
CEMS-Student-Dashboard/
│
├── app.py
├── events.csv
├── my_registrations.csv
├── certificates.csv
├── notifications.csv
└── README.md
```

---

## ⚙️ Requirements

Install dependencies before running the app:

```bash
pip install streamlit pandas
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

The application will open in your browser automatically.

---

## 📊 Data Files

The app uses the following CSV files:

### 1. events.csv

Contains all available events.

Columns:

* id
* title
* category
* date
* time
* venue
* organizer
* description
* registered
* capacity
* emoji
* status

---

### 2. my_registrations.csv

Tracks student registered events.

Columns:

* event_id

---

### 3. certificates.csv

Stores student certificates.

Columns:

* event_title
* prize
* date
* issued_date

---

### 4. notifications.csv

Stores notification history.

Columns:

* message
* time
* type
* trigger
* email_sent
* whatsapp_sent

---

## 🤖 AI Recommendation Logic

The system recommends events based on:

* Student interest tags
* Events not yet registered
* Published event status
* Matching categories

---

## 🎨 UI Components

* Custom dark theme
* Stat cards
* Event cards
* Certificate cards
* Notification list
* Progress bars
* Sidebar navigation

---

## 📌 Pages Overview

### 1. Dashboard

* Quick stats
* AI recommendations
* Recent notifications
* Upcoming events

### 2. Browse Events

* Search events
* Filter by category
* Register for events
* Seat availability indicator

### 3. My Registrations

* Active registrations
* Cancel registrations
* Past events table

### 4. My Certificates

* View certificates
* Download certificate (TXT)

### 5. Notifications

* Email & WhatsApp history
* Filter by type

### 6. Profile

* Update personal info
* Set AI interests
* View statistics

---

## 🔮 Future Enhancements

* Real authentication system
* Admin panel
* Database integration (MySQL/PostgreSQL)
* Email automation
* WhatsApp API integration
* QR code attendance
* PDF certificate generation

---

## 🛠 Built With

* Python
* Streamlit
* Pandas
* Custom CSS

---

## 👨‍💻 Author

**CEMS Student Dashboard Project**

---

## 📄 License

This project is for educational purposes.
