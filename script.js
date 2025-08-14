function run() {

    // ======= API =======
  async function apiPost(url, data) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  }

  // ======= Konfiguration =======
  const API_URL = "/api/control"; // ggf. anpassen
  const DEBOUNCE_MS = 80;
  const KEEPALIVE_MS = 1500;

  // ======= UI-Elemente =======
  const leftEl = document.getElementById("left");
  const rightEl = document.getElementById("right");
  const leftValEl = document.getElementById("leftVal");
  const rightValEl = document.getElementById("rightVal");
  const statusEl = document.getElementById("status");
  const netPill = document.getElementById("netPill");
  const stopBtn = document.getElementById("stopBtn");
  const centerBtn = document.getElementById("centerBtn");

  function updateLabels() {
    leftValEl.textContent = leftEl.value;
    rightValEl.textContent = rightEl.value;
  }
  updateLabels();

  let debounceTimer = null;
  let lastSent = "";

  async function sendOnce() {
    const payload = {
      left: Number(leftEl.value),
      right: Number(rightEl.value),
    };
    const json = JSON.stringify(payload);
    if (json === lastSent) return; // nichts Neues
    lastSent = json;

    try {
      const res = await apiPost(API_URL, payload);
      console.log("gesendet:", payload, "antwort:", res); // Debug
      statusEl.textContent = "gesendet";
      netPill.classList.remove("err");
      netPill.classList.add("ok");
      clearTimeout(window.__okTimer);
      window.__okTimer = setTimeout(() => { statusEl.textContent = "bereit"; }, 800);
    } catch (e) {
      console.error(e);
      statusEl.textContent = "Fehler beim Senden";
      netPill.classList.remove("ok");
      netPill.classList.add("err");
    }
  }

  function scheduleSend() {
    updateLabels();
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(sendOnce, DEBOUNCE_MS);
  }

  leftEl.addEventListener("input", scheduleSend);
  rightEl.addEventListener("input", scheduleSend);

  stopBtn.addEventListener("click", () => {
    leftEl.value = 0;
    rightEl.value = 0;
    scheduleSend();
  });

  centerBtn.addEventListener("click", () => {
    leftEl.value = 0;
    rightEl.value = 0;
    scheduleSend();
  });

  // Optionaler Keepalive, falls Motoren bei Stille abschalten
  setInterval(() => {
    if (Number(leftEl.value) === 0 && Number(rightEl.value) === 0) return;
    sendOnce();
  }, KEEPALIVE_MS);

} 

window.onload = run;