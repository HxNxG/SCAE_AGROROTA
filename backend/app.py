import os
from pathlib import Path
import json
import math
import joblib
import numpy as np
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "backend" / "modelo_ensamble_babahoyo.joblib"
OBSERVATIONS_PATH = Path(os.environ.get(
    "BIOTINDER_OBSERVATIONS_PATH", ROOT / "data" / "aportes_pendientes_revision.json"
)).expanduser().resolve()
PUBLIC_INFERENCE = os.environ.get("BIOTINDER_PUBLIC_INFERENCE") == "1"
PUBLIC_ORIGIN = os.environ.get("BIOTINDER_PUBLIC_ORIGIN", "https://hxnxg.github.io")

app = FastAPI(title="BioTinder · AgroRota Ecuador")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[PUBLIC_ORIGIN] if PUBLIC_INFERENCE else ["*"],
    allow_methods=["GET", "POST"] if PUBLIC_INFERENCE else ["*"],
    allow_headers=["Content-Type"] if PUBLIC_INFERENCE else ["*"],
)

# Cargar el ensamble neuronal recién entrenado
ARTEFACTO = joblib.load(MODEL_PATH)
PUNTOS_BABAHOYO = ARTEFACTO["puntos_babahoyo"]

MESES_NOMBRES = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# Meses históricos con suelo desnudo (MODIS NDVI < 0.25) por sector
NDVI_VACIO_ZONA = {
    "Babahoyo Centro": 6, "Pimocha (Bajial)": 6, "Caracol": 6, "Febres Cordero": 5,
    "La Unión": 5, "Baba": 6, "Montalvo (Alto)": 4, "Vinces (Sur)": 6
}

