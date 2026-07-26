# Dynamic Cell Qualification Protocol (CQP) Generator

A production-grade document automation service and web frontend that ingests cell qualification source documents (`TMP_*.docx`, `ACL_*.docx`, `DATASHEET_*.pdf`) and automatically renders finished, correctly-formatted Cell Qualification Protocols (`CQP_<cell>.docx`) matching regulatory standards under framework **IESF-4400**.

---

## 🚀 Quickstart (Run in < 5 Minutes)

### Option 1: Local Python Environment
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the application server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open **`http://localhost:8000`** in your browser.

---

### Option 2: Docker Compose
```bash
docker-compose up --build
```
Open **`http://localhost:8000`** in your browser.

---

## 🧪 Running the Test Suite
Execute the full unit and integration test suite across **Set A**, **Set B**, and **Set C**:
```bash
PYTHONPATH=. pytest
```

---

## 📁 Repository Structure
```
cell-qualification-generator/
├── app/
│   ├── main.py                     # FastAPI server & route handlers
│   ├── models/                     # Pydantic schemas (CellQualificationData, DutyProfile)
│   ├── generator/                  # Document generation & OpenXML engine
│   │   ├── core.py                 # Core orchestrator & input auto-correction
│   │   ├── pdf_parser.py           # Multi-engine PDF datasheet extractor
│   │   ├── docx_parser.py          # TMP & ACL parsers
│   │   ├── template_engine.py      # Run-consolidation & block cloning
│   │   └── docx_builder.py         # Table merging & document locking
│   └── frontend/                   # React + Vite web user interface
├── outputs/                        # Clean generated protocol outputs (Set A, B, C)
├── test_files/                     # Input sets (Set A, B, C), template, & GOLD reference
├── SOLUTION.md                     # Architecture blueprint & failure mode analysis
├── requirements.txt                # Python package dependencies
├── Dockerfile                      # Container build definition
└── docker-compose.yml              # Container composition specification
```

---

## 📄 Submission Files
The clean final outputs generated for all three input sets are saved in `outputs/`:
- **`outputs/CQP_SetA_Output.docx`** (Set A: `CYG-21700-50G`)
- **`outputs/CQP_SetB_Output.docx`** (Set B: `AUR-PR-340`)
- **`outputs/CQP_SetC_Output.docx`** (Set C: `PLX-PCH-088`)
