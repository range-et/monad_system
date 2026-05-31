# Scenario: Calm

**One-line intent:** "Everything is nominal. Give me an at-a-glance status check; don't shout."

## Activity context
- Skiing (ski-AR) / casual cruise / phone idle view (device-only)
- All physical systems within nominal range
- No environmental threats
- User wants passive monitoring without being distracted from the activity

## State variables (within nominal)
- Heart rate: 132 bpm (Zone 2)
- Speed: 38 km/h (or 0 for device-only idle)
- Elevation: 2,140 m
- Time elapsed: 01:23:45
- Distance: 14.2 km
- Battery: 78%
- GPS: locked
- Weather: stable, clear

## Focal target
**The primary metric tile** — the current speed (`#focal-target` element). In calm mode the user glances to confirm their cruise pace; this is the "at-a-glance" datum.

## Visual treatment guidance
- Low information density (≤6 data points visible)
- Monochrome / muted accent tones only — no warning colors
- Generous spacing
- The focal-target tile is *first among equals* (larger numeric, but not screaming)
- Underlay (AR variants): UI should occupy minimum real estate, leave most of the scene visible

## What "good" looks like for this scenario
A first-second eye fixation lands on the focal target. The rest is peripheral, secondary, scanable but not demanding. The user trusts the system silence.
