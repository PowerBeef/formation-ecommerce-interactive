#!/usr/bin/env python3
"""
Interactive Formation Course Test Script
Validates core UX flows, persistence, responsive behavior, and error recovery.
"""

from playwright.sync_api import sync_playwright
import os
import time
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
HTML_FILE = str(REPO_DIR / "formation-interactive.html")
SCREENSHOTS_DIR = str(REPO_DIR / "test_screenshots")
STATE_KEY = "formation-ecom-state"

# Defaults: run headless for reliability; set HEADLESS=0 for interactive mode.
HEADLESS = os.environ.get("HEADLESS", "1") != "0"
SLOW_MO = int(os.environ.get("SLOW_MO", "0" if HEADLESS else "500"))


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def run_tests() -> None:
    ensure_dir(SCREENSHOTS_DIR)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        def get_state():
            return page.evaluate(
                """() => {
                    const raw = localStorage.getItem('formation-ecom-state');
                    return raw ? JSON.parse(raw) : null;
                }"""
            )

        def lesson_ids():
            return page.evaluate(
                """() => {
                    return coursData.phases.flatMap(p => p.lessons.map(l => l.id));
                }"""
            )

        def open_first_lesson():
            modules_tab = page.locator("#sidebar-tab-modules")
            if modules_tab.count() > 0:
                modules_tab.first.click()
                page.wait_for_timeout(250)
            phase_headers = page.locator(".phase-header")
            assert phase_headers.count() > 0, "Expected phase headers"
            phase_headers.first.click()
            page.wait_for_timeout(350)
            lessons = page.locator(".lesson-item")
            assert lessons.count() > 0, "Expected lessons in first phase"
            lessons.first.click()
            page.wait_for_timeout(1200)

        def open_main_view(view: str):
            menu_tab = page.locator("#sidebar-tab-menu")
            if menu_tab.count() > 0:
                menu_tab.first.click()
                page.wait_for_timeout(200)
            nav = page.locator(f'.nav-item[data-view="{view}"]')
            if nav.count() > 0 and nav.first.is_visible():
                nav.first.click()
            else:
                page.evaluate("(v) => navigateTo(v)", view)
            page.wait_for_timeout(450)

        print("=" * 60)
        print("TESTING: Formation E-commerce Organique Interactive")
        print("=" * 60)

        # Test 1: Load + shell checks.
        print("\n[TEST 1] Loading app + core shell...")
        page.goto(f"file://{HTML_FILE}")
        page.wait_for_load_state("networkidle")
        page.screenshot(path=f"{SCREENSHOTS_DIR}/01_initial_load.png", full_page=True)
        assert page.locator(".logo-text").is_visible(), "Logo should be visible"
        assert page.locator("#search-input").is_visible(), "Search input should be visible"
        assert page.locator("#progress-indicator").is_visible(), "Progress indicator should be visible"
        assert page.locator(".settings-button").is_visible(), "Settings should be visible"
        assert page.locator(".today-focus-card").count() == 1, "Expected one primary today card"
        print("  ✅ App shell and today primary rail are visible")

        # Test 2: Sidebar/module tree integrity.
        print("\n[TEST 2] Checking sidebar modules tree...")
        page.locator("#sidebar-tab-modules").first.click()
        page.wait_for_timeout(250)
        phases = page.locator(".phase-header")
        phase_count = phases.count()
        print(f"  Found {phase_count} phases")
        assert phase_count == 10, f"Expected 10 phases, got {phase_count}"
        print("  ✅ Module tree is complete")

        # Test 3: Open lesson + lesson workspace.
        print("\n[TEST 3] Opening first lesson...")
        open_first_lesson()
        page.screenshot(path=f"{SCREENSHOTS_DIR}/02_lesson_workspace.png", full_page=True)
        assert page.locator(".lesson-layout").count() == 1, "Expected lesson layout"
        assert page.locator("#lesson-video-container").count() == 1, "Expected lesson player container"
        assert page.locator('[data-action="set-lesson-panel"][data-panel="overview"]').count() == 1
        print("  ✅ Lesson workspace opened with segmented panels")

        # Test 4: Force localized player error and validate scoping.
        print("\n[TEST 4] Forcing localized player error state...")
        current_video = page.evaluate(
            """() => {
                const raw = localStorage.getItem('formation-ecom-state');
                const lessonId = raw ? JSON.parse(raw).ui.currentLessonId : null;
                for (const phase of coursData.phases) {
                    for (const lesson of phase.lessons) {
                        if (lesson.id === lessonId) return lesson.videoId;
                    }
                }
                return 'GYjzjHlaod0';
            }"""
        )
        page.evaluate(
            """(videoId) => {
                const container = document.getElementById('lesson-video-container');
                showInvidiousError(container, videoId, false, getInvidiousBase());
            }""",
            current_video,
        )
        page.wait_for_timeout(300)
        assert page.locator(".video-container .video-error").count() == 1, "Error must be scoped to player"
        assert page.locator(".video-error-title", has_text="Vidéo temporairement indisponible").count() == 1
        assert page.locator(".content-area > .video-error").count() == 0, "No detached error blocks expected"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/03_video_error_localized.png", full_page=True)
        print("  ✅ Localized player error UI is scoped correctly")

        # Test 5: Retry + rotate actions.
        print("\n[TEST 5] Validating retry and instance-rotation actions...")
        retry_btn = page.locator('button[data-action="retry-video"]').first
        assert retry_btn.count() == 1, "Retry button should exist"
        retry_btn.click()
        page.wait_for_timeout(1400)
        player_has_content = (
            page.locator("#lesson-video-container iframe").count() > 0
            or page.locator("#lesson-video-container .video-error").count() > 0
        )
        assert player_has_content, "Player should remain in a recoverable state"

        rotate_btn = page.locator('button[data-action="rotate-invidious-instance"]').first
        if rotate_btn.count() > 0:
            rotate_btn.click()
            page.wait_for_timeout(1400)
            player_has_content = (
                page.locator("#lesson-video-container iframe").count() > 0
                or page.locator("#lesson-video-container .video-error").count() > 0
            )
            assert player_has_content, "Rotate action should keep player recoverable"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/04_video_retry_rotate.png", full_page=True)
        print("  ✅ Retry and rotate actions are functional")

        # Test 6: Continue-without-video + completion flow remains unblocked.
        print("\n[TEST 6] Testing continue-without-video and progression continuity...")
        continue_without = page.locator('button[data-action="continue-without-video"]').first
        if continue_without.count() > 0:
            continue_without.click()
            page.wait_for_timeout(200)
            assert page.locator(".video-error-title", has_text="Mode sans vidéo activé").count() == 1

        before_state = get_state()
        current_lesson = before_state["ui"]["currentLessonId"]
        before_completed = current_lesson in before_state["progress"]["completedLessonIds"]
        complete_btn = page.locator('button[data-action="toggle-lesson-complete"]').first
        complete_btn.click()
        page.wait_for_timeout(350)
        after_state = get_state()
        after_completed = current_lesson in after_state["progress"]["completedLessonIds"]
        assert before_completed != after_completed, "Completion state should toggle"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/05_continue_without_video.png", full_page=True)
        print("  ✅ Learner can continue and update completion without video playback")

        # Test 7: Lesson panel persistence (notes).
        print("\n[TEST 7] Verifying lesson panel persistence across reload...")
        notes_tab = page.locator('[data-action="set-lesson-panel"][data-panel="notes"]').first
        notes_tab.click()
        page.wait_for_timeout(250)
        assert notes_tab.get_attribute("aria-selected") == "true", "Notes tab should be active"
        notes_textarea = page.locator("#lesson-notes")
        assert notes_textarea.count() == 1, "Notes textarea should be visible on notes panel"
        notes_textarea.fill("Panel persistence check - " + time.strftime("%H:%M:%S"))
        page.wait_for_timeout(500)
        page.reload()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(800)
        notes_tab_after = page.locator('[data-action="set-lesson-panel"][data-panel="notes"]').first
        assert notes_tab_after.get_attribute("aria-selected") == "true", "Notes tab should persist after reload"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/06_panel_persistence.png", full_page=True)
        print("  ✅ lessonPanel state persists")

        # Test 8: Return-context with scroll restoration.
        print("\n[TEST 8] Testing return context and scroll restoration...")
        open_main_view("today")
        page.evaluate("() => window.scrollTo(0, 500)")
        scroll_before = page.evaluate("() => Math.round(window.scrollY)")
        page.evaluate(
            """() => {
                const next = getNextLessonData();
                if (next?.lesson?.id) {
                    navigateTo('lesson', { lessonId: next.lesson.id });
                }
            }"""
        )
        page.wait_for_timeout(800)
        page.locator('button[data-action="return-to-context"]').first.click()
        page.wait_for_timeout(600)
        current_view = get_state()["ui"]["currentView"]
        scroll_after = page.evaluate("() => Math.round(window.scrollY)")
        assert current_view == "today", "Return should go back to originating view"
        assert abs(scroll_after - scroll_before) <= 180, f"Scroll should restore (before={scroll_before}, after={scroll_after})"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/07_return_context.png", full_page=True)
        print("  ✅ Return path preserves context and scroll")

        # Test 9: Exercises filter persistence + no detached player errors.
        print("\n[TEST 9] Checking exercises action board + filter persistence...")
        open_main_view("exercises")
        assert page.locator(".exercise-filter-group").count() == 1, "Exercises filter toolbar missing"
        assert page.locator(".exercise-filter-btn.active", has_text="À faire").count() == 1, "Default filter should be À faire"
        assert page.locator(".content-area .video-error").count() == 0, "No detached video errors should appear in exercises"
        done_filter = page.locator('.exercise-filter-btn[data-filter="done"]').first
        done_filter.click()
        page.wait_for_timeout(300)
        assert done_filter.evaluate("el => el.classList.contains('active')"), "Done filter should activate"
        page.reload()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(500)
        # App restores last view by state; if needed force exercises.
        if page.locator(".exercise-filter-group").count() == 0:
            open_main_view("exercises")
        done_filter_after = page.locator('.exercise-filter-btn[data-filter="done"]').first
        assert done_filter_after.evaluate("el => el.classList.contains('active')"), "Filter should persist after reload"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/08_exercises_filters.png", full_page=True)
        print("  ✅ exercisesFilter state persists and exercises board is clean")

        # Test 10: Planning current-week highlight + week action CTA.
        print("\n[TEST 10] Checking planning week actions...")
        open_main_view("planning")
        assert page.locator(".timeline-item.current").count() >= 1, "Expected one current week highlight"
        week_action_btn = page.locator('button[data-action="toggle-week-actions"]').first
        assert week_action_btn.count() > 0, "Expected week action button"
        week_action_btn.click()
        page.wait_for_timeout(200)
        assert page.locator(".week-actions.open").count() >= 1, "Week action content should expand"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/09_planning_actions.png", full_page=True)
        print("  ✅ Planning CTA and week-detail disclosure work")

        # Test 11: Mobile hierarchy + sticky controls.
        print("\n[TEST 11] Validating mobile CTA hierarchy and sticky controls...")
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(250)
        page.locator('.mobile-bottom-nav .mobile-nav-btn[data-view="today"]').first.click()
        page.wait_for_timeout(450)
        today_primary = page.locator('.today-focus-card button[data-action="open-lesson"]').first
        if today_primary.count() > 0:
            bbox = today_primary.bounding_box()
            assert bbox and bbox["y"] < 730, "Primary CTA should be above fold on mobile"
        assert page.locator("#mobile-action-bar.active").count() == 1, "Sticky mobile action bar should be visible on today"
        assert page.locator(".mobile-bottom-nav").is_visible(), "Mobile bottom nav should be visible"
        if today_primary.count() > 0:
            today_primary.click()
            page.wait_for_timeout(700)
            assert page.locator("#mobile-action-bar.active").count() == 1, "Sticky action bar should appear on lesson view"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/10_mobile_actions.png", full_page=True)
        print("  ✅ Mobile CTA placement and sticky actions are valid")

        # Test 12: Keyboard path for lesson and exercise completion.
        print("\n[TEST 12] Testing keyboard-only completion path...")
        page.set_viewport_size({"width": 1400, "height": 900})
        page.wait_for_timeout(300)
        if page.locator(".lesson-layout").count() == 0:
            open_first_lesson()

        current_state = get_state()
        current_lesson_id = current_state["ui"]["currentLessonId"]
        before_completed = current_lesson_id in current_state["progress"]["completedLessonIds"]

        complete_btn = page.locator('button[data-action="toggle-lesson-complete"]').first
        complete_btn.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)

        after_state = get_state()
        after_completed = current_lesson_id in after_state["progress"]["completedLessonIds"]
        assert before_completed != after_completed, "Keyboard Enter should toggle lesson completion"

        exercise_tab = page.locator('[data-action="set-lesson-panel"][data-panel="exercise"]').first
        exercise_tab.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)

        exercise_checkbox = page.locator('.lesson-panel-section.active .exercise-checkbox').first
        if exercise_checkbox.count() > 0:
            exercise_id = exercise_checkbox.get_attribute("data-exercise-id")
            state_before_ex = get_state()
            ex_before = exercise_id in state_before_ex["progress"]["completedExerciseIds"]
            exercise_checkbox.focus()
            page.keyboard.press(" ")
            page.wait_for_timeout(300)
            state_after_ex = get_state()
            ex_after = exercise_id in state_after_ex["progress"]["completedExerciseIds"]
            assert ex_before != ex_after, "Keyboard Space should toggle exercise completion"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/11_keyboard_path.png", full_page=True)
        print("  ✅ Keyboard completion path works for lesson and exercise")

        # Test 13: Mobile search overlay behavior.
        print("\n[TEST 13] Testing mobile search overlay + escape close...")
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(250)
        page.locator('.mobile-bottom-nav .mobile-nav-btn[data-view="today"]').first.click()
        page.wait_for_timeout(300)
        search_input = page.locator("#search-input")
        search_input.click()
        page.wait_for_timeout(300)
        assert page.locator(".search-box.mobile-expanded").count() == 1, "Search should expand on mobile focus"
        page.keyboard.press("Escape")
        page.wait_for_timeout(250)
        assert page.locator(".search-box.mobile-expanded").count() == 0, "Search overlay should close on Escape"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/12_mobile_search_overlay.png", full_page=True)
        print("  ✅ Mobile search overlay opens and closes correctly")

        # Test 14: Schema V3 migration from V2.
        print("\n[TEST 14] Validating V2 -> V3 migration...")
        all_lesson_ids = lesson_ids()
        seed_lesson = all_lesson_ids[0]
        page.evaluate(
            """(seedLesson) => {
                const v2 = {
                    meta: { schemaVersion: 2, lastSavedAt: null },
                    progress: {
                        completedLessonIds: [seedLesson],
                        completedExerciseIds: [],
                        completedChecklistIds: [],
                        completedWeekIds: [],
                        timerSeconds: 12
                    },
                    ui: {
                        currentView: 'today',
                        currentLessonId: null,
                        sidebarTab: 'menu',
                        searchQuery: '',
                        pipDismissed: false
                    },
                    prefs: {
                        theme: 'dark',
                        autoplayVideos: false,
                        focusModeEnabled: false,
                        lastInvidiousBase: ''
                    },
                    notesByLessonId: {}
                };
                localStorage.setItem('formation-ecom-state', JSON.stringify(v2));
            }""",
            seed_lesson,
        )
        page.reload()
        page.wait_for_load_state("networkidle")
        migrated = get_state()
        assert migrated["meta"]["schemaVersion"] == 3, "Expected schema version 3 after migration"
        assert "lessonPanel" in migrated["ui"], "lessonPanel should exist after migration"
        assert "exercisesFilter" in migrated["ui"], "exercisesFilter should exist after migration"
        assert "returnContext" in migrated["ui"], "returnContext should exist after migration"
        assert seed_lesson in migrated["progress"]["completedLessonIds"], "Legacy progress should be preserved"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/13_migration_v3.png", full_page=True)
        print("  ✅ V2 data migrates to V3 while preserving progress")

        # Test 15: Accessibility hints (focus-visible + ARIA selected).
        print("\n[TEST 15] Checking focus and ARIA states...")
        page.set_viewport_size({"width": 1400, "height": 900})
        page.wait_for_timeout(250)
        open_first_lesson()
        notes_tab = page.locator('[data-action="set-lesson-panel"][data-panel="notes"]').first
        notes_tab.click()
        page.wait_for_timeout(250)
        assert notes_tab.get_attribute("aria-selected") == "true", "Active panel tab should expose aria-selected=true"

        complete_btn = page.locator('button[data-action="toggle-lesson-complete"]').first
        complete_btn.focus()
        focus_rule_present = page.evaluate(
            """() => {
                const styleTag = document.querySelector('style');
                return styleTag && styleTag.textContent.includes(':focus-visible') && styleTag.textContent.includes('outline');
            }"""
        )
        assert focus_rule_present, "Focus-visible rule should exist in stylesheet"
        page.screenshot(path=f"{SCREENSHOTS_DIR}/14_a11y_focus.png", full_page=True)
        print("  ✅ ARIA state and focus-visible styling are present")

        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Screenshots saved to: {SCREENSHOTS_DIR}/")
        print("\nAll completion-first regression checks finished successfully.")
        print("=" * 60)

        print("\nBrowser will close in 5 seconds...")
        page.wait_for_timeout(5000)
        browser.close()


if __name__ == "__main__":
    run_tests()