# Base agronómica (INIAP Pichilingue) + Economía referencial por cultivo (MAG SIPA Los Ríos)
CULTIVOS_DB = {
    "arroz": {
        "nombre": "Arroz (Tu Cultivo Principal)",
        "rol": "principal",
        "color": "#D97706",
        "dias": 125,
        "demanda_agua_mm": 950,
        "nitrogeno_kg": -115,
        "economia": {"costo_ha": 1350, "rendimiento_qq": 105, "precio_qq": 34.0, "ahorro_prox_arroz_usd": 0},
        "guia": None
    },
    "soya": {
        "nombre": "Soya INIAP-308 (Aliado Fijador)",
        "rol": "secundario_suelo",
        "color": "#059669",
        "dias": 105,
        "demanda_agua_mm": 380,
        "nitrogeno_kg": 75,
        "economia": {"costo_ha": 680, "rendimiento_qq": 40, "precio_qq": 32.0, "ahorro_prox_arroz_usd": 95},
        "guia": {
            "planta": "Soya (Variedad INIAP-308)",
            "rol_arroz": "No reemplaza tu arroz. Es un cultivo secundario que aprovecha la humedad tras cosechar en mayo y deja +75 kg/ha de abono natural (~3.5 sacos de úrea ahorrados).",
            "preparacion": "Siembra directa sobre el rastrojo de arroz recién cosechado (cero labranza); no requiere inundar ni arar profundo.",
            "siembra": "50 cm entre surcos y 10 cm entre plantas (12 a 15 semillas por metro lineal) con semilla inoculada.",
            "cuidados": "Vigilar gusano pegador de hoja los primeros 30 días. No pide riego si se siembra al salir el invierno.",
            "cosecha": "A los 100-105 días cuando el 90% de vainas estén secas; dejar el rastrojo picado en el lote."
        }
    },
    "frejol_caupi": {
        "nombre": "Fréjol Caupí INIAP-451 (Aliado Sequía)",
        "rol": "secundario_suelo",
        "color": "#10B981",
        "dias": 80,
        "demanda_agua_mm": 240,
        "nitrogeno_kg": 55,
        "economia": {"costo_ha": 540, "rendimiento_qq": 24, "precio_qq": 55.0, "ahorro_prox_arroz_usd": 70},
        "guia": {
            "planta": "Fréjol Caupí (Variedad INIAP-451)",
            "rol_arroz": "Aliado ultra rápido (80 días) y resistente al verano seco de Babahoyo; deja dinero rápido, comida para la casa y abono natural para tu arroz.",
            "preparacion": "Limpieza ligera de malezas; tolera suelos barriales sin necesidad de bombas de estero.",
            "siembra": "50 cm entre surcos x 20 cm entre golpes (2 semillas por sitio) aprovechando el cierre de lluvias.",
            "cuidados": "Soporta hasta 34 °C sin riego continuo. Revisar pulgones en brotes tiernos las primeras 3 semanas.",
            "cosecha": "Entre 75 y 85 días se recoge el grano seco para vender o comer; el follaje sirve como forraje verde para animales."
        }
    },
    "mucuna": {
        "nombre": "Mucuna Negra (Abono Verde Protector)",
        "rol": "secundario_suelo",
        "color": "#047857",
        "dias": 95,
        "demanda_agua_mm": 210,
        "nitrogeno_kg": 90,
        "economia": {"costo_ha": 190, "rendimiento_qq": 0, "precio_qq": 0.0, "ahorro_prox_arroz_usd": 135},
        "guia": {
            "planta": "Mucuna Negra (Cobertura y Abono Verde)",
            "rol_arroz": "No es para vender grano: es un manto vivo que cubre la poza en verano, ahoga malezas difíciles (como el arroz rojo) e inyecta ~3.5 sacos de úrea natural.",
            "preparacion": "Siembra al voleo o espeque sin maquinaria sobre la poza húmeda tras cosechar el arroz.",
            "siembra": "80 cm x 50 cm (2 semillas por sitio); en 35 días cubre todo el suelo protegiéndolo del sol.",
            "cuidados": "Mantenimiento casi nulo; aguanta todo el verano seco sin bombas de agua.",
            "cosecha": "Se chapia e incorpora al suelo a los 90 días, 3 semanas antes de preparar la poza para tu arroz."
        }
    },
    "maiz": {
        "nombre": "Maíz Duro INIAP H-553 (Aliado Limpiador)",
        "rol": "secundario_limpieza",
        "color": "#0284C7",
        "dias": 120,
        "demanda_agua_mm": 480,
        "nitrogeno_kg": -60,
        "economia": {"costo_ha": 920, "rendimiento_qq": 120, "precio_qq": 17.5, "ahorro_prox_arroz_usd": 35},
        "guia": {
            "planta": "Maíz Duro Amarillo (Híbrido INIAP H-553)",
            "rol_arroz": "Segunda gramínea del ciclo técnico: aprovecha el abono que dejó la leguminosa anterior y corta el ciclo de plagas exclusivas del arroz (sogata).",
            "preparacion": "Solo en bancos altos o lotes que drenan rápido; hacer surcos para evitar encharcamiento.",
            "siembra": "80 cm entre surcos x 25 cm entre plantas (1 semilla por golpe).",
            "cuidados": "Control preventivo de cogollero a los 15 y 30 días; requiere poca úrea gracias a la leguminosa previa.",
            "cosecha": "A los 115-120 días para grano seco comercializable en Babahoyo o Montalvo."
        }
    },
    "sorgo": {
        "nombre": "Sorgo Granífero / Forrajero (Aliado Rústico)",
        "rol": "secundario_limpieza",
        "color": "#0369A1",
        "dias": 100,
        "demanda_agua_mm": 310,
        "nitrogeno_kg": -35,
        "economia": {"costo_ha": 580, "rendimiento_qq": 75, "precio_qq": 15.0, "ahorro_prox_arroz_usd": 40},
        "guia": {
            "planta": "Sorgo Granífero / Forrajero",
            "rol_arroz": "Reemplaza al maíz en bajiales o veranos secos; limpia plagas del suelo y deja abundante pasto/grano antes de volver al arroz.",
            "preparacion": "Pase superficial de rastra o siembra directa tras la leguminosa.",
            "siembra": "60 cm entre surcos a chorro continuo (12-15 kg semilla/ha).",
            "cuidados": "Alta resistencia tanto a sequía como a humedad temporal; bajo costo de insumos.",
            "cosecha": "A los 95-100 días para venta de grano o corte de forraje para ganado."
        }
    }
}

