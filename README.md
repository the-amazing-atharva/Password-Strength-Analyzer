# 🔐 Enterprise Password Strength Analyzer Multi-Toolkit

An **industrial-grade password intelligence engine** with web API support.
Includes a **password analyzer**, **secure password generator**, **passphrase generator**, and **breach detection** using [Have I Been Pwned (HIBP)](https://haveibeenpwned.com/).

---

## 🖥 Features

### **Password Analyzer**

- **Entropy Calculation**: Measures password randomness and unpredictability
- **Length Analysis**: Checks if password meets minimum security requirements
- **Character Variety**: Detects use of uppercase, lowercase, numbers, and special characters
- **Common Pattern Detection**: Identifies sequential characters, repeated patterns, and keyboard walks
- **Dictionary Attack Detection**: Checks against common weak passwords
- **Strength Score**: Provides overall security rating (0-100)
- Detects character sets (uppercase, lowercase, numbers, special)
- Computes:
  - Shannon entropy
  - Theoretical entropy
  - Effective entropy (penalized for common patterns)

- Detects patterns and vulnerabilities:
  - Common passwords & dictionary words
  - Years, months, seasons, name+number patterns
  - Sequential characters, keyboard walks, repeated substrings

- Crack time simulations for various attack scenarios
- Enterprise-style **strength score (0–100)** with rating
- **Breach check** via HIBP API (shows number of times password appeared in leaks)

### 🎲 Secure Password Generator

- **Cryptographically Secure**: Uses `secrets` module for true randomness
- **Customizable Length**: Generate passwords from 8 to 128 characters
- **Character Set Options**: Include/exclude uppercase, lowercase, numbers, special characters
- **Memorable Passwords**: Generate passphrases using random words
- **Multiple Passwords**: Batch generation capability
- **Excludes Ambiguous Characters**: Optional exclusion of similar-looking characters (O/0, l/1)

### 🛡️ Vulnerability Detection

- **Breach Database Check**: Warns about commonly compromised passwords
- **Keyboard Pattern Detection**: Identifies patterns like "qwerty", "asdf"
- **Sequential Characters**: Detects "abc", "123", etc.
- **Repeated Characters**: Flags excessive character repetition
- **Personal Information**: Warns against using common names, dates

### **Passphrase Generator**

- Generates human-readable passphrases
- Options for number of words, capitalization, separators, and optional numbers

### **Breach Checker**

- Check if a password has appeared in known breaches
- Uses **k-Anonymity** to protect your password privacy

### **Web API**

- Flask-based endpoints for integration or web UI:
  - `POST /analyze` → Password analysis
  - `POST /generate` → Password generation
  - `POST /passphrase` → Passphrase generation
  - `POST /pwned` → Breach check

---

## ⚡ Installation

```bash
# Clone the repository
git clone https://github.com/the-amazing-atharva/Password-Strength-Analyzer.git
cd Passsword-Strength-Analyzer

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

**`requirements.txt` example:**

```
Flask>=2.0
requests>=2.28
```

---

## 🚀 Usage

### Run Flask App

```bash
python app.py
```

- Visit: `http://127.0.0.1:5000/`
- API endpoints accept JSON POST requests

---

### Password Analysis

**Request:**

```bash
POST /analyze
Content-Type: application/json

{
  "password": "MyP@ssw0rd123"
}
```

**Response:**

```json
{
  "password": "MyP@ssw0rd123",
  "length": 13,
  "shannon_entropy": 41.78,
  "theoretical_entropy": 77.55,
  "effective_entropy": 45.5,
  "log10_guess_space": 13.69,
  "character_sets": {"lowercase": true, "uppercase": true, "numbers": true, "special": true},
  "charset_size": 94,
  "patterns_detected": {
    "common_password": false,
    "dictionary_words": ["password"],
    "year": false,
    "word_year": false,
    "season_year": false,
    "month_year": false,
    "name_number": false,
    "sequential": false,
    "keyboard_walk": false,
    "repeated_substrings": false
  },
  "score": 38,
  "rating": "WEAK",
  "crack_time_estimates": {...},
  "pwned_count": 5
}
```

---

### Generate a Secure Password

**Request:**

```bash
POST /generate
Content-Type: application/json

{
  "length": 16,
  "uppercase": true,
  "lowercase": true,
  "numbers": true,
  "special": true,
  "exclude_ambiguous": true
}
```

**Response:**

```json
{
  "password": "G7x!pQ9vR$4hLm8Z"
}
```

---

### Generate a Passphrase

**Request:**

```bash
POST /passphrase
Content-Type: application/json

{
  "words": 4,
  "separator": "-",
  "capitalize": true,
  "include_number": true
}
```

**Response:**

```json
{
  "passphrase": "Alpha-Bravo-Delta-Foxtrot42"
}
```

---

### Check Password Breaches (HIBP)

**Request:**

```bash
POST /pwned
Content-Type: application/json

{
  "password": "MyP@ssw0rd123"
}
```

**Response:**

```json
{
  "pwned": true,
  "count": 5
}
```

---

## Time to Crack Estimates

| Password Type | Length | Character Set | Brute Force Time   |
| ------------- | ------ | ------------- | ------------------ |
| Numbers only  | 8      | 10            | ~2.5 hours         |
| Lowercase     | 8      | 26            | ~2 days            |
| Mixed case    | 8      | 52            | ~1 month           |
| + Numbers     | 8      | 62            | ~2 months          |
| + Special     | 8      | 94            | ~7 months          |
| + Special     | 12     | 94            | ~6,000 years       |
| + Special     | 16     | 94            | ~1.5 million years |

\*Assumes 10 billion attempts per second

## NIST Guidelines Compliance

This tool follows NIST SP 800-63B recommendations:

- ✅ Minimum length of 8 characters
- ✅ No complexity requirements (but encouraged)
- ✅ Check against breach databases
- ✅ No periodic password changes required
- ✅ Allow all printable ASCII characters

## Future Enhancements

- [ ] Multi-language support
- [ ] Custom dictionary support
- [ ] Password history tracking

## 🛡 Security Notes

- Passwords are **never stored**; only analyzed on the fly
- Uses **`secrets`** module for cryptographically secure random generation
- Breach check uses **k-Anonymity** (first 5 chars of SHA1 hash) to protect your password
- Effective entropy penalizes common patterns, words, sequences, and keyboard walks

---

## References

- [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Password Guidelines](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Shannon Entropy](<https://en.wikipedia.org/wiki/Entropy_(information_theory)>)
- [Password Strength](https://en.wikipedia.org/wiki/Password_strength)

---

## 👨‍💻 Author

@the-amazing-atharva
