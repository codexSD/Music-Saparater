from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil
from pathlib import Path

from app.utils import extract_audio, combine_audio_video, run_demucs, get_demucs_outputs

app = FastAPI()

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process")
async def process_file(
    file: UploadFile = File(...),
    isolation_type: str = Form(...)
):
    # Generate unique ID for file processing
    process_id = str(uuid.uuid4())
    
    # Get file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_stem = os.path.splitext(file.filename)[0]
    
    # Validate file type
    valid_extensions = ['.mp3', '.wav', '.mp4', '.mkv', '.mov']
    if file_extension not in valid_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    
    # Determine if file is audio or video
    is_video = file_extension in ['.mp4', '.mkv', '.mov']
    
    # Setup file paths
    upload_path = f"uploads/{process_id}{file_extension}"
    audio_path = f"uploads/{process_id}.wav"
    output_dir = f"outputs/{process_id}"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save uploaded file
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Extract audio if video file
        if is_video:
            extract_audio(upload_path, audio_path)
        else:
            # If audio file, use it directly
            audio_path = upload_path
        
        # Run Demucs
        run_demucs(audio_path, output_dir)
        
        # Get vocal and no_vocal paths
        vocal_path, no_vocal_path = get_demucs_outputs(output_dir, Path(audio_path).stem)
        
        # Create output file based on isolation type
        if is_video:
            # For video files, need to merge audio back with video
            output_file = f"outputs/{file_stem}_{isolation_type}{file_extension}"
            selected_audio = vocal_path if isolation_type == "vocals" else no_vocal_path
            combine_audio_video(upload_path, selected_audio, output_file)
        else:
            # For audio files, just use the separated audio
            output_extension = '.wav'  # Demucs outputs WAV files
            output_file = f"outputs/{file_stem}_{isolation_type}{output_extension}"
            selected_audio = vocal_path if isolation_type == "vocals" else no_vocal_path
            shutil.copy(selected_audio, output_file)
        
        # Return the processed file
        return FileResponse(
            path=output_file,
            filename=os.path.basename(output_file),
            media_type="application/octet-stream"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    finally:
        # Clean up temporary files
        if os.path.exists(upload_path):
            os.remove(upload_path)
        
        if is_video and os.path.exists(audio_path):
            os.remove(audio_path) 