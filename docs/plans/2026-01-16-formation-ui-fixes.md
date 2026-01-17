# Formation Interactive UI Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix French accents throughout the interface, verify exercises data, and implement key UI improvements.

**Architecture:** Single-file HTML with embedded CSS/JS. All changes are in `formation-interactive.html`. The file uses JavaScript template literals for dynamic content, so we need to fix both static HTML and JS string literals.

**Tech Stack:** Vanilla HTML/CSS/JavaScript, localStorage for persistence

---

## Task 1: Fix French Accents in Static UI Elements

**Files:**
- Modify: `formation-interactive.html:1071` (search placeholder)
- Modify: `formation-interactive.html:1081` (timer button)

**Step 1: Fix search placeholder accent**

Change line 1071 from:
```html
<input type="text" class="search-input" placeholder="Rechercher une lecon..." id="search-input" oninput="handleSearch(this.value)">
```
to:
```html
<input type="text" class="search-input" placeholder="Rechercher une leçon..." id="search-input" oninput="handleSearch(this.value)">
```

**Step 2: Fix timer button accent**

Change line 1081 from:
```html
▶️ Demarrer
```
to:
```html
▶️ Démarrer
```

**Step 3: Verify changes**

Open file in browser and confirm:
- Search placeholder shows "Rechercher une leçon..."
- Timer button shows "▶️ Démarrer"

**Step 4: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to static UI elements (search, timer)"
```

---

## Task 2: Fix French Accents in Dashboard Stats

**Files:**
- Modify: `formation-interactive.html:1761` (Lecons completees)
- Modify: `formation-interactive.html:1766` (Exercices realises)
- Modify: `formation-interactive.html:1771` (Temps d'etude)

**Step 1: Fix "Lecons completees" label**

Change line 1761 from:
```javascript
<div class="stat-label">Lecons completees</div>
```
to:
```javascript
<div class="stat-label">Leçons complétées</div>
```

**Step 2: Fix "Exercices realises" label**

Change line 1766 from:
```javascript
<div class="stat-label">Exercices realises</div>
```
to:
```javascript
<div class="stat-label">Exercices réalisés</div>
```

**Step 3: Fix "Temps d'etude" label**

Change line 1771 from:
```javascript
<div class="stat-label">Temps d'etude total</div>
```
to:
```javascript
<div class="stat-label">Temps d'étude total</div>
```

**Step 4: Verify changes**

Refresh browser, go to Dashboard and confirm stats show:
- "Leçons complétées"
- "Exercices réalisés"
- "Temps d'étude total"

**Step 5: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to dashboard stat labels"
```

---

## Task 3: Fix French Accents in Sidebar

**Files:**
- Modify: `formation-interactive.html:1681` (lecons count)

**Step 1: Fix sidebar lesson count**

Change line 1681 from:
```javascript
<div class="phase-progress">${completedCount}/${totalCount} lecons</div>
```
to:
```javascript
<div class="phase-progress">${completedCount}/${totalCount} leçons</div>
```

**Step 2: Verify changes**

Refresh browser and confirm sidebar shows "0/3 leçons" (with cedilla)

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accent to sidebar lesson count"
```

---

## Task 4: Fix French Accents in Lesson Navigation

**Files:**
- Modify: `formation-interactive.html:1921` (Lecon precedente)
- Modify: `formation-interactive.html:1926` (Marquer comme termine)
- Modify: `formation-interactive.html:1931` (Lecon suivante)

**Step 1: Fix "Lecon precedente" button**

Change line 1921 from:
```javascript
← Lecon precedente
```
to:
```javascript
← Leçon précédente
```

**Step 2: Fix "Marquer comme termine" button**

Change line 1926 from:
```javascript
${isCompleted ? '↩️ Marquer comme non termine' : '✅ Marquer comme termine'}
```
to:
```javascript
${isCompleted ? '↩️ Marquer comme non terminé' : '✅ Marquer comme terminé'}
```

**Step 3: Fix "Lecon suivante" button**

Change line 1931 from:
```javascript
Lecon suivante →
```
to:
```javascript
Leçon suivante →
```

**Step 4: Verify changes**

Click on a lesson and confirm buttons show:
- "← Leçon précédente"
- "✅ Marquer comme terminé"
- "Leçon suivante →"

**Step 5: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to lesson navigation buttons"
```

