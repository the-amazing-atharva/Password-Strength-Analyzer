from flask import Flask, render_template, request, jsonify
from password_tool import EnterprisePasswordAnalyzer, EnterprisePasswordGenerator
import hashlib
import requests

app = Flask(__name__)


# ==========================================================
# HOME
# ==========================================================
@app.route("/")
def index():
    return render_template("index.html")


# ==========================================================
# PASSWORD ANALYZER
# ==========================================================
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    analyzer = EnterprisePasswordAnalyzer(password)
    analysis = analyzer.get_full_analysis()

    return jsonify(analysis)


# ==========================================================
# PASSWORD GENERATOR
# ==========================================================
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    length = int(data.get("length", 16))
    use_uppercase = bool(data.get("uppercase", True))
    use_lowercase = bool(data.get("lowercase", True))
    use_numbers = bool(data.get("numbers", True))
    use_special = bool(data.get("special", True))
    exclude_ambiguous = bool(data.get("exclude_ambiguous", False))

    password = EnterprisePasswordGenerator.generate_password(
        length=length,
        use_uppercase=use_uppercase,
        use_lowercase=use_lowercase,
        use_numbers=use_numbers,
        use_special=use_special,
        exclude_ambiguous=exclude_ambiguous
    )

    return jsonify({"password": password})


# ==========================================================
# PASSPHRASE GENERATOR
# ==========================================================
@app.route("/passphrase", methods=["POST"])
def passphrase():
    data = request.json
    words = int(data.get("words", 4))
    separator = data.get("separator", "-")
    capitalize = bool(data.get("capitalize", False))
    include_number = bool(data.get("include_number", False))

    phrase = EnterprisePasswordGenerator.generate_passphrase(
        num_words=words,
        separator=separator,
        capitalize=capitalize,
        include_number=include_number
    )

    return jsonify({"passphrase": phrase})


# ==========================================================
# PWNED PASSWORD / BREACH CHECK
# ==========================================================
@app.route("/pwned", methods=["POST"])
def pwned():
    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    # SHA1 hash of the password
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    # Query HIBP API using k-Anonymity (first 5 chars of SHA1)
    res = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if res.status_code != 200:
        return jsonify({"error": "HIBP API error"}), 500

    # Check if the suffix exists in the response
    count = 0
    for line in res.text.splitlines():
        h, c = line.split(":")
        if h == suffix:
            count = int(c)
            break

    return jsonify({"pwned": count > 0, "count": count})


@app.route("/harden", methods=["POST"])
def harden():
    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "No password provided"}), 400

    hardened = EnterprisePasswordGenerator.harden_password(password)
    return jsonify({"hardened": hardened})


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    app.run(debug=True)
