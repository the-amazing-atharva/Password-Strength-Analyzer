from typing import Dict, List, Tuple
import string
import secrets
import math
import re
from datetime import datetime
import hashlib
import requests  # NEW: for breach check


# ==========================================================
# GLOBAL INTELLIGENCE CONFIGURATION
# ==========================================================

CURRENT_YEAR = datetime.now().year
MIN_YEAR = 1950
MAX_YEAR = CURRENT_YEAR + 5

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "12345678", "12345",
    "1234567", "password1", "123123", "1234567890",
    "qwerty", "abc123", "111111", "1234", "admin",
    "letmein", "welcome", "monkey", "dragon",
    "master", "sunshine", "princess", "login",
    "admin123", "solo", "1q2w3e4r", "starwars",
    "qwertyuiop", "654321", "batman", "superman"
}

COMMON_WORDS = {
    "password", "pass", "admin", "user",
    "root", "login", "welcome", "company",
    "test", "guest"
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
# ENTERPRISE PASSWORD ANALYZER
# ==========================================================

class EnterprisePasswordAnalyzer:
    """
    Industrial-grade password intelligence engine.
    Combines entropy modeling + structural pattern analysis +
    dictionary intelligence + attacker simulation.
    """

    def __init__(self, password: str):
        self.password = password
        self.length = len(password)
        self.normalized = self._normalize_leet(password)

    # ------------------------------------------------------
    # Normalization
    # ------------------------------------------------------

    def _normalize_leet(self, text: str) -> str:
        return text.lower().translate(LEET_MAP)

    # ------------------------------------------------------
    # Character Set Analysis
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # ENTROPY CALCULATIONS
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # ADVANCED PATTERN DETECTION
    # ------------------------------------------------------

    def detect_common_password(self) -> bool:
        return self.normalized in COMMON_PASSWORDS

    def detect_dictionary_words(self) -> List[str]:
        found = []
        for word in COMMON_WORDS:
            if word in self.normalized:
                found.append(word)
        return found

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

    # ------------------------------------------------------
    # EFFECTIVE ENTROPY MODEL
    # ------------------------------------------------------

    def effective_entropy(self) -> float:
        entropy = self.theoretical_entropy()

        penalty = 0

        if self.detect_common_password():
            penalty += 40

        penalty += len(self.detect_dictionary_words()) * 10

        if self.detect_year():
            penalty += 10

        if self.detect_word_year():
            penalty += 15

        if self.detect_season_year() or self.detect_month_year():
            penalty += 15

        if self.detect_name_number():
            penalty += 10

        if self.detect_sequential_patterns():
            penalty += 10

        if self.detect_keyboard_patterns():
            penalty += 15

        if self.detect_repeated_substrings():
            penalty += 15

        return max(0, entropy - penalty)

    # ------------------------------------------------------
    # CRACK TIME SIMULATION
    # ------------------------------------------------------

    def _format_time(self, seconds: float) -> str:
        if seconds < 1:
            return "Instant"
        units = [
            ("years", 31536000),
            ("days", 86400),
            ("hours", 3600),
            ("minutes", 60),
            ("seconds", 1),
        ]
        for name, count in units:
            value = seconds // count
            if value >= 1:
                return f"{int(value)} {name}"
        return "Instant"

    def crack_time_estimates(self) -> Dict[str, str]:
        entropy = self.effective_entropy()
        guesses = 2 ** entropy

        scenarios = {
            "online_throttled_100ps": 100,
            "online_unthrottled_10kps": 10_000,
            "offline_bcrypt_100kps": 100_000,
            "offline_fast_gpu_10Bps": 10_000_000_000
        }

        results = {}
        for name, rate in scenarios.items():
            seconds = guesses / rate
            results[name] = self._format_time(seconds)

        # Classic GPU brute-force
        charset_size = self.calculate_charset_size()
        if charset_size > 0:
            total_combinations = charset_size ** self.length
            seconds_gpu = total_combinations / 10_000_000_000
            results["classic_gpu_bruteforce"] = self._format_time(seconds_gpu)
        else:
            results["classic_gpu_bruteforce"] = "Instant"

        return results

    # ------------------------------------------------------
    # BREACH CHECK USING HAVE I BEEN PWNED
    # ------------------------------------------------------

    def check_pwned_password(self) -> int:
        """
        Returns number of times password appears in breaches.
        0 = safe, -1 = API error.
        """
        sha1 = hashlib.sha1(self.password.encode("utf-8")).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        try:
            res = requests.get(url, timeout=5)
            if res.status_code != 200:
                return -1
            hashes = res.text.splitlines()
            for line in hashes:
                h, count = line.split(":")
                if h == suffix:
                    return int(count)
            return 0
        except requests.RequestException:
            return -1

    # ------------------------------------------------------
    # ENTERPRISE SCORING (0–100)
    # ------------------------------------------------------

    def calculate_strength_score(self) -> Tuple[int, str]:
        entropy = self.effective_entropy()
        score = min(100, int((entropy / 120) * 100))
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

    # ------------------------------------------------------
    # FULL ENTERPRISE REPORT
    # ------------------------------------------------------

    def get_full_analysis(self) -> Dict:
        score, rating = self.calculate_strength_score()
        pwned_count = self.check_pwned_password()  # NEW

        return {
            "password": self.password,
            "length": self.length,
            "shannon_entropy": round(self.shannon_entropy(), 2),
            "theoretical_entropy": round(self.theoretical_entropy(), 2),
            "effective_entropy": round(self.effective_entropy(), 2),
            "log10_guess_space": round(
                math.log10(2 ** self.effective_entropy()
                           ) if self.effective_entropy() > 0 else 0, 2
            ),
            "character_sets": self.get_character_sets(),
            "charset_size": self.calculate_charset_size(),
            "patterns_detected": {
                "common_password": self.detect_common_password(),
                "dictionary_words": self.detect_dictionary_words(),
                "year": self.detect_year(),
                "word_year": self.detect_word_year(),
                "season_year": self.detect_season_year(),
                "month_year": self.detect_month_year(),
                "name_number": self.detect_name_number(),
                "sequential": self.detect_sequential_patterns(),
                "keyboard_walk": self.detect_keyboard_patterns(),
                "repeated_substrings": self.detect_repeated_substrings(),
            },
            "score": score,
            "rating": rating,
            "crack_time_estimates": self.crack_time_estimates(),
            "pwned_count": pwned_count  # NEW
        }


# ==========================================================
# ENTERPRISE PASSWORD GENERATOR (UNCHANGED)
# ==========================================================

class EnterprisePasswordGenerator:
    @staticmethod
    def generate_password(
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_numbers: bool = True,
        use_special: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
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
            ambiguous = "O0l1I|"
            chars = ''.join(c for c in chars if c not in ambiguous)
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
    def generate_passphrase(
        num_words: int = 4,
        separator: str = "-",
        capitalize: bool = False,
        include_number: bool = False
    ) -> str:
        words = [
            "alpha", "bravo", "charlie", "delta", "echo",
            "foxtrot", "golf", "hotel", "india", "juliet",
            "kilo", "lima", "mike", "november", "oscar",
            "papa", "quebec", "romeo", "sierra", "tango",
            "uniform", "victor", "whiskey", "xray",
            "yankee", "zulu", "cipher", "encrypt",
            "secure", "shield", "guard", "protect",
            "fortress", "vault", "lock", "token"
        ]
        selected = [secrets.choice(words) for _ in range(num_words)]
        if capitalize:
            selected = [w.capitalize() for w in selected]
        phrase = separator.join(selected)
        if include_number:
            phrase += str(secrets.randbelow(100))
        return phrase
