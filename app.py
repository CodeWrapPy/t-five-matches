from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import os
import threading

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '4f7a2b9e1c8d3f5a6b0e9d8c7b6a5f4e')

# ── Mail Configuration ────────────────────────────────────────────────────────
# DO NOT add a second block below this — it will overwrite these env vars!
app.config['MAIL_SERVER']         = 'smtp.gmail.com'
app.config['MAIL_PORT']           = 587        # 587+TLS works on Render; 465 times out
app.config['MAIL_USE_TLS']        = True
app.config['MAIL_USE_SSL']        = False
app.config['MAIL_USERNAME']       = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']       = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('T-Five Matches', os.environ.get('MAIL_USERNAME'))

mail = Mail(app)


def send_async_email(app, msg):
    """Send in background thread — prevents gunicorn WORKER TIMEOUT."""
    with app.app_context():
        try:
            mail.send(msg)
            print("[MAIL] Sent successfully")
        except Exception as e:
            print(f"[MAIL ERROR] {type(e).__name__}: {e}")


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/enquiry", methods=["GET", "POST"])
def enquiry():
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        company = request.form.get("company", "").strip()
        phone   = request.form.get("phone", "").strip()
        email   = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not phone or not message:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("enquiry"))

        msg = Message(
            subject=f"New B2B Enquiry from {company if company else name}",
            recipients=['balchandanihet@gmail.com'],
            body=f"""New Matchbox Enquiry Received
================================
Name    : {name}
Company : {company or 'N/A'}
Phone   : {phone}
Email   : {email or 'N/A'}

Message:
{message}
""",
            reply_to=email if email else None
        )

        # Fire and forget — user gets success page instantly
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.daemon = True
        thread.start()

        session['user_name'] = name
        return redirect(url_for("success"))

    return render_template("enquiry.html")


@app.route("/success")
def success():
    name = session.pop('user_name', 'Partner')
    return render_template("success.html", name=name)


@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(debug=False)
