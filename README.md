<div align="center">

<img src="https://img.shields.io/badge/version-1.0.0-00b4d8?style=for-the-badge&logo=water" alt="version"/>
<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python"/>
<img src="https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white" alt="flask"/>
<img src="https://img.shields.io/badge/Gemini_Vision-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="gemini"/>
<img src="https://img.shields.io/badge/Vercel-Deploy-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="vercel"/>

<br/><br/>

# 🌊 Madero H2O: Guardián del Agua

### Super-App de Cultura Hídrica con Inteligencia Artificial

**Ciudad Madero, Tamaulipas, México**

*Monitoreo ciudadano de fugas · Lirio acuático · Calidad del agua*

<br/>

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

</div>

---

## 📋 Tabla de Contenidos

- [¿Qué es Madero H2O?](#-qué-es-madero-h2o)
- [Problemática Local](#-problemática-local)
- [Módulos de IA](#-módulos-de-ia)
- [Arquitectura](#-arquitectura)
- [Stack Tecnológico](#-stack-tecnológico)
- [Instalación Local](#-instalación-local)
- [Variables de Entorno](#-variables-de-entorno)
- [Endpoints API](#-endpoints-api)
- [Deploy en Vercel](#-deploy-en-vercel)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contexto e Impacto Local](#-contexto-e-impacto-local)
- [Licencia](#-licencia)

---

## 💡 ¿Qué es Madero H2O?

**Madero H2O: Guardián del Agua** es una aplicación web de **cultura hídrica ciudadana** diseñada específicamente para Ciudad Madero, Tamaulipas. Permite a los ciudadanos reportar y analizar problemas hídricos usando únicamente la cámara de su dispositivo, con el respaldo de un **agente de Inteligencia Artificial basado en Google Gemini Vision**.

> El sistema transforma a cada ciudadano en un **guardián activo del agua**, convirtiendo una fotografía en un reporte estructurado que llega directamente a las autoridades competentes.

---

## 🌍 Problemática Local

| Problema | Impacto |
|----------|---------|
| 💧 **Fugas no reportadas** | Entre el **40% y 60%** del agua se pierde por fugas no detectadas a tiempo en Latinoamérica |
| 🌿 **Lirio acuático** | La proliferación en la **Laguna del Chairel** obstruye el flujo y encarece la potabilización |
| 🔬 **Variaciones de calidad** | La posible **intrusión salina** en el sistema lagunario requiere monitoreo visual constante |

---

## 🤖 Módulos de IA

### 💧 Módulo 1 — Monitor Ciudadano de Fugas

```
📸 Usuario fotografía mancha de humedad o brote en vía pública
         ↓
🤖 Gemini Vision analiza: ¿es fuga real o agua estancada?
         ↓
📊 Clasifica severidad: Baja | Media | Alta | Crítica
         ↓
📍 Geolocaliza el reporte y lo envía a COMAPA Sur
```

**Output del agente:**
```json
{
  "fuga_detectada": true,
  "severidad": "alta",
  "tipo": "tuberia_rota",
  "confianza": 87,
  "descripcion": "Se observa brote de agua activo en banqueta...",
  "recomendacion": "Llamar al número de emergencias de COMAPA Sur inmediatamente.",
  "urgencia_reporte": "alta"
}
```

---

### 🌿 Módulo 2 — Alerta de Invasión de Lirio Acuático

```
📸 Ciudadano sube foto de la superficie de la Laguna del Chairel
         ↓
🤖 Gemini segmenta la imagen y estima cobertura de lirio (0-100%)
         ↓
🚨 Genera alerta priorizada para brigadas de limpieza
         ↓
🗺️ Zona marcada en el mapa de calor
```

**Output del agente:**
```json
{
  "lirio_detectado": true,
  "cobertura_porcentaje": 65,
  "desechos_detectados": true,
  "tipo_desechos": "plasticos",
  "urgencia": "alta",
  "confianza": 91,
  "recomendacion_brigada": "Zona norte del Chairel requiere intervención en 24h..."
}
```

---

### 🔬 Módulo 3 — Asistente de Calidad y Turbidez

```
📸 Usuario fotografía vaso de agua contra fondo blanco
         ↓
🤖 Gemini analiza colorimetría: color, turbidez, partículas visibles
         ↓
✅ Determina aptitud: consumo humano / uso doméstico / riego
         ↓
⚠️ Emite advertencia ciudadana si detecta contaminación
```

**Output del agente:**
```json
{
  "color_predominante": "amarillento",
  "turbidez_nivel": 4,
  "turbidez_descripcion": "ligeramente_turbia",
  "apto_consumo_humano": false,
  "apto_uso_domestico": true,
  "apto_riego": true,
  "confianza": 78,
  "recomendacion": "No recomendable para consumo directo. Contacte a COMAPA Sur."
}
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND (Browser)                    │
│  index.html · dashboard.html · style.css · app.js       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │  Módulo  │ │  Módulo  │ │  Módulo  │  Leaflet.js     │
│  │   Fuga   │ │  Lirio   │ │ Calidad  │  (Mapa Calor)   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘                 │
└───────┼────────────┼────────────┼────────────────────────┘
        │   POST imagen_b64       │
        ▼                         ▼
┌─────────────────────────────────────────────────────────┐
│              BACKEND — Flask (app.py)                   │
│                                                         │
│    /analizar/fuga  /analizar/lirio  /analizar/calidad   │
│                         ↓                               │
│           Agente Orquestador (prompts.py)               │
│                         ↓                               │
│           Google Gemini 2.5 Flash Vision                │
│                         ↓                               │
│           SQLite / SQLAlchemy (models.py)               │
│           /reportes   /estadisticas   /dashboard        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Función |
|------|-----------|---------|
| **IA / Visión** | Google Gemini 2.5 Flash | Análisis multimodal de imágenes |
| **Backend** | Python 3.10+ + Flask | API REST y servidor web |
| **Base de Datos** | SQLite + SQLAlchemy | Historial de reportes |
| **Mapa** | Leaflet.js | Mapa de calor interactivo |
| **Frontend** | HTML5 + CSS3 + JavaScript | SPA glassmorphism dark mode |
| **Deploy** | Vercel | Hosting serverless |
| **Geolocalización** | Web Geolocation API | Localización del reporte |

---

## 🚀 Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/madero-h2o.git
cd madero-h2o

# 2. Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
# source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Abre .env y reemplaza tu_api_key_aqui con tu API Key de Google AI Studio

# 5. Ejecutar la aplicación
python app.py
```

Abre tu navegador en: **http://localhost:5002** 🌊

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (nunca lo subas a GitHub):

```env
GEMINI_API_KEY=tu_api_key_de_google_ai_studio
SECRET_KEY=madero-h2o-guardian-2025
```

> 🔑 Obtén tu API Key **gratis** en: [Google AI Studio → aistudio.google.com](https://aistudio.google.com/)

---

## 📡 Endpoints API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Página principal con los 3 módulos |
| `GET` | `/dashboard` | Panel con mapa de calor y estadísticas |
| `POST` | `/analizar/fuga` | Análisis de fuga de agua en imagen |
| `POST` | `/analizar/lirio` | Detección de lirio acuático en imagen |
| `POST` | `/analizar/calidad` | Análisis colorimétrico de muestra de agua |
| `GET` | `/reportes` | Lista JSON de reportes (para el mapa) |
| `GET` | `/estadisticas` | Conteos por módulo y severidad |

### Body — POST `/analizar/<modulo>`

```json
{
  "imagen_b64": "data:image/jpeg;base64,/9j/4AAQSkZ...",
  "latitud": 22.2744,
  "longitud": -97.8326
}
```

### Response exitosa

```json
{
  "modulo": "fuga",
  "label": "Fuga de Agua",
  "resultado": { ... },
  "severidad": "alta",
  "reporte_id": 7,
  "coordenadas": { "lat": 22.2744, "lon": -97.8326 }
}
```

---

## 🌐 Deploy en Vercel

### Paso 1 — Subir a GitHub

```bash
git remote add origin https://github.com/<tu-usuario>/madero-h2o.git
git branch -M main
git push -u origin main
```

### Paso 2 — Importar en Vercel

1. Ve a [vercel.com](https://vercel.com) e inicia sesión con tu cuenta de GitHub
2. Clic en **Add New... → Project**
3. Selecciona el repositorio `madero-h2o`
4. En **Environment Variables**, agrega:

   | Key | Value |
   |-----|-------|
   | `GEMINI_API_KEY` | `tu_api_key_aqui` |

5. Clic en **Deploy** 🚀

Tu app estará disponible en: `https://madero-h2o.vercel.app`

> **⚠️ Nota Vercel**: Al ser serverless, SQLite es efímero por sesión. El mapa mostrará reportes de demostración de Ciudad Madero y los generados en la sesión actual.

### Actualizaciones automáticas

Cada `git push` al branch `main` dispara un redeploy automático en Vercel:

```bash
git add .
git commit -m "feat: descripción del cambio"
git push
```

---

## 📁 Estructura del Proyecto

```
madero-h2o/
│
├── 📄 app.py               # Backend Flask — agente orquestador
├── 📄 models.py            # SQLite + SQLAlchemy + datos demo
├── 📄 prompts.py           # Prompts de IA por módulo
│
├── 📄 requirements.txt     # Dependencias Python
├── 📄 vercel.json          # Configuración de deploy
├── 📄 .env.example         # Plantilla de variables de entorno
├── 📄 .gitignore           # .env excluido del repositorio
│
├── 📁 templates/
│   ├── 📄 index.html       # SPA principal (3 módulos)
│   └── 📄 dashboard.html   # Mapa de calor + estadísticas
│
└── 📁 static/
    ├── 📁 css/
    │   └── 📄 style.css    # Design system glassmorphism
    └── 📁 js/
        └── 📄 app.js       # Lógica frontend
```

---

## 📍 Contexto e Impacto Local

| Aspecto | Detalle |
|---------|---------|
| **Ciudad** | Ciudad Madero, Tamaulipas, México |
| **Organismo operador** | COMAPA Sur · CAEAT |
| **Sistema lagunario** | Laguna del Chairel · Laguna del Carpintero |
| **Planta potabilizadora** | Sistema Lagunario-Chairel |
| **Pérdida de agua** | 40–60% por fugas no reportadas (promedio Latinoamérica) |
| **Lirio acuático** | Especie invasora (*Eichhornia crassipes*) que obstruye el flujo y encarece la potabilización |
| **Norma de calidad** | NOM-127-SSA1-2021 — Agua para uso y consumo humano |

---

## 🤝 Contribuciones

Este es un proyecto académico. Si quieres contribuir:

1. Haz un fork del repositorio
2. Crea un branch: `git checkout -b feature/nueva-funcionalidad`
3. Haz tus cambios y un commit: `git commit -m 'feat: nueva funcionalidad'`
4. Sube el branch: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

```
MIT License

Copyright (c) 2025 — Proyecto Académico, Programación Web, 10mo Semestre
Ciudad Madero, Tamaulipas, México
```

---

<div align="center">

**Desarrollado con ❤️ para Ciudad Madero, Tamaulipas**

`Python` · `Flask` · `Google Gemini` · `Leaflet.js` · `Vercel`

*Cada foto que tomas puede salvar millones de litros de agua* 💧

</div>
