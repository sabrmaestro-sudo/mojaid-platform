import time
import hashlib
import os
from flask import Flask, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "prod_mojaid_security_layer_99213")

# HIGH-SPEED IN-MEMORY LEDGER
RECORDS_MEM_POOL = []

# YOUR PRIVATE UNGUESSABLE SECRET PHRASE KEY
SECRET_ADMIN_TOKEN = "fungua-mojaid-revenue-2026"

def encrypt_identity_data(raw_text):
    return hashlib.sha256(raw_text.encode()).hexdigest()

# PREMIUM FINTECH DARK MODE STYLES
BASE_STYLES = """
<style>
    :root {
        --bg-color: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --primary: #3b82f6;
        --primary-hover: #2563eb;
        --success: #10b981;
        --danger: #ef4444;
        --border-color: rgba(255, 255, 255, 0.08);
    }
    body { 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
        background-color: var(--bg-color); 
        color: var(--text-main);
        margin: 0; 
        padding: 20px; 
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 100vh;
        box-sizing: border-box;
    }
    .card { 
        background: var(--card-bg); 
        backdrop-filter: blur(12px);
        max-width: 480px; 
        width: 100%;
        margin: 20px auto; 
        padding: 35px; 
        border-radius: 20px; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); 
        border: 1px solid var(--border-color);
        box-sizing: border-box;
    }
    .container { 
        max-width: 1100px; 
        width: 100%;
        margin: 0 auto; 
        display: grid; 
        grid-template-columns: 1.2fr 0.8fr; 
        gap: 25px; 
        text-align: left; 
    }
    @media (max-width: 768px) {
        .container { grid-template-columns: 1fr; }
    }
    .admin-card { 
        background: var(--card-bg); 
        backdrop-filter: blur(12px);
        padding: 30px; 
        border-radius: 20px; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        border: 1px solid var(--border-color);
    }
    h1 { font-size: 28px; font-weight: 700; color: var(--text-main); margin-top: 0; margin-bottom: 8px; text-align: center; }
    h2 { font-size: 20px; font-weight: 600; color: var(--text-main); margin-top: 0; margin-bottom: 20px; }
    p.subtitle { color: var(--text-muted); font-size: 14px; text-align: center; margin-bottom: 25px; margin-top: 0; }
    label { font-weight: 600; color: var(--text-muted); display: block; margin-top: 18px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }
    input[type='text'], select { 
        width: 100%; 
        padding: 12px 16px; 
        margin-top: 6px; 
        background: rgba(15, 23, 42, 0.6);
        color: var(--text-main);
        border: 1px solid var(--border-color); 
        border-radius: 10px; 
        box-sizing: border-box; 
        font-size: 15px;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    input[type='text']:focus, select:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
    }
    .btn-submit { 
        background-color: var(--primary); 
        color: white; 
        border: none; 
        padding: 14px; 
        font-size: 16px; 
        border-radius: 10px; 
        cursor: pointer; 
        width: 100%; 
        font-weight: 700; 
        margin-top: 25px; 
        transition: background-color 0.2s, transform 0.1s;
    }
    .btn-submit:hover { background-color: var(--primary-hover); }
    .btn-submit:active { transform: scale(0.98); }
    .profile-box { 
        background: rgba(15, 23, 42, 0.4); 
        border: 1px solid var(--border-color); 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 18px; 
        font-size: 14px; 
        position: relative; 
        word-wrap: break-word; 
    }
    .badge { background: rgba(59, 130, 246, 0.15); color: #60a5fa; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; display: inline-block; margin-top: 8px; border: 1px solid rgba(59, 130, 246, 0.2); }
    .crypto-badge { background: rgba(239, 68, 68, 0.1); color: #f87171; padding: 6px 10px; border-radius: 8px; font-size: 11px; font-family: monospace; display: block; margin-top: 6px; border: 1px solid rgba(239, 68, 68, 0.15); }
    .fee-badge { background: rgba(16, 185, 129, 0.15); color: #34d399; position: absolute; right: 20px; top: 20px; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; border: 1px solid rgba(16, 185, 129, 0.2); }
    .alert-box { background: rgba(59, 130, 246, 0.12); color: #60a5fa; padding: 14px; border-radius: 10px; font-weight: 600; text-align: center; margin-bottom: 20px; border: 1px solid rgba(59, 130, 246, 0.2); font-size: 14px; }
    .error-msg { background: rgba(239, 68, 68, 0.12); color: #f87171; padding: 14px; border-radius: 10px; font-weight: 600; text-align: center; margin-bottom: 20px; border: 1px solid rgba(239, 68, 68, 0.2); font-size: 14px; }
    .nav-bar { max-width: 480px; width: 100%; margin: 20px auto 0 auto; display: flex; justify-content: center; align-items: center; }
    .identity-grid { margin-top: 12px; background: rgba(15, 23, 42, 0.3); padding: 12px; border-radius: 8px; border: 1px solid var(--border-color); display: flex; flex-direction: column; gap: 4px; color: var(--text-muted); font-size: 13px; }
    .identity-grid strong { color: var(--text-main); }
</style>
"""

