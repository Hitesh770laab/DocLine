# app.py
from flask import Flask, jsonify, request, send_from_directory, render_template, redirect, url_for, session
from flask_cors import CORS
import pandas as pd
import os
import uuid
import threading


# Import your existing backend modules (make sure src is a package or reachable)
# They should be at DocLine/src/
from src.simulator import run_simulation
from src.scheduler_lp import run_batch_scheduler
from src.hybrid_scheduler import run_hybrid_scheduler

def login_required(route_function):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return route_function(*args, **kwargs)
    wrapper.__name__ = route_function.__name__
    return wrapper

UPLOAD_FOLDER = "data"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "docline_secret_2025_admin_key"   # change for production
CORS(app)


# ---------- Utility ----------
def save_uploaded_csv(file_storage):
    filename = f"patients_{uuid.uuid4().hex}.csv"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file_storage.save(path)
    return path


# ---------- Routes (UI) ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # CHANGE THESE FOR REAL SYSTEM USE:
        ADMIN_USER = "Hitesh"
        ADMIN_PASS = "671410705"

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/")
@login_required
def index():
    return render_template("index.html")
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)
#---------user management routes ---------
@app.route("/user")
def user_dashboard():
    return render_template("user_dashboard.html")

#----------log out route ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------- API Endpoints ----------
@app.route("/api/run_greedy", methods=["POST"])
def api_run_greedy():
    """
    Expects JSON:
    { "num_doctors": int, "lam": float, "mu": float, "sim_time": int }
    """
    body = request.get_json() or {}
    num_doctors = int(body.get("num_doctors", 3))
    lam = float(body.get("lam", 1/5))
    mu = float(body.get("mu", 1/12))
    sim_time = int(body.get("sim_time", 480))

    result = run_simulation(num_doctors=num_doctors, lam=lam, mu=mu, sim_time=sim_time)
    return jsonify({"status": "ok", "result": result})


@app.route("/api/run_lp", methods=["POST"])
@login_required
def api_run_lp():
    """
    Accepts multipart/form-data with a CSV file or JSON payload.
    If file uploaded: field name 'file'
    JSON fallback: { "patients": [...], "service_time": {...}, "emergency_flags": {...}, "num_doctors": int, "slots": int }
    """
    # file upload path
    if "file" in request.files:
        f = request.files["file"]
        csv_path = save_uploaded_csv(f)
        df = pd.read_csv(csv_path)
    else:
        body = request.get_json() or {}
        if "patients" in body:
            df = pd.DataFrame({
                "name": body["patients"],
                "service_time": [body.get("service_time", {}).get(p, 10) for p in body["patients"]],
                "emergency_flag": [body.get("emergency_flags", {}).get(p, 0) for p in body["patients"]]
            })
        else:
            return jsonify({"status": "error", "message": "No file or JSON data provided"}), 400

    # Validate
    required = {"name", "service_time", "emergency_flag"}
    if not required.issubset(set(df.columns)):
        return jsonify({"status": "error", "message": f"CSV must contain columns: {required}"}), 400

    patients = df["name"].astype(str).tolist()
    service_time = df.set_index("name")["service_time"].astype(int).to_dict()
    emergency_flags = df.set_index("name")["emergency_flag"].astype(int).to_dict()

    num_doctors = int(request.form.get("num_doctors", request.args.get("num_doctors", 3)))
    slots = int(request.form.get("slots", request.args.get("slots", 8)))
    slots_list = list(range(int(slots)))
    doctors = [f"D{j}" for j in range(1, num_doctors + 1)]

    # Run LP (blocking call) — consider background thread for long jobs
    df_lp = run_batch_scheduler(patients, doctors, slots_list, service_time, emergency_flags)

    out_path = os.path.join(OUTPUT_FOLDER, f"lp_schedule_{uuid.uuid4().hex}.csv")
    df_lp.to_csv(out_path, index=False)

    return jsonify({"status": "ok", "schedule_csv": out_path, "schedule_preview": df_lp.head(10).to_dict(orient="records")})


@app.route("/api/run_hybrid", methods=["POST"])
@login_required
def api_run_hybrid():
    """
    Example POST JSON: {"num_doctors":3, "lam":0.2, "mu":0.083333, "sim_time":480}
    """
    body = request.get_json() or {}
    num_doctors = int(body.get("num_doctors", 3))
    lam = float(body.get("lam", 1/5))
    mu = float(body.get("mu", 1/12))
    sim_time = int(body.get("sim_time", 480))

    result = run_hybrid_scheduler(num_doctors=num_doctors, lam=lam, mu=mu, sim_time=sim_time)
    return jsonify({"status": "ok", "result": result})


# Serve output CSVs
@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
