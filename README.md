# TradeNimbus

Real-time stock price tracker built with Django, Celery, Channels, Redis, WebSockets, and yfinance.

---

## 🚀 Features

- Select multiple NIFTY50 stock tickers to track.
- Real-time price updates via WebSockets using Django Channels.
- Background price fetching using Celery workers.
- REST-like structure without login or signup.
- Simple, responsive UI with Bootstrap 5.

---

## 📦 Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Setup – Step by Step](#setup—step-by-step)  
3. [Run the App](#run-the-app)  
4. [Redis, Celery & Channels Setup](#redis-celery--channels-setup)  
5. [Assumptions](#assumptions)  
6. [Notes & Troubleshooting](#notes--troubleshooting)

---

## 🧩 Prerequisites

- Python 3.10+  
- `pip` (Python package installer)  
- `git` (for cloning the repo)  
- Redis server (for Channels layer & Celery broker)

---

## 🔧 Setup — Step by Step

1. **Clone the repository**

   ```bash
   git clone https://github.com/Lucifer-Stone/TradeNimbus.git
   cd TradeNimbus
   
2. **Create a virtual environment**
python -m venv venv

3. **Activate the environment**
- Windows
  ```
  venv\Scripts\activate
  ```
- macOS / Linux
  ```
  source venv/bin/activate
  ```
 4. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```
 5. **Install Redis**
    Windows: Use Redis on Windows.
    macOS: brew install redis
    Linux: sudo apt install redis-server

 6. **Apply database migrations**
    ```
    python manage.py migrate
    ```
    
▶️ Run the App
Open three separate terminals:

  1. Django development server
     ```
     python manage.py runserver
     ```
  2. Celery worker
     ```
     celery -A tradenimbus worker --loglevel=info
     ```
  3. Celery beat scheduler
     ```
     celery -A tradenimbus beat --loglevel=info
     ```
     
🕸️ **Redis, Celery & Channels Setup**

- Redis acts as a broker (Celery) and channel layer (Channels).
- Celery fetches real-time stock info via yfinance.
- Django Channels + ASGI push updates over WebSockets to clients.

📝 **Assumptions Made**

- Stock tickers are restricted to NIFTY50, validated via yfinance.
- No user authentication—session-managed by query string.
- WebSocket routing expects a room_name (like track) for grouping requests.
- All data is stored in-memory; no persistent database storage for stock prices.
- Styling uses Bootstrap 5, focusing on responsiveness over design polish.

⚠️ **Notes & Troubleshooting**

If Celery raises SerializerNotInstalled: No encoder/decoder installed for 'a', add to your settings.py:

If yfinance errors with websockets.sync, install or upgrade:
```
pip install --upgrade websockets
```

🔄 **How It Works (Architecture)**

- User selects stocks via a Django form.
- Form submits AJAX + reload, triggering Celery fetch tasks.
- Celery requests prices using yfinance, pushes result via Channels layer.
- WebSocket broadcasts JSON updates to active clients.
- Frontend JS updates the HTML DOM dynamically.
- Color-coded row updates (green/red) indicate real-time movement.
