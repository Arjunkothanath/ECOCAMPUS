# ♻️ CampusEcoTrack — Smart Waste Management System

A modern web-based waste management platform designed for educational campuses. It streamlines bin monitoring, feedback handling, staff coordination, and scheduled waste collection — with role-based access and clean UI.

![CampusEcoTrack](https://img.shields.io/badge/Django-4.x-green.svg) ![Status](https://img.shields.io/badge/status-Completed-brightgreen.svg)

---

## 🚀 Features

🔐 **Role-Based Login System**
- Admin, Corporate, Head Staff, Staff, Student

🗑 **Bin Management**
- Add/Edit/Delete bins with location, category, and fill level
- Corporate collects full bins and schedules collection

🗣 **Feedback System**
- Alerts, Suggestions & Complaints
- Smart status tracking (Pending, Resolved, Read/Unread)

📅 **Smart Scheduling**
- Corporate sets monthly collection dates
- Auto-reschedule logic for missed collections

📬 **Email Notification**
- Admin → Corporate on “Bin Full” status

📊 **Dashboard Overviews**
- Modern dashboards for all roles
- Clean stat cards, actions, and links

---

## 🛠 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3 (Red-Black-White Theme)
- **Database:** SQLite (default)
- **Authentication:** Django’s built-in system
- **Email:** Gmail SMTP with App Passwords

---

## 🧑‍💻 User Roles

| Role        | Access |
|-------------|--------|
| 🛠 **Admin** | Manage users, bins, see all feedback, mark bin full |
| 🧑‍💼 **Corporate** | View & collect bins, schedule collection, see feedback |
| 👨‍💼 **Head Staff** | Add/manage staff, view user feedback, submit feedback |
| 🧑‍🔧 **Staff** | Submit alerts/suggestions, view student feedback |
| 🎓 **Student** | Submit feedback, track feedback status |

---

## 📂 Folder Structure
campusecotrack/
├── admins/
├── corporate/
├── users/
├── general/
├── templates/
│ └── [dashboard.html, feedbacks.html, ...]
├── static/
│ └── [admin.css, dashboard.css, feedback.css, ...]
├── manage.py
└── README.md


---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/campusecotrack.git
cd campusecotrack

# 2. Create virtual environment
python -m venv eco
source eco/bin/activate  # On Windows: eco\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up database
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver

