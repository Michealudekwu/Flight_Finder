# ✈️ Flight Comparison Web App

A real-time **Flight Comparison Web Application** built with **Python (Flask)** and the **Amadeus API**, designed to help users automatically find and compare flight deals efficiently.  
This upgraded version includes a **SQLite database** for user authentication, **hashed passwords** for security, and a **live deployment** for easy access.

---

## 🚀 Features

- 🔍 **Real-Time Flight Search** — Fetches live flight data using the Amadeus API.  
- 👤 **User Authentication** — Secure sign-up and login functionality.  
- 🔒 **Password Security** — Implements PBKDF2-SHA256 hashing for strong password protection.  
- 🗄️ **Database Integration** — Uses SQLite for managing user data and authentication records.  
- 🌐 **Deployed Application** — Fully deployed for public access (link below).  
- ⚡ **Performance Optimized** — Reduced manual flight search time by over 80%.  

---

## 🧠 What I Learned

- Integrating REST APIs with Flask  
- Building and connecting a backend database (SQLite)  
- Implementing secure authentication systems  
- Managing environment variables using `python-dotenv`  
- Deploying and maintaining a live web application  

---

## 🛠️ Tech Stack

| Category | Technologies |
|-----------|---------------|
| **Backend** | Python, Flask |
| **Frontend** | HTML, CSS |
| **Database** | SQLite |
| **API** | Amadeus API |
| **Security** | PBKDF2-SHA256 password hashing |
| **Environment** | python-dotenv |

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Michealudekwu/flight-comparison-app.git
   cd flight-comparison-app
   
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   
   venv\Scripts\activate

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt

4.  **Set up environment vaiables**
    ```bash
     API_KEY=your_amadeus_api_key
     API_SECRET=your_amadeus_api_secret

5. **Run the application**
   ```bash
   flask run

6. **Access the app**
   Visit http://127.0.0.1:5000 in your browser.


🌍 Live Demo

🔗 Deployed App: https://flight-finder-2-0.onrender.com

🧩 Future Improvements

Add flight alert notifications (email or SMS)

Implement user flight history and favorites

Add advanced filtering (e.g., price range, layovers)

Integrate booking redirection for selected flights
