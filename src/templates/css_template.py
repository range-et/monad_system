def create_css_template(
    background_color="#ffffff",
    primary_text_color="#000000",
    secondary_text_color="#212529",
    information_1_color="#80ffdb",
    information_2_color="#48bfe3",
    information_3_color="#5390d9",
    warning_color="#ffba08",
    alert_color="#d00000",
    highlight_color="#ffd60a",
    disabled_color="#6c757d",
    start_color="#00ff00",
    end_color="#ff0000",
    foot_color="#964B00",
    hand_color="#FFCBA4"
):
    return f"""
:root {{
    --background: {background_color};
    --primary-text: {primary_text_color};
    --secondary-text: {secondary_text_color};
    --information-1: {information_1_color}; 
    --information-2: {information_2_color};
    --information-3: {information_3_color};
    --warning: {warning_color};
    --alert: {alert_color};
    --highlight: {highlight_color};
    --disabled: {disabled_color};
    --start: {start_color};
    --finish: {end_color};
    --foot: {foot_color};
    --hand: {hand_color};
}}
"""


def create_monad_system(
    # --- Dark theme backgrounds/text ---
    bg_dark="#121212",
    layer01_dark="#1e1e1e",
    layer02_dark="#262626",
    layer03_dark="#333333",
    text_primary_dark="#E0E0E0",
    text_secondary_dark="#B0B0B0",
    text_disabled_dark="#757575",
    border_dark="#3d3d3d",
    border_subtle_dark="#2a2a2a",
    # --- Light theme backgrounds/text ---
    bg_light="#f4f4f4",
    layer01_light="#ffffff",
    layer02_light="#f4f4f4",
    layer03_light="#e8e8e8",
    text_primary_light="#161616",
    text_secondary_light="#525252",
    text_disabled_light="#8d8d8d",
    border_light="#c6c6c6",
    border_subtle_light="#e0e0e0",
    # --- Shared semantic colors ---
    interactive="#03A9F4",
    interactive_hover="#0288d1",
    interactive_active="#0277bd",
    support_info="#00BCD4",
    support_success="#8BC34A",
    support_warning="#FFC107",
    support_error="#F44336",
    highlight="#FFEB3B",
    disabled="#757575",
    # --- Movement / domain colors ---
    move_start="#4CAF50",
    move_hand="#03A9F4",
    move_foot="#FFEB3B",
    move_finish="#9C27B0",
):
    return f"""/*
 * Monad System
 * Generated from colors.json — do not edit directly.
 *
 * Tiers:
 *   Strata  — CSS custom properties (--strata-*)       connective state
 *   Monad   — Structural layout (.monad-*)              root containers
 *   Atomos  — Primitive components (.atomos-*)          indivisible units
 *   Threshold — Navigation & transitions (.threshold-*) state crossings
 *
 * Principle: Form follows Function. Every element earns its place.
 */

/* =========================================================================
   FONTS — Inter · JetBrains Mono · Lora  (Google Fonts)
   ========================================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono:wght@400;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

/* =========================================================================
   AKASHA — DARK (DEFAULT)
   The connective state layer. All components read from these.
   ========================================================================= */
:root {{
  /* Ground */
  --strata-bg:             {bg_dark};
  --strata-layer-01:       {layer01_dark};
  --strata-layer-02:       {layer02_dark};
  --strata-layer-03:       {layer03_dark};

  /* Type */
  --strata-text-primary:   {text_primary_dark};
  --strata-text-secondary: {text_secondary_dark};
  --strata-text-disabled:  {text_disabled_dark};

  /* Structure */
  --strata-border:         {border_dark};
  --strata-border-subtle:  {border_subtle_dark};
  --strata-overlay:        rgba(0,0,0,0.72);

  /* Signal */
  --strata-interactive:        {interactive};
  --strata-interactive-hover:  {interactive_hover};
  --strata-interactive-active: {interactive_active};

  /* Status */
  --strata-info:     {support_info};
  --strata-success:  {support_success};
  --strata-warning:  {support_warning};
  --strata-error:    {support_error};
  --strata-info-bg:    {support_info}1a;
  --strata-success-bg: {support_success}1a;
  --strata-warning-bg: {support_warning}1a;
  --strata-error-bg:   {support_error}1a;

  /* Domain */
  --strata-move-start:  {move_start};
  --strata-move-hand:   {move_hand};
  --strata-move-foot:   {move_foot};
  --strata-move-finish: {move_finish};

  /* Misc */
  --strata-highlight:  {highlight};
  --strata-disabled:   {disabled};
  --opacity-low:       0.2;
  --opacity-high:      0.8;

  /* Type system */
  --font-sans:   'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-mono:   'JetBrains Mono', 'Menlo', 'Courier New', monospace;
  --font-serif:  'Lora', 'Georgia', Times, serif;

  /* Scale */
  --type-xs:   0.75rem;
  --type-sm:   0.875rem;
  --type-base: 1rem;
  --type-md:   1.125rem;
  --type-lg:   1.25rem;
  --type-xl:   1.5rem;
  --type-2xl:  1.75rem;
  --type-3xl:  2rem;
  --type-4xl:  2.625rem;
  --type-5xl:  3.375rem;

  /* Grid (8px base unit) */
  --space-1:  8px;
  --space-2:  16px;
  --space-3:  24px;
  --space-4:  32px;
  --space-6:  48px;
  --space-8:  64px;
  --space-10: 80px;

  /* Threshold timing — linear, predictable */
  --threshold-fast:   80ms linear;
  --threshold-base:   160ms linear;
  --threshold-slow:   280ms linear;
}}

/* =========================================================================
   AKASHA — LIGHT
   ========================================================================= */
[data-strata="light"] {{
  --strata-bg:             {bg_light};
  --strata-layer-01:       {layer01_light};
  --strata-layer-02:       {layer02_light};
  --strata-layer-03:       {layer03_light};
  --strata-text-primary:   {text_primary_light};
  --strata-text-secondary: {text_secondary_light};
  --strata-text-disabled:  {text_disabled_light};
  --strata-border:         {border_light};
  --strata-border-subtle:  {border_subtle_light};
  --strata-overlay:        rgba(0,0,0,0.5);
}}

@media (prefers-color-scheme: light) {{
  :root:not([data-strata="dark"]) {{
    --strata-bg:             {bg_light};
    --strata-layer-01:       {layer01_light};
    --strata-layer-02:       {layer02_light};
    --strata-layer-03:       {layer03_light};
    --strata-text-primary:   {text_primary_light};
    --strata-text-secondary: {text_secondary_light};
    --strata-text-disabled:  {text_disabled_light};
    --strata-border:         {border_light};
    --strata-border-subtle:  {border_subtle_light};
    --strata-overlay:        rgba(0,0,0,0.5);
  }}
}}

/* =========================================================================
   BASE RESET
   ========================================================================= */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ font-size: 16px; scroll-behavior: smooth; }}

body {{
  font-family: var(--font-sans);
  font-size: var(--type-base);
  font-weight: 400;
  line-height: 1.5;
  color: var(--strata-text-primary);
  background-color: var(--strata-bg);
  -webkit-font-smoothing: antialiased;
  transition: background-color var(--threshold-base), color var(--threshold-base);
}}

h1, h2, h3, h4, h5, h6 {{
  font-family: var(--font-sans);
  font-weight: 600;
  line-height: 1.2;
  color: var(--strata-text-primary);
  letter-spacing: -0.01em;
}}
h1 {{ font-size: clamp(1.75rem,  4vw + 0.5rem,  var(--type-4xl)); }}
h2 {{ font-size: clamp(1.5rem,   3vw + 0.5rem,  var(--type-3xl)); }}
h3 {{ font-size: clamp(1.25rem,  2.5vw + 0.25rem, var(--type-2xl)); }}
h4 {{ font-size: clamp(1.125rem, 2vw + 0.125rem, var(--type-xl)); }}
h5 {{ font-size: clamp(1rem,     1.5vw,          var(--type-lg)); }}
h6 {{ font-size: var(--type-base); }}

p {{ color: var(--strata-text-secondary); line-height: 1.65; }}

a {{
  color: var(--strata-interactive);
  text-decoration: none;
  transition: color var(--threshold-fast);
}}
a:hover {{ color: var(--strata-interactive-hover); text-decoration: underline; }}

code, pre {{
  font-family: var(--font-mono);
  font-size: var(--type-sm);
  background: var(--strata-layer-02);
  border: 1px solid var(--strata-border-subtle);
}}
code {{ padding: 1px 5px; }}
pre  {{ padding: var(--space-2); overflow-x: auto; border-left: 2px solid var(--strata-interactive); }}

::selection {{
  background: {interactive};
  color: {bg_dark};
}}

:focus-visible {{
  outline: 2px solid var(--strata-interactive);
  outline-offset: 1px;
}}

/* Scrollbar — Webkit (Chrome, Safari, Edge) */
::-webkit-scrollbar {{ width: 8px; height: 8px; }}
::-webkit-scrollbar-track {{ background: var(--strata-bg); }}
::-webkit-scrollbar-thumb {{
  background: var(--strata-border);
  border: 2px solid var(--strata-bg);
}}
::-webkit-scrollbar-thumb:hover {{ background: var(--strata-interactive); }}

/* Scrollbar — Firefox */
* {{ scrollbar-width: thin; scrollbar-color: var(--strata-border) var(--strata-bg); }}

/* =========================================================================
   MONAD — GRID  (8px base unit, 16 columns)
   ========================================================================= */
.monad-grid {{
  display: grid;
  grid-template-columns: repeat(16, 1fr);
  gap: var(--space-2);
  width: 100%;
  max-width: 1584px;
  margin-inline: auto;
  padding-inline: var(--space-2);
}}
.monad-row {{
  display: grid;
  grid-template-columns: repeat(16, 1fr);
  gap: var(--space-2);
}}

@media (max-width: 1056px) {{
  .monad-grid {{ grid-template-columns: repeat(8, 1fr); }}
  .monad-row  {{ grid-template-columns: repeat(8, 1fr); }}
  .monad-col-md-full {{ grid-column: 1 / -1 !important; }}
  .monad-col-md-half {{ grid-column: span 4 !important; }}
}}
@media (max-width: 672px) {{
  .monad-grid {{ grid-template-columns: repeat(4, 1fr); padding-inline: 0; }}
  .monad-row  {{ grid-template-columns: repeat(4, 1fr); }}
  [class*="monad-col-"]:not([class*="monad-col-sm-"]) {{ grid-column: span 4; }}
  .monad-col-sm-full {{ grid-column: 1 / -1 !important; }}
  .monad-col-sm-half {{ grid-column: span 2 !important; }}
}}

.monad-col-1  {{ grid-column: span 1; }}
.monad-col-2  {{ grid-column: span 2; }}
.monad-col-3  {{ grid-column: span 3; }}
.monad-col-4  {{ grid-column: span 4; }}
.monad-col-5  {{ grid-column: span 5; }}
.monad-col-6  {{ grid-column: span 6; }}
.monad-col-7  {{ grid-column: span 7; }}
.monad-col-8  {{ grid-column: span 8; }}
.monad-col-9  {{ grid-column: span 9; }}
.monad-col-10 {{ grid-column: span 10; }}
.monad-col-11 {{ grid-column: span 11; }}
.monad-col-12 {{ grid-column: span 12; }}
.monad-col-13 {{ grid-column: span 13; }}
.monad-col-14 {{ grid-column: span 14; }}
.monad-col-15 {{ grid-column: span 15; }}
.monad-col-16 {{ grid-column: span 16; }}

/* =========================================================================
   MONAD — SHELL  (structural layout)
   ========================================================================= */
.monad-layout {{
  display: flex;
  min-height: calc(100vh - 48px);
}}

.monad-header {{
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  height: 48px;
  padding-inline: var(--space-2);
  background: var(--strata-layer-01);
  border-bottom: 1px solid var(--strata-border);
}}
.monad-header__name {{
  font-size: var(--type-base);
  font-weight: 600;
  color: var(--strata-text-primary);
  letter-spacing: 0.01em;
  white-space: nowrap;
}}
.monad-header__actions {{
  display: flex;
  align-items: center;
  gap: var(--space-1);
  margin-left: auto;
}}

.monad-rail {{
  width: 240px;
  min-height: 100vh;
  padding: var(--space-2) 0;
  background: var(--strata-layer-01);
  border-right: 1px solid var(--strata-border);
  flex-shrink: 0;
}}
.monad-rail__section {{
  padding: var(--space-2) var(--space-2) var(--space-1);
  font-size: var(--type-xs);
  font-weight: 600;
  color: var(--strata-text-disabled);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}}
.monad-rail__item {{
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: 9px var(--space-2);
  font-size: var(--type-sm);
  color: var(--strata-text-secondary);
  cursor: pointer;
  border: none;
  background: transparent;
  width: 100%;
  text-align: left;
  text-decoration: none;
  transition: background var(--threshold-fast), color var(--threshold-fast);
}}
.monad-rail__item:hover {{
  background: var(--strata-layer-02);
  color: var(--strata-text-primary);
}}
.monad-rail__item.active {{
  background: var(--strata-layer-02);
  color: var(--strata-interactive);
  border-left: 2px solid var(--strata-interactive);
  padding-left: calc(var(--space-2) - 2px);
}}

.monad-content {{
  flex: 1;
  padding: var(--space-4);
  min-width: 0;
}}

/* =========================================================================
   THRESHOLD — NAVIGATION  (traversal elements)
   ========================================================================= */
.threshold-nav {{
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}}
.threshold-nav a, .threshold-link {{
  display: inline-block;
  padding: 6px var(--space-2);
  font-size: var(--type-sm);
  font-weight: 400;
  color: var(--strata-text-secondary);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: color var(--threshold-fast), border-color var(--threshold-fast);
}}
.threshold-nav a:hover, .threshold-link:hover {{
  color: var(--strata-text-primary);
  text-decoration: none;
}}
.threshold-nav a.active, .threshold-link.active {{
  color: var(--strata-interactive);
  border-bottom-color: var(--strata-interactive);
}}

/* Hamburger toggle */
.threshold-toggle {{
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  padding: 0;
  background: transparent;
  border: 1px solid var(--strata-border);
  cursor: pointer;
  color: var(--strata-text-secondary);
  transition: background var(--threshold-fast), color var(--threshold-fast);
  flex-shrink: 0;
}}
.threshold-toggle:hover {{ background: var(--strata-layer-02); color: var(--strata-text-primary); }}
.threshold-toggle__bar {{
  display: block;
  width: 16px;
  height: 2px;
  background: currentColor;
  transition: transform var(--threshold-fast), opacity var(--threshold-fast);
}}
.threshold-toggle[aria-expanded="true"] .threshold-toggle__bar:nth-child(1) {{ transform: translateY(7px) rotate(45deg); }}
.threshold-toggle[aria-expanded="true"] .threshold-toggle__bar:nth-child(2) {{ opacity: 0; }}
.threshold-toggle[aria-expanded="true"] .threshold-toggle__bar:nth-child(3) {{ transform: translateY(-7px) rotate(-45deg); }}

/* Overlay backdrop */
.threshold-overlay {{
  display: none;
  position: fixed;
  inset: 0;
  background: var(--strata-overlay);
  z-index: 199;
}}
.threshold-overlay.is-visible {{ display: block; }}

@media (max-width: 1056px) {{
  .threshold-toggle {{ display: flex; }}
  .threshold-nav {{
    display: none;
    position: fixed;
    top: 48px;
    left: 0;
    right: 0;
    background: var(--strata-layer-01);
    border-bottom: 2px solid var(--strata-border);
    padding: var(--space-2);
    z-index: 98;
    flex-direction: column;
    gap: 2px;
  }}
  .threshold-nav.is-open {{ display: flex; }}
  .threshold-nav a {{
    padding: var(--space-1) var(--space-2);
    width: 100%;
    border-bottom: none;
  }}
  .monad-rail {{
    position: fixed;
    top: 48px;
    left: 0;
    bottom: 0;
    z-index: 200;
    transform: translateX(-100%);
    transition: transform var(--threshold-base);
    min-height: unset;
    overflow-y: auto;
  }}
  .monad-rail.is-open {{ transform: translateX(0); }}
  .monad-content {{ padding: var(--space-3); }}
}}
@media (max-width: 672px) {{
  .monad-content {{ padding: var(--space-2); }}
}}

/* =========================================================================
   AKASHA TOGGLE  (theme switcher)
   ========================================================================= */
.strata-toggle {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  background: transparent;
  border: 1px solid var(--strata-border);
  color: var(--strata-text-secondary);
  cursor: pointer;
  font-size: var(--type-sm);
  font-family: var(--font-mono);
  transition: background var(--threshold-fast), color var(--threshold-fast), border-color var(--threshold-fast);
}}
.strata-toggle:hover {{
  background: var(--strata-interactive);
  color: #fff;
  border-color: var(--strata-interactive);
}}

/* =========================================================================
   ATOMOS — BUTTONS  (indivisible action units)
   ========================================================================= */
.atomos-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-1);
  padding: 10px var(--space-2);
  font-family: var(--font-sans);
  font-size: var(--type-sm);
  font-weight: 400;
  line-height: 1;
  border: 1px solid transparent;
  cursor: pointer;
  white-space: nowrap;
  text-decoration: none;
  letter-spacing: 0.01em;
  transition:
    background var(--threshold-fast),
    border-color var(--threshold-fast),
    color var(--threshold-fast);
}}
.atomos-btn:disabled {{ opacity: 0.35; cursor: not-allowed; pointer-events: none; }}
.atomos-btn--sm {{ padding: 6px var(--space-2); font-size: var(--type-xs); }}
.atomos-btn--lg {{ padding: 14px var(--space-3); font-size: var(--type-base); }}

.atomos-btn--primary {{
  background: var(--strata-interactive);
  color: #fff;
  border-color: var(--strata-interactive);
}}
.atomos-btn--primary:hover  {{ background: var(--strata-interactive-hover);  border-color: var(--strata-interactive-hover); }}
.atomos-btn--primary:active {{ background: var(--strata-interactive-active); border-color: var(--strata-interactive-active); }}

.atomos-btn--secondary {{
  background: transparent;
  color: var(--strata-interactive);
  border-color: var(--strata-interactive);
}}
.atomos-btn--secondary:hover  {{ background: var(--strata-interactive); color: #fff; }}
.atomos-btn--secondary:active {{ background: var(--strata-interactive-active); color: #fff; border-color: var(--strata-interactive-active); }}

.atomos-btn--danger {{
  background: var(--strata-error);
  color: #fff;
  border-color: var(--strata-error);
}}
.atomos-btn--danger:hover  {{ background: #d32f2f; border-color: #d32f2f; }}
.atomos-btn--danger:active {{ background: #b71c1c; border-color: #b71c1c; }}

.atomos-btn--ghost {{
  background: transparent;
  color: var(--strata-text-secondary);
  border-color: transparent;
}}
.atomos-btn--ghost:hover {{
  background: var(--strata-layer-02);
  color: var(--strata-text-primary);
  border-color: var(--strata-border);
}}

/* =========================================================================
   ATOMOS — CARDS  (contained surface units)
   ========================================================================= */
.atomos-card {{
  background: var(--strata-layer-01);
  border: 1px solid var(--strata-border);
  padding: var(--space-3);
}}
.atomos-card--interactive {{ cursor: pointer; }}
.atomos-card--interactive:hover {{ border-color: var(--strata-interactive); }}
.atomos-card--flat {{ border-color: var(--strata-border-subtle); }}

.atomos-card__header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
  padding-bottom: var(--space-2);
  border-bottom: 1px solid var(--strata-border-subtle);
}}
.atomos-card__title {{ font-size: var(--type-base); font-weight: 600; color: var(--strata-text-primary); }}
.atomos-card__body  {{ color: var(--strata-text-secondary); font-size: var(--type-sm); }}

.atomos-tile {{
  background: var(--strata-layer-01);
  border: 1px solid var(--strata-border);
  padding: var(--space-3);
  cursor: pointer;
  transition: background var(--threshold-fast), border-color var(--threshold-fast);
}}
.atomos-tile:hover  {{ background: var(--strata-layer-02); border-color: var(--strata-interactive); }}
.atomos-tile.active {{
  background: var(--strata-layer-02);
  border-left: 2px solid var(--strata-interactive);
  padding-left: calc(var(--space-3) - 2px);
}}

/* Stat variant */
.atomos-stat {{
  background: var(--strata-layer-01);
  border: 1px solid var(--strata-border);
  border-top: 2px solid var(--strata-border);
  padding: var(--space-3);
}}
.atomos-stat--signal   {{ border-top-color: var(--strata-interactive); }}
.atomos-stat--success  {{ border-top-color: var(--strata-success); }}
.atomos-stat--warning  {{ border-top-color: var(--strata-warning); }}
.atomos-stat--error    {{ border-top-color: var(--strata-error); }}

.atomos-stat__eyebrow {{
  font-size: var(--type-xs);
  font-weight: 600;
  color: var(--strata-text-disabled);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: var(--space-1);
}}
.atomos-stat__value {{
  font-size: var(--type-3xl);
  font-weight: 300;
  color: var(--strata-text-primary);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}}
.atomos-stat__label {{ font-size: var(--type-sm); color: var(--strata-text-secondary); margin-top: 4px; }}
.atomos-stat__delta {{ font-size: var(--type-xs); margin-top: 6px; font-family: var(--font-mono); }}
.atomos-stat__delta--up   {{ color: var(--strata-success); }}
.atomos-stat__delta--down {{ color: var(--strata-error); }}

@media (max-width: 672px) {{
  .atomos-card, .atomos-tile, .atomos-stat {{ padding: var(--space-2); }}
}}

/* =========================================================================
   ATOMOS — TAGS & BADGES
   ========================================================================= */
.atomos-tag {{
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 7px;
  font-size: var(--type-xs);
  font-weight: 600;
  font-family: var(--font-mono);
  border: 1px solid transparent;
  letter-spacing: 0.04em;
  white-space: nowrap;
}}
.atomos-tag--info    {{ background: var(--strata-info-bg);    color: var(--strata-info);    border-color: var(--strata-info); }}
.atomos-tag--success {{ background: var(--strata-success-bg); color: var(--strata-success); border-color: var(--strata-success); }}
.atomos-tag--warning {{ background: var(--strata-warning-bg); color: var(--strata-warning); border-color: var(--strata-warning); }}
.atomos-tag--error   {{ background: var(--strata-error-bg);   color: var(--strata-error);   border-color: var(--strata-error); }}
.atomos-tag--neutral {{ background: var(--strata-layer-02); color: var(--strata-text-secondary); border-color: var(--strata-border); }}

.atomos-badge {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  font-size: 10px;
  font-weight: 700;
  font-family: var(--font-mono);
  background: var(--strata-interactive);
  color: #fff;
}}
.atomos-badge--error {{ background: var(--strata-error); }}

/* =========================================================================
   ATOMOS — NOTICES  (status communication)
   ========================================================================= */
.atomos-notice {{
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-left: 3px solid transparent;
  font-size: var(--type-sm);
}}
.atomos-notice__icon  {{ flex-shrink: 0; margin-top: 1px; font-family: var(--font-mono); }}
.atomos-notice__body  {{ flex: 1; }}
.atomos-notice__title {{ font-weight: 600; color: var(--strata-text-primary); margin-bottom: 2px; letter-spacing: 0.01em; }}
.atomos-notice__msg   {{ color: var(--strata-text-secondary); }}
.atomos-notice__close {{
  background: transparent; border: none; cursor: pointer; padding: 0;
  color: var(--strata-text-disabled); font-size: var(--type-base); flex-shrink: 0;
  transition: color var(--threshold-fast);
}}
.atomos-notice__close:hover {{ color: var(--strata-text-primary); }}

.atomos-notice--info    {{ background: var(--strata-info-bg);    border-color: var(--strata-info); }}
.atomos-notice--success {{ background: var(--strata-success-bg); border-color: var(--strata-success); }}
.atomos-notice--warning {{ background: var(--strata-warning-bg); border-color: var(--strata-warning); }}
.atomos-notice--error   {{ background: var(--strata-error-bg);   border-color: var(--strata-error); }}

/* =========================================================================
   ATOMOS — FORMS
   ========================================================================= */
.atomos-field {{
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: var(--space-3);
}}
.atomos-label {{
  font-size: var(--type-xs);
  font-weight: 600;
  color: var(--strata-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}

.atomos-input, .atomos-select, .atomos-textarea {{
  width: 100%;
  font-family: var(--font-sans);
  font-size: var(--type-sm);
  color: var(--strata-text-primary);
  background: var(--strata-layer-01);
  border: 1px solid var(--strata-border);
  outline: none;
  -webkit-appearance: none;
  transition: border-color var(--threshold-fast);
}}
.atomos-input    {{ padding: 10px var(--space-2); }}
.atomos-select   {{ padding: 10px var(--space-2); cursor: pointer; }}
.atomos-textarea {{ padding: var(--space-2); resize: vertical; min-height: 96px; }}

.atomos-input::placeholder {{ color: var(--strata-text-disabled); }}
.atomos-input:focus, .atomos-select:focus, .atomos-textarea:focus {{
  border-color: var(--strata-interactive);
  box-shadow: inset 2px 0 0 var(--strata-interactive);
}}
.atomos-input:disabled {{
  opacity: 0.45;
  cursor: not-allowed;
  background: var(--strata-layer-02);
}}
.atomos-input--error {{ border-color: var(--strata-error); }}
.atomos-input--error:focus {{ box-shadow: inset 2px 0 0 var(--strata-error); }}

.atomos-helper {{ font-size: var(--type-xs); color: var(--strata-text-disabled); font-family: var(--font-mono); }}
.atomos-helper--error {{ color: var(--strata-error); }}

/* Toggle switch */
.atomos-switch {{
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
}}
.atomos-switch__track {{
  position: relative;
  width: 36px;
  height: 20px;
  background: var(--strata-layer-03);
  border: 1px solid var(--strata-border);
  transition: background var(--threshold-fast), border-color var(--threshold-fast);
  flex-shrink: 0;
}}
.atomos-switch__track::after {{
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  background: var(--strata-text-disabled);
  transition: transform var(--threshold-fast), background var(--threshold-fast);
}}
.atomos-switch input:checked + .atomos-switch__track {{ background: var(--strata-interactive); border-color: var(--strata-interactive); }}
.atomos-switch input:checked + .atomos-switch__track::after {{ transform: translateX(16px); background: #fff; }}
.atomos-switch input {{ position: absolute; opacity: 0; width: 0; height: 0; }}
.atomos-switch__label {{ font-size: var(--type-sm); color: var(--strata-text-secondary); }}

/* =========================================================================
   ATOMOS — TABLE
   ========================================================================= */
.atomos-table-wrap {{
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--strata-border);
}}
.atomos-table-wrap > .atomos-table {{ border: none; min-width: 480px; }}

.atomos-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: var(--type-sm);
}}
.atomos-table th {{
  padding: var(--space-1) var(--space-2);
  text-align: left;
  font-size: var(--type-xs);
  font-weight: 700;
  font-family: var(--font-mono);
  color: var(--strata-text-disabled);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 2px solid var(--strata-border);
  background: var(--strata-layer-01);
}}
.atomos-table td {{
  padding: var(--space-1) var(--space-2);
  color: var(--strata-text-primary);
  border-bottom: 1px solid var(--strata-border-subtle);
  vertical-align: middle;
}}
.atomos-table tbody tr {{ transition: background var(--threshold-fast); }}
.atomos-table tbody tr:hover {{ background: var(--strata-layer-02); }}
.atomos-table--zebra tbody tr:nth-child(even) {{ background: var(--strata-layer-01); }}
.atomos-table--zebra tbody tr:nth-child(odd)  {{ background: var(--strata-bg); }}
.atomos-table--zebra tbody tr:hover {{ background: var(--strata-layer-02); }}

@media (max-width: 672px) {{
  .atomos-table {{ display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }}
}}

/* =========================================================================
   ATOMOS — PROGRESS
   ========================================================================= */
.atomos-progress {{
  height: 4px;
  background: var(--strata-layer-03);
  overflow: hidden;
}}
.atomos-progress__fill {{
  height: 100%;
  width: var(--progress, 0%);
  background: var(--strata-interactive);
  transition: width var(--threshold-slow);
}}
.atomos-progress__fill--success {{ background: var(--strata-success); }}
.atomos-progress__fill--warning {{ background: var(--strata-warning); }}
.atomos-progress__fill--error   {{ background: var(--strata-error); }}

/* =========================================================================
   ATOMOS — DOMAIN HOLDS  (movement-specific, never reuse for status)
   ========================================================================= */
.atomos-hold {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px;
  font-size: var(--type-xs);
  font-weight: 700;
  font-family: var(--font-mono);
  border: 1px solid transparent;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}}
.atomos-hold::before {{
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  background: currentColor;
}}

.atomos-hold--start  {{ color: var(--strata-move-start);  background: {move_start}18;  border-color: var(--strata-move-start); }}
.atomos-hold--hand   {{ color: var(--strata-move-hand);   background: {move_hand}18;   border-color: var(--strata-move-hand); }}
.atomos-hold--foot   {{ color: var(--strata-move-foot);   background: {move_foot}18;   border-color: var(--strata-move-foot); }}
.atomos-hold--finish {{ color: var(--strata-move-finish); background: {move_finish}18; border-color: var(--strata-move-finish); }}

/* =========================================================================
   UTILITIES
   ========================================================================= */
.mn-divider {{
  border: none;
  border-top: 1px solid var(--strata-border-subtle);
  margin: var(--space-3) 0;
}}
.mn-spacer {{ flex: 1; }}

.mn-text-primary   {{ color: var(--strata-text-primary); }}
.mn-text-secondary {{ color: var(--strata-text-secondary); }}
.mn-text-disabled  {{ color: var(--strata-text-disabled); }}
.mn-text-info      {{ color: var(--strata-info); }}
.mn-text-success   {{ color: var(--strata-success); }}
.mn-text-warning   {{ color: var(--strata-warning); }}
.mn-text-error     {{ color: var(--strata-error); }}
.mn-text-mono      {{ font-family: var(--font-mono); }}
.mn-truncate       {{ overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.mn-sr-only        {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border-width: 0; }}

/* Responsive show/hide */
.mn-hide-sm {{ }}
.mn-hide-md {{ }}
.mn-show-sm {{ display: none; }}
.mn-show-md {{ display: none; }}
@media (max-width: 672px) {{
  .mn-hide-sm {{ display: none !important; }}
  .mn-show-sm {{ display: revert !important; }}
}}
@media (max-width: 1056px) {{
  .mn-hide-md {{ display: none !important; }}
  .mn-show-md {{ display: revert !important; }}
}}
"""
