import os
import traceback
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.utils.file_handlers import save_upload_to_tempfile
from app.generator.core import generate_protocol

app = FastAPI(title="CQP Generator API")

@app.post("/generate")
async def generate_cqp(
    tmp_file: UploadFile = File(...),
    acl_file: UploadFile = File(...),
    datasheet_file: UploadFile = File(...),
    market: str = Form("EU / UN-38.3")
):
    output_path = os.path.abspath("outputs/CQP_Generated.docx")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    template_path = os.path.abspath("test_files/template/CQP_Template.docx")
    if not os.path.exists(template_path):
        template_path = os.path.abspath("template/CQP_Template.docx")
        
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file CQP_Template.docx not found.")
    
    try:
        with save_upload_to_tempfile(tmp_file, ".docx") as tmp_path, \
             save_upload_to_tempfile(acl_file, ".docx") as acl_path, \
             save_upload_to_tempfile(datasheet_file, ".pdf") as pdf_path:
             
            generate_protocol(
                tmp_path=tmp_path,
                acl_path=acl_path,
                datasheet_path=pdf_path,
                market=market,
                output_path=output_path,
                template_path=template_path
            )
            
        return FileResponse(
            path=output_path,
            filename="CQP_Generated.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return FileResponse("app/frontend/index.html")

app.mount("/", StaticFiles(directory="app/frontend"), name="static")
