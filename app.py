from flask import Flask, render_template, request, jsonify
from password_tool import EnterprisePasswordAnalyzer, EnterprisePasswordGenerator

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    analyzer = EnterprisePasswordAnalyzer(password)
    analysis = analyzer.get_full_analysis()

    return jsonify(analysis)


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


if __name__ == "__main__":
    app.run(debug=True)
