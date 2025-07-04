from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

# ----------  Excel Parser Logic ----------

def parse_excel(file_path: str) -> dict:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    workbook = pd.read_excel(file_path, sheet_name=None)
    extracted = {}
    name_tracker = {}

    for sheet, data in workbook.items():
        num_rows, num_cols = data.shape
        active_section = None
        section_content = {}

        for i in range(num_rows):
            row = data.iloc[i].fillna("").astype(str)

            
            is_header_found = False
            for j in range(num_cols):
                cell = row.iloc[j].strip()
                if cell.isupper() and len(cell) > 2 and " " in cell:
                    is_header_found = True
                    break

            if is_header_found:
                
                if active_section and section_content:
                    title = _resolve_name_conflict(active_section, extracted, name_tracker)
                    extracted[title] = section_content
                    section_content = {}
                active_section = cell  
                continue

            
            if active_section and row.iloc[0].strip():
                label = row.iloc[0].strip()

                
                if label.isupper() and " " in label and len(label) > 2:
                    continue

                values = pd.to_numeric(row.iloc[1:], errors="coerce").dropna().tolist()
                section_content[label] = values

        
        if active_section and section_content:
            title = _resolve_name_conflict(active_section, extracted, name_tracker)
            extracted[title] = section_content

    return extracted


def _resolve_name_conflict(name, storage, counter):
    if name in counter:
        counter[name] += 1
        return f"{name} #{counter[name]}"
    else:
        counter[name] = 1
        if name in storage:
            storage[f"{name} #1"] = storage.pop(name)
            return f"{name} #2"
        return name

# ---------- Data Access Helpers ----------

def get_table_names(data: dict) -> list:
    return list(data.keys())

def extract_row_keys(data: dict, table: str) -> list:
    if table not in data:
        raise ValueError(f"Table '{table}' not available.")
    return list(data[table].keys())

def calculate_sum(data: dict, table: str, row: str) -> float:
    if table not in data:
        raise ValueError(f"No such table: '{table}'")
    if row not in data[table]:
        raise ValueError(f"Row '{row}' not found in table '{table}'")
    return sum(data[table][row])

# ---------- Load Excel ----------

DATA_PATH = "Data/capbudg.xls"
parsed_tables = parse_excel(DATA_PATH)

# ---------- FastAPI Setup ----------

app = FastAPI(
    title="Excel Table API",
    description="FastAPI for accessing and manipulating Excel tables",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

api = APIRouter()

@api.get("/list_tables")
def list_tables():
    try:
        return {"tables": get_table_names(parsed_tables)}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@api.get("/get_table_details")
def get_rows(table_name: str = Query(...)):
    try:
        return {
            "table": table_name,
            "rows": extract_row_keys(parsed_tables, table_name)
        }
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@api.get("/row_sum")
def get_sum(table_name: str = Query(...), row_name: str = Query(...)):
    try:
        total = calculate_sum(parsed_tables, table_name, row_name)
        return {
            "table": table_name,
            "row": row_name,
            "sum": total
        }
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

app.include_router(api)
