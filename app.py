import time
import hashlib
import os
from flask import Flask, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mojaid_super_secret_key_123")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("MojaID2026!#".encode()).hexdigest()

# MEMORY REVENUE TRACKING POOL
RECORDS_MEM_POOL = []

def encrypt_identity_data(raw_text):
    return hashlib.sha256(raw_text.encode()).hexdigest()

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
        
        encrypted_nida = encrypt_identity_data(nida_id)
        current_time = time.strftime("%H:%M:%S")
        
        duplicate_found = False
        for record in RECORDS_MEM_POOL:
            if record["hash"] == encrypted_nida:
                duplicate_found = True
                break
                
        if duplicate_found:
            error_msg = '<p style="color:red;font-weight:bold;text-align:center;">⚠️ Security Intercept: Fingerprint matches existing row.</p>'
        else:
            tx_reference = f"TX{int(time.time())}MZ"
            RECORDS_MEM_POOL.insert(0, {
                "name": full_name,
                "hash": encrypted_nida,
                "net": network,
                "fee": 300,
                "ref": tx_reference,
                "time": current_time
            })
            alert_msg = f'<p style="color:#0369a1;background:#e0f2fe;padding:12px;border-radius:8px;font-weight:bold;text-align:center;">🔔 Payment Cleared via {network}! Ref: {tx_reference}</p>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MojaID Wallet</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; text-align: center; }}
            .card {{ background: white; max-width: 450px; margin: 40px auto; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 8px solid #1e3a8a; text-align: left; }}
            h1 {{ color: #1e3a8a; margin-bottom: 5px; text-align: center; }}
            label {{ font-weight: bold; color: #333; display: block; margin-top: 15px; font-size: 14px; }}
            input[type="text"] {{ width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
            select {{ width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 6px; width:100%; }}
            .btn-submit {{ background-color: #1a365d; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; margin-top:10px; }}
            .nav-bar {{ max-width: 450px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
            .btn-nav {{ text-decoration: none; color: #1e3a8a; font-weight: bold; border: 1px solid #1e3a8a; padding: 6px 12px; border-radius: 6px; font-size:14px; }}
        </style>
    </head>
    <body>
        <div class="nav-bar">
            <strong style="color:#1e3a8a;">MojaID System</strong>
            <a href="/admin" class="btn-nav">🔐 Admin Portal</a>
        </div>
        <div class="card">
            <h1>Citizen Wallet Registry</h1>
            {alert_msg}
            {error_msg}
            <form method="POST">
                <label>Full Name:</label>
                <input type="text" name="full_name" required>
                <label>Private NIDA ID:</label>
                <input type="text" name="nida_id" placeholder="199XXXXXXXXXXXX..." required>
                <label>Billing Method:</label>
                <select name="network">
                    <option value="M-Pesa">Vodacom M-Pesa</option>
                    <option value="Tigo Pesa">Tigo Pesa</option>
                    <option value="Airtel Money">Airtel Money</option>
                </select>
                <label>Account Phone Number:</label>
                <input type="text" name="phone" placeholder="07XXXXXXXX" required>
                <button type="submit" class="btn-submit">🔒 Verify & Sync Identity (300 TZS)</button>
            </form>
        </div>
    </body>
    </html>
    """

# --- SECURE ADMIN GATEWAY ---
@app.route("/admin", methods=["GET", "POST"])
def admin():
    error_msg = ""
    
    if session.get("logged_in"):
        running_total = 0
        ledger_html = ""
        
        for p in RECORDS_MEM_POOL:
            running_total += p["fee"]
            ledger_html += f"""
            <div style="background:#f8fafc; border:1px solid #e2e8f0; padding:15px; border-radius:8px; margin-bottom:15px; font-size:13px; position:relative; word-wrap:break-word;">
                <div style="background:#dcfce7; color:#166534; position:absolute; right:15px; top:15px; padding:4px; border-radius:12px; font-size:11px; font-weight:bold;">PAID +{p['fee']} TZS</div>
                <strong>👤 {p['name']}</strong> <small style="color:#64748b;">(Via {p['net']})</small><br>
                <span style="background:#e0e7ff; color:#3730a3; padding:4px; border-radius:12px; font-size:11px; font-weight:bold;">🔒 SHA-256 Encrypted NIDA Signature:</span>
                <span style="background:#fee2e2; color:#991b1b; padding:4px; border-radius:12px; font-size:11px; font-family:monospace; display:block; margin-top:5px;">{p['hash']}</span>
                <small style="color:#64748b; display:inline-block; margin-top:8px;">Ref ID: {p['ref']} | Sync Time: {p['time']}</small>
            </div>
            """
            
        if not RECORDS_MEM_POOL:
            ledger_html = '<p style="color:#888; text-align:center;">No encrypted records stored.</p>'

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>MojaID Corporate Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }}
                .container {{ max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 20px; }}
                .card {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 8px solid #16a34a; }}
                h2 {{ color: #1e3a8a; margin-top: 0; }}
                .nav-bar {{ max-width: 900px; margin: 0 auto 15px auto; display: flex; justify-content: space-between; align-items: center; }}
                .btn-logout {{ text-decoration: none; color: #dc2626; font-weight: bold; border: 1px solid #dc2626; padding: 6px 12px; border-radius: 6px; font-size:14px; }}
            </style>
        </head>
        <body>
            <div class="nav-bar">
                <strong style="color:#1e3a8a; font-size:20px;">MojaID Administration</strong>
                <a href="/logout" class="btn-logout">🚪 Logout</a>
            </div>
            <div class="container">
                <div class="card">
                    <h2>🔒 Encrypted Financial Ledger ({len(RECORDS_MEM_POOL)})</h2>
                    <div style="max-height:450px; overflow-y:auto;">
                        {ledger_html}
                    </div>
                </div>
                <div class="card" style="text-align:center; display:flex; flex-direction:column; justify-content:center; align-items:center;">
                    <h2>Platform Net Revenue</h2>
                    <div style="font-size:42px; font-weight:bold; color:#16a34a; margin:20px 0;">{running_total:,} TZS</div>
                    <p style="color:#64748b; font-size:13px; max-width:200px;">This financial metrics stream is completely invisible to public consumers.</p>
                </div>
            </div>
        </body>
        </html>
        """

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        input_password_hash = hashlib.sha256(password.encode()).hexdigest()

        if username == ADMIN_USERNAME and input_password_hash == ADMIN_PASSWORD_HASH:
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            error_msg = '<p style="color:red;font-weight:bold;text-align:center;">⚠️ Authentication Rejected: Invalid Credentials.</p>'

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MojaID Admin Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }}
            .card {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 8px solid #1e3a8a; max-width: 380px; margin: 80px auto; }}
            h2 {{ color: #1e3a8a; margin-top: 0; text-align:center; }}
            label {{ font-weight: bold; color: #333; display: block; margin-top: 15px; font-size: 14px; }}
            input[type="text"], input[type="password"] {{ width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
            .btn-submit {{ background-color: #16a34a; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; margin-top:10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Admin Authentication</h2>
            {error_msg}
            <form method="POST">
