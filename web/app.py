import json
import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
APP_DIR = Path("/app")
DATA_PATH = APP_DIR / "data/processed/income_by_region_clean.csv"
DB_PATH = APP_DIR / "db/income.db"
REPORTS_DIR = APP_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

app = FastAPI(
    title="Open Data Analytics",
    description="API and web dashboard for the Dockerized open data analytics project.",
    version="1.0.0",
)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_preview(limit: int = 20) -> list[dict]:
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH).head(limit).to_dict(orient="records")

    if DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(
                "select * from income_by_region limit ?",
                conn,
                params=(limit,),
            ).to_dict(orient="records")

    return []


def list_figures() -> list[str]:
    if not FIGURES_DIR.exists():
        return []
    return sorted(path.name for path in FIGURES_DIR.glob("*.png"))


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "data_preview": load_preview(),
            "quality": read_json(REPORTS_DIR / "data_quality_report.json"),
            "research": read_json(REPORTS_DIR / "data_research_report.json"),
            "figures": list_figures(),
        },
    )


@app.get("/api/data-preview")
def api_data_preview(limit: int = 20):
    return {"items": load_preview(limit)}


@app.get("/api/quality")
def api_quality():
    return read_json(REPORTS_DIR / "data_quality_report.json")


@app.get("/api/research")
def api_research():
    return read_json(REPORTS_DIR / "data_research_report.json")


@app.get("/api/figures")
def api_figures():
    return {"items": list_figures()}


@app.get("/figures/{filename}")
def figures(filename: str):
    figure_path = FIGURES_DIR / filename
    if not figure_path.exists():
        return {"error": "Figure not found"}
    return FileResponse(figure_path)


@app.get("/health")
def health():
    return {"status": "ok"}
