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

  // -------------------------
  // Strength bar
  // -------------------------
  bar.style.width = data.score + "%";
  if (data.score < 40) bar.className = "h-4 rounded-full bg-red-500";
  else if (data.score < 70) bar.className = "h-4 rounded-full bg-yellow-500";
  else bar.className = "h-4 rounded-full bg-green-500";

  // -------------------------
  // Score & rating
  // -------------------------
  text.innerText = `${data.score}/100 - ${data.rating}`;

  // -------------------------
  // Detailed analysis
  // -------------------------
  results.innerHTML = `
    <p>🔐 <strong>Shannon Entropy:</strong> ${data.shannon_entropy} bits</p>
    <p>📊 <strong>Theoretical Entropy:</strong> ${data.theoretical_entropy} bits</p>
    <p>⚡ <strong>Effective Entropy:</strong> ${data.effective_entropy} bits</p>
    <p>📏 <strong>Length:</strong> ${data.length}</p>
    <p>🧮 <strong>Character Sets:</strong> ${Object.entries(data.character_sets)
      .filter(([k, v]) => v)
      .map(([k]) => k)
      .join(", ")}</p>
    <p>🔣 <strong>Charset Size:</strong> ${data.charset_size}</p>
    <p>⏱ <strong>Estimated Crack Times:</strong></p>
  `;

  // -------------------------
  // Dynamically list crack times
  // -------------------------
  const crackTimesUL = document.createElement("ul");
  crackTimesUL.className = "ml-4 list-disc";

  for (const [key, value] of Object.entries(data.crack_time_estimates)) {
    const li = document.createElement("li");
    const name = key
      .replace(/_/g, " ")
      .replace(/\b\w/g, (c) => c.toUpperCase()); // Capitalize words
    li.textContent = `${name}: ${value}`;
    crackTimesUL.appendChild(li);
  }

  results.appendChild(crackTimesUL);

  // -------------------------
  // Patterns detected
  // -------------------------
  results.innerHTML += `
    <p>⚠ <strong>Patterns Detected:</strong></p>
    <ul class="ml-4 list-disc">
      <li>Common Password: ${data.patterns_detected.common_password}</li>
      <li>Dictionary Words: ${data.patterns_detected.dictionary_words.join(", ") || "None"}</li>
      <li>Year: ${data.patterns_detected.year}</li>
      <li>Word+Year: ${data.patterns_detected.word_year}</li>
      <li>Season+Year: ${data.patterns_detected.season_year}</li>
      <li>Month+Year: ${data.patterns_detected.month_year}</li>
      <li>Name+Number: ${data.patterns_detected.name_number}</li>
      <li>Sequential: ${data.patterns_detected.sequential}</li>
      <li>Keyboard Walk: ${data.patterns_detected.keyboard_walk}</li>
      <li>Repeated Substrings: ${data.patterns_detected.repeated_substrings}</li>
    </ul>
  `;
}

async function generatePassword() {
  const length = document.getElementById("length").value;
  const use_uppercase = document.getElementById("uppercase").checked;
  const use_lowercase = document.getElementById("lowercase").checked;
  const use_numbers = document.getElementById("numbers").checked;
  const use_special = document.getElementById("special").checked;
  const exclude_ambiguous = document.getElementById("excludeAmbiguous").checked;

  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      length,
      uppercase: use_uppercase,
      lowercase: use_lowercase,
      numbers: use_numbers,
      special: use_special,
      exclude_ambiguous,
    }),
  });

  const data = await response.json();
  document.getElementById("generatedPassword").value = data.password;
}

async function generatePassphrase() {
  const words = document.getElementById("words").value;
  const separator = document.getElementById("separator").value;
  const capitalize = document.getElementById("capitalize").checked;
  const includeNumber = document.getElementById("includeNumber").checked;

  const response = await fetch("/passphrase", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      words,
      separator,
      capitalize,
      include_number: includeNumber,
    }),
  });

  const data = await response.json();
  document.getElementById("generatedPassphrase").value = data.passphrase;
}

function copyPassword() {
  const field = document.getElementById("generatedPassword");
  field.select();
  document.execCommand("copy");
  alert("Copied to clipboard!");
}

function copyPassphrase() {
  const field = document.getElementById("generatedPassphrase");
  field.select();
  document.execCommand("copy");
  alert("Copied to clipboard!");
}

function toggleVisibility() {
  const input = document.getElementById("passwordInput");
  input.type = input.type === "password" ? "text" : "password";
}
