#!/usr/bin/env python3
"""
YouTube Video Transcription Tool
=================================
Downloads audio from YouTube videos and transcribes them using OpenAI Whisper.

Open-source tools used:
- yt-dlp: https://github.com/yt-dlp/yt-dlp
- OpenAI Whisper: https://github.com/openai/whisper

This runs entirely locally - no API keys or cloud services needed.
"""

import os
import json
import subprocess
import sys
from pathlib import Path

# Check for required packages
def check_and_install_packages():
    """Check and install required packages."""
    packages_needed = []

    # Check yt-dlp
    try:
        import yt_dlp
        print("✅ yt-dlp is installed")
    except ImportError:
        packages_needed.append("yt-dlp")

    # Check whisper
    try:
        import whisper
        print("✅ openai-whisper is installed")
    except ImportError:
        packages_needed.append("openai-whisper")

    if packages_needed:
        print(f"\n📦 Installing missing packages: {', '.join(packages_needed)}")
        for package in packages_needed:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("✅ All packages installed!\n")
        return True
    return False

def get_failed_videos():
    """Get list of videos that failed to get transcripts."""
    results_path = "transcripts/all_results.json"

    if not os.path.exists(results_path):
        print("❌ No results file found. Run fetch_transcripts.py first.")
        return []

    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)

    failed_videos = [
        video for video in results
        if not video.get('transcript_success', False)
    ]

    return failed_videos

def download_audio(video_id: str, output_dir: str) -> str:
    """
    Download audio from a YouTube video using yt-dlp.

    Args:
        video_id: YouTube video ID
        output_dir: Directory to save the audio file

    Returns:
        Path to the downloaded audio file
    """
    import yt_dlp

    output_path = os.path.join(output_dir, f"{video_id}.mp3")

    # Skip if already downloaded
    if os.path.exists(output_path):
        return output_path

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, f"{video_id}.%(ext)s"),
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        print(f"  ❌ Download failed: {e}")
        return None

def transcribe_audio(audio_path: str, model_name: str = "base") -> dict:
    """
    Transcribe audio file using OpenAI Whisper.

    Args:
        audio_path: Path to the audio file
        model_name: Whisper model to use (tiny, base, small, medium, large)

    Returns:
        Dictionary with transcription results
    """
    import whisper

    try:
        # Load model (will download on first use)
        model = whisper.load_model(model_name)

        # Transcribe with language detection
        result = model.transcribe(
            audio_path,
            language=None,  # Auto-detect language
            verbose=False
        )

        return {
            'success': True,
            'text': result['text'],
            'language': result.get('language', 'unknown'),
            'segments': result.get('segments', [])
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    print("=" * 60)
    print("YouTube Video Transcription Tool")
    print("Using: yt-dlp + OpenAI Whisper (100% local & open-source)")
    print("=" * 60)
    print()

    # Check and install packages
    if check_and_install_packages():
        # Re-import after installation
        print("Packages installed. Please run the script again.")
        return

    # Configuration
    AUDIO_DIR = "audio_downloads"
    TRANSCRIPT_DIR = "transcripts"
    WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
    # Note: "base" is a good balance of speed and accuracy
    # "tiny" is faster but less accurate
    # "medium" or "large" are more accurate but slower and need more RAM

    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

    # Get videos that failed
    failed_videos = get_failed_videos()

    if not failed_videos:
        print("✅ All videos already have transcripts!")
        return

    print(f"📋 Found {len(failed_videos)} videos without transcripts")
    print(f"🎤 Using Whisper model: {WHISPER_MODEL}")
    print()

    # Process each video
    results = []
    successful = 0
    failed = 0

    for i, video in enumerate(failed_videos, 1):
        video_id = video['id']
        title = video['title'][:50]

        print(f"\n[{i}/{len(failed_videos)}] {title}...")

        # Step 1: Download audio
        print("  📥 Downloading audio...")
        audio_path = download_audio(video_id, AUDIO_DIR)

        if not audio_path or not os.path.exists(audio_path):
            print("  ❌ Download failed, skipping...")
            failed += 1
            results.append({
                **video,
                'whisper_success': False,
                'error': 'Download failed'
            })
            continue

        # Step 2: Transcribe with Whisper
        print("  🎤 Transcribing with Whisper...")
        transcription = transcribe_audio(audio_path, WHISPER_MODEL)

        if transcription['success']:
            successful += 1
            print(f"  ✅ Success! (Language: {transcription.get('language', 'unknown')})")

            # Save individual transcript
            safe_title = "".join(c for c in video['title'] if c.isalnum() or c in ' -_')[:50]
            transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}_{safe_title}_whisper.txt")

            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {video['title']}\n")
                f.write(f"Video ID: {video_id}\n")
                f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                f.write(f"Duration: {video.get('duration', 'Unknown')}\n")
                f.write(f"Transcribed with: OpenAI Whisper ({WHISPER_MODEL})\n")
                f.write(f"Detected Language: {transcription.get('language', 'unknown')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(transcription['text'])

            results.append({
                **video,
                'whisper_success': True,
                'whisper_language': transcription.get('language'),
                'transcript_file': transcript_path
            })
        else:
            failed += 1
            print(f"  ❌ Transcription failed: {transcription.get('error', 'Unknown error')[:50]}")
            results.append({
                **video,
                'whisper_success': False,
                'error': transcription.get('error', 'Unknown error')
            })

    # Save results
    whisper_results_path = os.path.join(TRANSCRIPT_DIR, "whisper_results.json")
    with open(whisper_results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Append to combined transcripts
    combined_path = os.path.join(TRANSCRIPT_DIR, "COMBINED_TRANSCRIPTS.txt")
    with open(combined_path, 'a', encoding='utf-8') as f:
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("WHISPER TRANSCRIPTIONS (Videos without YouTube subtitles)\n")
        f.write("=" * 80 + "\n")

        for result in results:
            if result.get('whisper_success') and 'transcript_file' in result:
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"VIDEO: {result['title']}\n")
                f.write(f"URL: https://www.youtube.com/watch?v={result['id']}\n")
                f.write(f"Duration: {result.get('duration', 'Unknown')}\n")
                f.write(f"Transcribed with: Whisper ({WHISPER_MODEL})\n")
                f.write("=" * 80 + "\n\n")

                try:
                    with open(result['transcript_file'], 'r', encoding='utf-8') as tf:
                        content = tf.read()
                        if "=" * 60 in content:
                            content = content.split("=" * 60 + "\n\n", 1)[-1]
                        f.write(content)
                except:
                    pass
                f.write("\n\n")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total videos processed: {len(failed_videos)}")
    print(f"Successfully transcribed: {successful}")
    print(f"Failed: {failed}")
    print(f"\nOutput files:")
    print(f"  📁 Audio files: {AUDIO_DIR}/")
    print(f"  📋 Whisper results: {whisper_results_path}")
    print(f"  📖 Individual transcripts: {TRANSCRIPT_DIR}/")
    print(f"  📖 Combined transcripts updated: {combined_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
