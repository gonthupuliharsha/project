from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
import uuid
import os
from flask_mail import Mail, Message

from services.analyzer import analyze_location
from services.demand_service import demand_score
from services.clustering import get_cluster_data
from services.recommendation_service import generate_recommendation_zones

app = Flask(__name__)
CORS(app)

# -----------------------------
# PATH FIX (IMPORTANT)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "../dataset")

# -----------------------------
# MAIL CONFIGURATION
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rupasribadagala@gmail.com'
app.config['MAIL_PASSWORD'] = 'tmamzrhwooelsojl'

mail = Mail(app)

# -----------------------------
# LOAD FACILITIES DATASET
# -----------------------------
facilities_file = os.path.join(DATASET_PATH, "facilities.csv")
facilities_df = pd.read_csv(facilities_file)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# CREATE USERS TABLE
# -----------------------------
def create_table():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        reset_token TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return "Backend Server Running Successfully"


# -----------------------------
# SIGNUP API
# -----------------------------
@app.route("/signup", methods=["POST"])
def signup():

    data_input = request.get_json()

    name = data_input.get("name")
    email = data_input.get("email")
    password = data_input.get("password")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if user:
        conn.close()
        return jsonify({"message": "Email already exists"})

    cursor.execute(
        "INSERT INTO users(name,email,password) VALUES(?,?,?)",
        (name, email, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful"})


# -----------------------------
# LOGIN API
# -----------------------------
@app.route("/login", methods=["POST"])
def login():

    data_input = request.get_json()

    email = data_input.get("email")
    password = data_input.get("password")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"})


# -----------------------------
# FORGOT PASSWORD API
# -----------------------------
@app.route("/forgot_password", methods=["POST"])
def forgot_password():

    data_input = request.get_json()
    email = data_input.get("email")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "Email not registered"})

    token = str(uuid.uuid4())

    cursor.execute(
        "UPDATE users SET reset_token=? WHERE email=?",
        (token, email)
    )

    conn.commit()
    conn.close()

    reset_link = f"http://127.0.0.1:5500/reset_password.html?token={token}"

    try:

        msg = Message(
            "Password Reset Link",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )

        msg.body = f"""
Hello,

Click the link below to reset your password:

{reset_link}

If you did not request this, please ignore this email.
"""

        mail.send(msg)

        return jsonify({"message": "Reset link sent to your email"})

    except Exception as e:
        return jsonify({
            "message": "Failed to send email",
            "error": str(e)
        })


# -----------------------------
# RESET PASSWORD API
# -----------------------------
@app.route("/reset_password", methods=["POST"])
def reset_password():

    data_input = request.get_json()

    token = data_input.get("token")
    new_password = data_input.get("password")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE reset_token=?",
        (token,)
    )

    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({"message": "Invalid or expired token"})

    cursor.execute(
        "UPDATE users SET password=?, reset_token=NULL WHERE reset_token=?",
        (new_password, token)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Password reset successful"})


# -----------------------------
# FACILITIES DATA FOR MAP
# -----------------------------
@app.route("/facilities", methods=["GET"])
def facilities():

    result = facilities_df.to_dict(orient="records")
    return jsonify(result)


# -----------------------------
# LOCATION ANALYSIS API
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        print("Incoming:", data)

        lat = float(data["latitude"])
        lon = float(data["longitude"])
        facility = data["facility"]

        result = analyze_location(lat, lon, facility)

        print("Result:", result)

        return jsonify(result)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})


# -----------------------------
# DEMAND PREDICTION API
# -----------------------------
@app.route("/predict_demand", methods=["POST"])
def predict_demand():

    try:

        data_input = request.get_json()

        lat = float(data_input.get("latitude"))
        lon = float(data_input.get("longitude"))
        facility = data_input.get("facility")

        score = demand_score(lat, lon, facility)

        return jsonify({
            "facility": facility,
            "demand_score": score
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# -----------------------------
# HEATMAP DATA API
# -----------------------------
@app.route("/heatmap_data", methods=["GET"])
def heatmap_data():

    population_file = os.path.join(DATASET_PATH, "population.csv")
    population_df = pd.read_csv(population_file)

    result = []

    for _, row in population_df.iterrows():

        result.append({
            "lat": row["latitude"],
            "lon": row["longitude"],
            "weight": row["population"]
        })

    return jsonify(result)


# -----------------------------
# CLUSTER DATA API
# -----------------------------
@app.route("/clusters", methods=["GET"])
def clusters():

    data = get_cluster_data()

    return jsonify(data.to_dict(orient="records"))


# -----------------------------
# RECOMMENDATION ZONES API
# -----------------------------
@app.route("/recommendation_zones", methods=["GET"])
def recommendation_zones():

    print("API HIT 🔥")

    facility = request.args.get("facility", "hospital")
    print("Facility received:", facility)   # 👈 ADD THIS

    zones = generate_recommendation_zones(facility)

    print("Zones count:", len(zones))       # 👈 ADD THIS

    return jsonify(zones)



# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)