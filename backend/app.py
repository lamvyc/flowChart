# --------------------------------------------------
# 导入所需的 Python 模块
# --------------------------------------------------
# Flask        : Web 框架，类似前端的 Express / Koa
# Flask_CORS   : 解决跨域，让前端 5173 端口可以访问后端 5000
# sqlite3      : Python 内置数据库驱动，零依赖
# datetime     : 获取当前时间，记录到数据库
# os & json    : 文件路径处理 + JSON 序列化/反序列化
# 语法：
#from ... import ...：导入模块中的某些变量/函数（类似前端的 import { useState } from 'react'）
#
#import xxx：导入整个模块
# --------------------------------------------------
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import json

# --------------------------------------------------
# 数据库文件路径（首运行自动创建 flowcharts.db）
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/ 目录
DATABASE = os.path.join(BASE_DIR, "flowcharts.db")

app = Flask(__name__)
# Enable CORS so that the Vue front-end (running on another port) can access the API
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --------------------------------------------------
# Helper functions for DB access
# --------------------------------------------------

def get_db():
    """（每个请求）懒加载 SQLite 连接，保证同一次请求公用一个连接"""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Access columns by name
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """请求结束后自动关闭数据库连接，避免资源泄漏"""
    db = g.pop("db", None)
    if db is not None:
        db.close()


# --------------------------------------------------
# DB schema initialisation
# --------------------------------------------------

def init_db():
    """初始化数据库表结构（如果不存在就创建）"""
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS charts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )
        """
    )
    db.commit()


# --------------------------------------------------
# Application startup
# --------------------------------------------------

# In Flask 3.x, the 'before_first_request' hook has been removed.
# We'll initialise the database right after creating the app instead.

with app.app_context():
    init_db()


# --------------------------------------------------
# API endpoints
# --------------------------------------------------


@app.route("/api/charts", methods=["GET"])
def list_charts():
    """列出所有流程图（只返回 id、name、created_at）"""
    db = get_db()
    rows = db.execute("SELECT id, name, created_at FROM charts ORDER BY id DESC").fetchall()
    charts = [dict(row) for row in rows]
    return jsonify(charts)


@app.route("/api/charts/<int:chart_id>", methods=["GET"])
def get_chart(chart_id):
    """根据 id 获取完整的流程图数据"""
    db = get_db()
    row = db.execute("SELECT * FROM charts WHERE id = ?", (chart_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Chart not found"}), 404
    chart = dict(row)
    # JSON decode the stored 'data' field before sending it back
    chart["data"] = json.loads(chart["data"])
    return jsonify(chart)


@app.route("/api/charts", methods=["POST"])
def create_chart():
    """创建新的流程图，Body = {name, data}。data 可为任意 JSON"""
    payload = request.get_json(force=True)
    name = payload.get("name")
    data = payload.get("data")  # Can be arbitrary JSON serialisable structure

    if not name or data is None:
        return jsonify({"error": "Missing 'name' or 'data' in request body"}), 400

    db = get_db()
    db.execute(
        "INSERT INTO charts (name, data, created_at) VALUES (?, ?, ?)",
        (name, json.dumps(data), datetime.utcnow().isoformat()),
    )
    db.commit()
    chart_id = db.execute("SELECT last_insert_rowid() as id").fetchone()["id"]
    return jsonify({"id": chart_id}), 201


@app.route("/api/charts/<int:chart_id>", methods=["PUT"])
def update_chart(chart_id):
    """更新已有流程图（根据 id 覆盖 name / data）"""
    payload = request.get_json(force=True)
    name = payload.get("name")
    data = payload.get("data")

    if data is None:
        return jsonify({"error": "Missing 'data' in request body"}), 400

    db = get_db()
    db.execute(
        "UPDATE charts SET name = ?, data = ? WHERE id = ?",
        (name, json.dumps(data), chart_id),
    )
    db.commit()
    return jsonify({"status": "updated"})


@app.route("/api/charts/<int:chart_id>", methods=["DELETE"])
def delete_chart(chart_id):
    """根据 id 删除流程图"""
    db = get_db()
    db.execute("DELETE FROM charts WHERE id = ?", (chart_id,))
    db.commit()
    return jsonify({"status": "deleted"})


# --------------------------------------------------
# Entry point
# --------------------------------------------------

if __name__ == "__main__":
    # 本地开发直接运行；线上推荐用 gunicorn / uwsgi 等
    app.run(debug=True, host="0.0.0.0", port=5000) 