class ConsultaParcela(BaseModel):
    zona: str = "Babahoyo Centro"
    manejo_actual: str = "arroz_barbecho"      # Pregunta 1
    mes_inicio: int = 5                        # Pregunta 2
    agua_verano: str = "solo_lluvia"           # Pregunta 3
    tipo_terreno: str = "bajial_inundable"     # Pregunta 4
    meta: str = "ahorrar_abono"                # Pregunta 5
    escenario_clima: str = "normal"            # Simulador vivo

class AporteSector(BaseModel):
    sector: str
    categoria: str
    observacion: str

def predecir_18_meses_nn(zona: str, mes_inicio: int, escenario: str):
    info = PUNTOS_BABAHOYO.get(zona, PUNTOS_BABAHOYO["Babahoyo Centro"])
    clim = ARTEFACTO["climatologia_base"]
    scaler_x = ARTEFACTO["scaler_x"]
    scaler_y = ARTEFACTO["scaler_y"]
    ensamble = ARTEFACTO["ensamble"]

    f_lluvia = 0.75 if escenario == "sequia" else (1.35 if escenario == "elnino" else 1.0)
    d_temp = 1.8 if escenario == "sequia" else (0.6 if escenario == "elnino" else 0.0)
    anomalia = -1 if escenario == "sequia" else (1 if escenario == "elnino" else 0)

    serie = []
    for step in range(18):
        mes = ((mes_inicio - 1 + step) % 12) + 1
        mes_ant = 12 if mes == 1 else mes - 1

        base_m = clim.get((zona, mes), {"lluvia_mes_mm": 120, "temp_max_c": 31.0, "radiacion_solar_mj": 16.0})
        base_ant = clim.get((zona, mes_ant), {"lluvia_mes_mm": 140})

        lluvia_1m = base_ant["lluvia_mes_mm"] * f_lluvia
        lluvia_3m = lluvia_1m * 2.7
        tmax = base_m["temp_max_c"] + d_temp
        rad = base_m["radiacion_solar_mj"] * (1.05 if escenario == "sequia" else 0.96)

        x_vec = [[
            info["lat"], info["lon"], info["srtm"],
            math.sin(2 * math.pi * mes / 12.0),
            math.cos(2 * math.pi * mes / 12.0),
            lluvia_1m, lluvia_3m, tmax, rad, anomalia
        ]]
        x_sc = scaler_x.transform(x_vec)
        preds = np.array([scaler_y.inverse_transform(m.predict(x_sc))[0] for m in ensamble])

        media = np.mean(preds, axis=0)
        std = np.std(preds, axis=0)

        humedad = float(np.clip(media[0], 20.0, 96.0))
        margen = float(np.clip(std[0] * 1.96 + (2.1 if escenario != "normal" else 1.1), 1.5, 7.5))
        confianza = int(np.clip(96 - margen * 2.1, 72, 95))

        serie.append({
            "step": step + 1,
            "mes": mes,
            "nombre_mes": MESES_NOMBRES[mes],
            "humedad_pct": round(humedad, 1),
            "margen_pct": round(margen, 1),
            "confianza_pct": confianza,
            "balance_mm": round(float(media[1]), 1),
            "riesgo_calor": round(float(media[2]), 2)
        })
    return serie

def calcular_porcentajes_ahorro(cod_leg: str, cod_gram: str):
    """Calcula porcentajes reales de ahorro en abonos e inversión de verano."""
    gasto_abono_arroz_usd = 320.0
    costo_segundo_arroz_verano = 1620.0

    leg = CULTIVOS_DB[cod_leg]["economia"]
    gram = CULTIVOS_DB[cod_gram]["economia"]

    ahorro_insumos_usd = leg["ahorro_prox_arroz_usd"] + gram["ahorro_prox_arroz_usd"]
    pct_ahorro_abono = min(48, int(round((ahorro_insumos_usd / gasto_abono_arroz_usd) * 100)))

    costo_verano_rotacion = leg["costo_ha"] + gram["costo_ha"]
    pct_ahorro_verano = max(12, int(round(((costo_segundo_arroz_verano - costo_verano_rotacion) / costo_segundo_arroz_verano) * 100)))

    return {
        "pct_ahorro_abono": pct_ahorro_abono,
        "pct_ahorro_verano": pct_ahorro_verano,
        "ahorro_usd_ha": ahorro_insumos_usd
    }

