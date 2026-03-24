# Face Identity Verification - Setup Instructions

This project consists of two separate backend servers that power the web interface and the face recognition camera feed. They both need to be running for the application to work completely.

## Prerequisites

1. **Node.js**: You need Node.js installed to run the dashboard interface. (Download at https://nodejs.org/)
2. **Python**: You need Python installed to run the face recognition logic. (Download at https://www.python.org/)
3. **MySQL**: The Node backend connects to a MySQL database named `ftslogin` locally on user `root` with no password.
   - Install **XAMPP** or **WAMP**.
   - Start the **MySQL** module.
   - Open phpMyAdmin (http://localhost/phpmyadmin) and create a database named `ftslogin`.
4. **C++ Build Tools (Python)**: Installing `face_recognition` and `dlib` in Python requires C++ build tools installed via Visual Studio, or using the supplied `dlib-19.24.1-cp311-cp311-win_amd64.whl` wheel file if you are using Python 3.11.

## How to Run

The easiest way to run both servers simultaneously is to double-click the **`run_servers.bat`** script in the root folder.

This script will automatically:
1. Open a terminal and run `npm install` and `node app.js` for the Node server.
2. Open a separate terminal and run `py -m pip install -r requirements.txt` and `py wait.py` for the Flask server.
3. Wait 5 seconds, and then automatically open `http://localhost:3000/dashboard` in your browser.

## Troubleshooting

- **Black Screen / Infinite Loader on Camera Frame**: Make sure the Flask server is running perfectly on port 5000 and your webcam is accessible and not being used by another application.
- **Database Errors**: Verify that your MySQL server is running properly via XAMPP.
- **`dlib` Installation Failure**: If `pip install` fails while installing `dlib`, you must install the Visual Studio C++ build tools, or manually install the wheel file via: `pip install "New folder\dlib-19.24.1-cp311-cp311-win_amd64.whl"` (if using Python 3.11).
