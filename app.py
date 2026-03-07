from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '4f7a2b9e1c8d3f5a6b0e9d8c7b6a5f4e')

# --- Mail Configuration ---
# Reads from Render Environment Variables in production.
# To test locally, set these as environment variables or temporarily hardcode them.
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('T-Five Matches', os.environ.get('MAIL_USERNAME'))

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
            recipients=['balchandanihet@gmail.com'],
            body=f"""
New Matchbox Enquiry Received:

Name:    {name}
Company: {company}
Phone:   {phone}
Email:   {email}

Message:
{message}
            """,
            reply_to=email
        )

        try:
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
    name = session.get('user_name', 'Partner')
    return render_template("success.html", name=name)


if __name__ == "__main__":
    app.run(debug=False)
