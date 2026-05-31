# Scenario: Alert

**One-line intent:** "Something is approaching out-of-bounds. Look at the flagged item; route around it."

## Activity context
- Climbing (climb-AR primary) / device-only mid-route check
- One subsystem flagged amber: not critical, but the user should look at it now
- No immediate physical risk yet
- Decision-support state: do I push through, change pace, or back off?

## State variables
- Heart rate: 168 bpm (Zone 4 — climbing toward redline) ← **flagged amber**
- Route progress: 14 / 22 moves complete
- Grip time on current hold: 00:34
- Total time on wall: 12:47
- Pump indicator: 78% (climbing)
- Partner status: ON BELAY (nominal)
- Weather: cloud build-up detected on horizon
- Battery: 64%

## Focal target
**The HR-zone flag callout** (`#focal-target` element). The user needs to see this first to make a pacing decision before the next move.

## Visual treatment guidance
- Moderate information density (8–12 data points)
- One element clearly amber/caution-coded — used sparingly to preserve signal
- Other elements neutral
- The flagged item visually pops *relative to its neighbors* without dominating the entire field
- Underlay: UI can grow slightly to accommodate the flag but should not fully occlude the climbing scene

## What "good" looks like for this scenario
First-second eye fixation lands on the flagged HR-zone callout, not on any other (nominal) tile. The rest of the UI is present but recedes.
