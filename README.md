# 🏆 University Sports Management System

A comprehensive, database-driven web application for managing university sports activities built with **Python (Streamlit)** and **Microsoft SQL Server**.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Database Configuration](#database-configuration)
- [Running the App](#running-the-app)
- [Branch Structure](#branch-structure)
- [Team Members](#team-members)

---

## 📖 About the Project

The University Sports Management System (USMS) is designed to digitize and streamline sports administration at university level. It replaces manual record-keeping with a centralized, interactive platform that manages everything from student registration to tournament analytics.

---

## ✨ Features

| Module | Description |
|---|---|
| 🏠 **Dashboard** | Real-time KPIs, charts, top scorers, recent matches |
| 👨‍🎓 **Students** | Register, search, edit student athletes |
| 🏋️ **Coaches** | Manage coach profiles and sport assignments |
| 👥 **Teams** | Form teams, manage rosters and player positions |
| 🏆 **Tournaments** | Schedule tournaments, register teams, track expenses |
| 🎯 **Matches** | Record match results, scores, and player performances |
| 🏃 **Practice Sessions** | Schedule sessions, mark attendance |
| 🏏 **Equipment** | Track inventory, issue and return equipment |
| 🤕 **Injuries** | Log injuries, monitor recovery status |
| ⭐ **Player Ratings** | Coach ratings with top player analytics |
| 📊 **Points Table** | Live tournament standings |
| 🥇 **Dept Rankings** | Department-wise sports rankings |
| 🔔 **Reminders** | Notifications and announcements |

---

## 🛠 Tech Stack

- **Frontend:** Python, Streamlit, Plotly
- **Backend:** Python (OOP, Repository Pattern)
- **Database:** Microsoft SQL Server (SSMS)
- **Driver:** ODBC Driver 17 for SQL Server
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```
UniSports/
├── database_connection.py    # SQL Server connection (Singleton pattern)
├── backend.py                # Business logic (Repository pattern)
├── frontend.py               # Streamlit UI (all pages)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## ✅ Prerequisites

Before running this project make sure you have:

- Python 3.8 or higher → https://www.python.org/downloads/
- Microsoft SQL Server → https://www.microsoft.com/en-us/sql-server/sql-server-downloads
- SQL Server Management Studio (SSMS) → https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms
- ODBC Driver 17 for SQL Server → https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Git → https://git-scm.com/download/win

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/UniSports.git
cd UniSports
```

### 2. Switch to Develop Branch
```bash
git checkout develop
```

### 3. Create Virtual Environment
```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

### 1. Create the Database
Open SSMS and run:
```sql
CREATE DATABASE UniversitySportsDB;
```

### 2. Find Your Server Name
Run this in SSMS Query Window:
```sql
SELECT @@SERVERNAME;
```

### 3. Update Connection Settings
Open `database_connection.py` and update:
```python
self.server   = 'YOUR_SERVER_NAME'   # e.g. DESKTOP-XXXXX or localhost
self.database = 'UniversitySportsDB'
self.driver   = '{ODBC Driver 17 for SQL Server}'
self.trusted_connection = 'yes'      # Windows Authentication
```

### 4. Test the Connection
Run the app, go to **🔌 DB Connection** page and click **Test Connection**.

---

## ▶️ Running the App

```bash
python -m streamlit run frontend.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 🌿 Branch Structure

| Branch | Purpose |
|---|---|
| `main` | Final stable release |
| `develop` | Integration branch — all files combined |
| `gui` | Frontend UI code (`frontend.py`) |
| `database` | Database and backend code (`database_connection.py`, `backend.py`) |

---

## 👥 Team Members

| Name | Role |
|---|---|
| Taha Nadeem | Database & Backend |
| Waqar Imran | Database Coneection & Frontend |

---

## 📦 Requirements

Contents of "requirements.txt":
```
streamlit
pandas
plotly
pyodbc
```

---

> **Note:** Make sure SQL Server service is running before launching the app.
> You can verify by searching **Services** in Windows Start menu and checking **SQL Server (MSSQLSERVER)** is Running.
