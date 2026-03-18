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
<!-- Derived from the Monad System design language — colors.json               -->
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
    background="#121212",
    line_highlight="#1e1e1e",
    insertion_point="#03A9F4",
    invisibles="#333333",
    selection="#0D3F55",
    # ── Plain text ────────────────────────────────────────────────────────────
    plain_text="#E0E0E0",
    # ── Comments ──────────────────────────────────────────────────────────────
    comment="#757575",
    comment_doc="#757575",
    comment_doc_keyword="#03A9F4",
    # ── Keywords / operators ──────────────────────────────────────────────────
    keyword="#03A9F4",
    preprocessor="#9C27B0",
    # ── String / number literals ──────────────────────────────────────────────
    string="#8BC34A",
    character="#8BC34A",
    number="#FFC107",
    url="#03A9F4",
    # ── Identifiers ───────────────────────────────────────────────────────────
    identifier_class="#00BCD4",
    identifier_class_system="#00BCD4",
    identifier_type="#00BCD4",
    identifier_type_system="#00BCD4",
    identifier_function="#00BCD4",
    identifier_function_system="#00BCD4",
    identifier_constant="#FFEB3B",
    identifier_constant_system="#FFEB3B",
    identifier_variable="#E0E0E0",
    identifier_variable_system="#E0E0E0",
    identifier_macro="#9C27B0",
    identifier_macro_system="#9C27B0",
    declaration_other="#E0E0E0",
    declaration_type="#00BCD4",
    attribute="#B0B0B0",
    # ── Gutter ────────────────────────────────────────────────────────────────
    gutter_bg="#0d0d0d",
    gutter_fg="#757575",
    # ── Console ───────────────────────────────────────────────────────────────
    console_bg="#121212",
    console_fg="#E0E0E0",
    console_input="#03A9F4",
    console_output="#B0B0B0",
    console_exec_status="#757575",
    console_cursor="#03A9F4",
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
    background="#f4f4f4",
    line_highlight="#ebebeb",
    insertion_point="#0288d1",
    invisibles="#c6c6c6",
    selection="#ABD3E9",
    # ── Plain text ────────────────────────────────────────────────────────────
    plain_text="#161616",
    # ── Comments ──────────────────────────────────────────────────────────────
    comment="#8d8d8d",
    comment_doc="#8d8d8d",
    comment_doc_keyword="#0288d1",
    # ── Keywords / operators ──────────────────────────────────────────────────
    keyword="#0288d1",
    preprocessor="#6a1b9a",
    # ── String / number literals ──────────────────────────────────────────────
    string="#558b2f",
    character="#558b2f",
    number="#e65c00",
    url="#0288d1",
    # ── Identifiers ───────────────────────────────────────────────────────────
    identifier_class="#00838f",
    identifier_class_system="#00838f",
    identifier_type="#00838f",
    identifier_type_system="#00838f",
    identifier_function="#00838f",
    identifier_function_system="#00838f",
    identifier_constant="#7b6000",
    identifier_constant_system="#7b6000",
    identifier_variable="#161616",
    identifier_variable_system="#161616",
    identifier_macro="#6a1b9a",
    identifier_macro_system="#6a1b9a",
    declaration_other="#161616",
    declaration_type="#00838f",
    attribute="#525252",
    # ── Gutter ────────────────────────────────────────────────────────────────
    gutter_bg="#ffffff",
    gutter_fg="#8d8d8d",
    # ── Console ───────────────────────────────────────────────────────────────
    console_bg="#f4f4f4",
    console_fg="#161616",
    console_input="#0288d1",
    console_output="#525252",
    console_exec_status="#8d8d8d",
    console_cursor="#0288d1",
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