---

## Task 5: Fix French Accents in Exercises Section

**Files:**
- Modify: `formation-interactive.html:1993` (Duree estimee)

**Step 1: Fix "Duree estimee" label**

Change line 1993 from:
```javascript
<p style="margin-top: 8px; color: var(--accent-blue);">⏱️ Duree estimee: ${ex.duration}</p>
```
to:
```javascript
<p style="margin-top: 8px; color: var(--accent-blue);">⏱️ Durée estimée: ${ex.duration}</p>
```

**Step 2: Verify changes**

Go to Exercises section and confirm each exercise shows "Durée estimée:"

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to exercise duration label"
```

---

## Task 6: Fix French Accents in Timeline Section

**Files:**
- Modify: `formation-interactive.html:2025` (Roadmap complete)

**Step 1: Fix timeline description**

Change line 2025 from:
```javascript
<p style="color: var(--text-secondary); margin-bottom: 30px;">Roadmap complete pour lancer ta premiere marque</p>
```
to:
```javascript
<p style="color: var(--text-secondary); margin-bottom: 30px;">Roadmap complète pour lancer ta première marque</p>
```

**Step 2: Verify changes**

Go to Planning section and confirm subtitle shows "Roadmap complète pour lancer ta première marque"

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to timeline description"
```

---

## Task 7: Fix French Accents in Timer Toggle

**Files:**
- Modify: `formation-interactive.html:2143` (Demarrer button reset)

**Step 1: Fix timer button reset text**

Change line 2143 from:
```javascript
btn.innerHTML = '▶️ Demarrer';
```
to:
```javascript
btn.innerHTML = '▶️ Démarrer';
```

**Step 2: Verify changes**

Start timer, then stop it - confirm button shows "▶️ Démarrer"

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accent to timer button reset"
```

---

## Task 8: Fix French Accents in Exercise Data

**Files:**
- Modify: `formation-interactive.html:1582` (evaluer)
- Modify: `formation-interactive.html:1594` (reponses)
- Modify: `formation-interactive.html:1600` (detail)
- Modify: `formation-interactive.html:1612` (premiere)

**Step 1: Fix exercise descriptions with accents**

Change line 1582 from:
```javascript
description: 'Lister 10 problemes et les evaluer selon les 5 criteres.',
```
to:
```javascript
description: 'Lister 10 problèmes et les évaluer selon les 5 critères.',
```

Change line 1594 from:
```javascript
description: 'Creer un questionnaire et obtenir 20-30 reponses.',
```
to:
```javascript
description: 'Créer un questionnaire et obtenir 20-30 réponses.',
```

Change line 1600 from:
```javascript
description: 'Analyser 5 concurrents en detail.',
```
to:
```javascript
description: 'Analyser 5 concurrents en détail.',
```

Change line 1612 from:
```javascript
description: 'Ecrire et produire ta premiere video.',
```
to:
```javascript
description: 'Écrire et produire ta première vidéo.',
```

Change line 1618 from:
```javascript
description: 'Evaluer ton site selon les 13 criteres.',
```
to:
```javascript
description: 'Évaluer ton site selon les 13 critères.',
```

**Step 2: Verify changes**

Go to Exercises section and confirm descriptions have proper accents

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to exercise descriptions"
```

---

## Task 9: Fix French Accents in Timeline Data

**Files:**
- Modify: `formation-interactive.html:1624` (selectionne)
- Modify: `formation-interactive.html:1628` (analyses)
- Modify: `formation-interactive.html:1629` (videos, prets)
- Modify: `formation-interactive.html:1630` (Premieres)

**Step 1: Fix timeline deliverables with accents**

Change line 1624 from:
```javascript
{ week: 2, title: 'Sourcing', tasks: 'Exercice 2: Contact fournisseurs 1688/Alibaba', deliverable: 'Fournisseur selectionne' },
```
to:
```javascript
{ week: 2, title: 'Sourcing', tasks: 'Exercice 2: Contact fournisseurs 1688/Alibaba', deliverable: 'Fournisseur sélectionné' },
```

