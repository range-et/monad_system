"""
Xcode color theme generator for the Monad System.

Accepts palette tokens and returns .xccolortheme plist strings for:
  - "Monad Dark.xccolortheme"
  - "Monad Light.xccolortheme"

Xcode stores user themes in:
  ~/Library/Developer/Xcode/UserData/FontAndColorThemes/

Install: copy the .xccolortheme files to that directory, then
restart Xcode and select the theme via:
  Settings → Themes → Monad Dark / Monad Light
"""

from datetime import datetime


def _c(hex_color):
    """Convert #RRGGBB to Xcode's space-separated 'R G B A' float string (alpha=1)."""
    h = hex_color.lstrip("#")
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return f"{r:.4f} {g:.4f} {b:.4f} 1"


def _plist(colors, fonts, title="Monad Dark"):
    """Render the full .xccolortheme plist XML from resolved color/font dicts."""
    date_str = datetime.now().strftime("%Y-%m-%d")

    def _kv(key, value):
        return f"\t<key>{key}</key>\n\t<string>{value}</string>"

    def _nested_kv(key, value):
        return f"\t\t<key>{key}</key>\n\t\t<string>{value}</string>"

    canvas_keys = [
        "DVTConsoleDebuggerInputTextColor",
        "DVTConsoleDebuggerOutputTextColor",
        "DVTConsoleExecStatusTextColor",
        "DVTConsoleTextBackgroundColor",
        "DVTConsoleTextColor",
        "DVTConsoleTextInsertionPointColor",
        "DVTLineCounterBackgroundColor",
        "DVTLineCounterTextColor",
        "DVTSourceTextBackground",
        "DVTSourceTextCurrentLineHighlightColor",
        "DVTSourceTextInsertionPointColor",
        "DVTSourceTextInvisiblesColor",
        "DVTSourceTextSelectionColor",
    ]

    syntax_keys = [
        "xcode.syntax.attribute",
        "xcode.syntax.character",
        "xcode.syntax.comment",
        "xcode.syntax.comment.doc",
        "xcode.syntax.comment.doc.keyword",
        "xcode.syntax.declaration.other",
        "xcode.syntax.declaration.type",
        "xcode.syntax.identifier.class",
        "xcode.syntax.identifier.class.system",
        "xcode.syntax.identifier.constant",
        "xcode.syntax.identifier.constant.system",
        "xcode.syntax.identifier.function",
        "xcode.syntax.identifier.function.system",
        "xcode.syntax.identifier.macro",
        "xcode.syntax.identifier.macro.system",
        "xcode.syntax.identifier.type",
        "xcode.syntax.identifier.type.system",
        "xcode.syntax.identifier.variable",
        "xcode.syntax.identifier.variable.system",
        "xcode.syntax.keyword",
        "xcode.syntax.number",
        "xcode.syntax.plain",
        "xcode.syntax.preprocessor",
        "xcode.syntax.string",
        "xcode.syntax.url",
    ]

    canvas_block = "\n".join(_kv(k, colors[k]) for k in canvas_keys if k in colors)
    syntax_block = "\n".join(_nested_kv(k, colors[k]) for k in syntax_keys if k in colors)
    font_block   = "\n".join(_nested_kv(k, v) for k, v in fonts.items())

    return f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<!-- {title} — Xcode Color Theme                                               -->
