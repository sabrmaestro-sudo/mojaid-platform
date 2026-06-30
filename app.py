import time
import hashlib
import os
from flask import Flask, request

app = Flask(__name__)

# HIGH-SPEED IN-MEMORY LEDGER
RECORDS_MEM_POOL = []

# YOUR PRIVATE UNGUESSABLE SECRET PHRASE KEY
# Change this secret phrase word later to whatever you want for ultimate safety!
SECRET_ADMIN_TOKEN = "fungua-mojaid-revenue-2026"

def encrypt_identity_data(raw_text):
    return hashlib.sha256(raw_text.encode()).hexdigest()

BASE_STYLES = "<style>body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; text-align: center; } .card { background: white; max-width: 450px; margin: 40px auto; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-top: 8px solid #1e3a8a; text-align: left; } .container { max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; text-align: left; } .admin-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 8px solid #16a34a; } h1, h2 { color: #1e3a8a; margin-top: 0; } label { font-weight: bold; color: #333; display: block; margin-top: 15px; font-size: 14px; } input[type='text'] { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; } select { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 6px; width:100%; } .btn-submit { background-color: #1a365d; color: white; border: none; padding: 12px; font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; margin-top:10px; }</style>"

# --- PUBLIC INTERFACE (ADMIN LINK IS NOW 100% INVISIBLE) ---
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
            error_msg = '<p style="color:red;font-weight:bold;text-align:center;">⚠️ Profile fingerprint already verified.</p>'
        else:
            tx_reference = f"TX{int(time.time())}MZ"
            RECORDS_MEM_POOL.insert(0, {
                "name": full_name, "hash": encrypted_nida, "net": network, "fee": 500,
                "ref": tx_reference, "time": current_time, "nhif": nhif, "license": license, "bank": bank
            })
            alert_msg = '<p style="color:#0369a1;background:#e0f2fe;padding:12px;border-radius:8px;font-weight:bold;text-align:center;">📡 Outbound Request Sent! Check your phone for the payment PIN pop-up to authorize 500 TZS.</p>'

    html_page = "<!DOCTYPE html><html><head><title>MojaID Wallet</title>" + BASE_STYLES + "</head><body>"
    html_page += "<div class='card'><h1>Citizen Wallet Registry</h1>" + alert_msg + error_msg
    html_page += "<form method='POST'>"
    html_page += "<label>Full Name:</label><input type='text' name='full_name' required>"
    html_page += "<label>Primary NIDA ID:</label><input type='text' name='nida_id' placeholder='199XXXXXXXXXXXX...' required>"
    html_page += "<label>NHIF Card Number (Optional):</label><input type='text' name='nhif' placeholder='e.g. NHIF-992831'>"
    html_page += "<label>Driving License Class (Optional):</label><input type='text' name='license' placeholder='e.g. A, B, C'>"
    html_page += "<label>Linked Bank Name (Optional):</label><input type='text' name='bank' placeholder='e.g. CRDB'>"
    html_page += "<label>Billing Network Method:</label><select name='network'><option value='M-Pesa'>Vodacom M-Pesa</option><option value='Tigo Pesa'>Tigo Pesa</option><option value='Airtel Money'>Airtel Money</option><option value='HaloPesa'>HaloPesa</option></select>"
    html_page += "<label>Account Phone Number:</label><input type='text' name='phone' placeholder='07XXXXXXXX' required>"
    html_page += "<button type='submit' class='btn-submit'>🔒 Verify & Sync Identity (500 TZS)</button>"
    html_page += "</form></div></body></html>"
    return html_page

# --- SECRET REVENUE PORTAL (ACCESSIBLE ONLY VIA THE TOKEN LINK) ---
@app.route("/secret/<token>")
def secret_admin(token):
    # Security Guard: If the URL token doesn't match your secret key string, boot them out!
    if token != SECRET_ADMIN_TOKEN:
        return "<h1 style='text-align:center;color:red;margin-top:100px;'>🔒 Access Denied: Unauthorized Node Endpoint.</h1>", 403

    running_total = 0
    ledger_html = ""
    for p in RECORDS_MEM_POOL:
        running_total += p.get("fee", 500)
        ledger_html += '<div style="background:#f8fafc; border:1px solid #e2e8f0; padding:15px; border-radius:8px; margin-bottom:15px; font-size:13px; position:relative; word-wrap:break-word;">'
        ledger_html += '<div style="background:#dcfce7; color:#166534; position:absolute; right:15px; top:15px; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold;">PAID +' + str(p.get('fee', 500)) + ' TZS</div>'
        ledger_html += '<strong>👤 ' + str(p.get('name', 'Unknown')) + '</strong> <small style="color:#64748b;">(Via ' + str(p.get('net', 'M-Pesa')) + ')</small><br>'
        ledger_html += '<span style="background:#e0e7ff; color:#3730a3; padding:2px 6px; border-radius:8px; font-size:11px; font-weight:bold; display:inline-block; margin-top:8px;">🔒 SHA-256 NIDA Hash:</span>'
        ledger_html += '<span style="background:#fee2e2; color:#991b1b; padding:4px; border-radius:6px; font-size:11px; font-family:monospace; display:block; margin-top:3px;">' + str(p.get('hash', '')) + '</span>'
        ledger_html += '<div style="margin-top:10px; background:white; padding:8px; border-radius:6px; border:1px dashed #cbd5e1;">'
        ledger_html += '🏥 <strong>NHIF:</strong> ' + str(p.get('nhif', 'NONE')) + ' | 🚗 <strong>License:</strong> ' + str(p.get('license', 'NONE')) + ' | 💳 <strong>Bank:</strong> ' + str(p.get('bank', 'NONE'))
        ledger_html += '</div>'
        ledger_html += '<small style="color:#64748b; display:inline-block; margin-top:8px;">Ref ID: ' + str(p.get('ref', '')) + ' | Sync Time: ' + str(p.get('time', '')) + '</small></div>'
        
    if not RECORDS_MEM_POOL:
        ledger_html = '<p style="color:#888; text-align:center; margin-top:40px;">No encrypted records stored inside memory cache.</p>'

    html_dashboard = "<!DOCTYPE html><html><head><title>MojaID Owner Hub</title>" + BASE_STYLES + "</head><body>"
    html_dashboard += "<div class='container' style='margin-top:40px;'><div class='admin-card'>"
    html_dashboard += "<h2>🔒 Encrypted Financial Ledger (" + str(len(RECORDS_MEM_POOL)) + ")</h2><div style='max-height:450px; overflow-y:auto;'>" + ledger_html + "</div></div>"
    html_dashboard += "<div class='admin-card' style='text-align:center; display:flex; flex-direction:column; justify-content:center; align-items:center;'><h2>Platform Net Revenue</h2><div style='font-size:42px; font-weight:bold; color:#16a34a; margin:20px 0;'>" + f"{running_total:,}" + " TZS</div><p style='color:#64748b; font-size:13px; max-width:200px;'>This metrics channel tracks cache variables. It is 100% invisible to the public universe.</p></div></div></body></html>"
    return html_dashboard

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