Change line 1628 from:
```javascript
{ week: 6, title: 'Veille contenu', tasks: 'Exercice 5: 50 contenus analyses', deliverable: 'Tableau veille rempli' },
```
to:
```javascript
{ week: 6, title: 'Veille contenu', tasks: 'Exercice 5: 50 contenus analysés', deliverable: 'Tableau veille rempli' },
```

Change line 1629 from:
```javascript
{ week: 7, title: 'Production contenu', tasks: 'Exercice 6: 10-15 videos', deliverable: 'Stock de contenus prets' },
```
to:
```javascript
{ week: 7, title: 'Production contenu', tasks: 'Exercice 6: 10-15 vidéos', deliverable: 'Stock de contenus prêts' },
```

Change line 1630 from:
```javascript
{ week: 8, title: 'Lancement testing', tasks: 'Publication quotidienne', deliverable: 'Premieres ventes!' }
```
to:
```javascript
{ week: 8, title: 'Lancement testing', tasks: 'Publication quotidienne', deliverable: 'Premières ventes!' }
```

**Step 2: Verify changes**

Go to Planning section and confirm deliverables have proper accents

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to timeline deliverables"
```

---

## Task 10: Fix French Accents in Quote and Completion Message

**Files:**
- Modify: `formation-interactive.html:1799` (complete, lecons)
- Modify: `formation-interactive.html:1808` (debutant, competences, decisions, consequence)

**Step 1: Fix completion message**

Change line 1799 from:
```javascript
<p>Tu as complete toutes les lecons! Continue avec les exercices pratiques.</p>
```
to:
```javascript
<p>Tu as complété toutes les leçons! Continue avec les exercices pratiques.</p>
```

**Step 2: Fix quote text**

Change line 1808 from:
```javascript
<div class="quote-text">"Ton objectif en tant que debutant, c'est de devenir un bon fondateur. Quand tu auras des competences, tu vas prendre de bonnes decisions, mettre en place de bonnes actions, et par consequence, tu vas faire beaucoup d'argent."</div>
```
to:
```javascript
<div class="quote-text">"Ton objectif en tant que débutant, c'est de devenir un bon fondateur. Quand tu auras des compétences, tu vas prendre de bonnes décisions, mettre en place de bonnes actions, et par conséquence, tu vas faire beaucoup d'argent."</div>
```

**Step 3: Verify changes**

Go to Dashboard and confirm quote has proper accents

**Step 4: Commit**

```bash
git add formation-interactive.html
git commit -m "fix: add accents to quote and completion message"
```

---

## Task 11: Verify All 7 Exercises Render Correctly

**Files:**
- Review: `formation-interactive.html:1578-1621` (exercises array)
- Review: `formation-interactive.html:1972-2004` (showExercises function)

**Step 1: Verify exercise data count**

The exercises array at lines 1578-1621 contains exactly 7 exercises:
- ex-1: Brainstorming Produit
- ex-2: Simulation de Sourcing
- ex-3: Avatar Client
- ex-4: Veille Concurrentielle
- ex-5: Veille de Contenu
- ex-6: Premier Script Video
- ex-7: Audit de Site

**Step 2: Test rendering in browser**

1. Open the formation in browser
2. Click "Exercices" in sidebar
3. Scroll through the page
4. Count all visible exercises - should be 7

**Step 3: Document findings**

The exercises array has all 7 items. If only 3 show in browser, it may be a CSS overflow issue. Check by scrolling the exercises view.

**Step 4: Commit (if no code changes needed)**

```bash
git commit --allow-empty -m "verify: confirmed all 7 exercises render correctly"
```

---

## Task 12: Add Keyboard Navigation for Lessons

**Files:**
- Modify: `formation-interactive.html` (add after line ~2160, after init())

**Step 1: Add keyboard event listener**

Add this code block after the `init()` call (around line 2162):

```javascript
// Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (state.currentView === 'lesson' && state.currentLesson) {
        const allLessons = coursData.phases.flatMap(p => p.lessons);
        const currentIndex = allLessons.findIndex(l => l.id === state.currentLesson);

        if (e.key === 'ArrowLeft' && currentIndex > 0) {
            showLesson(allLessons[currentIndex - 1].id);
        } else if (e.key === 'ArrowRight' && currentIndex < allLessons.length - 1) {
            showLesson(allLessons[currentIndex + 1].id);
        }
    }
});
```

**Step 2: Test keyboard navigation**

1. Open a lesson
2. Press Left Arrow - should go to previous lesson
3. Press Right Arrow - should go to next lesson
4. On first lesson, Left Arrow should do nothing
5. On last lesson, Right Arrow should do nothing

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "feat: add keyboard navigation for lessons (arrow keys)"
```

