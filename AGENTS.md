# Repository Guidelines

## Project Structure & Module Organization
- `formation-interactive.html` is the primary, single-file app (HTML/CSS/JS) for the course player.
- `index.html` is the GitHub Pages entry point and should mirror `formation-interactive.html`.
- `fetch_transcripts.py` and `transcribe_missing_videos.py` implement the transcript pipeline.
- `transcripts/` stores per-video transcripts (e.g., `<video_id>_<title>.txt`), `_whisper` outputs, and combined files.
- `audio_downloads/` contains MP3s for Whisper transcription (ignored by git).
- `test_formation.py` and `test_screenshots/` support Playwright UI checks.
- `docs/` holds planning notes and supplemental docs.

## Build, Test, and Development Commands
- Create and activate a venv:
  `python3 -m venv venv && source venv/bin/activate`
- Transcript fetch dependencies:
  `pip install scrapetube youtube-transcript-api`
- Whisper transcription dependencies:
  `pip install yt-dlp openai-whisper`
- Run transcript jobs:
  `python fetch_transcripts.py` or `python transcribe_missing_videos.py`
- Playwright testing (optional):
  `pip install playwright && python -m playwright install && python test_formation.py`

## Coding Style & Naming Conventions
- Python: 4-space indentation, keep functions small and descriptive.
- HTML/CSS/JS: keep everything in `formation-interactive.html`; use the existing CSS variables in `:root` for new theme colors.
- Transcript files: preserve the `<video_id>_<title>.txt` naming pattern; keep large binaries out of git.

## Testing Guidelines
- Primary check is manual: open `formation-interactive.html` in Chrome and verify UI/UX flows.
- `test_formation.py` is a legacy Playwright script that generates screenshots into `test_screenshots/` (git-ignored).
- No formal coverage targets are enforced; prioritize key UI paths and transcript integrity.

## Commit & Pull Request Guidelines
- Follow the established commit style: `feat: ...`, `docs: ...`, `fix: ...`.
- PRs should include a short summary, test notes, and screenshots for UI changes.
- If `formation-interactive.html` changes, update `index.html` before pushing.

## Deployment Notes
- The live site is GitHub Pages backed by `index.html`. After updates:
  `cp formation-interactive.html index.html && git add -A && git commit -m "feat: ..." && git push`
