"""
models.py — Modelos de base de datos para Madero H2O: Guardián del Agua
Usa SQLite local (desarrollo) con fallback a /tmp (Vercel serverless)
"""

import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Determinar ruta de la base de datos
# En Vercel, el sistema de archivos es efímero; usamos /tmp
if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/madero_h2o.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "madero_h2o.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modulo = Column(String(20), nullable=False)  # 'fuga', 'lirio', 'calidad'
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    severidad = Column(String(20), nullable=True)  # baja, media, alta, critica
    descripcion = Column(Text, nullable=True)
    confianza = Column(Float, nullable=True)
    datos_extra = Column(Text, nullable=True)  # JSON string con datos adicionales del módulo
    timestamp = Column(DateTime, default=datetime.utcnow)
    ciudad = Column(String(100), default="Ciudad Madero, Tamaulipas")


def init_db():
    """Inicializar la base de datos y crear tablas."""
    Base.metadata.create_all(engine)
    _seed_demo_data()


def _seed_demo_data():
    """Insertar datos de demostración si la base está vacía."""
    session = SessionLocal()
    try:
        count = session.query(Reporte).count()
        if count == 0:
            demo_reportes = [
                Reporte(
                    modulo="fuga",
                    latitud=22.2705,
                    longitud=-97.8451,
                    severidad="alta",
                    descripcion="Fuga en tubería principal, Av. Hidalgo esq. con Calle 3",
                    confianza=87.0,
                    datos_extra='{"tipo": "tuberia_rota", "urgencia_reporte": "alta"}',
                ),
                Reporte(
                    modulo="fuga",
                    latitud=22.2791,
                    longitud=-97.8320,
                    severidad="media",
                    descripcion="Humedad en banqueta, posible fuga de válvula subterránea",
                    confianza=72.0,
                    datos_extra='{"tipo": "valvula_defectuosa", "urgencia_reporte": "media"}',
                ),
                Reporte(
                    modulo="lirio",
                    latitud=22.2631,
                    longitud=-97.8412,
                    severidad="alta",
                    descripcion="Cobertura de lirio acuático al 65% en canal norte del Chairel",
                    confianza=91.0,
                    datos_extra='{"cobertura_porcentaje": 65, "desechos_detectados": true}',
                ),
                Reporte(
                    modulo="lirio",
                    latitud=22.2598,
                    longitud=-97.8289,
                    severidad="media",
                    descripcion="Presencia moderada de lirio y desechos plásticos",
                    confianza=83.0,
                    datos_extra='{"cobertura_porcentaje": 35, "desechos_detectados": true}',
                ),
                Reporte(
                    modulo="calidad",
                    latitud=22.2744,
                    longitud=-97.8390,
                    severidad="media",
                    descripcion="Agua con turbidez leve, posible sedimento en suspensión",
                    confianza=78.0,
                    datos_extra='{"turbidez_nivel": 4, "apto_consumo_humano": false, "color_predominante": "amarillento"}',
                ),
                Reporte(
                    modulo="fuga",
                    latitud=22.2812,
                    longitud=-97.8267,
                    severidad="critica",
                    descripcion="Brote de agua en calle 5, colonia Guadalupe",
                    confianza=95.0,
                    datos_extra='{"tipo": "brote_superficial", "urgencia_reporte": "inmediata"}',
                ),
            ]
            session.add_all(demo_reportes)
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def guardar_reporte(modulo: str, latitud: float, longitud: float, severidad: str,
                    descripcion: str, confianza: float, datos_extra: str = None) -> int:
    """Guardar un nuevo reporte en la base de datos."""
    session = SessionLocal()
    try:
        reporte = Reporte(
            modulo=modulo,
            latitud=latitud,
            longitud=longitud,
            severidad=severidad,
            descripcion=descripcion,
            confianza=confianza,
            datos_extra=datos_extra,
        )
        session.add(reporte)
        session.commit()
        return reporte.id
    except Exception:
        session.rollback()
        return -1
    finally:
        session.close()


def obtener_reportes(limite: int = 100) -> list:
    """Obtener los últimos reportes para el mapa de calor."""
    session = SessionLocal()
    try:
        reportes = (
            session.query(Reporte)
            .order_by(Reporte.timestamp.desc())
            .limit(limite)
            .all()
        )
        return [
            {
                "id": r.id,
                "modulo": r.modulo,
                "latitud": r.latitud,
                "longitud": r.longitud,
                "severidad": r.severidad,
                "descripcion": r.descripcion,
                "confianza": r.confianza,
                "datos_extra": r.datos_extra,
                "timestamp": r.timestamp.strftime("%d/%m/%Y %H:%M") if r.timestamp else "",
                "ciudad": r.ciudad,
            }
            for r in reportes
        ]
    finally:
        session.close()


def obtener_estadisticas() -> dict:
    """Obtener estadísticas generales para el dashboard."""
    session = SessionLocal()
    try:
        total = session.query(Reporte).count()
        fugas = session.query(Reporte).filter(Reporte.modulo == "fuga").count()
        lirio = session.query(Reporte).filter(Reporte.modulo == "lirio").count()
        calidad = session.query(Reporte).filter(Reporte.modulo == "calidad").count()
        criticas = session.query(Reporte).filter(Reporte.severidad == "critica").count()
        return {
            "total": total,
            "fugas": fugas,
            "lirio": lirio,
            "calidad": calidad,
            "criticas": criticas,
        }
    finally:
        session.close()