---

## Task 13: Add Tooltips for Truncated Lesson Titles

**Files:**
- Modify: `formation-interactive.html:1687-1690` (lesson item rendering)

**Step 1: Add title attribute for tooltip**

Change line 1687-1690 from:
```javascript
<div class="lesson-item ${state.completedLessons.includes(lesson.id) ? 'completed' : ''} ${state.currentLesson === lesson.id ? 'active' : ''}"
    onclick="showLesson('${lesson.id}')">
    <div class="lesson-checkbox">${state.completedLessons.includes(lesson.id) ? '✓' : ''}</div>
    <span>${lesson.title}</span>
</div>
```
to:
```javascript
<div class="lesson-item ${state.completedLessons.includes(lesson.id) ? 'completed' : ''} ${state.currentLesson === lesson.id ? 'active' : ''}"
    onclick="showLesson('${lesson.id}')"
    title="${lesson.title}">
    <div class="lesson-checkbox">${state.completedLessons.includes(lesson.id) ? '✓' : ''}</div>
    <span>${lesson.title}</span>
</div>
```

**Step 2: Test tooltips**

1. Hover over a truncated lesson title in sidebar
2. Tooltip should show full title after brief delay

**Step 3: Commit**

```bash
git add formation-interactive.html
git commit -m "feat: add tooltips to show full lesson titles on hover"
```

---

## Task 14: Add Reset Progress Confirmation

**Files:**
- Modify: `formation-interactive.html` (add to Resources section, around line 2090)

**Step 1: Add reset function**

Add this function after the `showResources()` function (around line 2090):

```javascript
function resetProgress() {
    if (confirm('Êtes-vous sûr de vouloir réinitialiser toute votre progression? Cette action est irréversible.')) {
        localStorage.removeItem('formation-ecom-state');
        state = {
            completedLessons: [],
            completedExercises: [],
            completedWeeks: [],
            notes: {},
            currentView: 'dashboard',
            currentLesson: null,
            timerRunning: false,
            timerSeconds: 0,
        };
        showDashboard();
    }
}
```

**Step 2: Add reset button to Resources section**

In the `showResources()` function, add before the closing `</div>` of fade-in (around line 2089):

```javascript
<div class="section-card" style="margin-top: 30px; border-color: var(--accent-red);">
    <div class="section-header">
        <div class="section-title">⚠️ Zone Dangereuse</div>
    </div>
    <div class="section-content">
        <p style="margin-bottom: 15px; color: var(--text-secondary);">Réinitialiser ta progression supprimera toutes tes leçons complétées, exercices, notes et temps d'étude.</p>
        <button class="btn" style="background: var(--accent-red); color: white;" onclick="resetProgress()">
            🗑️ Réinitialiser ma progression
        </button>
    </div>
</div>
```

**Step 3: Test reset functionality**

1. Complete some lessons and exercises
2. Go to Resources section
3. Click "Réinitialiser ma progression"
4. Confirm dialog should appear
5. On confirm, all progress should reset to 0

**Step 4: Commit**

```bash
git add formation-interactive.html
git commit -m "feat: add reset progress button with confirmation dialog"
```

---

## Final Verification

**Step 1: Full smoke test**

1. Open formation-interactive.html in browser
2. Check Dashboard - all labels have accents
3. Check sidebar - "leçons" has cedilla
4. Click on a lesson - navigation buttons have accents
5. Check Exercises - all 7 visible, "Durée estimée" has accents
6. Check Planning - deliverables have accents
7. Check Resources - Reset button is present
8. Test keyboard navigation (arrow keys in lesson view)
9. Test tooltip on truncated lesson titles
10. Test reset progress button

**Step 2: Final commit**

```bash
git add -A
git commit -m "chore: complete UI fixes and improvements"
```
