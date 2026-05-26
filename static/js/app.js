/**
 * app.js — Lógica frontend para Madero H2O: Guardián del Agua
 * Maneja: módulos, upload de imágenes, geoloc, análisis IA, mapa
 */

// ─── Estado global ────────────────────────────────────────────
const State = {
  moduloActivo: null,
  imagenB64: null,
  imagenNombre: null,
  latitud: null,
  longitud: null,
  geoObtenida: false,
};

// ─── Configuración de módulos ─────────────────────────────────
const MODULOS_CONFIG = {
  fuga: {
    label: "Monitor de Fugas",
    icon: "💧",
    color: "#e63946",
    geo: true, // requiere geolocalización
  },
  lirio: {
    label: "Alerta de Lirio Acuático",
    icon: "🌿",
    color: "#52b788",
    geo: false,
  },
  calidad: {
    label: "Calidad del Agua",
    icon: "🔬",
    color: "#00b4d8",
    geo: false,
  },
};

// ─── DOM References ───────────────────────────────────────────
const uploadSection  = document.getElementById("upload-section");
const resultsSection = document.getElementById("results-section");
const dropZone       = document.getElementById("drop-zone");
const fileInput      = document.getElementById("file-input");
const previewCont    = document.getElementById("preview-container");
const previewImg     = document.getElementById("preview-img");
const previewName    = document.getElementById("preview-name");
const btnAnalyze     = document.getElementById("btn-analyze");
const btnAnalyzeText = document.getElementById("btn-analyze-text");
const btnAnalyzeSpin = document.getElementById("btn-analyze-spinner");
const geoInfo        = document.getElementById("geo-info");
const geoText        = document.getElementById("geo-text");

// ─── Init ─────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  setupModuleCards();
  setupDropZone();
  setupFileInput();
  requestGeolocation();
});

// ─── Module Cards ─────────────────────────────────────────────
function setupModuleCards() {
  const cards = document.querySelectorAll(".module-card");
  cards.forEach((card) => {
    card.addEventListener("click", () => {
      const modulo = card.dataset.modulo;
      activateModule(modulo, card);
    });
  });
}

function activateModule(modulo, cardEl) {
  // Update state
  State.moduloActivo = modulo;
  State.imagenB64 = null;
  State.imagenNombre = null;

  // Update card UI
  document.querySelectorAll(".module-card").forEach((c) => c.classList.remove("active"));
  if (cardEl) cardEl.classList.add("active");

  // Show upload section
  uploadSection.classList.add("visible");

  // Update upload title
  const cfg = MODULOS_CONFIG[modulo];
  document.getElementById("upload-module-icon").textContent = cfg.icon;
  document.getElementById("upload-module-title").textContent = cfg.label;

  // Show/hide geo
  if (geoInfo) {
    geoInfo.style.display = cfg.geo ? "flex" : "none";
  }

  // Reset preview
  previewCont.classList.remove("visible");
  previewImg.src = "";
  previewName.textContent = "";
  if (fileInput) fileInput.value = "";

  // Hide results
  resultsSection.classList.remove("visible");

  // Scroll to upload section
  uploadSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ─── Drop Zone ────────────────────────────────────────────────
function setupDropZone() {
  if (!dropZone) return;

  dropZone.addEventListener("click", () => fileInput.click());

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
      processImageFile(file);
    } else {
      showToast("⚠️", "Archivo inválido", "Solo se aceptan imágenes (JPG, PNG, WEBP).", "media");
    }
  });
}

function setupFileInput() {
  if (!fileInput) return;
  fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) processImageFile(file);
  });
}

function processImageFile(file) {
  if (file.size > 10 * 1024 * 1024) {
    showToast("⚠️", "Imagen demasiado grande", "El límite es 10MB.", "alta");
    return;
  }

  const reader = new FileReader();
  reader.onload = (ev) => {
    State.imagenB64 = ev.target.result; // incluye el prefijo data:image/...
    State.imagenNombre = file.name;

    previewImg.src = State.imagenB64;
    previewName.textContent = file.name;
    previewCont.classList.add("visible");
  };
  reader.readAsDataURL(file);
}

// ─── Remove image ─────────────────────────────────────────────
function removeImage() {
  State.imagenB64 = null;
  State.imagenNombre = null;
  previewCont.classList.remove("visible");
  previewImg.src = "";
  if (fileInput) fileInput.value = "";
}

// ─── Geolocalización ──────────────────────────────────────────
function requestGeolocation() {
  if (!navigator.geolocation) return;

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      State.latitud = pos.coords.latitude;
      State.longitud = pos.coords.longitude;
      State.geoObtenida = true;
      if (geoText) {
        geoText.textContent = `Ubicación detectada: ${State.latitud.toFixed(4)}, ${State.longitud.toFixed(4)}`;
      }
    },
    () => {
      State.latitud = 22.2744;
      State.longitud = -97.8326;
      if (geoText) {
        geoText.textContent = "Usando ubicación por defecto: Ciudad Madero, Tam.";
      }
    },
    { timeout: 8000 }
  );
}