<!-- Generated from Monad System colors.json                                  -->
<!-- Generated {date_str}                                                      -->
<!--                                                                           -->
<!-- Install: cp "{title}.xccolortheme"                                        -->
<!--   ~/Library/Developer/Xcode/UserData/FontAndColorThemes/                 -->
<!-- Activate: Xcode → Settings → Themes → {title}                            -->
<plist version="1.0">
<dict>
{canvas_block}
\t<key>DVTSourceTextSyntaxColors</key>
\t<dict>
{syntax_block}
\t</dict>
\t<key>DVTSourceTextSyntaxFonts</key>
\t<dict>
{font_block}
\t</dict>
</dict>
</plist>
"""


# ─── Dark theme ───────────────────────────────────────────────────────────────

def create_xcode_dark_theme(
    # ── Canvas ────────────────────────────────────────────────────────────────
    background="#0F1113",
    line_highlight="#171A1E",
    insertion_point="#1E88C8",
    invisibles="#2A313A",
    selection="#143549",
    # ── Plain text ────────────────────────────────────────────────────────────
    plain_text="#EEF2F6",
    # ── Comments ──────────────────────────────────────────────────────────────
    comment="#7D8794",
    comment_doc="#7D8794",
    comment_doc_keyword="#1E88C8",
    # ── Keywords / operators ──────────────────────────────────────────────────
    keyword="#1E88C8",
    preprocessor="#9C27B0",
    # ── String / number literals ──────────────────────────────────────────────
    string="#6EAD45",
    character="#6EAD45",
    number="#D7A12A",
    url="#1E88C8",
    # ── Identifiers ───────────────────────────────────────────────────────────
    identifier_class="#2B9ED1",
    identifier_class_system="#2B9ED1",
    identifier_type="#2B9ED1",
    identifier_type_system="#2B9ED1",
    identifier_function="#2B9ED1",
    identifier_function_system="#2B9ED1",
    identifier_constant="#FFEB3B",
    identifier_constant_system="#FFEB3B",
    identifier_variable="#EEF2F6",
    identifier_variable_system="#EEF2F6",
    identifier_macro="#9C27B0",
    identifier_macro_system="#9C27B0",
    declaration_other="#EEF2F6",
    declaration_type="#2B9ED1",
    attribute="#B6BFCC",
    # ── Gutter ────────────────────────────────────────────────────────────────
    gutter_bg="#0A0C0E",
    gutter_fg="#7D8794",
    # ── Console ───────────────────────────────────────────────────────────────
    console_bg="#0F1113",
    console_fg="#EEF2F6",
    console_input="#1E88C8",
    console_output="#B6BFCC",
    console_exec_status="#7D8794",
    console_cursor="#1E88C8",
    # ── Font ──────────────────────────────────────────────────────────────────
    font_name="SFMono-Regular",
    font_size=13.0,
):
    """Return the Monad Dark Xcode theme plist as a string."""
    bold = font_name.replace("Regular", "Medium")

    colors = {
        # Console
        "DVTConsoleDebuggerInputTextColor":    _c(console_input),
        "DVTConsoleDebuggerOutputTextColor":   _c(console_output),
        "DVTConsoleExecStatusTextColor":       _c(console_exec_status),
        "DVTConsoleTextBackgroundColor":       _c(console_bg),
        "DVTConsoleTextColor":                 _c(console_fg),
        "DVTConsoleTextInsertionPointColor":   _c(console_cursor),
        # Gutter
        "DVTLineCounterBackgroundColor":       _c(gutter_bg),
        "DVTLineCounterTextColor":             _c(gutter_fg),
        # Editor canvas
        "DVTSourceTextBackground":             _c(background),
        "DVTSourceTextCurrentLineHighlightColor": _c(line_highlight),
        "DVTSourceTextInsertionPointColor":    _c(insertion_point),
        "DVTSourceTextInvisiblesColor":        _c(invisibles),
        "DVTSourceTextSelectionColor":         _c(selection),
        # Syntax tokens
        "xcode.syntax.attribute":                     _c(attribute),
        "xcode.syntax.character":                     _c(character),
        "xcode.syntax.comment":                       _c(comment),
        "xcode.syntax.comment.doc":                   _c(comment_doc),
        "xcode.syntax.comment.doc.keyword":           _c(comment_doc_keyword),
        "xcode.syntax.declaration.other":             _c(declaration_other),
        "xcode.syntax.declaration.type":              _c(declaration_type),
        "xcode.syntax.identifier.class":              _c(identifier_class),
        "xcode.syntax.identifier.class.system":       _c(identifier_class_system),
        "xcode.syntax.identifier.constant":           _c(identifier_constant),
        "xcode.syntax.identifier.constant.system":    _c(identifier_constant_system),
        "xcode.syntax.identifier.function":           _c(identifier_function),
        "xcode.syntax.identifier.function.system":    _c(identifier_function_system),
        "xcode.syntax.identifier.macro":              _c(identifier_macro),
        "xcode.syntax.identifier.macro.system":       _c(identifier_macro_system),
        "xcode.syntax.identifier.type":               _c(identifier_type),
        "xcode.syntax.identifier.type.system":        _c(identifier_type_system),
        "xcode.syntax.identifier.variable":           _c(identifier_variable),
        "xcode.syntax.identifier.variable.system":    _c(identifier_variable_system),
        "xcode.syntax.keyword":                       _c(keyword),
        "xcode.syntax.number":                        _c(number),
        "xcode.syntax.plain":                         _c(plain_text),
        "xcode.syntax.preprocessor":                  _c(preprocessor),
        "xcode.syntax.string":                        _c(string),
        "xcode.syntax.url":                           _c(url),
    }

    fonts = {
        "xcode.syntax.comment":             f"{font_name} - {font_size}",
        "xcode.syntax.comment.doc":         f"{font_name} - {font_size}",
        "xcode.syntax.comment.doc.keyword": f"{bold} - {font_size}",
        "xcode.syntax.keyword":             f"{bold} - {font_size}",
        "xcode.syntax.preprocessor":        f"{font_name} - {font_size}",
    }

    return _plist(colors, fonts, title="Monad Dark")


# ─── Light theme ──────────────────────────────────────────────────────────────

def create_xcode_light_theme(
    # ── Canvas ────────────────────────────────────────────────────────────────
    background="#F2F4F7",
    line_highlight="#EDF1F5",
    insertion_point="#1A74AA",
    invisibles="#BCC6D2",
    selection="#B1CEE0",
    # ── Plain text ────────────────────────────────────────────────────────────
    plain_text="#141A22",
    # ── Comments ──────────────────────────────────────────────────────────────
    comment="#7E8998",
    comment_doc="#7E8998",
    comment_doc_keyword="#1A74AA",
    # ── Keywords / operators ──────────────────────────────────────────────────
    keyword="#1A74AA",
    preprocessor="#6D1B7B",
    # ── String / number literals ──────────────────────────────────────────────
    string="#47702D",
    character="#47702D",
    number="#A17920",
    url="#1A74AA",
    # ── Identifiers ───────────────────────────────────────────────────────────
    identifier_class="#1C6788",
    identifier_class_system="#1C6788",
    identifier_type="#1C6788",
    identifier_type_system="#1C6788",
    identifier_function="#1C6788",
    identifier_function_system="#1C6788",
    identifier_constant="#765916",
    identifier_constant_system="#765916",
    identifier_variable="#141A22",
    identifier_variable_system="#141A22",
    identifier_macro="#6D1B7B",
    identifier_macro_system="#6D1B7B",
    declaration_other="#141A22",
    declaration_type="#1C6788",
    attribute="#4F5A69",
    # ── Gutter ────────────────────────────────────────────────────────────────
    gutter_bg="#ffffff",
    gutter_fg="#7E8998",
    # ── Console ───────────────────────────────────────────────────────────────
    console_bg="#F2F4F7",
    console_fg="#141A22",
    console_input="#1A74AA",
    console_output="#4F5A69",
    console_exec_status="#7E8998",
    console_cursor="#1A74AA",
    # ── Font ──────────────────────────────────────────────────────────────────
    font_name="SFMono-Regular",
    font_size=13.0,
):
    """Return the Monad Light Xcode theme plist as a string."""
    bold = font_name.replace("Regular", "Medium")

    colors = {
        # Console
        "DVTConsoleDebuggerInputTextColor":    _c(console_input),
        "DVTConsoleDebuggerOutputTextColor":   _c(console_output),
        "DVTConsoleExecStatusTextColor":       _c(console_exec_status),
        "DVTConsoleTextBackgroundColor":       _c(console_bg),
        "DVTConsoleTextColor":                 _c(console_fg),
        "DVTConsoleTextInsertionPointColor":   _c(console_cursor),
        # Gutter
        "DVTLineCounterBackgroundColor":       _c(gutter_bg),
        "DVTLineCounterTextColor":             _c(gutter_fg),
        # Editor canvas
        "DVTSourceTextBackground":             _c(background),
        "DVTSourceTextCurrentLineHighlightColor": _c(line_highlight),
        "DVTSourceTextInsertionPointColor":    _c(insertion_point),
        "DVTSourceTextInvisiblesColor":        _c(invisibles),
        "DVTSourceTextSelectionColor":         _c(selection),
        # Syntax tokens
        "xcode.syntax.attribute":                     _c(attribute),
        "xcode.syntax.character":                     _c(character),
        "xcode.syntax.comment":                       _c(comment),
        "xcode.syntax.comment.doc":                   _c(comment_doc),
        "xcode.syntax.comment.doc.keyword":           _c(comment_doc_keyword),
        "xcode.syntax.declaration.other":             _c(declaration_other),
        "xcode.syntax.declaration.type":              _c(declaration_type),
        "xcode.syntax.identifier.class":              _c(identifier_class),
        "xcode.syntax.identifier.class.system":       _c(identifier_class_system),
        "xcode.syntax.identifier.constant":           _c(identifier_constant),
        "xcode.syntax.identifier.constant.system":    _c(identifier_constant_system),
        "xcode.syntax.identifier.function":           _c(identifier_function),
        "xcode.syntax.identifier.function.system":    _c(identifier_function_system),
        "xcode.syntax.identifier.macro":              _c(identifier_macro),
        "xcode.syntax.identifier.macro.system":       _c(identifier_macro_system),
        "xcode.syntax.identifier.type":               _c(identifier_type),
        "xcode.syntax.identifier.type.system":        _c(identifier_type_system),
        "xcode.syntax.identifier.variable":           _c(identifier_variable),
        "xcode.syntax.identifier.variable.system":    _c(identifier_variable_system),
        "xcode.syntax.keyword":                       _c(keyword),
        "xcode.syntax.number":                        _c(number),
        "xcode.syntax.plain":                         _c(plain_text),
        "xcode.syntax.preprocessor":                  _c(preprocessor),
        "xcode.syntax.string":                        _c(string),
        "xcode.syntax.url":                           _c(url),
    }

    fonts = {
        "xcode.syntax.comment":             f"{font_name} - {font_size}",
        "xcode.syntax.comment.doc":         f"{font_name} - {font_size}",
        "xcode.syntax.comment.doc.keyword": f"{bold} - {font_size}",
        "xcode.syntax.keyword":             f"{bold} - {font_size}",
        "xcode.syntax.preprocessor":        f"{font_name} - {font_size}",
    }

    return _plist(colors, fonts, title="Monad Light")
