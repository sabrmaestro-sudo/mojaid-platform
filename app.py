import time
import hashlib
import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mojaid_super_secret_key_123")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hashlib.sha256("MojaID2026!#".encode()).hexdigest()

# MEMORY STORAGE: Holds profiles safely in system memory to completely bypass database file errors
RECORDS_MEM_POOL = []

def encrypt_identity_data(raw_text):
    return hashlib.sha256(raw_text.encode()).hexdigest()

def trigger_mobile_money_stk_push(phone_number, amount_tzs):
    time.sleep(0.1)
    return {"status": "SUCCESS", "reference": f"TX{int(time.time())}MZ"}

CSS_STYLES = """
body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }
.container { max-width: 1100px; margin: 0 auto; }
.card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 8px solid #1e3a8a; margin-bottom: 20px; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
h1, h2 { color: #1e3a8a; margin-top: 0; }
label { font-weight: bold; color: #333; display: block; margin-top: 10px; font-size: 14px; }
input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
select { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 6px; }
.btn-submit { background-color: #1a365d; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; }
.profile-box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; position: relative; word-wrap: break-word; }
.badge { background: #e0e7ff; color: #3730a3; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 5px; }
.crypto-badge { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-family: monospace; display: block; margin-top: 5px; }
.fee-badge { background: #dcfce7; color: #166534; position: absolute; right: 15px; top: 15px; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
.alert-box { background: #e0f2fe; color: #0369a1; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 15px; }
.error-msg { color: #dc2626; font-weight: bold; margin-bottom: 15px; text-align: center; }
.nav-bar { max-width: 1100px; margin: 0 auto 15px auto; display: flex; justify-content: space-between; align-items: center; }
.btn-nav { text-decoration: none; color: #1e3a8a; font-weight: bold; border: 1px solid #1e3a8a; padding: 6px 12px; border-radius: 6px; }
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MojaID Production Hub</title>
    <style>{{ custom_css }}</style>
</head>
<body>

    <div class="nav-bar">
        <strong style="font-size: 20px; color:#1e3a8a;">MojaID System</strong>
        {% if is_admin %}
            <a href="/logout" class="btn-nav" style="color:#dc2626; border-color:#dc2626;">🚪 Admin Logout</a>
        {% else %}
            <a href="/admin" class="btn-nav">🔐 Admin Dashboard Portal</a>
        {% endif %}
    </div>

    <div class="container">
        {% if view == "public" %}
            <div class="card" style="max-width: 500px; margin: 0 auto;">
                <h2>Citizen Wallet Registry</h2>
                {% if alert %}<div class="alert-box">🔔 {{ alert }}</div>{% endif %}
                {% if error %}<div class="error-msg">⚠️ {{ error }}</div>{% endif %}
                
                <form method="POST" action="/">
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
        {% endif %}

        {% if view == "login" %}
            <div class="card" style="max-width: 400px; margin: 50px auto;">
                <h2>System Administrator Authentication</h2>
                {% if error %}<div class="error-msg">⚠️ {{ error }}</div>{% endif %}
                <form method="POST" action="/admin">
                    <label>Admin Username:</label>
                    <input type="text" name="username" required>
                    
                    <label>Security Password:</label>
                    <input type="password" name="password" required>
                    
                    <button type="submit" class="btn-submit" style="background-color: #16a34a;">🔓 Verify Credentials</button>
                </form>
            </div>
        {% endif %}

        {% if view == "admin_dashboard" %}
            <div class="grid-2">
                <div class="card">
                    <h2>🔒 Encrypted Financial Ledger ({{ total_count }})</h2>
                    <div style="max-height: 400px; overflow-y: auto;">
                        {% if total_count == 0 %}
                            <p style="color: #888; text-align: center; margin-top: 50px;">No encrypted records stored.</p>
                        {% endif %}
                        {% for p in saved_profiles %}
                            <div class="profile-box">
                                <div class="fee-badge">PAID +{{ p.fee }} TZS</div>
                                <strong>👤 {{ p.name }}</strong> <small style="color:#64748b;">(Via {{ p.net }})</small><br>
                                <span class="badge">🔒 SHA-256 Encrypted NIDA Signature:</span>
                                <span class="crypto-badge">{{ p.hash }}</span>
                                <small style="color: #64748b; display:inline-block; margin-top:8px;">Ref ID: {{ p.ref }} | Sync Time: {{ p.time }}</small>
                            </div>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="card" style="text-align: center; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <h2 style="margin-bottom: 5px;">Platform Net Revenue</h2>
                    <div style="font-size: 48px; font-weight: bold; color: #16a34a; margin: 20px 0;">
                        {{ total_revenue }} TZS
                    </div>
                    <p style="color:#64748b; max-width: 300px; font-size:14px;">This panel tracks live incoming revenue memory variables securely.</p>
                </div>
            </div>
        {% endif %}
    </div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    alert = None
    if request.method == "POST":
        full_name = request.form.get("full_name")
        nida_id = request.form.get("nida_id")
        network = request.form.get("network")
        phone = request.form.get("phone")
        fee_charged = 300
        
        encrypted_nida = encrypt_identity_data(nida_id)
        current_time = time.strftime("%H:%M:%S")
        
        # Check for duplicates in our memory pool array
        duplicate_found = False
        for record in RECORDS_MEM_POOL:
            if record["hash"] == encrypted_nida:
                duplicate_found = True
                break
                
        if duplicate_found:
            error = "Security Intercept: Fingerprint matches existing row."
        else:
            payment_response = trigger_mobile_money_stk_push(phone, fee_charged)
            if payment_response["status"] == "SUCCESS":
                tx_reference = payment_response["reference"]
                
                # Append directly to our tracking array structure
                RECORDS_MEM_POOL.insert(0, {
                    "name": full_name,
                    "hash": encrypted_nida,
                    "net": network,
                    "fee": fee_charged,
                    "ref": tx_reference,
                    "time": current_time
                })
                alert = "Secure registration and billing request simulation authorized!"
                
    return render_template_string(HTML_TEMPLATE, view="public", alert=alert, error=error, is_admin=False, custom_css=CSS_STYLES)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    if session.get("logged_in"):
        running_total = 0
        for record in RECORDS_MEM_POOL:
            running_total += record["fee"]

        return render_template_string(
            HTML_TEMPLATE, 
            view="admin_dashboard", 
            saved_profiles=RECORDS_MEM_POOL, 
            total_count=len(RECORDS_MEM_POOL),
            total_revenue=running_total, 
            is_admin=True, 
            custom_css=CSS_STYLES
        )

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        input_password_hash = hashlib.sha256(password.encode()).hexdigest()

