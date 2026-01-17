#!/usr/bin/env python3
"""
YouTube Channel Transcript Extractor
=====================================
Open-source tool to fetch all video transcripts from a YouTube channel.

Libraries used:
- scrapetube: https://github.com/dermasmid/scrapetube
- youtube-transcript-api: https://github.com/jdepoix/youtube-transcript-api
"""

import os
import json
import time
from datetime import datetime

try:
    import scrapetube
except ImportError:
    print("Please install scrapetube: pip install scrapetube")
    exit(1)

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
except ImportError:
    print("Please install youtube-transcript-api: pip install youtube-transcript-api")
    exit(1)


def get_channel_videos(channel_username: str) -> list:
    """
    Get all videos from a YouTube channel.

    Args:
        channel_username: The channel username (e.g., 'sofiankasmi')

    Returns:
        List of video dictionaries with id, title, etc.
    """
    print(f"🔍 Fetching videos from channel: @{channel_username}")

    videos = []
    try:
        # scrapetube can work with channel username
        for video in scrapetube.get_channel(channel_username=channel_username):
            video_info = {
                'id': video['videoId'],
                'title': video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title'),
                'published': video.get('publishedTimeText', {}).get('simpleText', 'Unknown'),
                'views': video.get('viewCountText', {}).get('simpleText', 'Unknown'),
                'duration': video.get('lengthText', {}).get('simpleText', 'Unknown'),
            }
            videos.append(video_info)
            print(f"  Found: {video_info['title'][:60]}...")
    except Exception as e:
        print(f"❌ Error fetching channel videos: {e}")
        print("   Trying alternative method with channel URL...")
        try:
            # Alternative: try with channel URL format
            channel_url = f"https://www.youtube.com/@{channel_username}"
            for video in scrapetube.get_channel(channel_url=channel_url):
                video_info = {
                    'id': video['videoId'],
                    'title': video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title'),
                    'published': video.get('publishedTimeText', {}).get('simpleText', 'Unknown'),
                    'views': video.get('viewCountText', {}).get('simpleText', 'Unknown'),
                    'duration': video.get('lengthText', {}).get('simpleText', 'Unknown'),
                }
                videos.append(video_info)
                print(f"  Found: {video_info['title'][:60]}...")
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")

    print(f"✅ Found {len(videos)} videos total")
    return videos


def fetch_transcript(video_id: str, languages: list = ['fr', 'en']) -> dict:
    """
    Fetch transcript for a single video.

    Args:
        video_id: YouTube video ID
        languages: List of language codes to try (in order of preference)

    Returns:
        Dictionary with transcript data or error info
    """
    ytt_api = YouTubeTranscriptApi()
    formatter = TextFormatter()

    try:
        # Try to get transcript in preferred languages
        transcript = ytt_api.fetch(video_id, languages=languages)

        # Format as plain text
        text = formatter.format_transcript(transcript)

        return {
            'success': True,
            'transcript': text,
            'segments': transcript,  # Keep raw segments with timestamps
            'language': languages[0] if transcript else 'unknown'
        }
    except Exception as e:
        # Try to list available transcripts
        try:
            transcript_list = ytt_api.list(video_id)
            available = [t.language_code for t in transcript_list]

            # Try any available transcript
            if available:
                transcript = ytt_api.fetch(video_id, languages=available)
                text = formatter.format_transcript(transcript)
                return {
                    'success': True,
                    'transcript': text,
                    'segments': transcript,
                    'language': available[0]
                }
        except:
            pass

        return {
            'success': False,
            'error': str(e),
            'transcript': None
        }


def main():
    # Configuration
    CHANNEL_USERNAME = "sofiankasmi"  # The channel to scrape
    OUTPUT_DIR = "transcripts"
    DELAY_BETWEEN_REQUESTS = 1  # Seconds between requests to be respectful

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("YouTube Channel Transcript Extractor")
    print("=" * 60)
    print(f"Channel: @{CHANNEL_USERNAME}")
    print(f"Output: {OUTPUT_DIR}/")
    print("=" * 60)
    print()

    # Step 1: Get all videos from channel
    videos = get_channel_videos(CHANNEL_USERNAME)

    if not videos:
        print("❌ No videos found. Please check the channel username.")
        return

    # Save video list
    video_list_path = os.path.join(OUTPUT_DIR, "video_list.json")
    with open(video_list_path, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print(f"\n📋 Video list saved to: {video_list_path}")

    # Step 2: Fetch transcripts for each video
    print("\n" + "=" * 60)
    print("Fetching transcripts...")
    print("=" * 60)

    results = []
    successful = 0
    failed = 0

    for i, video in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] {video['title'][:50]}...")

        result = fetch_transcript(video['id'])

        video_result = {
            **video,
            'transcript_success': result['success'],
            'transcript_language': result.get('language', 'N/A'),
        }

        if result['success']:
            successful += 1
            print(f"  ✅ Success ({result.get('language', 'unknown')})")

            # Save individual transcript
            safe_title = "".join(c for c in video['title'] if c.isalnum() or c in ' -_')[:50]
            transcript_path = os.path.join(OUTPUT_DIR, f"{video['id']}_{safe_title}.txt")

            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {video['title']}\n")
                f.write(f"Video ID: {video['id']}\n")
                f.write(f"URL: https://www.youtube.com/watch?v={video['id']}\n")
                f.write(f"Duration: {video['duration']}\n")
                f.write(f"Published: {video['published']}\n")
                f.write("=" * 60 + "\n\n")
                f.write(result['transcript'])

            video_result['transcript_file'] = transcript_path
        else:
            failed += 1
            print(f"  ❌ Failed: {result.get('error', 'Unknown error')[:50]}")
            video_result['error'] = result.get('error', 'Unknown error')

        results.append(video_result)

        # Be respectful with rate limiting
        if i < len(videos):
            time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save combined results
    results_path = os.path.join(OUTPUT_DIR, "all_results.json")
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Create a combined transcript file for easy reading
    combined_path = os.path.join(OUTPUT_DIR, "COMBINED_TRANSCRIPTS.txt")
    with open(combined_path, 'w', encoding='utf-8') as f:
        f.write(f"Combined Transcripts from @{CHANNEL_USERNAME}\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            if result['transcript_success'] and 'transcript_file' in result:
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"VIDEO: {result['title']}\n")
                f.write(f"URL: https://www.youtube.com/watch?v={result['id']}\n")
                f.write(f"Duration: {result['duration']}\n")
                f.write("=" * 80 + "\n\n")

                # Read the individual transcript
                try:
                    with open(result['transcript_file'], 'r', encoding='utf-8') as tf:
                        content = tf.read()
                        # Skip the header we already added
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
    print(f"Total videos: {len(videos)}")
    print(f"Successful transcripts: {successful}")
    print(f"Failed: {failed}")
    print(f"\nOutput files:")
    print(f"  📋 Video list: {video_list_path}")
    print(f"  📊 Results: {results_path}")
    print(f"  📖 Combined: {combined_path}")
    print(f"  📁 Individual transcripts: {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
