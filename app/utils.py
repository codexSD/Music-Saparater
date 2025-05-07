import subprocess
import os
import tempfile
from pathlib import Path
import torch
import numpy as np
from typing import Dict, Any, Optional

def extract_audio(video_path, audio_path):
    """
    Extract audio from a video file using FFmpeg.
    
    Args:
        video_path (str): Path to the video file
        audio_path (str): Path where the extracted audio will be saved
    """
    cmd = [
        "ffmpeg", 
        "-i", video_path, 
        "-q:a", "0", 
        "-map", "a", 
        audio_path, 
        "-y"
    ]
    
    subprocess.run(cmd, check=True)

def combine_audio_video(original_video, new_audio, output_path):
    """
    Combine video from the original file with a new audio track using FFmpeg.
    
    Args:
        original_video (str): Path to the original video file
        new_audio (str): Path to the new audio file
        output_path (str): Path where the combined video will be saved
    """
    cmd = [
        "ffmpeg",
        "-i", original_video,
        "-i", new_audio,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path,
        "-y"
    ]
    
    subprocess.run(cmd, check=True)

def run_demucs(audio_path, output_dir, options: Optional[Dict[str, Any]] = None):
    """
    Run Demucs to separate vocals and instrumental parts with options.
    
    Args:
        audio_path (str): Path to the audio file
        output_dir (str): Directory where separated tracks will be saved
        options (dict, optional): Additional processing options
            - quality: "fast", "medium", "better", "best"
            - noise_reduction: True/False
            - stem_balance: -1.0 to 1.0 (negative: more vocals, positive: more music)
    """
    # Default options
    if options is None:
        options = {}
    
    # Check if CUDA is available
    device_arg = ["--device", "cuda"] if torch.cuda.is_available() else []
    
    # Quality settings
    quality = options.get("quality", "better")
    quality_args = []
    
    if quality == "fast":
        quality_args = ["--shifts", "2"]
    elif quality == "medium":
        quality_args = ["--shifts", "5"]
    elif quality == "better":
        quality_args = ["--shifts", "10"]
    elif quality == "best":
        quality_args = ["--shifts", "15"]
    
    # Build the command
    cmd = [
        "demucs",
        "--two-stems=vocals",
        "-o", output_dir,
    ] + device_arg + quality_args + [audio_path]
    
    print(f"Running Demucs with command: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    # Apply post-processing if needed
    vocal_path, no_vocal_path = get_demucs_outputs(output_dir, Path(audio_path).stem)
    
    # Apply noise reduction if enabled
    if options.get("noise_reduction", False) and os.path.exists(vocal_path):
        apply_noise_reduction(vocal_path, vocal_path)
    
    # Apply stem balance if specified
    stem_balance = options.get("stem_balance", 0)
    if stem_balance != 0 and os.path.exists(vocal_path) and os.path.exists(no_vocal_path):
        adjust_stem_balance(vocal_path, no_vocal_path, stem_balance)

def get_demucs_outputs(output_dir, file_stem):
    """
    Get the paths to the vocal and no_vocal files from Demucs output.
    
    Args:
        output_dir (str): Directory where Demucs saved the separated tracks
        file_stem (str): Base name of the processed file without extension
    
    Returns:
        tuple: (vocals_path, no_vocals_path)
    """
    # Check which model folder exists (htdemucs or htdemucs_ft)
    model_dirs = ["htdemucs", "htdemucs_ft", "htdemucs_6s", "mdx_extra"]
    model_dir = None
    
    for dir_name in model_dirs:
        potential_path = os.path.join(output_dir, dir_name)
        if os.path.exists(potential_path):
            model_dir = potential_path
            break
    
    if not model_dir:
        raise Exception("No output found from Demucs processing")
    
    # Get the exact file name from the Demucs output directory
    file_dirs = os.listdir(model_dir)
    if not file_dirs:
        raise Exception("No output found from Demucs processing")
    
    file_dir = file_dirs[0]  # Take the first directory, which should correspond to our file
    
    # Paths to the vocal and no_vocal files
    vocals_path = os.path.join(model_dir, file_dir, "vocals.wav")
    no_vocals_path = os.path.join(model_dir, file_dir, "no_vocals.wav")
    
    # Ensure files exist
    if not os.path.exists(vocals_path) or not os.path.exists(no_vocals_path):
        raise Exception("Demucs did not produce the expected output files")
    
    return vocals_path, no_vocals_path

def apply_noise_reduction(input_path, output_path):
    """
    Apply noise reduction to an audio file using FFmpeg.
    
    Args:
        input_path (str): Path to the input audio file
        output_path (str): Path where the noise-reduced audio will be saved
    """
    # Create a temporary file for the processed audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_path = temp_file.name
    temp_file.close()
    
    try:
        # Apply noise reduction filter
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-af", "anlmdn=s=0.001:p=0.95:r=0.9",
            temp_path,
            "-y"
        ]
        
        subprocess.run(cmd, check=True)
        
        # Replace the original file with the processed file
        os.replace(temp_path, output_path)
    
    except Exception as e:
        # Clean up temp file in case of error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"Error applying noise reduction: {str(e)}")

def adjust_stem_balance(vocals_path, no_vocals_path, balance):
    """
    Adjust the balance between vocals and instrumental parts.
    
    Args:
        vocals_path (str): Path to the vocals audio file
        no_vocals_path (str): Path to the no_vocals audio file
        balance (float): Balance value from -1.0 to 1.0
            - Negative: enhance vocals
            - Positive: enhance instrumental
    """
    # Create temporary files
    temp_vocals = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_no_vocals = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_vocals_path = temp_vocals.name
    temp_no_vocals_path = temp_no_vocals.name
    temp_vocals.close()
    temp_no_vocals.close()
    
    try:
        # Determine volume adjustments based on balance
        vocal_vol = 1.0 + max(0, -balance)
        music_vol = 1.0 + max(0, balance)
        
        # Adjust volumes
        subprocess.run([
            "ffmpeg",
            "-i", vocals_path,
            "-filter:a", f"volume={vocal_vol}",
            temp_vocals_path,
            "-y"
        ], check=True)
        
        subprocess.run([
            "ffmpeg",
            "-i", no_vocals_path,
            "-filter:a", f"volume={music_vol}",
            temp_no_vocals_path,
            "-y"
        ], check=True)
        
        # Replace original files
        os.replace(temp_vocals_path, vocals_path)
        os.replace(temp_no_vocals_path, no_vocals_path)
        
    except Exception as e:
        # Clean up temp files in case of error
        if os.path.exists(temp_vocals_path):
            os.remove(temp_vocals_path)
        if os.path.exists(temp_no_vocals_path):
            os.remove(temp_no_vocals_path)
        print(f"Error adjusting stem balance: {str(e)}") 