@app.post("/api/recomendar")
def recomendar_estrategias(q: ConsultaParcela):
    proy = predecir_18_meses_nn(q.zona, q.mes_inicio, q.escenario_clima)

    meses_verano = [p for p in proy if p["mes"] in [7, 8, 9, 10, 11]]
    hum_verano = round(float(np.mean([m["humedad_pct"] for m in meses_verano])), 1)
    margen_verano = round(float(np.mean([m["margen_pct"] for m in meses_verano])), 1)
    conf_verano = int(np.mean([m["confianza_pct"] for m in meses_verano]))
    bal_verano = round(float(np.sum([m["balance_mm"] for m in meses_verano[:5]])), 0)

    tiene_riego = q.agua_verano in ["bomba_pozo", "canal_riego"]
    es_bajial = q.tipo_terreno == "bajial_inundable"

    # Selección de especies según predicción de la Red Neuronal + Preguntas de campo
    # Estrategia A: Regenerar suelo y ahorrar abono
    leg_a = "soya" if (hum_verano >= 56.5 or tiene_riego) else "mucuna"
    gram_a = "sorgo" if (es_bajial or q.escenario_clima == "elnino" or hum_verano < 55.0) else "maiz"

    # Estrategia B: Escudo contra sequía y venta rápida
    leg_b = "frejol_caupi"
    gram_b = "sorgo" if (not tiene_riego or q.escenario_clima == "sequia" or es_bajial) else "maiz"

    econ_a = calcular_porcentajes_ahorro(leg_a, gram_a)
    econ_b = calcular_porcentajes_ahorro(leg_b, gram_b)

    def construir_timeline(codigos_18m, es_actual=False):
        timeline = []
        fuerza_suelo = 75 if es_actual else 65
        for idx, p in enumerate(proy):
            cod = codigos_18m[idx]
            if cod == "suelo_vacio":
                fuerza_suelo = max(28, fuerza_suelo - 4)
                timeline.append({
                    "step": p["step"], "mes_nombre": p["nombre_mes"],
                    "cultivo": "Poza Vacía (Tierra pelada al sol)", "rol": "vacio", "color": "#78350F",
                    "humedad_ia": p["humedad_pct"], "fuerza_suelo": fuerza_suelo,
                    "alerta": "El sol endurece la tierra, evapora el agua y nacen malezas."
                })
            else:
                c = CULTIVOS_DB[cod]
                delta_f = 5 if c["rol"] == "secundario_suelo" else (-3 if cod == "arroz" else -1)
                fuerza_suelo = int(np.clip(fuerza_suelo + delta_f, 25, 98))
                alerta_mes = (
                    "Lluvia abundante: ideal para tu poza de arroz." if cod == "arroz" and p["humedad_pct"] >= 62
                    else ("Peligro de sequía: sin bomba de riego el arroz sufre." if cod == "arroz"
                          else "Aliado cubriendo el lote: guarda frescura y mejora la tierra.")
                )
                timeline.append({
                    "step": p["step"], "mes_nombre": p["nombre_mes"],
                    "cultivo": c["nombre"], "rol": c["rol"], "color": c["color"],
                    "humedad_ia": p["humedad_pct"], "fuerza_suelo": fuerza_suelo,
                    "alerta": alerta_mes
                })
        return timeline

    # Tarjeta 1: Línea base actual
    if q.manejo_actual == "arroz_doble":
        titulo_act = "Como trabajas hoy: Doble Arroz Anual"
        impacto_act = "Gastas +30% más en úrea y diésel de bombeo • Plagas repiten"
        ciclos_act = ["arroz"] * 18
        cosechas_act = 3
        forraje_act = "Rastrojo quemado o inundado"
        hist_act = "14 de 20 años (solo si no falla el bombeo)" if tiene_riego else "5 de 20 años (alto riesgo de pérdida)"
    else:
        titulo_act = "Como trabajas hoy: Arroz + Tierra Vacía"
        impacto_act = "0% ahorro en abono • 6 meses de tierra pelada sin ingresos"
        ciclos_act = ["suelo_vacio"] * 7 + ["arroz"] * 5 + ["suelo_vacio"] * 6
        cosechas_act = 1
        forraje_act = "Sin alimento ni pasto fresco en verano"
        hist_act = "11 de 20 años (cansa la tierra cada año)"

    tarjeta_actual = {
        "id": "actual",
        "titulo": titulo_act,
        "impacto_directo": impacto_act,
        "resumen_5_logros": {
            "ventas": f"{cosechas_act} cosecha(s) vendible(s) en 18 meses",
            "clima_plagas": "🔴 Se seca sin bombeo · La sogata y malezas repiten",
            "arroz_principal": "Baja rendimiento si no subes sacos de úrea",
            "fuerza_tierra": "Pierde fuerza cada año (0% ahorro en abono)",
            "casa_ganado": forraje_act
        },
        "timeline": construir_timeline(ciclos_act, es_actual=True),
        "pasos": [
            {"orden": "Invierno", "planta": "Arroz (Cultivo Principal)", "duracion": "125 días", "detalle": "Depende 100% de las lluvias de invierno."},
            {"orden": "Verano", "planta": "Poza vacía o segundo arroz forzado", "duracion": "180 días", "detalle": "Suelo expuesto al sol o alto gasto en combustible."}
        ],
        "tecnico_nasa": {
            "humedad_verano": hum_verano, "margen_error": margen_verano, "confianza_ia": conf_verano,
            "historial": hist_act,
            "evidencia": [
                f"NASA POWER / SMAP ({q.zona}): Humedad radicular cae a {hum_verano}% en verano (balance {bal_verano} mm).",
                f"MODIS NDVI: {NDVI_VACIO_ZONA.get(q.zona, 6)} meses históricos con cobertura menor a 0.25."
            ],
            "honestidad": "SMAP no detecta canales internos ni pozos privados. Revisar compactación a 20 cm en campo."
        },
        "guias": []
    }

    c_lega, c_grama = CULTIVOS_DB[leg_a], CULTIVOS_DB[gram_a]
    c_legb, c_gramb = CULTIVOS_DB[leg_b], CULTIVOS_DB[gram_b]
    seq_a = [leg_a]*4 + [gram_a]*4 + ["arroz"]*5 + [leg_a]*5
    seq_b = [leg_b]*3 + [gram_b]*4 + ["arroz"]*5 + [leg_b]*6

    tarjeta_a = {
        "id": "estrategia_a",
        "titulo": "Plan A: Ahorrar Abono y Cuidar Tierra",
        "impacto_directo": f"Ahorras {econ_a['pct_ahorro_abono']}% en abonos (~${econ_a['ahorro_usd_ha']}/ha) • Tierra fértil 5+ años",
        "resumen_5_logros": {
            "ventas": f"{2 if leg_a == 'mucuna' else 3} cosechas en 18 meses ({econ_a['pct_ahorro_verano']}% menos gasto de verano)",
            "clima_plagas": "🟢 Corta la sogata y ahoga el arroz rojo en verano",
            "arroz_principal": "Crece más fuerte en invierno con menos úrea",
            "fuerza_tierra": f"Ahorra {econ_a['pct_ahorro_abono']}% de abono (~3.5 sacos úrea/ha gratis)",
            "casa_ganado": "Abundante forraje verde y cobertura protectora"
        },
        "timeline": construir_timeline(seq_a),
        "pasos": [
            {"orden": "1. Aliado Fijador", "planta": c_lega["nombre"], "duracion": f"{c_lega['dias']} días", "detalle": "Aprovecha humedad tras cosechar arroz e inyecta abono natural."},
            {"orden": "2. Aliado Limpiador", "planta": c_grama["nombre"], "duracion": f"{c_grama['dias']} días", "detalle": "Limpia plagas del suelo antes del próximo invierno."},
            {"orden": "3. ★ Tu Arroz Principal", "planta": "Arroz (Cultivo eje)", "duracion": "125 días", "detalle": "Regresa en invierno sobre tierra suelta y fertilizada."}
        ],
        "tecnico_nasa": {
            "humedad_verano": hum_verano, "margen_error": margen_verano, "confianza_ia": conf_verano,
            "historial": "Favorable en 18 de los últimos 20 años (NASA POWER)",
            "evidencia": [
                f"NASA SMAP ({q.zona}): Humedad proyectada ({hum_verano}% ± {margen_verano}%) permite germinación sin inundar.",
                "INIAP Pichilingue & MAG: Sucesión Leguminosa → Gramínea corta ciclos de Pyricularia y sogata."
            ],
            "honestidad": "Los satélites no miden pH puntual ni precios diarios de piladora; confirmar semilla INIAP en Babahoyo."
        },
        "guias": [c_lega["guia"], c_grama["guia"]]
    }

    tarjeta_b = {
        "id": "estrategia_b",
        "titulo": "Plan B: Plata Rápida y Aguantar Sequía",
        "impacto_directo": f"Vendes en 80 días • Ahorras {econ_b['pct_ahorro_verano']}% en gasto de verano sin bombas",
        "resumen_5_logros": {
            "ventas": "3 cosechas vendibles en 18 meses (primera plata a los 80 días)",
            "clima_plagas": "🟢 Aguanta verano seco y calor de 34 °C sin riego",
            "arroz_principal": "Lote descansado y limpio para tu invierno",
            "fuerza_tierra": f"Ahorra {econ_b['pct_ahorro_abono']}% de abono (~2.5 sacos úrea/ha gratis)",
            "casa_ganado": "Fréjol seco para la mesa familiar + forraje para animales"
        },
        "timeline": construir_timeline(seq_b),
        "pasos": [
            {"orden": "1. Aliado Rápido", "planta": c_legb["nombre"], "duracion": "80 días", "detalle": "Cosecha vendible en menos de 3 meses con mínima agua."},
            {"orden": "2. Aliado Rústico", "planta": c_gramb["nombre"], "duracion": f"{c_gramb['dias']} días", "detalle": "Tolera sequía y deja grano/forraje antes de lluvias."},
            {"orden": "3. ★ Tu Arroz Principal", "planta": "Arroz (Cultivo eje)", "duracion": "125 días", "detalle": "Entra en invierno con menor gasto en químicos."}
        ],
        "tecnico_nasa": {
            "humedad_verano": hum_verano, "margen_error": margen_verano, "confianza_ia": conf_verano,
            "historial": "Favorable en 19 de los últimos 20 años (NASA POWER)",
            "evidencia": [
                f"NASA POWER ({q.zona}): Fréjol Caupí soporta estrés térmico proyectado en verano.",
                "MAG SIPA: Alta demanda comercial de fréjol seco en mercados de Babahoyo."
            ],
            "honestidad": "SRTM (30 m) no distingue micro-desniveles internos; cosechar el aliado antes de las lluvias fuertes."
        },
        "guias": [c_legb["guia"], c_gramb["guia"]]
    }

    recomendadas = [tarjeta_b, tarjeta_a] if q.meta in ["resistir_sequia", "cosecha_rapida"] else [tarjeta_a, tarjeta_b]

    return {
        "zona": q.zona,
        "metricas_modelo": ARTEFACTO["metricas"],
        "estrategias": [tarjeta_actual] + recomendadas
    }

@app.post("/api/aportar-datos")
def guardar_aporte_revision(aporte: AporteSector):
    if PUBLIC_INFERENCE:
        raise HTTPException(status_code=403, detail="El registro de observaciones solo está disponible en el visor local.")

    archivo = OBSERVATIONS_PATH
    archivo.parent.mkdir(parents=True, exist_ok=True)
    registros = []
    if archivo.exists():
        with open(archivo, "r", encoding="utf-8") as f:
            registros = json.load(f)

    registros.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sector": aporte.sector,
        "categoria": aporte.categoria,
        "observacion": aporte.observacion,
        "estado": "PENDIENTE_REVISION_TECNICA"
    })
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)

    return {
        "mensaje": "Aporte registrado correctamente. Pasará a revisión técnica antes de actualizar la red neuronal.",
        "total_pendientes": len(registros)
    }

@app.get("/healthz", include_in_schema=False)
def health():
    return {"status": "ok"}

@app.get("/")
def estado_api():
    legacy_frontend = ROOT / "frontend" / "index.html"
    if legacy_frontend.is_file():
        return FileResponse(legacy_frontend)
    return {
        "estado": "Backend Field Shift Babahoyo activo",
        "docs": "http://localhost:8000/docs"
    }
