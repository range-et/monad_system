"""Extract the NASA 1976 Graphics Standards Manual into Markdown + JSON via Gemini.

Reads `GEMENI_KEY` from `.env`, uploads the PDF to the Gemini Files API,
and runs two extraction prompts: one for a reference Markdown document, one
for a structured design-token JSON.

Outputs:
  docs/nasa_design_manual.md
  benchmark/nasa_system.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "docs" / "nasa_graphics_manual_nhb_1430-2_jan_1976.pdf"
MD_OUT = ROOT / "docs" / "nasa_design_manual.md"
JSON_OUT = ROOT / "benchmark" / "nasa_system.json"
ENV_PATH = ROOT / ".env"

MODEL = "gemini-2.5-pro"

MD_PROMPT = (
    "Convert this NASA Graphics Standards Manual into clean Markdown. "
    "Preserve the section hierarchy (use #, ##, ### headings that mirror the "
    "manual's numbering, e.g. '## 1.0 Introduction', '### 1.1 Purpose'). "
    "Transcribe specifications, rules, dimensions, and color/typography "
    "definitions verbatim where possible. For every figure or illustration, "
    "insert a line of the form `[Figure N: <short caption describing what is "
    "depicted>]`. Summarize tables faithfully as Markdown tables when "
    "feasible; otherwise as bullet lists. Fix obvious OCR artifacts (broken "
    "ligatures, stray characters) but never invent content. Do not wrap the "
    "whole document in a code fence. The output will be a reference document "
    "for designers — be thorough; do not skip pages."
)

JSON_PROMPT = (
    "Extract a design system specification from this NASA Graphics Standards "
    "Manual and return it as a single JSON object. Include:\n"
    "  - colors: array of objects with `name`, `role` (semantic), `hex` and "
    "`rgb` if specified or derivable, plus any process/PMS/ink references the "
    "manual gives.\n"
    "  - typography: font families, weights, allowed sizes, line heights, "
    "tracking, and hierarchy rules (e.g. headline vs. body vs. caption).\n"
    "  - grid: page grid, columns, gutters, margins, modular units.\n"
    "  - spacing: any clear-space, padding, or proportional rules.\n"
    "  - layout_principles: short string array of stated design principles "
    "(e.g. 'symbol must always appear with at least 1x its width of clear "
    "space').\n"
    "  - logo: construction rules, minimum sizes, forbidden modifications.\n"
    "  - applications: notable application categories covered (stationery, "
    "vehicles, signage, etc.) as a string array.\n"
    "Return ONLY the JSON object — no Markdown fences, no commentary. If a "
    "value is not specified in the manual, omit the key rather than guessing."
)


def load_api_key() -> str:
    """Read GEMENI_KEY from .env without printing it."""
    if not ENV_PATH.exists():
        raise SystemExit(f"Missing .env at {ENV_PATH}")
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == "GEMENI_KEY":
            return v.strip().strip('"').strip("'")
    raise SystemExit("GEMENI_KEY not found in .env")


def upload_pdf(client: genai.Client) -> types.File:
    print(f"Uploading {PDF_PATH.name} ({PDF_PATH.stat().st_size/1_000_000:.2f} MB)...")
    f = client.files.upload(
        file=PDF_PATH,
        config=types.UploadFileConfig(mime_type="application/pdf"),
    )
    # Wait for ACTIVE state
    while f.state and f.state.name == "PROCESSING":
        time.sleep(2)
        f = client.files.get(name=f.name)
    if f.state and f.state.name != "ACTIVE":
        raise SystemExit(f"File upload failed: state={f.state.name}")
    print(f"  uploaded: {f.name}  state={f.state.name}")
    return f


def call_gemini(client: genai.Client, pdf_file: types.File, prompt: str, label: str) -> tuple[str, object]:
    print(f"[{label}] generating with {MODEL} ...")
    t0 = time.time()
    resp = client.models.generate_content(
        model=MODEL,
        contents=[pdf_file, prompt],
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=32768,
        ),
    )
    dt = time.time() - t0
    text = resp.text or ""
    usage = getattr(resp, "usage_metadata", None)
    print(f"[{label}] done in {dt:.1f}s, {len(text)} chars")
    if usage:
        print(f"[{label}] usage: {usage}")
    return text, usage


def strip_code_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        # remove leading ```lang\n and trailing ```
        nl = s.find("\n")
        if nl != -1:
            s = s[nl + 1 :]
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()


def main() -> int:
    api_key = load_api_key()
    if not PDF_PATH.exists():
        raise SystemExit(f"PDF not found: {PDF_PATH}")
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.parent.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=api_key)
    pdf_file = upload_pdf(client)

    try:
        md_text, md_usage = call_gemini(client, pdf_file, MD_PROMPT, "markdown")
        md_clean = strip_code_fences(md_text) if md_text.lstrip().startswith("```") else md_text
        MD_OUT.write_text(md_clean, encoding="utf-8")
        print(f"  wrote {MD_OUT}  ({MD_OUT.stat().st_size} bytes)")

        json_text, json_usage = call_gemini(client, pdf_file, JSON_PROMPT, "json")
        json_clean = strip_code_fences(json_text)
        try:
            parsed = json.loads(json_clean)
            JSON_OUT.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
            print(f"  wrote {JSON_OUT}  ({JSON_OUT.stat().st_size} bytes, valid JSON)")
            colors = parsed.get("colors", []) if isinstance(parsed, dict) else []
            print(f"  top-level keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'non-dict'}")
            print(f"  color count:    {len(colors) if isinstance(colors, list) else 'n/a'}")
        except json.JSONDecodeError as e:
            # Save raw for inspection so the work isn't lost.
            raw_path = JSON_OUT.with_suffix(".raw.txt")
            raw_path.write_text(json_text, encoding="utf-8")
            print(f"  JSON parse failed: {e}; raw saved to {raw_path}")
            return 2
    finally:
        try:
            client.files.delete(name=pdf_file.name)
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
