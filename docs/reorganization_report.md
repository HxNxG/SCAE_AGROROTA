# Reorganization and verification

Base `9a0d9b107d9a43806e1da531a0cb28e9fa4d7442`. Work is on the local branch `biotinder/reorganization-audit`. See the [inventory and migration map](reorganization_audit.md) and [scientific evidence](data_and_model.md).

## Final layout

```text
SCAE_AGROROTA/
├── README.md                         International evaluation guide
├── docs/                             Audit, methods, verification and handoff
├── 01_…/ through 10_…/                 Data packages and their source tooling
├── backend/
│   ├── app.py                        Recommendation/observation API
│   ├── modelo_ensamble_babahoyo.joblib
│   ├── train_nn.py                   Compatibility CLI
│   └── ml/                           Training and read-only artifact audit
├── data/                             Committed training CSV
├── tests/                            Recommendation and observation tests
├── proyecto-agricultura-ia/
│   ├── backend/app/                  Parcel validation and climate API
│   ├── backend/tests/                Existing climate and geography tests
│   ├── frontend/                     Browser app, Node proxy and static example
│   ├── scripts/                      Geographic/climate preparation
│   └── docs/                         Technical pilot documentation
└── .github/workflows/pages.yml        Existing optional static deployment
```

The training implementation moved from `backend/train_nn.py` into `backend/ml/train_nn.py`; the original CLI remains a compatibility launcher. Model, training CSV, acquisition tools, source packages, geographic services and frontend paths remain in place. Relative startup commands and the API contract are preserved. API file paths now resolve from the repository rather than the caller's directory. The observations file can be configured via `BIOTINDER_OBSERVATIONS_PATH`; keep it outside the repository if using a custom path. No original files or Git history were removed. The model, training CSV and retrieval scripts were not rewritten by verification.

The frontend now labels ensemble stability, margin and soil index as heuristic and presents agronomic and economic outputs as prototype estimates. Metric values, crop rules, thresholds and simulation parameters were not changed. The repository catalog now points evaluators to the actual interface, services and evidence. The Spanish run guide remains available.

## Verification on Windows, Python 3.13 and Node 24

| Check | Observed result |
| --- | --- |
| `uv run --offline --no-project --python 3.13 --with-requirements requirements.txt --with httpx python -m unittest discover -s tests -v` at repository root | 2 tests passed. Pimocha/drought and Caracol/normal returned different three-card results, 18 months per card. Observation remained pending in a temporary file. |
| `uv run --offline --no-project --python 3.13 --with-requirements requirements.txt python -m unittest discover -s tests -v` from `proyecto-agricultura-ia/backend` | 8 tests passed for geometry, IMERG, SMAP and MODIS. |
| Start `python -m uvicorn backend.app:app` from root and `python -m uvicorn app.main:app` from the geographic backend directory on temporary loopback ports | Both OpenAPI endpoints returned HTTP 200. A Babahoyo point passed validation. The climate API returned 189 monthly IMERG entries, eight SMAP frames and 202 MODIS frames. Processes were stopped after verification. |
| `python -m backend.ml.audit_artifact` with root dependencies | Reproduced the 384-row internal holdout. 96/96 stored climatology groups matched and the checked-in CSV differed from the current fallback generator. |
| `node --check` for JavaScript and Node scripts | 19 files passed. |
| Scoped relative-link check and `git diff --check` | Checked the new documentation and run guide, including relative paths. |
| Full retraining and fresh provider acquisition | **NOT RUN.** These would contact external services or regenerate training output. |
| Browser visual regression, independent field validation and public deployment | **NOT RUN.** The repository's existing Pages workflow was not executed. |

## Remaining work

1. Capture POWER request metadata and raw responses with checksums. Verify units and compare time- and location-held-out predictions with climatology before using scores in decisions.
2. Validate crop advice, soil indices and savings with locally dated references and field measurements. Keep assumptions visible and prevent public collection of farmer observations until moderation, retention and access controls are implemented.
3. Review old links and assets that refer to unversioned local samples. Preserve the current packages and assess external archival for large future releases; identify applicable source terms separately from any future project license.
4. Add a maintained deployment route after deciding ownership and hosting. GitHub Pages currently packages a static example and cannot run FastAPI.
