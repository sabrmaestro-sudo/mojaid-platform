import time
import hashlib
import os
import io
import base64
import qrcode
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

SECRET_ADMIN_TOKEN = "fungua-mojaid-revenue-2026"
B2B_API_TOKEN = "mojaid_live_b2b_token_xyz789"

B2B_PARTNER_WALLETS = {
    "mojaid_live_b2b_token_xyz789": {
        "institution_name": "Muhimbili National Hospital Node",
        "balance": 5000
    }
}

B2B_VERIFICATION_REVENUE = 0

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
            alert_msg = f"📡 Pipeline verified over {network} gateway. Encryption matrix token generated."
            
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

@app.route("/api/v1/verify", methods=["GET"])
def b2b_verify_api():
    global B2B_VERIFICATION_REVENUE
    client_auth_token = request.headers.get("X-MojaID-Auth") or request.args.get("auth_token")
    if client_auth_token not in B2B_PARTNER_WALLETS:
        return jsonify({"status": "ERROR", "message": "Authentication Failed: Invalid API Token"}), 401
        
    partner = B2B_PARTNER_WALLETS[client_auth_token]
    VERIFICATION_COST = 500
    if partner["balance"] < VERIFICATION_COST:
        return jsonify({"status": "BILLING_ERROR", "message": "Insufficient balance."}), 402
        
    scanned_hash = request.args.get("qr_hash")
    for profile in RECORDS_MEM_POOL:
        if profile["hash"] == scanned_hash:
            partner["balance"] -= VERIFICATION_COST
            B2B_VERIFICATION_REVENUE += VERIFICATION_COST
            return jsonify({
                "status": "SUCCESS", "verified": True,
                "billing": {"charge": VERIFICATION_COST, "remaining_balance": partner["balance"], "institution": partner["institution_name"]},
                "data": {"full_name": profile["name"], "nhif_status": profile["nhif"], "license_class": profile["license"], "banking_institution": profile["bank"], "account_status": profile["status"]}
            }), 200
    return jsonify({"status": "SUCCESS", "verified": False}), 404

@app.route("/secret/<token>")
def secret_admin(token):
    if token != SECRET_ADMIN_TOKEN:
        return "🔒 Access Denied", 403
    customer_registration_fees = sum(p.get("fee", 500) for p in RECORDS_MEM_POOL)
    combined_net_worth = customer_registration_fees + B2B_VERIFICATION_REVENUE
    return render_template("admin.html", saved_profiles=RECORDS_MEM_POOL, total_count=len(RECORDS_MEM_POOL), total_revenue=combined_net_worth)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
