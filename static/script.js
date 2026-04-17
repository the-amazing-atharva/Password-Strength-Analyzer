// ==========================================================
// PASSWORD ANALYZER
// ==========================================================
async function analyzePassword() {
  const password = document.getElementById("passwordInput").value;
  if (!password) return;

  const response = await fetch("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });

  const data = await response.json();
  const bar = document.getElementById("strengthBar");
  const text = document.getElementById("strengthText");
  const results = document.getElementById("analysisResults");

  // Update Attacker Analysis Section
  const attackerSec = document.getElementById("attackerSection");
  const attackerMeaning = document.getElementById("attackerMeaning");
  const attackerGuesses = document.getElementById("attackerGuesses");

  attackerSec.classList.remove("hidden");
  attackerMeaning.innerText = `Estimate: ${data.attacker_analysis.meaning}`;
  attackerGuesses.innerText = `Attacker would need approx. 10^${data.attacker_analysis.guesses_log10} guesses.`;

  // Strength bar
  bar.style.width = data.score + "%";
  if (data.score < 40) bar.className = "h-4 rounded-full bg-red-500";
  else if (data.score < 70) bar.className = "h-4 rounded-full bg-yellow-500";
  else bar.className = "h-4 rounded-full bg-green-500";

  text.innerText = `${data.score}/100 - ${data.rating}`;

  // -------------------------
  // FULL Results Display
  // -------------------------
  results.innerHTML = `
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-black/20 p-4 rounded-xl border border-white/5">
        <h4 class="font-bold text-indigo-300 mb-2">📊 Entropy & Metrics</h4>
        <ul class="space-y-1 opacity-90">
          <li>• Shannon Entropy: <strong>${data.shannon_entropy} bits</strong></li>
          <li>• Effective Entropy: <strong>${data.effective_entropy} bits</strong></li>
          <li>• Theoretical Entropy: <strong>${data.theoretical_entropy} bits</strong></li>
          <li>• Length: <strong>${data.length}</strong></li>
          <li>• Unique Characters: <strong>${data.unique_chars}</strong></li>
          <li>• Charset Size: <strong>${data.charset_size}</strong></li>
          <li>• Spatial Complexity: <strong>${data.spatial_complexity}</strong></li>
        </ul>
      </div>

      <div class="bg-black/20 p-4 rounded-xl border border-white/5">
        <h4 class="font-bold text-indigo-300 mb-2">🔍 Patterns Detected</h4>
        <ul class="space-y-1 opacity-90">
          <li>• Casing Style: <strong>${data.patterns_detected.casing}</strong></li>
          <li>• Dictionary Words: <strong>${data.patterns_detected.dictionary_words.join(", ") || "None"}</strong></li>
          <li>• Leet Speak: <strong>${data.patterns_detected.leet_speak ? "Detected" : "None"}</strong></li>
          <li>• Year Detected: <strong>${data.patterns_detected.year ? "Detected" : "None"}</strong></li>
          <li>• Sequential (abc/123): <strong>${data.patterns_detected.sequential ? "Detected" : "None"}</strong></li>
          <li>• Keyboard Walk: <strong>${data.patterns_detected.keyboard_walk ? "Detected" : "None"}</strong></li>
          <li>• Repeated Substrings: <strong>${data.patterns_detected.repeated_substrings ? "Detected" : "None"}</strong></li>
          <li>• Common Password: <strong>${data.patterns_detected.common_password ? "⚠️ YES" : "No"}</strong></li>
        </ul>
      </div>
    </div>

    <div class="bg-black/20 p-4 rounded-xl mt-4 border border-white/5">
      <h4 class="font-bold text-indigo-300 mb-2">⏱ Estimated Crack Times (Effective)</h4>
      <div id="crackTimes" class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs"></div>
    </div>
  `;

  // Dynamically populate crack times
  const crackTimesContainer = document.getElementById("crackTimes");
  for (const [key, value] of Object.entries(data.crack_time_estimates)) {
    const p = document.createElement("p");
    const name = key
      .replace(/_/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase());
    p.innerHTML = `<span class="opacity-70">${name}:</span> <strong>${value}</strong>`;
    crackTimesContainer.appendChild(p);
  }
}

// ==========================================================
// PWNED / BREACH CHECK
// ==========================================================
async function checkPwnedPassword(password) {
  const warningEl = document.getElementById("pwnedWarning");
  if (!password) {
    warningEl.innerText = "";
    return;
  }
  warningEl.innerText = "Checking...";
  try {
    const res = await fetch("/pwned", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    const data = await res.json();
    if (data.pwned) {
      warningEl.innerHTML = `⚠ Found in breaches ${data.count} times!`;
      warningEl.className =
        "mt-2 font-bold text-white bg-red-700/50 p-2 rounded-xl animate-pulse";
    } else {
      warningEl.innerHTML = "✅ Not found in known breaches.";
      warningEl.className =
        "mt-2 font-semibold text-white bg-green-700/50 p-2 rounded-xl";
    }
  } catch (err) {
    warningEl.innerText = "Error checking API";
  }
}

// ==========================================================
// GENERATORS
// ==========================================================
async function generatePassword() {
  const length = document.getElementById("length").value;
  const res = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      length,
      uppercase: document.getElementById("uppercase").checked,
      lowercase: document.getElementById("lowercase").checked,
      numbers: document.getElementById("numbers").checked,
      special: document.getElementById("special").checked,
      exclude_ambiguous: document.getElementById("excludeAmbiguous").checked,
    }),
  });
  const data = await res.json();
  document.getElementById("generatedPassword").value = data.password;
}

async function generatePassphrase() {
  const res = await fetch("/passphrase", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      words: document.getElementById("words").value,
      separator: document.getElementById("separator").value,
      capitalize: document.getElementById("capitalize").checked,
      include_number: document.getElementById("includeNumber").checked,
    }),
  });
  const data = await res.json();
  document.getElementById("generatedPassphrase").value = data.passphrase;
}

// ==========================================================
// UTILITIES (UPDATED)
// ==========================================================

// New: Toggles the Entropy Explanation Panel
function toggleEntropyInfo() {
  const info = document.getElementById("entropyInfo");
  if (info) {
    info.classList.toggle("hidden");
  }
}

// Fixed: Toggles the Breach Info Panel
function toggleBreachInfo() {
  const info = document.getElementById("breachInfo");
  if (info) {
    info.classList.toggle("hidden");
  }
}

// Fixed: Clears the Pwned Input field and warnings
function clearPwnedInput() {
  const input = document.getElementById("pwnedInput");
  const warning = document.getElementById("pwnedWarning");
  if (input) input.value = "";
  if (warning) {
    warning.innerText = "";
    warning.className = ""; // Reset background colors/animations
  }
}

function copyPassword() {
  const field = document.getElementById("generatedPassword");
  field.select();
  document.execCommand("copy");
}

function copyPassphrase() {
  const field = document.getElementById("generatedPassphrase");
  field.select();
  document.execCommand("copy");
}

function toggleVisibility() {
  const i = document.getElementById("passwordInput");
  i.type = i.type === "password" ? "text" : "password";
}
