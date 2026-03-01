from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import os
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '4f7a2b9e1c8d3f5a6b0e9d8c7b6a5f4e') 

# --- Production Mail Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# These lines pull your private info from Render's settings
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('T-Five Matches', os.environ.get('MAIL_USERNAME'))

# --- Flask-Mail Configuration ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'newht.enquiry@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'wdzp atmv nxra sgox'     # Replace with your Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = 'newht.enquiry@gmail.com'

mail = Mail(app)

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
        name = request.form.get("name")
        company = request.form.get("company")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get("message")

        msg = Message(
            subject=f"New B2B Enquiry: {company if company else name}",
            recipients=['balchandanihet@gmail.com'], # Where you want to receive the lead
            body=f"""
            New Matchbox Enquiry Received:
            
            Name: {name}
            Company: {company}
            Phone: {phone}
            Email: {email}
            
            Message:
            {message}
            """,
            reply_to=email # Allows you to hit 'Reply' directly in your email app
        )

        try:
            # 2. Send the Mail
            mail.send(msg)
            session['user_name'] = name
            return redirect(url_for("success"))
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("There was an error sending your enquiry. Please try WhatsApp.", "error")
            return redirect(url_for("enquiry"))

    return render_template("enquiry.html")

@app.route("/success")
def success():
    # Retrieve the name from the session, default to 'Partner' if not found
    name = session.get('user_name', 'Partner')
    return render_template("success.html", name=name)

if __name__ == "__main__":
    app.run