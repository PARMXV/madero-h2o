"""
app.py — Backend principal de Madero H2O: Guardián del Agua
Flask + Google Gemini Vision para análisis de imágenes hídricas
"""

import os
import json
import base64
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "madero-h2o-2025")

# ─── Lazy initialization — evita crashes al importar en Vercel ───────────────

_gemini_client = None
_db_initialized = False


def get_gemini_client():
    """Inicializa el cliente de Gemini de forma lazy."""
    global _gemini_client
    if _gemini_client is None:
        from google import genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no configurada en las variables de entorno.")
        _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client


def ensure_db():
    """Inicializa la base de datos de forma lazy la primera vez que se necesita."""
    global _db_initialized
    if not _db_initialized:
        from models import init_db
        try:
            init_db()
        except Exception as e:
            print(f"[WARN] DB init falló (modo sin-persistencia): {e}")
        _db_initialized = True


# ─── Importaciones del proyecto ───────────────────────────────────────────────

from prompts import get_prompt_fuga, get_prompt_lirio, get_prompt_calidad

# ─── Mapeo de módulos ─────────────────────────────────────────────────────────

MODULOS = {
    "fuga": {
        "prompt_fn": get_prompt_fuga,
        "campo_severidad": "severidad",
        "label": "Fuga de Agua",
    },
    "lirio": {
        "prompt_fn": get_prompt_lirio,
        "campo_severidad": "urgencia",
        "label": "Lirio Acuático",
    },
    "calidad": {
        "prompt_fn": get_prompt_calidad,
        "campo_severidad": "turbidez_descripcion",
        "label": "Calidad del Agua",
    },
}

SEVERIDAD_NORM = {
    # fugas
    "ninguna": "baja",
    "baja": "baja",
    "media": "media",
    "alta": "alta",
    "critica": "critica",
    # lirio (urgencia → severidad)
    "sin_urgencia": "baja",
    "sin urgencia": "baja",
    # calidad (turbidez → severidad)
    "cristalina": "baja",
    "ligeramente_turbia": "baja",
    "turbia": "media",
    "muy_turbia": "alta",
    "opaca": "critica",
}


def normalizar_severidad(valor: str) -> str:
    if not valor:
        return "media"
    return SEVERIDAD_NORM.get(valor.lower(), "media")


def limpiar_json(texto: str) -> str:
    """Limpia respuesta de la API si aún viene envuelta en markdown."""
    texto = texto.strip()
    if texto.startswith("```"):
        texto = re.sub(r"^```(?:json)?\s*", "", texto)
        texto = re.sub(r"\s*```$", "", texto)
    return texto.strip()


# ─── Rutas ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    ensure_db()
    try:
        from models import obtener_estadisticas
        stats = obtener_estadisticas()
    except Exception:
        stats = {"total": 0, "fugas": 0, "lirio": 0, "calidad": 0, "criticas": 0}
    return render_template("dashboard.html", stats=stats)


@app.route("/reportes")
def reportes():
    """Endpoint JSON para el mapa de calor."""
    ensure_db()
    try:
        from models import obtener_reportes
        limite = request.args.get("limite", 100, type=int)
        datos = obtener_reportes(limite=limite)
    except Exception:
        datos = []
    return jsonify({"reportes": datos, "total": len(datos)})


@app.route("/estadisticas")
def estadisticas():
    ensure_db()
    try:
        from models import obtener_estadisticas
        return jsonify(obtener_estadisticas())
    except Exception:
        return jsonify({"total": 0, "fugas": 0, "lirio": 0, "calidad": 0, "criticas": 0})


@app.route("/analizar/<modulo>", methods=["POST"])
def analizar(modulo: str):
    """Endpoint orquestador: recibe imagen + contexto y delega al prompt correcto."""
    if modulo not in MODULOS:
        return jsonify({"error": f"Módulo '{modulo}' no reconocido. Usa: fuga, lirio, calidad"}), 400

    try:
        from google.genai import types

        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos."}), 400

        imagen_b64 = data.get("imagen_b64", "").strip()
        if not imagen_b64:
            return jsonify({"error": "No se proporcionó imagen."}), 400

        # Extraer mime type si viene con prefijo data:image/...
        mime_type = "image/jpeg"
        if imagen_b64.startswith("data:"):
            header, imagen_b64 = imagen_b64.split(",", 1)
            if "image/png" in header:
                mime_type = "image/png"
            elif "image/webp" in header:
                mime_type = "image/webp"
            elif "image/gif" in header:
                mime_type = "image/gif"

        # Geolocalización (solo fuga)
        latitud = data.get("latitud")
        longitud = data.get("longitud")

        # Coordenadas por defecto: Centro de Ciudad Madero
        lat_final = float(latitud) if latitud is not None else 22.2744
        lon_final = float(longitud) if longitud is not None else -97.8326

        # Construir contenido multimodal para Gemini
        prompt_texto = MODULOS[modulo]["prompt_fn"]()
        imagen_bytes = base64.b64decode(imagen_b64)

        contenido = [
            types.Part.from_bytes(data=imagen_bytes, mime_type=mime_type),
            types.Part.from_text(text=prompt_texto),
        ]

        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contenido,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=4096,
                response_mime_type="application/json",
            ),
        )

        raw = limpiar_json(response.text)

        try:
            resultado = json.loads(raw)
        except json.JSONDecodeError as e:
            return jsonify({"error": f"No se pudo interpretar la respuesta de Gemini: {str(e)}"}), 500

        # Determinar severidad normalizada
        campo_sev = MODULOS[modulo]["campo_severidad"]
        severidad_raw = resultado.get(campo_sev, "media")
        severidad = normalizar_severidad(str(severidad_raw))

        descripcion = resultado.get("descripcion", "Sin descripción disponible.")
        confianza = resultado.get("confianza", 50)

        # Guardar en base de datos (falla silenciosamente si DB no disponible)
        reporte_id = -1
        ensure_db()
        try:
            from models import guardar_reporte
            datos_extra = json.dumps(resultado)
            reporte_id = guardar_reporte(
                modulo=modulo,
                latitud=lat_final,
                longitud=lon_final,
                severidad=severidad,
                descripcion=descripcion,
                confianza=float(confianza),
                datos_extra=datos_extra,
            )
        except Exception as db_err:
            print(f"[WARN] No se pudo guardar en DB: {db_err}")

        return jsonify({
            "modulo": modulo,
            "label": MODULOS[modulo]["label"],
            "resultado": resultado,
            "severidad": severidad,
            "reporte_id": reporte_id,
            "coordenadas": {"lat": lat_final, "lon": lon_final},
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "api key" in error_msg.lower():
            return jsonify({"error": "API Key inválida o no configurada en Vercel."}), 500
        if "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return jsonify({"error": "Límite de solicitudes alcanzado. Intenta en un momento."}), 429
        return jsonify({"error": f"Error interno: {error_msg}"}), 500


if __name__ == "__main__":
    ensure_db()
    app.run(debug=True, port=5002)
