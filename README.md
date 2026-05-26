# 🌊 Madero H2O: Guardián del Agua

**Super-App de Cultura Hídrica para Ciudad Madero, Tamaulipas**

Aplicación web que integra **Inteligencia Artificial (Google Gemini Vision)** para el monitoreo hídrico ciudadano. Permite detectar fugas de agua, proliferación de lirio acuático y analizar la calidad del agua mediante fotografías.

---

## 🎯 Módulos

| Módulo | Descripción | Impacto |
|--------|-------------|---------|
| 💧 **Monitor de Fugas** | Detecta y clasifica fugas en vía pública | Reportes directos a COMAPA Sur |
| 🌿 **Alerta de Lirio** | Estima cobertura de lirio acuático en el Sistema Lagunario-Chairel | Priorización de brigadas de limpieza |
| 🔬 **Calidad del Agua** | Análisis colorimétrico y de turbidez | Guía de aptitud para consumo, uso doméstico o riego |

---

## 🏗️ Stack Tecnológico

- **Backend**: Python + Flask
- **IA/Visión**: Google Gemini 2.5 Flash (multimodal)
- **Base de datos**: SQLite + SQLAlchemy
- **Mapa**: Leaflet.js
- **Frontend**: HTML + CSS (Glassmorphism Dark Mode) + JavaScript vanilla
- **Deploy**: Vercel

---

## 🚀 Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/madero-h2o.git
cd madero-h2o

# 2. Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY

# 5. Ejecutar la aplicación
python app.py
```

La app estará disponible en: **http://localhost:5002**

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```env
GEMINI_API_KEY=tu_api_key_de_google_ai_studio
SECRET_KEY=madero-h2o-guardian-2025
```

Obtén tu API key gratis en: [Google AI Studio](https://aistudio.google.com/)

---

## 📡 Endpoints API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Página principal |
| `GET` | `/dashboard` | Panel de administración |
| `POST` | `/analizar/fuga` | Analiza imagen de posible fuga |
| `POST` | `/analizar/lirio` | Analiza imagen de lirio acuático |
| `POST` | `/analizar/calidad` | Analiza calidad del agua |
| `GET` | `/reportes` | JSON de todos los reportes |
| `GET` | `/estadisticas` | Estadísticas generales |

### Formato de Request (POST /analizar/\<modulo\>)

```json
{
  "imagen_b64": "data:image/jpeg;base64,...",
  "latitud": 22.2744,
  "longitud": -97.8326
}
```

---

## 🌐 Deploy en Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Importar este repositorio en [Vercel](https://vercel.com)
2. Configurar la variable de entorno `GEMINI_API_KEY` en Settings → Environment Variables
3. Deploy automático ✅

> **Nota**: En Vercel (serverless), los datos en SQLite persisten solo durante la sesión. El mapa de calor mostrará datos de demostración más los reportes de la sesión actual.

---

## 📍 Contexto Local

- **Ciudad**: Ciudad Madero, Tamaulipas, México
- **Organismos de agua**: COMAPA Sur, CAEAT
- **Cuerpos de agua**: Laguna del Chairel, Laguna del Carpintero, canales de Ciudad Madero
- **Problemática**: 40-60% de pérdida de agua por fugas en Latinoamérica; lirio acuático obstruye el flujo en el sistema lagunario

---

## 📄 Licencia

MIT License — Proyecto Académico, Programación Web, 10mo Semestre.

---

*Desarrollado con ❤️ para Ciudad Madero, Tamaulipas*
