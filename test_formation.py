#!/usr/bin/env python3
"""
Interactive Formation Course Test Script
Tests all features of formation-interactive.html using Playwright
"""

from playwright.sync_api import sync_playwright
import os
import time
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
HTML_FILE = str(REPO_DIR / "formation-interactive.html")
SCREENSHOTS_DIR = str(REPO_DIR / "test_screenshots")

# Defaults: run headless for reliability; set HEADLESS=0 for interactive mode.
HEADLESS = os.environ.get("HEADLESS", "1") != "0"
SLOW_MO = int(os.environ.get("SLOW_MO", "0" if HEADLESS else "500"))

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def run_tests():
    ensure_dir(SCREENSHOTS_DIR)

    def parse_hhmmss(value: str) -> int:
        parts = value.strip().split(":")
        if len(parts) != 3:
            raise ValueError(f"Unexpected time format: {value!r}")
        h, m, s = (int(p) for p in parts)
        return h * 3600 + m * 60 + s

    def get_dashboard_study_seconds(page) -> int:
        timer_card = page.locator(
            ".stat-card",
            has=page.locator(".stat-label", has_text="Temps d'étude total"),
        )
        assert timer_card.count() == 1, "Expected a single study-time stat card on dashboard"
        raw = timer_card.locator(".stat-value").inner_text()
        return parse_hhmmss(raw)

    with sync_playwright() as p:
        # Launch browser; set HEADLESS=0 to watch the run.
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        context = browser.new_context(viewport={'width': 1400, 'height': 900})
        page = context.new_page()

        print("=" * 60)
        print("TESTING: Formation E-commerce Organique Interactive")
        print("=" * 60)

        # Test 1: Load the page
        print("\n[TEST 1] Loading the HTML file...")
        page.goto(f"file://{HTML_FILE}")
        page.wait_for_load_state('networkidle')
        page.screenshot(path=f"{SCREENSHOTS_DIR}/01_initial_load.png", full_page=True)
        print("  ✅ Page loaded successfully")

        # Test 2: Verify header elements
        print("\n[TEST 2] Checking header elements...")
        logo = page.locator(".logo-text")
        assert logo.is_visible(), "Logo should be visible"
        search = page.locator("#search-input")
        assert search.is_visible(), "Search input should be visible"
        progress = page.locator("#progress-indicator")
        assert progress.is_visible(), "Progress indicator should be visible"
        settings = page.locator(".settings-button")
        assert settings.is_visible(), "Settings button should be visible"
        print("  ✅ Header elements present")

        # Test 3: Test sidebar navigation
        print("\n[TEST 3] Testing sidebar navigation...")
        modules_tab = page.locator("#sidebar-tab-modules")
        if modules_tab.count() > 0:
            modules_tab.first.click()
            page.wait_for_timeout(300)
        phases = page.locator(".phase-header")
        phase_count = phases.count()
        print(f"  Found {phase_count} phases in sidebar")
        assert phase_count == 10, f"Expected 10 phases, found {phase_count}"
        print("  ✅ All 10 phases present in sidebar")

        # Test 4: Expand a phase and click a lesson
        print("\n[TEST 4] Expanding Phase 1 and clicking first lesson...")
        first_phase = phases.first
        first_phase.click()
        page.wait_for_timeout(500)

        lessons = page.locator(".lesson-item")
        if lessons.count() > 0:
            lessons.first.click()
            page.wait_for_timeout(1000)
            page.screenshot(path=f"{SCREENSHOTS_DIR}/02_lesson_view.png", full_page=True)
            print("  ✅ Lesson view opened successfully")

        # Test 5: Check video placeholder is present
        print("\n[TEST 5] Checking video player...")
        page.wait_for_timeout(1000)
        iframe = page.locator(".video-container iframe")
        error_panel = page.locator(".video-error")
        if iframe.count() > 0:
            print("  ✅ Invidious iframe present")
        elif error_panel.count() > 0:
            print("  ✅ Invidious error panel visible")
        else:
            raise AssertionError("Expected Invidious iframe or error panel")

        # Test 6: Test notes functionality
        print("\n[TEST 6] Testing notes functionality...")
        notes_textarea = page.locator("#lesson-notes")
        if notes_textarea.is_visible():
            test_note = "Test note from Playwright automation - " + time.strftime("%H:%M:%S")
            notes_textarea.fill(test_note)
            # Trigger blur to save
            page.keyboard.press("Tab")
            page.wait_for_timeout(1000)
            page.screenshot(path=f"{SCREENSHOTS_DIR}/03_notes_saved.png", full_page=True)
            print(f"  ✅ Notes saved: '{test_note[:30]}...'")
        else:
            print("  ⚠️ Notes textarea not found in current view")

        # Test 7: Mark lesson as complete
        print("\n[TEST 7] Testing progress tracking (mark lesson complete)...")
        complete_btn = page.locator("button:has-text('Marquer comme')")
        if complete_btn.count() > 0:
            complete_btn.first.click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOTS_DIR}/04_lesson_completed.png", full_page=True)
            print("  ✅ Lesson marked as complete")
        else:
            print("  ⚠️ Complete button not found")

        # Test 8: Navigate to Exercises
        print("\n[TEST 8] Testing Exercises section...")
        menu_tab = page.locator("#sidebar-tab-menu")
        if menu_tab.count() > 0:
            menu_tab.first.click()
            page.wait_for_timeout(200)
        exercises_nav = page.locator('.nav-item[data-view="exercises"]')
        if exercises_nav.count() > 0:
            exercises_nav.first.click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOTS_DIR}/05_exercises.png", full_page=True)

            open_sections = page.locator("details.details-card[open]")
            assert open_sections.count() > 0, "Expected at least one exercises section open"
            exercise_items = page.locator(".exercise-item")
            print(f"  Found {exercise_items.count()} exercises")

            # Mark first exercise as complete
            if exercise_items.count() > 0:
                checkbox = page.locator(".exercise-checkbox").first
                checkbox.click()
                page.wait_for_timeout(300)
                print("  ✅ Exercise checkbox toggled")
        else:
            print("  ⚠️ Exercises nav not found")

        # Test 9: Navigate to Timeline
        print("\n[TEST 9] Testing Timeline section...")
        timeline_nav = page.locator('.nav-item[data-view="timeline"]')
        if timeline_nav.count() > 0:
            timeline_nav.first.click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOTS_DIR}/06_timeline.png", full_page=True)

            timeline_items = page.locator(".timeline-item")
            print(f"  Found {timeline_items.count()} weeks in timeline")
            print("  ✅ Timeline section works")
        else:
            print("  ⚠️ Timeline nav not found")

        # Test 10: Navigate to Resources
        print("\n[TEST 10] Testing Resources section...")
        resources_nav = page.locator('.nav-item[data-view="resources"]')
        if resources_nav.count() > 0:
            resources_nav.first.click()
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOTS_DIR}/07_resources.png", full_page=True)
            print("  ✅ Resources section works")
        else:
            print("  ⚠️ Resources nav not found")

        # Test 11: Test study timer
        print("\n[TEST 11] Testing study timer accumulation...")
        dashboard_nav = page.locator('.nav-item[data-view="dashboard"]')
        if dashboard_nav.count() > 0:
            page.evaluate("() => showDashboard()")
            page.wait_for_timeout(400)
            before_seconds = get_dashboard_study_seconds(page)

            # Open a lesson and let the timer run briefly.
            modules_tab = page.locator("#sidebar-tab-modules")
            if modules_tab.count() > 0:
                modules_tab.first.click()
                page.wait_for_timeout(200)
            phases.first.click()
            page.wait_for_timeout(300)
            lessons = page.locator(".lesson-item")
            if lessons.count() > 0:
                lessons.first.click()
                page.wait_for_timeout(2500)

            page.evaluate("() => showDashboard()")
            page.wait_for_timeout(400)
            after_seconds = get_dashboard_study_seconds(page)
            assert after_seconds >= before_seconds + 2, "Study time should increase while viewing a lesson"
            print(f"  ✅ Study time increased: {before_seconds}s → {after_seconds}s")
        else:
            print("  ⚠️ Dashboard nav not found")

        # Test 12: Test search functionality
        print("\n[TEST 12] Testing search functionality...")
        search_input = page.locator("#search-input")
        if search_input.is_visible():
            search_input.fill("formation")
            page.wait_for_timeout(500)
            page.screenshot(path=f"{SCREENSHOTS_DIR}/08_search.png", full_page=True)
            search_results = page.locator(".search-result-item")
            assert search_results.count() > 0, "Expected at least one search result"
            print(f"  Found {search_results.count()} search results for 'formation'")
            search_input.fill("")  # Clear search
            print("  ✅ Search functionality works")
        else:
            print("  ⚠️ Search input not found")

        # Test 13: Test localStorage persistence
        print("\n[TEST 13] Testing localStorage persistence...")
        # Check if state is saved
        local_storage = page.evaluate("() => localStorage.getItem('formation-ecom-state')")
        if local_storage:
            print(f"  State saved to localStorage ({len(local_storage)} chars)")
            print("  ✅ localStorage persistence works")
        else:
            print("  ⚠️ No state found in localStorage")

        # Test 14: Test responsive design (mobile)
        print("\n[TEST 14] Testing responsive design (mobile view)...")
        page.set_viewport_size({'width': 375, 'height': 812})  # iPhone X size
        page.wait_for_timeout(500)
        page.screenshot(path=f"{SCREENSHOTS_DIR}/09_mobile_view.png", full_page=True)
        print("  ✅ Mobile viewport screenshot captured")

        # Reset to desktop
        page.set_viewport_size({'width': 1400, 'height': 900})
        page.wait_for_timeout(300)

        # Test 15: Reload and verify persistence
        print("\n[TEST 15] Testing persistence after reload...")
        page.reload()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(500)

        # Check if notes persisted
        notes_textarea = page.locator("#lesson-notes")
        # Navigate to a lesson first
        modules_tab = page.locator("#sidebar-tab-modules")
        if modules_tab.count() > 0:
            modules_tab.first.click()
            page.wait_for_timeout(200)
        phases.first.click()
        page.wait_for_timeout(300)
        lessons = page.locator(".lesson-item")
        if lessons.count() > 0:
            lessons.first.click()
            page.wait_for_timeout(500)

        page.screenshot(path=f"{SCREENSHOTS_DIR}/10_after_reload.png", full_page=True)
        print("  ✅ Page reloaded - check screenshots for persistence")

        # Final summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Screenshots saved to: {SCREENSHOTS_DIR}/")
        print("\nAll core tests completed!")
        print("Please review the screenshots to verify visual appearance.")
        print("=" * 60)

        # Keep browser open for 5 seconds for visual inspection
        print("\nBrowser will close in 5 seconds...")
        page.wait_for_timeout(5000)

        browser.close()

if __name__ == "__main__":
    run_tests()
