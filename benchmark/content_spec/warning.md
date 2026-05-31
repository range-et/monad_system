# Scenario: Warning

**One-line intent:** "Critical condition right now. Look here, act here, ignore everything else."

## Activity context
- Climbing (climb-AR primary) / device-only emergency state
- Master-alarm equivalent: something requires *immediate* user action
- Other data is no longer relevant; the warning *is* the screen

## State variables (most suppressed)
- **WARNING: FALL RISK DETECTED** — anchor load spike + accelerometer event ← **the entire screen's purpose**
- Suggested action: "STABILIZE — confirm anchor"
- Heart rate: 192 bpm (redline)
- Time-since-trigger: 00:03
- Last secure hold: move 14 (3 moves back)
- Partner notified: YES

## Focal target
**The warning callout** (`#focal-target` element) — the headline phrase ("FALL RISK DETECTED" or equivalent). This is the *only* thing that matters in the first second.

## Visual treatment guidance
- Minimum information density — only what's needed to act
- Warning chrome dominates the canvas (color: NASA-derived red `#E4002B` is the reference; Monad maps to its highest-priority alert token)
- Other data is present but visually suppressed (small, low-contrast, peripheral)
- Underlay: UI may occupy a large center portion to ensure the warning is unmissable; the scene is contextually irrelevant in this state
- One-action affordance preferred (no menu, no choice paralysis)

## What "good" looks like for this scenario
First-second eye fixation lands on the warning callout with near-100% reliability. Mass-on-target should be very high — the rest of the canvas should be visually quiet enough that the warning *owns* the saliency.
