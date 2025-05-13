from flask import Flask, request, jsonify, render_template
from utils import lipa_na_mpesa_online

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def pay():
    phone = request.form.get('phone')  
    amount = request.form.get('amount')
    
    if not phone or not amount:
        return jsonify({"error": "Missing phone number or amount"}), 400

    try:
        response = lipa_na_mpesa_online(phone, amount)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)