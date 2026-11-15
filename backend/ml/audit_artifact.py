"""Compare the checked-in data, fallback generator and existing model without fitting."""

from hashlib import sha256

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from backend.app import ARTEFACTO, MODEL_PATH
from backend.ml.train_nn import ROOT, generar_dataset_respaldo


def main():
    dataset = ROOT / "data" / "dataset_babahoyo_2005_2024.csv"
    keys = ["zona", "anio", "mes"]
    data = pd.read_csv(dataset).sort_values(keys).reset_index(drop=True)
    fallback = generar_dataset_respaldo().sort_values(keys).reset_index(drop=True)
    if not data[keys].equals(fallback[keys]):
        raise ValueError("Dataset and fallback keys differ")

    columns = ["lluvia_mes_mm", "temp_max_c", "radiacion_solar_mj",
               "humedad_suelo_pct", "et0_mes_mm"]
    for column in columns:
        matches = np.isclose(data[column], fallback[column], rtol=1e-9, atol=1e-9).sum()
        print(f"{column}: {matches}/{len(data)} rows match the synthetic fallback")

    grouped = data.groupby(["zona", "mes"])[columns[:3]].mean().to_dict("index")
    climate = ARTEFACTO["climatologia_base"]
    matching = sum(
        all(np.isclose(value, climate[key][column]) for column, value in row.items())
        for key, row in grouped.items()
    )
    print(f"Stored climatology: {matching}/{len(grouped)} matching groups")

    features = data[ARTEFACTO["columnas_x"]].to_numpy()
    targets = data[ARTEFACTO["columnas_y"]].to_numpy()
    _, x_test, _, y_test = train_test_split(features, targets, test_size=.20, random_state=42)
    scaled = ARTEFACTO["scaler_x"].transform(x_test)
    estimates = np.mean([
        ARTEFACTO["scaler_y"].inverse_transform(model.predict(scaled))
        for model in ARTEFACTO["ensamble"]
    ], axis=0)
    print(f"Holdout: {len(x_test)} rows; R2={r2_score(y_test, estimates):.3f}; "
          f"MAE humidity={mean_absolute_error(y_test[:, 0], estimates[:, 0]):.2f} pp; "
          f"MAE balance={mean_absolute_error(y_test[:, 1], estimates[:, 1]):.1f} mm")
    print(f"Metrics stored in artifact: {ARTEFACTO['metricas']}")
    for path in (dataset, MODEL_PATH):
        print(f"SHA-256 {path.name}: {sha256(path.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
