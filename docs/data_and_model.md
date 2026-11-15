# Data and model evidence

Audit of the committed BioTinder prototype on 2026-11-15. Product documentation and repository coverage are separate. See the [detailed data inventory](../INFORME_DATOS_Y_VARIABLES.md), [resolution audit](../FIELD_SHIFT_AUDITORIA_DATOS.md) and [coverage gaps](../09_cobertura_y_brechas/ESTADO_POR_REGION.md).

## Status by source

| Class | Product or input | Evidence and use |
| --- | --- | --- |
| A · Downloaded, checked and used in the map | NASA GPM IMERG Final, GPM_3IMERGM V07B | January 2010–September 2025, 0.1°. The API reads the versioned canton-average and cell series. Tests compare cells with both input CSV segments. [Source and transformation](../02_clima_temperatura_y_meteorologia/GPM/README.md) |
| A · Downloaded, checked and used for a pilot | NASA SMAP L4 SPL4SMGP V008 | Eight three-hour frames on 2025-01-01, 28 cells on the native 9 km grid, surface and root-zone. The map serves this sample. The product starts in March 2015. Full historical per-cell coverage is not established in a fresh clone. [Pilot and historical limitations](../proyecto-agricultura-ia/docs/CAPA_HUMEDAD.md) |
| A · Downloaded, checked and used in the map | Terra MODIS MOD11C3.061 | January 2010–October 2026, 0.05°, day/night with QA and missing pixels. [Temperature pipeline](../proyecto-agricultura-ia/docs/CAPA_TEMPERATURA.md) |
| A · Committed and internally checked, provenance incomplete | 1,920-row training CSV, 2005–2024, eight sectors | The training script requests NASA POWER meteorology and radiation on product-dependent grids. The shipped CSV passes the artifact comparison below. Original response payloads, request metadata and a signed run manifest are unavailable for end-to-end verification. [Monthly API](https://power.larc.nasa.gov/docs/services/api/temporal/monthly/) |
| B · Collected or cataloged, not connected to recommendations | Terra MODIS MOD13C2 vegetation; HLS and other vegetation products; ISRIC SoilGrids v2; SRTM; agricultural tables | The vegetation archives include MODIS NDVI/EVI at 0.05°. The recommendation API does not read these files or SoilGrids. SoilGrids is an external ISRIC product at 250 m. The model uses fixed elevation annotations, with no live SRTM raster lookup. Crop figures are constants rather than a join to dated source tables. [MODIS collection](../04_vegetacion_cultivos_y_monitoreo/MODIS/README.md) · [ISRIC](../01_suelos_y_salud_del_suelo/ISRIC/README.md) · [SRTM](../05_topografia_y_modelado_del_terreno/SRTM/README.md) · [Agricultural files](../07_informacion_agropecuaria_ecuatoriana/README.md) |
| C · Proposed or partial | Historical SMAP cells, event flood masks, field validation and price evidence | Site-specific processing and validation remain pending. The optional local flood layer is static susceptibility from CONAGE, not a dated Sentinel-1 detection. [Flood layer](../proyecto-agricultura-ia/docs/SUSCEPTIBILIDAD_INUNDACIONES.md) |
| D · Synthetic or heuristic | Fallback, climate perturbations, crop impact and economic figures | The fallback generates seeded rows from fixed seasonal assumptions. Scenario changes, crop cycles, planting rules, costs, yields, soil strength, historical success text and savings are assumptions or estimates. |

## Committed model and reproducibility

The [trainer](../backend/ml/train_nn.py) requests `PRECTOTCORR`, `T2M_MAX`, `ALLSKY_SFC_SW_DWN`, `GWETROOT` and `EVPTRNS`. Any exception for a sector returns a fully synthetic fallback. Before retraining, record the source and units of each response and make fallback mode explicit. The prototype assumes daily-rate conversion for some monthly parameters. Verify that interpretation and the treatment of transpiration as an ET proxy. `GWETROOT × 100` represents percent of the source wetness index, not a field measurement of volumetric soil moisture.

The versioned CSV and deterministic fallback share row keys. With `rtol=1e-9, atol=1e-9`, **0 of 1,920 rows match per variable** for rainfall, temperature, radiation, humidity and the ET proxy. The artifact's **96 of 96** sector/month climatology groups match the committed CSV. This rules out an exact copy of the current fallback and supports the connection between the CSV and artifact. It does not authenticate the original NASA responses.

The artifact has five `MLPRegressor` estimators with hidden layers `(64, 32)`, separate feature/target scalers and ten inputs. The outputs are a root-zone wetness proxy, a derived rainfall-minus-ET balance and a threshold-based heat index. The audit replayed the existing model on the original **384-row random holdout** without fitting. It reproduced aggregate **R² 0.952**, **humidity MAE 1.47 percentage points** and **balance MAE 15.8 mm**. These are internal test statistics, not a confidence interval, field accuracy or skill for a future year. CSV and artifact checksums are printed by:

```powershell
python -m backend.ml.audit_artifact
```

The split is row-random, so neighboring months and the same sectors can appear on both sides. Imputation precedes the split. The rolling rainfall input includes the current month, which also participates in the balance target. In inference the proxy for three-month rain is 2.7 times the prior-month rain. These are potential leakage and train/serve mismatch. Next compare against seasonal baselines and hold out whole years and sectors, using only information available at the forecast issue date.

## Scenarios and agronomic rules

The 18-month run repeats seasonal inputs and applies fixed drought/El Niño perturbations such as rainfall multipliers 0.75 and 1.35. The temperature, rainfall and anomalies are scenario assumptions. The map's separate three-month reference uses calendar-month historical means and observed extremes, without dynamic forecasting. Neither feature has been validated as an operational forecast.

The service picks candidates such as soybean, mucuna, cowpea, maize or sorghum using water access, estimated summer wetness, terrain, selected scenario and the farmer's goal. Inspect [the service](../backend/app.py) for the exact thresholds and the hard-coded crop database. Reported crop savings have floors and caps and depend on assumed baselines. The service does not estimate actual farm profit, avoided emissions or measured climate adaptation. Text claiming frequencies like “18 of 20 years” is hard-coded and unverified.

The margin uses ensemble spread plus a fixed adjustment and clipping. The derived score `confianza_ia` maps that margin onto a bounded scale. The UI labels it as heuristic stability out of 100. Neither value is a calibrated interval, a probability of crop survival, or a rating of input quality.
