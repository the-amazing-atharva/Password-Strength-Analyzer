import os
from typing import Dict, List, Tuple
import string
import secrets
import math
import re
from datetime import datetime
import hashlib
import requests

# ==========================================================
# GLOBAL INTELLIGENCE CONFIGURATION
# ==========================================================

CURRENT_YEAR = datetime.now().year
MIN_YEAR = 1950
MAX_YEAR = CURRENT_YEAR + 5

# Get the absolute path to the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the path to the wordlist file dynamically
WORDLIST_PATH = os.path.join(
    BASE_DIR, 'data', '100k-most-used-passwords-NCSC.txt')

# Fallback list used if the external file is missing
FALLBACK_COMMON_PASSWORDS = {
    "password", "password123", "Pasword123", "123456", "123456789", "12345678", "12345",
    "1234567", "password1", "123123", "1234567890",
    "qwerty", "abc123", "111111", "1234", "admin",
    "letmein", "welcome", "monkey", "dragon",
    "master", "sunshine", "princess", "login",
    "admin123", "solo", "1q2w3e4r", "starwars",
    "qwertyuiop", "654321", "batman", "superman"
}


def load_enterprise_wordlist():
    """Loads 100k passwords into a set for O(1) lookup."""
    if os.path.exists(WORDLIST_PATH):
        try:
            with open(WORDLIST_PATH, "r", encoding="utf-8", errors="ignore") as f:
                # Using a set comprehension for maximum speed
                wordlist = {line.strip().lower() for line in f if line.strip()}
                print(
                    f"✅ Success: Loaded {len(wordlist)} passwords from {WORDLIST_PATH}")
                return wordlist
        except Exception as e:
            print(f"❌ Error loading wordlist: {e}")
            return FALLBACK_COMMON_PASSWORDS
    else:
        print(
            f"⚠️ Warning: Wordlist not found at {WORDLIST_PATH}. Using fallback.")
        return FALLBACK_COMMON_PASSWORDS


# Initialize the global set
COMMON_PASSWORDS = load_enterprise_wordlist()

COMMON_WORDS = {
    "password", "pass", "admin", "user", "word",
    "root", "login", "welcome", "company",
    "test", "guest", "security", "master"
}

COMMON_NAMES = {
    "john", "mike", "david", "sarah",
    "emma", "james", "robert", "linda"
}

SEASONS = {"spring", "summer", "fall", "winter", "autumn"}

MONTHS = {
    "january", "february", "march", "april",
    "may", "june", "july", "august",
    "september", "october", "november", "december"
}