// ─── Análisis ─────────────────────────────────────────────────
async function analizarImagen() {
  if (!State.imagenB64) {
    showToast("📷", "Sin imagen", "Por favor selecciona o arrastra una imagen.", "media");
    return;
  }

  if (!State.moduloActivo) {
    showToast("ℹ️", "Selecciona un módulo", "Elige Fuga, Lirio o Calidad.", "baja");
    return;
  }

  // Loading state
  btnAnalyze.disabled = true;
  btnAnalyzeText.textContent = "Analizando con IA…";
  btnAnalyzeSpin.style.display = "block";
  resultsSection.classList.remove("visible");

  try {
    const payload = {
      imagen_b64: State.imagenB64,
    };

    if (State.moduloActivo === "fuga") {
      payload.latitud  = State.latitud;
      payload.longitud = State.longitud;
    }

    const resp = await fetch(`/analizar/${State.moduloActivo}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await resp.json();

    if (!resp.ok || data.error) {
      showToast("❌", "Error de análisis", data.error || "Intenta de nuevo.", "critica");
      return;
    }

    renderResults(data);

  } catch (err) {
    showToast("❌", "Error de conexión", err.message, "critica");
  } finally {
    btnAnalyze.disabled = false;
    btnAnalyzeText.textContent = "Analizar con IA";
    btnAnalyzeSpin.style.display = "none";
  }
}

// ─── Render Results ───────────────────────────────────────────
function renderResults(data) {
  const { modulo, label, resultado, severidad, reporte_id } = data;
  const cfg = MODULOS_CONFIG[modulo] || {};

  // Severity badge
  const sevEl = document.getElementById("result-severity");
  sevEl.className = `severity-badge severity-${severidad}`;
  const SEV_LABELS = { baja: "Severidad Baja", media: "Severidad Media", alta: "Severidad Alta", critica: "🚨 Crítico" };
  sevEl.textContent = SEV_LABELS[severidad] || severidad;

  // Module label
  document.getElementById("result-module-label").textContent = `${cfg.icon || ""} ${label}`;

  // Description
  document.getElementById("result-description").textContent =
    resultado.descripcion || "Análisis completado.";

  // Confidence bar
  const conf = resultado.confianza || 50;
  document.getElementById("confidence-fill").style.width = conf + "%";
  document.getElementById("confidence-value").textContent = Math.round(conf) + "%";

  // Recomendación
  const rec = resultado.recomendacion || resultado.recomendacion_brigada || "Mantente atento a nuevas actualizaciones.";
  document.getElementById("result-recomendacion").textContent = rec;

  // Result grid (campos específicos por módulo)
  const grid = document.getElementById("result-grid");
  grid.innerHTML = buildResultGrid(modulo, resultado);

  // Report ID
  if (reporte_id && reporte_id > 0) {
    document.getElementById("result-report-id").textContent = `Reporte #${reporte_id} guardado`;
  }

  // Show section
  resultsSection.classList.add("visible");
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

  // Toast notification
  const toastIcon = severidad === "critica" ? "🚨" : severidad === "alta" ? "⚠️" : "✅";
  showToast(toastIcon, "Análisis completado", `${label} — ${SEV_LABELS[severidad] || severidad}`, severidad);
}

function buildResultGrid(modulo, r) {
  let items = [];

  if (modulo === "fuga") {
    items = [
      { label: "Fuga detectada", value: r.fuga_detectada ? "✅ Sí" : "❌ No" },
      { label: "Tipo", value: formatKey(r.tipo) },
      { label: "Urgencia", value: formatKey(r.urgencia_reporte) },
    ];
  } else if (modulo === "lirio") {
    items = [
      { label: "Lirio detectado", value: r.lirio_detectado ? "✅ Sí" : "❌ No" },
      { label: "Cobertura estimada", value: r.cobertura_porcentaje != null ? r.cobertura_porcentaje + "%" : "—" },
      { label: "Desechos", value: r.desechos_detectados ? `Sí (${formatKey(r.tipo_desechos)})` : "No" },
      { label: "Urgencia brigada", value: formatKey(r.urgencia) },
    ];
  } else if (modulo === "calidad") {
    items = [
      { label: "Color", value: formatKey(r.color_predominante) },
      { label: "Turbidez", value: r.turbidez_nivel != null ? `${r.turbidez_nivel}/10 — ${formatKey(r.turbidez_descripcion)}` : "—" },
      { label: "Apto consumo", value: r.apto_consumo_humano ? "✅ Sí" : "❌ No" },
      { label: "Apto uso doméstico", value: r.apto_uso_domestico ? "✅ Sí" : "⚠️ Revisar" },
      { label: "Apto riego", value: r.apto_riego ? "✅ Sí" : "❌ No" },
    ];
  }

  return items
    .map(
      (item) => `
      <div class="result-item">
        <div class="result-item-label">${item.label}</div>
        <div class="result-item-value">${item.value}</div>
      </div>`
    )
    .join("");
}

function formatKey(val) {
  if (!val) return "—";
  return String(val)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

// ─── Close upload section ─────────────────────────────────────
function cerrarUpload() {
  uploadSection.classList.remove("visible");
  document.querySelectorAll(".module-card").forEach((c) => c.classList.remove("active"));
  State.moduloActivo = null;
}

// ─── Toast notifications ──────────────────────────────────────
function showToast(icon, title, msg, level = "baja") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `
    <div class="toast-icon">${icon}</div>
    <div class="toast-body">
      <div class="toast-title">${title}</div>
      <div class="toast-msg">${msg}</div>
    </div>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(20px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ─── Nueva foto ───────────────────────────────────────────────
function nuevaFoto() {
  resultsSection.classList.remove("visible");
  removeImage();
  dropZone.scrollIntoView({ behavior: "smooth" });
}
