 
# 🎯 Face Authentication Attendance Management System

A secure and modern attendance management system that uses **face recognition technology** to automatically mark attendance. This project eliminates manual attendance processes and improves accuracy, security, and efficiency.

---

## 🚀 Features

- 🔐 Face Authentication for secure login
- 📸 Real-time face detection using webcam
- 🧠 Face recognition using trained dataset
- 📊 Attendance dashboard with records
- 📅 Automatic attendance marking with date & time
- 📁 CSV-based attendance storage
- 👤 User registration with face capture
- 🌐 Web-based interface using Flask

---

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **OpenCV**
- **NumPy**
- **Face Recognition (LBPH / Haarcascade)**
- **HTML, CSS, JavaScript**
- **Bootstrap (for UI)**

---## 📂 Project Structure

Attendance-management/
│

├── dataset/ # Stored face images (ignored in Git)

├── static/ # CSS, JS, assets

├── templates/ # HTML files

├── camera.py # Camera handling

├── app.py # Main Flask app

├── attendance.csv # Attendance records

├── requirements.txt # Dependencies

└── README.md # Project documentation


---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Nishanth088/Attendance-management.git
Navigate to the project folder:
cd Attendance-management
Install dependencies:
pip install -r requirements.txt
Run the application:
python app.py
Open browser and go to:
http://127.0.0.1:5000/
📸 How It Works
Register a user by capturing face images
System stores face data in dataset
Train the model
Start attendance system
When a face is detected:
It matches with stored data
Marks attendance automatically
📊 Attendance System
Attendance is saved in attendance.csv
Each entry includes:
Name / Roll Number
Date
Time
Dashboard shows attendance summary
🔒 Security Features
Prevents fake attendance using face recognition
Works only for registered users
Real-time verification
🧩 Future Improvements
Add database (MySQL / MongoDB)
Improve UI/UX design
Add face mask detection
Mobile app integration
Cloud deployment
🙋‍♂️ Author

Nishanth Prabhu
GitHub: https://github.com/Nishanth088

⭐ Support

If you like this project, give it a ⭐ on GitHub!


