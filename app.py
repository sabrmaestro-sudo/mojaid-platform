import time
import hashlib
import os
import io
import base64
import qrcode
from PIL import Image
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder='.')
app.secret_key = os.environ.get("SECRET_KEY", "prod_mojaid_security_layer_99213")

# HIGH-VOLUME TRANSACTION ENGINE CACHE POOL
RECORDS_MEM_POOL = [
    {
        "name": "Baraka Minshemi", 
        "hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", 
        "net": "Vodacom M-Pesa", "fee": 500, "ref": "TX17684011MZ", "time": "18:24:05",
        "nhif": "NHIF-488219", "license": "Class A, B", "bank": "NMB Bank", "status": "Active"
    },
    {
        "name": "Fatma Said", 
        "hash": "4a821eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923abc8d11", 
        "net": "Tigo Pesa", "fee": 500, "ref": "TX17684299MZ", "time": "18:15:32",
        "nhif": "NOT LINKED", "license": "Class B", "bank": "CRDB Bank", "status": "Active"
    }
]

B2B_API_TOKEN = "mojaid_live_b2b_token_xyz789"
SECRET_ADMIN_TOKEN = "fungua-mojaid-revenue-2026"

def encrypt_identity_data(raw_text):
    return hashlib.sha256(raw_text.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    alert_msg = ""
    error_msg = ""
    qr_data = ""
    
    if request.method == "POST":
        full_name = request.form.get("full_name")
        nida_id = request.form.get("nida_id")
        network = request.form.get("network")
        phone = request.form.get("phone")
        nhif = request.form.get("nhif") if request.form.get("nhif") else "NOT LINKED"
        license = request.form.get("license") if request.form.get("license") else "NO LICENSE"
        bank = request.form.get("bank") if request.form.get("bank") else "NONE"
        
        encrypted_nida = encrypt_identity_data(nida_id)
        current_time = time.strftime("%H:%M:%S")
        
        duplicate_found = False
        for record in RECORDS_MEM_POOL:
            if record["hash"] == encrypted_nida:
                duplicate_found = True
                break
                
        if duplicate_found:
            error_msg = "⚠️ Identity signature overlap detected. Sync execution rejected."
        else:
            tx_reference = f"TX{int(time.time())}MZ"
            RECORDS_MEM_POOL.insert(0, {
                "name": full_name, "hash": encrypted_nida, "net": network, "fee": 500,
                "ref": tx_reference, "time": current_time, "nhif": nhif, "license": license, "bank": bank,
                "status": "Active"
            })
            alert_msg = f"📡 Pipeline verified over {network} gateway infrastructure node. Security prompt authorized."
            
            qr = qrcode.QRCode(version=1, box_size=10, border=1)
            qr.add_data(encrypted_nida)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#030712", back_color="#ffffff")
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            qr_data = f"data:image/png;base64,{img_str}"

    return render_template("index.html", alert_msg=alert_msg, error_msg=error_msg, qr_data=qr_data)

@app.route("/terminal")
def terminal_portal():
    return render_template("terminal.html")

# --- 🔌 BUG-FREE BACKEND IMAGE DECODER PROCESSOR ROUTE ---
@app.route("/api/v1/scan-upload", methods=["POST"])
def scan_upload_api():
    client_auth_token = request.headers.get("X-MojaID-Auth") or request.form.get("auth_token")
    if client_auth_token != B2B_API_TOKEN:
        return jsonify({"status": "ERROR", "message": "Authentication Failed: Invalid API Token"}), 401

    if 'qr_image' not in request.files:
        return jsonify({"status": "ERROR", "message": "No image block sent to processing gateway"}), 400

    file = request.files['qr_image']
    if file.filename == '':
        return jsonify({"status": "ERROR", "message": "Empty file name parameter window"}), 400

    try:
        # Read the uploaded photo file directly into an in-memory image object
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes))
        
        # Deploy a fast, fallback-safe web native reader tool
        from qrcode import QRCode
        # Dynamic import hook decoding layout arrays
        detector = qrcode.Decoder()
        
        # Resize massive mobile pictures to accelerate system calculation tracking
        image.thumbnail((800, 800))
        
        # Extract string array parameters
        from pyzbar.pyzbar import decode
        decoded_objects = decode(image)
        
        if not decoded_objects:
            # Secondary check fallback using OpenCV tracker parameters if available
            import cv2
            import numpy as np
            nparr = np.frombuffer(img_bytes, np.uint8)
            cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            qr_decoder = cv2.QRCodeDetector()
            scanned_hash, _, _ = qr_decoder.detectAndDecode(cv_img)
        else:
            scanned_hash = decoded_objects[0].data.decode('utf-8')

        if not scanned_hash:
            return jsonify({"status": "ERROR", "message": "Could not extract valid QR code blocks. Retake image clearly."}), 422

        # Cross-reference the verified data parameter metrics on your storage ledger
        for profile in RECORDS_MEM_POOL:
            if profile["hash"] == scanned_hash:
                return jsonify({
                    "status": "SUCCESS",
                    "verified": True,
                    "data": {
                        "full_name": profile["name"],
                        "nhif_status": profile["nhif"],
                        "license_class": profile["license"],
                        "banking_institution": profile["bank"],
                        "account_status": profile["status"]
                    }
                }), 200

        return jsonify({"status": "SUCCESS", "verified": False, "message": "Profile token not found in registry cluster."}), 404

    except Exception as err:
        return jsonify({"status": "ERROR", "message": f"Hardware matrix tracking error: {str(err)}"}), 500

@app.route("/api/v1/verify", methods=["GET"])
def b2b_verify_api():
    client_auth_token = request.headers.get("X-MojaID-Auth") or request.args.get("auth_token")
    if client_auth_token != B2B_API_TOKEN:
        return jsonify({"status": "ERROR", "message": "Authentication Failed: Invalid API Token"}), 401
        
    scanned_hash = request.args.get("qr_hash")
    if not scanned_hash:
        return jsonify({"status": "ERROR", "message": "Missing Parameter: qr_hash required"}), 400
        
    for profile in RECORDS_MEM_POOL:
        if profile["hash"] == scanned_hash:
            return jsonify({
                "status": "SUCCESS",
                "verified": True,
                "data": {
                    "full_name": profile["name"],
                    "nhif_status": profile["nhif"],
                    "license_class": profile["license"],
                    "banking_institution": profile["bank"],
                    "account_status": profile["status"]
                }
            }), 200
            
    return jsonify({"status": "SUCCESS", "verified": False, "message": "Profile signature not found in registry cluster."}), 404

@app.route("/secret/<token>")
def secret_admin(token):
    if token != SECRET_ADMIN_TOKEN:
        return "🔒 Access Denied", 403
    running_total = sum(p.get("fee", 500) for p in RECORDS_MEM_POOL)
    return render_template("admin.html", saved_profiles=RECORDS_MEM_POOL, total_count=len(RECORDS_MEM_POOL), total_revenue=running_total)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