KEYBOARD_ROWS = [
    "1234567890",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

LEET_MAP = str.maketrans({
    "@": "a", "4": "a",
    "3": "e",
    "1": "l", "!": "i",
    "0": "o",
    "$": "s", "5": "s",
    "7": "t"
})


# ==========================================================
# ENTERPRISE PASSWORD ANALYZER (Updated Methods)
# ==========================================================

class EnterprisePasswordAnalyzer:
    def __init__(self, password: str):
        self.password = password
        self.length = len(password)
        # normalize to lowercase for matching, but keep original for casing checks
        self.normalized = self._normalize_leet(password)

    def _normalize_leet(self, text: str) -> str:
        return text.lower().translate(LEET_MAP)

    def detect_common_password(self) -> bool:
        """Checks if the password (or its leet version) is in the 100k list."""
        # We check the normalized version so 'P@ssw0rd123' -> 'password123'
        # which matches the entries in our list.
        return self.normalized in COMMON_PASSWORDS

    def detect_leet_speak(self) -> bool:
        """Improved: Only returns True if symbols are used as substitutions."""
        leet_chars = set("@431!0$57")
        return any(c in leet_chars for c in self.password)
    # --- CHARACTER SET & METRICS ---

    def get_character_sets(self) -> Dict[str, bool]:
        return {
            "lowercase": bool(re.search(r"[a-z]", self.password)),
            "uppercase": bool(re.search(r"[A-Z]", self.password)),
            "numbers": bool(re.search(r"\d", self.password)),
            "special": bool(re.search(r"[^\w]", self.password))
        }

    def calculate_charset_size(self) -> int:
        charset = self.get_character_sets()
        size = 0
        if charset["lowercase"]:
            size += 26
        if charset["uppercase"]:
            size += 26
        if charset["numbers"]:
            size += 10
        if charset["special"]:
            size += 32
        return size

    def shannon_entropy(self) -> float:
        if not self.password:
            return 0.0
        freq = {}
        for c in self.password:
            freq[c] = freq.get(c, 0) + 1
        entropy = 0.0
        for count in freq.values():
            p = count / self.length
            entropy -= p * math.log2(p)
        return entropy * self.length

    def theoretical_entropy(self) -> float:
        charset = self.calculate_charset_size()
        if charset == 0:
            return 0
        return self.length * math.log2(charset)

    def calculate_spatial_complexity(self) -> float:
        """Measures character variety relative to length."""
        if self.length == 0:
            return 0.0
        unique_chars = len(set(self.password))
        return round(unique_chars / self.length, 2)

    # --- PATTERN DETECTION ---

    def detect_common_password(self) -> bool:
        # This now checks against your 100k list!
        return self.normalized in COMMON_PASSWORDS

    def detect_dictionary_words(self) -> List[str]:
        found = []
        for word in COMMON_WORDS:
            if word in self.normalized:
                found.append(word)
        return found

    def detect_leet_speak(self) -> bool:
        # Only returns True if symbols are used in place of letters (the LEET_MAP keys)
        leet_chars = set("@431!0$57")
        return any(c in leet_chars for c in self.password)

    def detect_casing_mix(self) -> str:
        if self.password.islower():
            return "All Lowercase"
        if self.password.isupper():
            return "All Uppercase"
        if any(c.isupper() for c in self.password) and any(c.islower() for c in self.password):
            return "Mixed Case"
        return "None"

    def detect_year(self) -> bool:
        matches = re.findall(r"(19\d{2}|20\d{2})", self.password)
        for y in matches:
            if MIN_YEAR <= int(y) <= MAX_YEAR:
                return True
        return False

    def detect_word_year(self) -> bool:
        return bool(re.search(r"[A-Za-z]+(19\d{2}|20\d{2})", self.password))

    def detect_season_year(self) -> bool:
        lower = self.normalized
        for s in SEASONS:
            if re.search(fr"{s}(19\d{{2}}|20\d{{2}})", lower):
                return True
        return False

    def detect_month_year(self) -> bool:
        lower = self.normalized
        for m in MONTHS:
            if re.search(fr"{m}(19\d{{2}}|20\d{{2}})", lower):
                return True
        return False

    def detect_name_number(self) -> bool:
        lower = self.normalized
        for name in COMMON_NAMES:
            if re.search(fr"{name}\d+", lower):
                return True
        return False

    def detect_sequential_patterns(self) -> bool:
        seq = string.ascii_lowercase + string.digits
        rev = seq[::-1]
        lower = self.normalized
        for i in range(len(seq) - 2):
            if seq[i:i+3] in lower or rev[i:i+3] in lower:
                return True
        return False

    def detect_keyboard_patterns(self) -> bool:
        lower = self.normalized
        for row in KEYBOARD_ROWS:
            for i in range(len(row) - 2):
                fwd = row[i:i+3]
                rev = fwd[::-1]
                if fwd in lower or rev in lower:
                    return True
        return False

    def detect_repeated_substrings(self) -> bool:
        for size in range(2, self.length // 2 + 1):
            for i in range(self.length - size):
                sub = self.password[i:i+size]
                if self.password.count(sub) > 1:
                    return True
        return False

    # --- ENTROPY & CRACK TIMES ---

    def effective_entropy(self) -> float:
        """Matches entropy bits to the guess engine log10 result."""
        guesses = self._estimate_pattern_guesses()
        if guesses <= 1:
            return 0.0
        return round(math.log2(guesses), 2)

    def _format_time(self, seconds: float) -> str:
        if seconds < 1:
            return "Instant"
        units = [("years", 31536000), ("days", 86400),
                 ("hours", 3600), ("minutes", 60), ("seconds", 1)]
        for name, count in units:
            value = seconds // count
            if value >= 1:
                return f"{int(value)} {name}"
        return "Instant"

    def crack_time_estimates(self) -> Dict[str, str]:
        guesses = self._estimate_pattern_guesses()
        scenarios = {
            "online_throttled_100ps": 100,
            "online_unthrottled_10kps": 10_000,
            "offline_bcrypt_100kps": 100_000,
            "offline_fast_gpu_10Bps": 10_000_000_000
        }
        results = {}
        for name, rate in scenarios.items():
            results[name] = self._format_time(guesses / rate)

        charset_size = self.calculate_charset_size()
        if charset_size > 0:
            total_combinations = charset_size ** self.length
            results["classic_gpu_bruteforce"] = self._format_time(
                total_combinations / 10_000_000_000)
        else:
            results["classic_gpu_bruteforce"] = "Instant"
        return results

    # --- ROBUST GUESSING ENGINE ---

    def _estimate_pattern_guesses(self) -> float:
        if not self.password:
            return 0
        # Check against the 100k list first
        if self.normalized in COMMON_PASSWORDS:
            return 10.0

        remaining = self.normalized
        total_guesses = 1.0

        all_dicts = sorted(COMMON_WORDS | COMMON_NAMES |
                           SEASONS | MONTHS, key=len, reverse=True)
        for word in all_dicts:
            if word in remaining:
                total_guesses += 2000
                remaining = remaining.replace(word, "", 1)

        num_seq = re.search(r'\d+', remaining)
        if num_seq:
            seq_val = num_seq.group()
            if seq_val in "1234567890" or seq_val in "0987654321":
                total_guesses += 100
            else:
                total_guesses += (10 ** len(seq_val))
            remaining = remaining.replace(seq_val, "", 1)

        year_match = re.search(r'(19\d{2}|20\d{2})', remaining)
        if year_match:
            total_guesses += 3650
            remaining = remaining.replace(year_match.group(), "", 1)

        if remaining:
            charset_size = self.calculate_charset_size() or 26
            total_guesses *= (charset_size ** len(remaining))

        if self.password != self.password.lower():
            total_guesses *= 2
        if self.detect_leet_speak():
            total_guesses *= 1.5

        return total_guesses

    def get_zxcvbn_score(self) -> Dict:
        guesses = self._estimate_pattern_guesses()
        log_guesses = math.log10(guesses) if guesses > 0 else 0
        if log_guesses < 4:
            score, meaning = 0, "⚠️ Extremely Guessable"
        elif log_guesses < 7:
            score, meaning = 1, "❌ Weak (Pattern Found)"
        elif log_guesses < 9:
            score, meaning = 2, "OK (Fairly Unguessable)"
        elif log_guesses < 11:
            score, meaning = 3, "✅ Safely Unguessable"
        else:
            score, meaning = 4, "🛡️ Extremely Secure"
        return {"score": score, "guesses": int(guesses), "guesses_log10": round(log_guesses, 2), "meaning": meaning}

    def check_pwned_password(self) -> int:
        sha1 = hashlib.sha1(self.password.encode("utf-8")).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            res = requests.get(url, timeout=5)
            if res.status_code != 200:
                return -1
            for line in res.text.splitlines():
                h, count = line.split(":")
                if h == suffix:
                    return int(count)
            return 0
        except requests.RequestException:
            return -1

    def calculate_strength_score(self) -> Tuple[int, str]:
        entropy = self.effective_entropy()
        score = min(100, int((entropy / 80) * 100))
        if score < 20:
            rating = "VERY WEAK"
        elif score < 40:
            rating = "WEAK"
        elif score < 60:
            rating = "FAIR"
        elif score < 75:
            rating = "STRONG"
        elif score < 90:
            rating = "VERY STRONG"
        else:
            rating = "EXCELLENT"
        return score, rating

    def get_full_analysis(self) -> Dict:
        score, rating = self.calculate_strength_score()
        return {
            "password": self.password,
            "score": score,
            "rating": rating,
            "shannon_entropy": round(self.shannon_entropy(), 2),
            "theoretical_entropy": round(self.theoretical_entropy(), 2),
            "effective_entropy": self.effective_entropy(),
            "length": self.length,
            "charset_size": self.calculate_charset_size(),
            "unique_chars": len(set(self.password)),
            "spatial_complexity": self.calculate_spatial_complexity(),
            "character_sets": self.get_character_sets(),
            "patterns_detected": {
                "common_password": self.detect_common_password(),
                "dictionary_words": self.detect_dictionary_words(),
                "year": self.detect_year(),
                "leet_speak": self.detect_leet_speak(),
                "casing": self.detect_casing_mix(),
                "sequential": self.detect_sequential_patterns(),
                "keyboard_walk": self.detect_keyboard_patterns(),
                "repeated_substrings": self.detect_repeated_substrings(),
            },
            "crack_time_estimates": self.crack_time_estimates(),
            "pwned_count": self.check_pwned_password(),
            "attacker_analysis": self.get_zxcvbn_score()
        }


# ==========================================================
# GENERATORS
# ==========================================================

class EnterprisePasswordGenerator:
    @staticmethod
    def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_numbers=True, use_special=True, exclude_ambiguous=False) -> str:
        if length < 4:
            raise ValueError("Password length must be at least 4.")
        chars = ""
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not chars:
            raise ValueError("At least one character set required.")
        if exclude_ambiguous:
            for c in "O0l1I|":
                chars = chars.replace(c, "")

        password = []
        if use_lowercase:
            password.append(secrets.choice(string.ascii_lowercase))
        if use_uppercase:
            password.append(secrets.choice(string.ascii_uppercase))
        if use_numbers:
            password.append(secrets.choice(string.digits))
        if use_special:
            password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))

        for _ in range(length - len(password)):
            password.append(secrets.choice(chars))

        secrets.SystemRandom().shuffle(password)
        return ''.join(password)

    @staticmethod
    def generate_passphrase(num_words=4, separator="-", capitalize=False, include_number=False) -> str:
        words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa", "quebec", "romeo",
                 "sierra", "tango", "uniform", "victor", "whiskey", "xray", "yankee", "zulu", "cipher", "encrypt", "secure", "shield", "guard", "protect", "fortress", "vault", "lock", "token"]
        selected = [secrets.choice(words) for _ in range(num_words)]
        if capitalize:
            selected = [w.capitalize() for w in selected]
        phrase = separator.join(selected)
        if include_number:
            phrase += str(secrets.randbelow(100))
        return phrase
