current_status = "Idle"
current_otp = None
print("### BACKEND STARTED ###")
from flask import Flask, request, jsonify
from flask_cors import CORS

from blockchain import add_block
from otp import generate_otp, verify_otp
from policy import policy_decision

app = Flask(__name__)
CORS(app)   # allows frontend (Live Server) to talk to backend

current_otp = None


@app.route("/login", methods=["POST"])
def login():
    global current_status
    data = request.json

    if data["username"] == "user" and data["password"] == "1234":
        current_status = "User Authenticated"
        add_block("User authenticated")
        return jsonify({"status": "success"})
    
    current_status = "Login Failed"
    add_block("User failed login")
    return jsonify({"status": "fail"})


@app.route("/request-data", methods=["POST"])
def request_data():
    global current_status
    current_status = "Access Requested by User"
    add_block("User requested data")
    return jsonify({"message": "Request sent to admin"})


@app.route("/approve", methods=["POST"])
def approve():
    global current_status, current_otp
    current_otp = generate_otp()
    current_status = "Admin Approved – OTP Generated"
    add_block("Admin approved request")
    return jsonify({"otp": current_otp})



@app.route("/verify-otp", methods=["POST"])
def verify():
    global current_status
    data = request.json

    if data["otp"] == current_otp:
        current_status = "Access Granted"
        add_block("OTP verified – Access granted")
        return jsonify({"access": "GRANTED"})
    
    current_status = "OTP Failed"
    add_block("OTP verification failed")
    return jsonify({"access": "DENIED"})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": current_status})



if __name__ == "__main__":
    print("### BACKEND STARTED ###")
    app.run(host="0.0.0.0", port=5000, debug=True)

@app.route("/", methods=["GET"])
def health():
    return {
        "service": "Zero Trust Blockchain Backend",
        "status": "Running"
    }, 200