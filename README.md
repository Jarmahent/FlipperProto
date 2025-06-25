# Motorcycle Parts Resale Platform

## 🚀 Summary
This project is part of a business venture to purchase salvaged motorcycles, dismantle them, and sell their parts across multiple online platforms. By integrating auctions, structured disassembly, smart inventory tracking, and dynamic platform support (eBay, Facebook, etc.), the system aims to maximize part resale profit and streamline operations.

Built using FastAPI and SQLAlchemy with a modular design to support expansion into multiple sales channels.

## 📦 Features
- Track motorcycle purchases and parts inventory
- Estimate resale value per part
- Calculate ROI by vehicle and platform
- Cross-list parts across eBay, Facebook, Shopify, and more
- Custom barcode and locker/bin labeling support
- Dashboard for part status, profit, and sales insights

## 🛠 Tech Stack
- Python 3.11 (via `pyenv`)
- FastAPI + SQLAlchemy 2.0
- SQLite (dev) / MariaDB (prod-ready)
- Pydantic v2
- Celery + Redis (for background syncing)
- eBay SDK (with pluggable interface for others)

## 📥 Setup Instructions

### 1. Install Python with `pyenv`
```bash
pyenv install 3.11.9
pyenv local 3.11.9
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize database (SQLite for dev)
```bash
sqlite3 ./dev.db < sqlite_schema.sql
```

### 5. Run the app
```bash
uvicorn app.main:app --reload
```

## ⚙️ Project Structure (Initial)
```
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic v2 schemas
│   ├── ebay_client.py   # eBay integration
│   └── ...              # Future marketplace clients
├── dev.db               # SQLite database (development)
├── requirements.txt     # Dependencies
├── sqlite_schema.sql    # DB schema
└── README.md            # You are here
```

## 🔜 Coming Soon
- Marketplace webhook syncing
- Admin UI
- Auto-pricing tools based on eBay sold data
- Locker label printing and QR part lookup

---

_Developed by Kevin Hernandez – Fullstack Python Engineer & Founder_