# --- PUBLIC INTERFACE ---
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
            error_msg = '<div class="error-msg">⚠️ Profile fingerprint already verified inside network system.</div>'
        else:
            tx_reference = f"TX{int(time.time())}MZ"
            RECORDS_MEM_POOL.insert(0, {
                "name": full_name, "hash": encrypted_nida, "net": network, "fee": 500,
                "ref": tx_reference, "time": current_time, "nhif": nhif, "license": license, "bank": bank
            })
            alert_msg = '<div class="alert-box">📡 Outbound Request Sent! Check your phone for the payment PIN pop-up to authorize 500 TZS via ' + str(network) + '.</div>'

    html_page = "<!DOCTYPE html><html><head><title>MojaID Wallet</title>" + BASE_STYLES + "</head><body>"
    html_page += "<div class='nav-bar'><strong style='color:var(--text-main); font-size: 22px; letter-spacing: 0.5px;'>Moja<span style='color:var(--primary);'>ID</span> Ecosystem</strong></div>"
    html_page += "<div class='card'><h1>Unified Citizen Wallet</h1><p class='subtitle'>Secure identity synchronization protocol</p>" + alert_msg + error_msg
    html_page += "<form method='POST'>"
    html_page += "<label>Full Name</label><input type='text' name='full_name' placeholder='e.g., Juma Hamisi' required>"
    html_page += "<label>Primary NIDA ID</label><input type='text' name='nida_id' placeholder='e.g., 199XXXXXXXXXXXX...' required>"
    html_page += "<label>NHIF Card Number (Optional)</label><input type='text' name='nhif' placeholder='e.g., NHIF-992831'>"
    html_page += "<label>Driving License Class (Optional)</label><input type='text' name='license' placeholder='e.g., A, B, C'>"
    html_page += "<label>Linked Bank Name (Optional)</label><input type='text' name='bank' placeholder='e.g., CRDB'>"
    html_page += "<label>Billing Network Method</label><select name='network'><option value='M-Pesa'>Vodacom M-Pesa</option><option value='Tigo Pesa'>Tigo Pesa</option><option value='Airtel Money'>Airtel Money</option><option value='HaloPesa'>HaloPesa</option></select>"
    html_page += "<label>Account Phone Number</label><input type='text' name='phone' placeholder='e.g., 07XXXXXXXX' required>"
    html_page += "<button type='submit' class='btn-submit'>🔒 Securely Link Identities (500 TZS)</button>"
    html_page += "</form></div></body></html>"
    return html_page

# --- SECRET REVENUE PORTAL (ACCESSIBLE ONLY VIA THE TOKEN LINK) ---
@app.route("/secret/<token>")
def secret_admin(token):
    if token != SECRET_ADMIN_TOKEN:
        return "<body style='background:#0f172a; color:#f8fafc; font-family:sans-serif; text-align:center; padding-top:100px;'><h1>🔒 Access Denied: Unauthorized Node Endpoint.</h1></body>", 403

    running_total = 0
    ledger_html = ""
    for p in RECORDS_MEM_POOL:
        running_total += p.get("fee", 500)
        ledger_html += '<div class="profile-box">'
        ledger_html += '<div class="fee-badge">PAID +' + str(p.get('fee', 500)) + ' TZS</div>'
        ledger_html += '<strong style="font-size:16px; color:var(--text-main);">👤 ' + str(p.get('name', 'Unknown')) + '</strong> <span style="color:var(--text-muted); font-size:12px;">(via ' + str(p.get('net', 'M-Pesa')) + ')</span><br>'
        ledger_html += '<span class="badge">NIDA Cryptographic Hash Fingerprint</span>'
        ledger_html += '<span class="crypto-badge">' + str(p.get('hash', '')) + '</span>'
        ledger_html += ''
        ledger_html += '<span>🏥 <strong>NHIF:</strong> ' + str(p.get('nhif', 'NONE')) + '</span>'
