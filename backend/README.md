# FlowChart Backend (Python/Flask)

This directory contains a minimal Flask backend that provides RESTful APIs to **store and retrieve flow-chart data** in an SQLite database.

## 1. Quick start

```bash
# 1) (Recommended) create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the development server (port 5000)
python backend/app.py
```

The API will be available at `http://localhost:5000/api/*`.  
The Vue front-end (served by Vite on port 5173) can freely call the API thanks to CORS.

## 2. Available endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/api/charts` | List all saved flow charts (metadata only). |
| POST | `/api/charts` | Create a new chart. Body → `{ "name": "My chart", "data": { ... } }` |
| GET | `/api/charts/<id>` | Retrieve full chart payload. |
| PUT | `/api/charts/<id>` | Update existing chart. Body identical to POST. |
| DELETE | `/api/charts/<id>` | Delete a chart. |

## 3. Project structure

```
backend/
  ├── app.py        # Flask application & routes
  ├── flowcharts.db # SQLite database (auto-created on first run)
  └── README.md     # (this file)
requirements.txt    # Python dependencies
```

SQLite is used for maximum portability—no external DB server required.

## 4. Next steps

* Integrate the Vue components with these endpoints (e.g. `fetch` or `axios`).
* Containerise the backend (optional) with Docker & gunicorn for production.

---

### Learning resources

If you are new to Python & Flask:

1. **Flask official tutorial** – https://flask.palletsprojects.com/en/latest/quickstart/
2. **sqlite3 module docs** – https://docs.python.org/3/library/sqlite3.html
3. **Real-Python: Flask by Example** – https://realpython.com/flask-by-example/ 