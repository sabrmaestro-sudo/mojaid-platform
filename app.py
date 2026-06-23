import sqlite3
import time
import hashlib  # Built-in secure data cryptography library
from flask import Flask, render_template_string, request

app = Flask(__name__)
DB_FILE = "mojaid.db"

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            nida_id_encrypted TEXT NOT NULL UNIQUE,
            network TEXT,
            phone TEXT,
            fee_charged INTEGER,
            payment_reference TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- SECURITY MODULE: CRYPTOGRAPHIC HASHING ENGINE ---
def encrypt_identity_data(raw_text):
    """
    Transforms private data (like NIDA or Passports) into an unreadable, 
    one-way cryptographic hash. If a hacker steals the database, they cannot read it.
    """
    secure_hash_object = hashlib.sha256(raw_text.encode())
    return secure_hash_object.hexdigest()

# --- MOCK MOBILE MONEY API PROMPT ---
def trigger_mobile_money_stk_push(phone_number, amount_tzs):
    time.sleep(0.5)  # Simulate gateway connection
    mock_telecom_ref = f"TX{int(time.time())}MZ"
    return {"status": "SUCCESS", "reference": mock_telecom_ref}

# --- ADVANCED DASHBOARD TEMPLATE WITH LIVE CHART.JS ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MojaID Production Hub</title>
    <!-- Load Chart.js CDN directly into our visual user interface -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }
        .container { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px; }
        .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 8px solid #1e3a8a; }
        .full-width-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border-top: 8px solid #16a34a; }
        h1, h2 { color: #1e3a8a; margin-top: 0; }
        label { font-weight: bold; color: #333; display: block; margin-top: 10px; font-size: 14px; }
        input[type="text"] { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        select { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 6px; }
        .btn-submit { background-color: #1a365d; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; }
        .profile-box { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin-bottom: 15px; font-size: 13px; position: relative; word-wrap: break-word; }
        .badge { background: #e0e7ff; color: #3730a3; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 5px; }
        .crypto-badge { background: #fee2e2; color: #991b1b; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-family: monospace; display: block; margin-top: 5px; }
        .fee-badge { background: #dcfce7; color: #166534; position: absolute; right: 15px; top: 15px; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }
        .alert-box { background: #e0f2fe; color: #0369a1; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; margin-bottom: 15px; }
        .error-msg { color: #dc2626; font-weight: bold; margin-bottom: 15px; text-align: center; }
    </style>
</head>
<body>

    <div style="text-align: center; margin-bottom: 25px;">
        <h1>MojaID Production Hub</h1>
        <p style="color: #555;">🔒 SHA256 Encryption & 📊 Live Cumulative Analytics Engine Activated</p>
    </div>

    <!-- TOP SECTION: Business Intelligence Cashflow Analytics Chart -->
    <div class="full-width-card" style="max-width: 1100px; margin: 0 auto 20px auto;">
        <h2>📈 Total Cumulative Cashflow Earnings Timeline</h2>
        <div style="width: 100%; max-height: 250px;">
            <canvas id="earningsChart"></canvas>
        </div>
    </div>

    <div class="container">
        <!-- LEFT PANEL: Registration Entry Form -->
        <div class="card">
            <h2>Secure Gateway Entry</h2>
            {% if alert %}<div class="alert-box">🔔 {{ alert }}</div>{% endif %}
            {% if error %}<div class="error-msg">⚠️ {{ error }}</div>{% endif %}
            
            <form method="POST">
                <label>Full Name:</label>
                <input type="text" name="full_name" required>
                
                <label>Private NIDA ID (Will encrypt instantly):</label>
                <input type="text" name="nida_id" placeholder="199XXXXXXXXXXXX..." required>
                
                <label>Billing Method:</label>
                <select name="network">
                    <option value="M-Pesa">Vodacom M-Pesa</option>
                    <option value="Tigo Pesa">Tigo Pesa</option>
                    <option value="Airtel Money">Airtel Money</option>
                </select>

                <label>Account Phone Number:</label>
                <input type="text" name="phone" placeholder="07XXXXXXXX" required>
                
                <button type="submit" class="btn-submit">🔒 Verify & Collect 300 TZS</button>
            </form>
        </div>

        <!-- RIGHT PANEL: Database Registry Viewer -->
        <div class="card">
            <h2>Encrypted Database Ledger Records ({{ saved_profiles|length }})</h2>
            <div style="max-height: 450px; overflow-y: auto;">
                {% if not saved_profiles %}
                    <p style="color: #888; text-align: center; margin-top: 50px;">No transaction profiles found inside database ledger.</p>
                {% endif %}
                {% for p in saved_profiles %}
                    <div class="profile-box">
                        <div class="fee-badge">PAID +{{ p[5] }} TZS</div>
                        <strong>👤 {{ p[1] }}</strong> <small style="color:#64748b;">(Via {{ p[3] }})</small><br>
                        <span class="badge">🔒 SHA-256 Encrypted NIDA Signature:</span>
                        <span class="crypto-badge">{{ p[2] }}</span>
                        <small style="color: #64748b; display:inline-block; margin-top:8px;">Ref ID: {{ p[6] }} | Sync Time: {{ p[7] }}</small>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>

    <!-- SCRIPT INJECTION CODE: Connects Python Backend lists to browser JavaScript engine -->
    <script>
        const ctx = document.getElementById('earningsChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ chart_labels|tojson }},
                datasets: [{
                    label: 'Platform Profit Curve (TZS)',
                    data: {{ chart_data|tojson }},
                    borderColor: '#16a34a',
                    backgroundColor: 'rgba(22, 163, 74, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } }
            }
        });
    </script>

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
        
        # CORE UPGRADE: Cryptographically scramble private data before it hits long term storage
        encrypted_nida = encrypt_identity_data(nida_id)
        current_time = time.strftime("%H:%M:%S")
        
        payment_response = trigger_mobile_money_stk_push(phone, fee_charged)
        
        if payment_response["status"] == "SUCCESS":
            tx_reference = payment_response["reference"]
            try:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO profiles (full_name, nida_id_encrypted, network, phone, fee_charged, payment_reference, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (full_name, encrypted_nida, network, phone, fee_charged, tx_reference, current_time))
                conn.commit()
                conn.close()
                alert = f"Secure encrypted registration and billing completed!"
            except sqlite3.IntegrityError:
                error = "Security Intercept: Scrambled cryptographic fingerprint already matches a profile row."

    # --- ANALYTICS TIMELINE ENGINE GENERATOR ---
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, fee_charged FROM profiles ORDER BY id ASC")
    raw_history = cursor.fetchall()
    
    # Read full dataset reverse for displaying listing
    cursor.execute("SELECT * FROM profiles ORDER BY id DESC")
    saved_profiles = cursor.fetchall()
    conn.close()
    
    # Generate cumulative graph values step by step
    chart_labels = ["Launch"]
    chart_data = [0]
    running_total = 0
    
    for row in raw_history:
        timestamp_label = row[0]
        revenue_step = row[1]
        running_total += revenue_step
        chart_labels.append(timestamp_label)
        chart_data.append(running_total)

    return render_template_string(HTML_TEMPLATE, saved_profiles=saved_profiles, chart_labels=chart_labels, chart_data=chart_data, alert=alert, error=error)


if __name__ == "__main__":
    # Import the native operating system module to read cloud environment configurations
    import os
    
    # Render and other cloud networks automatically assign a dynamic PORT variable
    port = int(os.environ.get("PORT", 5000))
    
    # Launch the application on all available public network interfaces (0.0.0.0)
    app.run(host="0.0.0.0", port=port)


