from flask import Flask, request, render_template, redirect, url_for, flash
from utils import lipa_na_mpesa_online

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def pay():
    phone = request.form.get('phone')
    amount = request.form.get('amount')

    if not phone or not amount:
        flash("Please enter both phone number and amount.")
        return redirect(url_for('home'))

    try:
        response = lipa_na_mpesa_online(phone, amount)
        if response.get("success"):
            return redirect(url_for('payment_success'))
        else:
            flash(response.get("error", "Payment failed. Please try again."))
            return redirect(url_for('payment_failed'))
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}")
        return redirect(url_for('payment_failed'))

@app.route('/payment-success')
def payment_success():
    return render_template('success.html')

@app.route('/payment-failed')
def payment_failed():
    return render_template('fail.html')

if __name__ == "__main__":
    app.run(debug=True)
