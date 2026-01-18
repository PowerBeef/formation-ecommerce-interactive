# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project extracts video transcripts from Sofian Kasmi's YouTube channel (@sofiankasmi) and builds an interactive learning platform for his e-commerce marketing course. The content is in French.

## Key Components

### Python Scripts

- **fetch_transcripts.py**: Fetches YouTube transcripts using `scrapetube` and `youtube-transcript-api`. Outputs to `transcripts/` directory.
- **transcribe_missing_videos.py**: For videos without available subtitles, downloads audio via `yt-dlp` and transcribes locally using OpenAI Whisper. Audio saved to `audio_downloads/`.
- **test_formation.py**: Legacy Playwright-based test suite (prefer Claude in Chrome for testing).

### Output Files

- `transcripts/` - Individual transcript files (`.txt`) and combined results
- `audio_downloads/` - MP3 audio files from YouTube videos
- `FORMATION_MARKETING_ORGANIQUE_ECOMMERCE.md` - Structured course content document
- `formation-interactive.html` - Self-contained interactive course player (single HTML file with embedded CSS/JS)

## Development Commands

```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies for transcript fetching
pip install scrapetube youtube-transcript-api

# Install dependencies for local transcription (Whisper)
pip install yt-dlp openai-whisper

# Fetch transcripts from YouTube
python fetch_transcripts.py

# Transcribe videos without subtitles using Whisper
python transcribe_missing_videos.py

```

## Deployment

**IMPORTANT:** After making any changes to this project, always push to GitHub to keep the live site updated.

- **Live site:** https://powerbeef.github.io/formation-ecommerce-interactive/
- **Repository:** https://github.com/PowerBeef/formation-ecommerce-interactive

```bash
# After making changes, sync index.html and push
cp formation-interactive.html index.html
git add -A
git commit -m "Your change description"
git push
```

Note: `index.html` is the GitHub Pages entry point (copy of `formation-interactive.html`).

## Testing

**Always use Claude in Chrome** (MCP browser automation tools) for testing the interactive HTML interface. This allows real-time browser interaction and visual verification.

To test `formation-interactive.html`:
1. Open the file in Chrome: `file:///Users/patricedery/Coding%20Projects/Formation%20Samir/formation-interactive.html`
2. Use Claude in Chrome MCP tools (`mcp__claude-in-chrome__*`) to interact with and verify UI elements

## Architecture Notes

### Transcript Pipeline
1. `fetch_transcripts.py` first tries to get YouTube's built-in transcripts (French preferred, then English)
2. Videos without transcripts are logged to `transcripts/all_results.json`
3. `transcribe_missing_videos.py` reads failed videos and processes them with Whisper
4. Both scripts append to `transcripts/COMBINED_TRANSCRIPTS.txt`

### Interactive HTML Player
The `formation-interactive.html` file is a single self-contained file with:
- CSS variables for theming (dark mode by default)
- Sidebar navigation with 9 course phases
- Video embedding, notes, progress tracking, exercises
- localStorage persistence for user progress
- Study timer functionality
- Search across lessons
