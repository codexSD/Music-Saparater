import subprocess
import os
from pathlib import Path

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

def run_demucs(audio_path, output_dir):
    """
    Run Demucs to separate vocals and instrumental parts.
    
    Args:
        audio_path (str): Path to the audio file
        output_dir (str): Directory where separated tracks will be saved
    """
    cmd = [
        "demucs",
        "--two-stems=vocals",
        "-o", output_dir,
        audio_path
    ]
    
    subprocess.run(cmd, check=True)

def get_demucs_outputs(output_dir, file_stem):
    """
    Get the paths to the vocal and no_vocal files from Demucs output.
    
    Args:
        output_dir (str): Directory where Demucs saved the separated tracks
        file_stem (str): Base name of the processed file without extension
    
    Returns:
        tuple: (vocals_path, no_vocals_path)
    """
    # Demucs creates a 'htdemucs' directory by default
    model_dir = os.path.join(output_dir, "htdemucs")
    
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