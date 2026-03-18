"""
VS Code color theme generator for the Monad System.

Accepts palette tokens and returns JSON strings for:
  - monad-dark-color-theme.json
  - monad-light-color-theme.json
  - package.json  (extension manifest)

Generated output is standard VS Code JSONC (comments stripped for clean
machine output). Drop the three files into any folder registered as a VS Code
extension, or place them in:
  ~/.vscode/extensions/monad-system-theme-1.0.0/
"""

import json


# ─── Palette → workbench + token mappings ────────────────────────────────────

def _workbench_dark(p):
    """Build the workbench color dict for the dark theme from palette p."""
    bg      = p["bg"]
    l01     = p["layer01"]
    l02     = p["layer02"]
    l03     = p["layer03"]
    act_bg  = p["activity_bar_bg"]    # darkest surface
    txt_p   = p["text_primary"]
    txt_s   = p["text_secondary"]
    txt_d   = p["text_disabled"]
    brd     = p["border"]
    brd_s   = p["border_subtle"]
    ia      = p["interactive"]
    ia_h    = p["interactive_hover"]
    ia_a    = p["interactive_active"]
    info    = p["info"]
    succ    = p["success"]
    warn    = p["warning"]
    err     = p["error"]
    hi      = p["highlight"]

    return {
        # Editor canvas
        "editor.background":                          bg,
        "editor.foreground":                          txt_p,
        "editorCursor.foreground":                    ia,
        "editor.lineHighlightBackground":             l01,
        "editor.lineHighlightBorder":                 "#00000000",
        "editor.selectionBackground":                 ia + "30",
        "editor.selectionHighlightBackground":        ia + "18",
        "editor.inactiveSelectionBackground":         ia + "20",
        "editor.wordHighlightBackground":             info + "20",
        "editor.wordHighlightStrongBackground":       info + "30",
        "editor.findMatchBackground":                 warn + "40",
        "editor.findMatchHighlightBackground":        warn + "20",
        "editor.rangeHighlightBackground":            ia + "10",
        "editorIndentGuide.background1":              brd_s,
        "editorIndentGuide.activeBackground1":        brd,
        "editorRuler.foreground":                     brd_s,
        "editorWhitespace.foreground":                brd,
        "editorBracketMatch.background":              ia + "20",
        "editorBracketMatch.border":                  ia,
        "editorOverviewRuler.border":                 l01,
        "editorOverviewRuler.findMatchForeground":    warn,
        "editorOverviewRuler.selectionHighlightForeground": ia,
        "editorOverviewRuler.errorForeground":        err,
        "editorOverviewRuler.warningForeground":      warn,
        "editorOverviewRuler.infoForeground":         info,
        "editorGutter.background":                    bg,
        "editorGutter.addedBackground":               succ,
        "editorGutter.deletedBackground":             err,
        "editorGutter.modifiedBackground":            ia,
        # Line numbers
        "editorLineNumber.foreground":                brd,
        "editorLineNumber.activeForeground":          txt_d,
        # Diagnostics
        "editorError.foreground":                     err,
        "editorWarning.foreground":                   warn,
        "editorInfo.foreground":                      info,
        "editorHint.foreground":                      succ,
        # Activity bar
        "activityBar.background":                     act_bg,
        "activityBar.foreground":                     txt_p,
        "activityBar.inactiveForeground":             txt_d,
        "activityBar.border":                         brd,
        "activityBarBadge.background":                ia,
        "activityBarBadge.foreground":                act_bg,
        # Side bar
        "sideBar.background":                         l01,
        "sideBar.foreground":                         txt_s,
        "sideBar.border":                             brd,
        "sideBarTitle.foreground":                    txt_d,
        "sideBarSectionHeader.background":            l02,
        "sideBarSectionHeader.foreground":            txt_d,
        "sideBarSectionHeader.border":                brd,
        # File tree / list
        "list.activeSelectionBackground":             l02,
        "list.activeSelectionForeground":             txt_p,
        "list.inactiveSelectionBackground":           l01,
        "list.inactiveSelectionForeground":           txt_s,
        "list.hoverBackground":                       l01,
        "list.hoverForeground":                       txt_p,
        "list.focusBackground":                       l02,
        "list.focusForeground":                       txt_p,
        "list.highlightForeground":                   ia,
        "list.errorForeground":                       err,
        "list.warningForeground":                     warn,
        "listFilterWidget.background":                l02,
        "listFilterWidget.outline":                   ia,
        "listFilterWidget.noMatchesOutline":          err,
        # Title bar
        "titleBar.activeBackground":                  act_bg,
        "titleBar.activeForeground":                  txt_p,
        "titleBar.inactiveBackground":                act_bg,
        "titleBar.inactiveForeground":                txt_d,
        "titleBar.border":                            brd,
        # Tabs
        "editorGroupHeader.tabsBackground":           l01,
        "editorGroupHeader.noTabsBackground":         bg,
        "editorGroupHeader.border":                   brd,
        "tab.activeBackground":                       bg,
        "tab.activeForeground":                       txt_p,
        "tab.inactiveBackground":                     l01,
        "tab.inactiveForeground":                     txt_d,
        "tab.border":                                 brd,
        "tab.activeBorder":                           ia,
        "tab.activeBorderTop":                        "#00000000",
        "tab.unfocusedActiveBorder":                  brd,
        "tab.unfocusedActiveForeground":              txt_s,
        "tab.unfocusedInactiveForeground":            txt_d,
        "tab.hoverBackground":                        l02,
        "tab.hoverForeground":                        txt_p,
        # Status bar
        "statusBar.background":                       ia,
        "statusBar.foreground":                       act_bg,
        "statusBar.border":                           ia_a,
        "statusBar.noFolderBackground":               l02,
        "statusBar.noFolderForeground":               txt_s,
        "statusBar.debuggingBackground":              warn,
        "statusBar.debuggingForeground":              act_bg,
        "statusBarItem.hoverBackground":              ia_h + "20",
        "statusBarItem.activeBackground":             ia_a + "30",
        "statusBarItem.errorBackground":              err,
        "statusBarItem.errorForeground":              act_bg,
        "statusBarItem.warningBackground":            warn,
        "statusBarItem.warningForeground":            act_bg,
        # Panel
        "panel.background":                           l01,
        "panel.border":                               brd,
        "panel.dropBorder":                           ia,
        "panelTitle.activeForeground":                txt_p,
        "panelTitle.inactiveForeground":              txt_d,
        "panelTitle.activeBorder":                    ia,
        # Terminal
        "terminal.background":                        bg,
        "terminal.foreground":                        txt_p,
        "terminal.border":                            brd,
        "terminal.selectionBackground":               ia + "30",
        "terminalCursor.background":                  bg,
        "terminalCursor.foreground":                  ia,
        "terminal.ansiBlack":                         p["ansi_black"],
        "terminal.ansiRed":                           p["ansi_red"],
        "terminal.ansiGreen":                         p["ansi_green"],
        "terminal.ansiYellow":                        p["ansi_yellow"],
        "terminal.ansiBlue":                          p["ansi_blue"],
        "terminal.ansiMagenta":                       p["ansi_magenta"],
        "terminal.ansiCyan":                          p["ansi_cyan"],
        "terminal.ansiWhite":                         p["ansi_white"],
        "terminal.ansiBrightBlack":                   p["ansi_bright_black"],
        "terminal.ansiBrightRed":                     p["ansi_bright_red"],
        "terminal.ansiBrightGreen":                   p["ansi_bright_green"],
        "terminal.ansiBrightYellow":                  p["ansi_bright_yellow"],
        "terminal.ansiBrightBlue":                    p["ansi_bright_blue"],
        "terminal.ansiBrightMagenta":                 p["ansi_bright_magenta"],
        "terminal.ansiBrightCyan":                    p["ansi_bright_cyan"],
        "terminal.ansiBrightWhite":                   p["ansi_bright_white"],
        # Inputs
        "input.background":                           l02,
        "input.foreground":                           txt_p,
        "input.border":                               brd,
        "input.placeholderForeground":                txt_d,
        "inputOption.activeBorder":                   ia,
        "inputOption.activeBackground":               ia + "20",
        "inputOption.activeForeground":               txt_p,
        "inputValidation.infoBorder":                 info,
        "inputValidation.infoBackground":             info + "1a",
        "inputValidation.warningBorder":              warn,
        "inputValidation.warningBackground":          warn + "1a",
        "inputValidation.errorBorder":                err,
        "inputValidation.errorBackground":            err + "1a",
        # Dropdowns
        "dropdown.background":                        l02,
        "dropdown.foreground":                        txt_p,
        "dropdown.border":                            brd,
        # Buttons
        "button.background":                          ia,
        "button.foreground":                          act_bg,
        "button.hoverBackground":                     ia_h,
        "button.secondaryBackground":                 l02,
        "button.secondaryForeground":                 txt_p,
        "button.secondaryHoverBackground":            l03,
        # Badges
        "badge.background":                           ia,
        "badge.foreground":                           act_bg,
        # Scrollbar
        "scrollbarSlider.background":                 brd + "80",
        "scrollbarSlider.hoverBackground":            brd + "CC",
        "scrollbarSlider.activeBackground":           ia + "60",
        "scrollbar.shadow":                           "#00000060",
        # Progress
        "progressBar.background":                     ia,
        # Diff
        "diffEditor.insertedTextBackground":          succ + "18",
        "diffEditor.removedTextBackground":           err + "18",
        "diffEditor.insertedLineBackground":          succ + "10",
        "diffEditor.removedLineBackground":           err + "10",
        # Git decorations
        "gitDecoration.addedResourceForeground":      succ,
        "gitDecoration.modifiedResourceForeground":   ia,
        "gitDecoration.deletedResourceForeground":    err,
        "gitDecoration.untrackedResourceForeground":  p["move_start"],
        "gitDecoration.ignoredResourceForeground":    txt_d,
        "gitDecoration.conflictingResourceForeground": warn,
        "gitDecoration.submoduleResourceForeground":  info,
        # Notifications
        "notifications.background":                   l02,
        "notifications.foreground":                   txt_p,
        "notifications.border":                       brd,
        "notificationCenterHeader.background":        l03,
        "notificationCenterHeader.foreground":        txt_d,
        "notificationToast.border":                   brd,
        "notificationsErrorIcon.foreground":          err,
        "notificationsWarningIcon.foreground":        warn,
        "notificationsInfoIcon.foreground":           info,
        # Peek view
        "peekView.border":                            ia,
        "peekViewEditor.background":                  l02,
        "peekViewEditor.matchHighlightBackground":    warn + "30",
        "peekViewResult.background":                  l01,
        "peekViewResult.fileForeground":              txt_p,
        "peekViewResult.lineForeground":              txt_s,
        "peekViewResult.matchHighlightBackground":    warn + "30",
        "peekViewResult.selectionBackground":         l03,
        "peekViewResult.selectionForeground":         txt_p,
        "peekViewTitle.background":                   l03,
        "peekViewTitleLabel.foreground":              txt_p,
        "peekViewTitleDescription.foreground":        txt_d,
        # Breadcrumb
        "breadcrumb.background":                      bg,
        "breadcrumb.foreground":                      txt_d,
        "breadcrumb.focusForeground":                 txt_s,
        "breadcrumb.activeSelectionForeground":       txt_p,
        "breadcrumbPicker.background":                l02,
        # Menu
        "menu.background":                            l02,
        "menu.foreground":                            txt_p,
        "menu.selectionBackground":                   l03,
        "menu.selectionForeground":                   txt_p,
        "menu.selectionBorder":                       brd,
        "menu.separatorBackground":                   brd,
        "menu.border":                                brd,
        "menubar.selectionBackground":                l02,
        "menubar.selectionForeground":                txt_p,
        # Quick input
        "quickInput.background":                      l02,
        "quickInput.foreground":                      txt_p,
        "quickInputList.focusBackground":             l03,
        "quickInputList.focusForeground":             txt_p,
        "quickInputList.focusIconForeground":         ia,
        "quickInputTitle.background":                 l03,
        # Global chrome
        "focusBorder":                                ia,
        "foreground":                                 txt_p,
        "widget.shadow":                              "#00000080",
        "selection.background":                       ia + "30",
        "icon.foreground":                            txt_s,
        "disabledForeground":                         txt_d,
        "errorForeground":                            err,
        "descriptionForeground":                      txt_d,
        # Extensions
        "extensionButton.prominentBackground":        ia,
        "extensionButton.prominentForeground":        act_bg,
        "extensionButton.prominentHoverBackground":   ia_h,
        # Code lens
        "editorCodeLens.foreground":                  txt_d,
        # Lightbulb
        "editorLightBulb.foreground":                 warn,
        "editorLightBulbAutoFix.foreground":          succ,
        # Settings
        "settings.modifiedItemIndicator":             ia,
        "settings.focusedRowBackground":              l02,
        "settings.rowHoverBackground":                l02,
        # Welcome page
        "welcomePage.background":                     bg,
        "welcomePage.tileBackground":                 l02,
        "welcomePage.tileBorder":                     brd,
        "walkThrough.embeddedEditorBackground":       l01,
        # Merge
        "merge.currentHeaderBackground":              succ + "30",
        "merge.currentContentBackground":             succ + "15",
        "merge.incomingHeaderBackground":             ia + "30",
        "merge.incomingContentBackground":            ia + "15",
        "merge.border":                               brd,
        "merge.commonContentBackground":              warn + "15",
        "merge.commonHeaderBackground":               warn + "30",
        # Charts
        "charts.red":                                 err,
        "charts.blue":                                ia,
        "charts.yellow":                              warn,
        "charts.green":                               succ,
        "charts.purple":                              p["move_finish"],
        "charts.foreground":                          txt_p,
        "charts.lines":                               brd,
    }


def _workbench_light(p):
    """Build the workbench color dict for the light theme from palette p."""
    bg      = p["bg"]
    l01     = p["layer01"]
    l02     = p["layer02"]
    l03     = p["layer03"]
    txt_p   = p["text_primary"]
    txt_s   = p["text_secondary"]
    txt_d   = p["text_disabled"]
    brd     = p["border"]
    brd_s   = p["border_subtle"]
    ia      = p["interactive"]          # darker shade for light bg contrast
    ia_h    = p["interactive_hover"]
    ia_a    = p["interactive_active"]
    info    = p["info_dark"]
    succ    = p["success_dark"]
    warn    = p["warning"]
    err     = p["error_dark"]

    return {
        "editor.background":                          bg,
        "editor.foreground":                          txt_p,
        "editorCursor.foreground":                    ia,
        "editor.lineHighlightBackground":             l01,
        "editor.lineHighlightBorder":                 l03,
        "editor.selectionBackground":                 ia + "30",
        "editor.selectionHighlightBackground":        ia + "18",
        "editor.inactiveSelectionBackground":         ia + "20",
        "editor.wordHighlightBackground":             info + "20",
        "editor.wordHighlightStrongBackground":       info + "30",
        "editor.findMatchBackground":                 warn + "50",
        "editor.findMatchHighlightBackground":        warn + "28",
        "editor.rangeHighlightBackground":            ia + "15",
        "editorIndentGuide.background1":              brd_s,
        "editorIndentGuide.activeBackground1":        brd,
        "editorRuler.foreground":                     brd_s,
        "editorWhitespace.foreground":                brd,
        "editorBracketMatch.background":              ia + "20",
        "editorBracketMatch.border":                  ia,
        "editorOverviewRuler.border":                 l03,
        "editorOverviewRuler.errorForeground":        err,
        "editorOverviewRuler.warningForeground":      warn,
        "editorOverviewRuler.infoForeground":         info,
        "editorGutter.background":                    bg,
        "editorGutter.addedBackground":               succ,
        "editorGutter.deletedBackground":             err,
        "editorGutter.modifiedBackground":            ia,
        "editorLineNumber.foreground":                brd,
        "editorLineNumber.activeForeground":          txt_d,
        "editorError.foreground":                     err,
        "editorWarning.foreground":                   warn,
        "editorInfo.foreground":                      info,
        "editorHint.foreground":                      succ,
        "activityBar.background":                     l03,
        "activityBar.foreground":                     txt_p,
        "activityBar.inactiveForeground":             txt_d,
        "activityBar.border":                         brd,
        "activityBarBadge.background":                ia,
        "activityBarBadge.foreground":                "#ffffff",
        "sideBar.background":                         l01,
        "sideBar.foreground":                         txt_s,
        "sideBar.border":                             brd,
        "sideBarTitle.foreground":                    txt_d,
        "sideBarSectionHeader.background":            bg,
        "sideBarSectionHeader.foreground":            txt_d,
        "sideBarSectionHeader.border":                brd,
        "list.activeSelectionBackground":             l03,
        "list.activeSelectionForeground":             txt_p,
        "list.inactiveSelectionBackground":           bg,
        "list.inactiveSelectionForeground":           txt_s,
        "list.hoverBackground":                       bg,
        "list.hoverForeground":                       txt_p,
        "list.focusBackground":                       l03,
        "list.focusForeground":                       txt_p,
        "list.highlightForeground":                   ia,
        "list.errorForeground":                       err,
        "list.warningForeground":                     warn,
        "titleBar.activeBackground":                  l03,
        "titleBar.activeForeground":                  txt_p,
        "titleBar.inactiveBackground":                l03,
        "titleBar.inactiveForeground":                txt_d,
        "titleBar.border":                            brd,
        "editorGroupHeader.tabsBackground":           bg,
        "editorGroupHeader.noTabsBackground":         bg,
        "editorGroupHeader.border":                   brd,
        "tab.activeBackground":                       bg,
        "tab.activeForeground":                       txt_p,
        "tab.inactiveBackground":                     l01,
        "tab.inactiveForeground":                     txt_d,
        "tab.border":                                 brd,
        "tab.activeBorder":                           ia,
        "tab.activeBorderTop":                        "#00000000",
        "tab.unfocusedActiveBorder":                  brd,
        "tab.hoverBackground":                        l03,
        "tab.hoverForeground":                        txt_p,
        "statusBar.background":                       ia,
        "statusBar.foreground":                       "#ffffff",
        "statusBar.border":                           ia_a,
        "statusBar.noFolderBackground":               l03,
        "statusBar.noFolderForeground":               txt_s,
        "statusBar.debuggingBackground":              warn,
        "statusBar.debuggingForeground":              "#ffffff",
        "statusBarItem.errorBackground":              err,
        "statusBarItem.errorForeground":              "#ffffff",
        "statusBarItem.warningBackground":            warn,
        "statusBarItem.warningForeground":            "#ffffff",
        "panel.background":                           l01,
        "panel.border":                               brd,
        "panel.dropBorder":                           ia,
        "panelTitle.activeForeground":                txt_p,
        "panelTitle.inactiveForeground":              txt_d,
        "panelTitle.activeBorder":                    ia,
        "terminal.background":                        bg,
        "terminal.foreground":                        txt_p,
        "terminal.border":                            brd,
        "terminal.selectionBackground":               ia + "30",
        "terminalCursor.background":                  bg,
        "terminalCursor.foreground":                  ia,
        "terminal.ansiBlack":                         p["ansi_black"],
        "terminal.ansiRed":                           p["ansi_red"],
        "terminal.ansiGreen":                         p["ansi_green"],
        "terminal.ansiYellow":                        p["ansi_yellow"],
        "terminal.ansiBlue":                          p["ansi_blue"],
        "terminal.ansiMagenta":                       p["ansi_magenta"],
        "terminal.ansiCyan":                          p["ansi_cyan"],
        "terminal.ansiWhite":                         p["ansi_white"],
        "terminal.ansiBrightBlack":                   p["ansi_bright_black"],
        "terminal.ansiBrightRed":                     p["ansi_bright_red"],
        "terminal.ansiBrightGreen":                   p["ansi_bright_green"],
        "terminal.ansiBrightYellow":                  p["ansi_bright_yellow"],
        "terminal.ansiBrightBlue":                    p["ansi_bright_blue"],
        "terminal.ansiBrightMagenta":                 p["ansi_bright_magenta"],
        "terminal.ansiBrightCyan":                    p["ansi_bright_cyan"],
        "terminal.ansiBrightWhite":                   p["ansi_bright_white"],
        "input.background":                           l01,
        "input.foreground":                           txt_p,
        "input.border":                               brd,
        "input.placeholderForeground":                txt_d,
        "inputOption.activeBorder":                   ia,
        "inputOption.activeBackground":               ia + "20",
        "inputValidation.infoBorder":                 info,
        "inputValidation.infoBackground":             "#e0f7fa",
        "inputValidation.warningBorder":              warn,
        "inputValidation.warningBackground":          "#fff8e1",
        "inputValidation.errorBorder":                err,
        "inputValidation.errorBackground":            "#ffebee",
        "dropdown.background":                        l01,
        "dropdown.foreground":                        txt_p,
        "dropdown.border":                            brd,
        "button.background":                          ia,
        "button.foreground":                          "#ffffff",
        "button.hoverBackground":                     ia_h,
        "button.secondaryBackground":                 l03,
        "button.secondaryForeground":                 txt_p,
        "button.secondaryHoverBackground":            brd,
        "badge.background":                           ia,
        "badge.foreground":                           "#ffffff",
        "scrollbarSlider.background":                 brd + "80",
        "scrollbarSlider.hoverBackground":            brd + "CC",
        "scrollbarSlider.activeBackground":           ia + "60",
        "progressBar.background":                     ia,
        "diffEditor.insertedTextBackground":          succ + "20",
        "diffEditor.removedTextBackground":           err + "20",
        "diffEditor.insertedLineBackground":          succ + "12",
        "diffEditor.removedLineBackground":           err + "12",
        "gitDecoration.addedResourceForeground":      p["success_dark"],
        "gitDecoration.modifiedResourceForeground":   ia,
        "gitDecoration.deletedResourceForeground":    p["error_dark"],
        "gitDecoration.untrackedResourceForeground":  p["success_dark"],
        "gitDecoration.ignoredResourceForeground":    txt_d,
        "gitDecoration.conflictingResourceForeground": warn,
        "focusBorder":                                ia,
        "foreground":                                 txt_p,
        "widget.shadow":                              "#00000018",
        "selection.background":                       ia + "30",
        "icon.foreground":                            txt_s,
        "disabledForeground":                         txt_d,
        "errorForeground":                            p["error_dark"],
        "descriptionForeground":                      txt_d,
        "quickInput.background":                      l01,
        "quickInput.foreground":                      txt_p,
        "quickInputList.focusBackground":             l03,
        "quickInputList.focusForeground":             txt_p,
        "extensionButton.prominentBackground":        ia,
        "extensionButton.prominentForeground":        "#ffffff",
        "extensionButton.prominentHoverBackground":   ia_h,
        "settings.modifiedItemIndicator":             ia,
        "settings.focusedRowBackground":              bg,
        "settings.rowHoverBackground":                bg,
        "merge.currentHeaderBackground":              succ + "30",
        "merge.currentContentBackground":             succ + "15",
        "merge.incomingHeaderBackground":             ia + "30",
        "merge.incomingContentBackground":            ia + "15",
        "merge.commonHeaderBackground":               warn + "30",
        "merge.commonContentBackground":              warn + "15",
        "charts.red":                                 p["error_dark"],
        "charts.blue":                                ia,
        "charts.yellow":                              warn,
        "charts.green":                               p["success_dark"],
        "charts.purple":                              p["move_finish_dark"],
        "charts.foreground":                          txt_p,
        "charts.lines":                               brd,
    }


def _token_colors_dark(p):
    """Syntax token color rules (TextMate scopes) for the dark theme."""
    txt_p = p["text_primary"]
    txt_s = p["text_secondary"]
    txt_d = p["text_disabled"]
    ia    = p["interactive"]
    info  = p["info"]
    succ  = p["success"]
    warn  = p["warning"]
    err   = p["error"]
    hi    = p["highlight"]
    fin   = p["move_finish"]

    # Derived shades used for syntax
    info_light  = p.get("info_light",  "#4DD0E1")
    ia_light    = p.get("ia_light",    "#29B6F6")
    succ_vivid  = p.get("succ_vivid",  "#4CAF50")
    fin_light   = p.get("fin_light",   "#CE93D8")

    return [
        {"name": "Text base",
         "scope": ["source", "text"],
         "settings": {"foreground": txt_p}},

        # Comments
        {"name": "Comment",
         "scope": ["comment", "punctuation.definition.comment"],
         "settings": {"foreground": txt_d, "fontStyle": "italic"}},

        # Keywords / storage
        {"name": "Keyword",
         "scope": ["keyword", "keyword.control", "storage", "storage.type",
                   "storage.modifier", "keyword.other.using",
                   "keyword.other.import"],
         "settings": {"foreground": ia}},
        {"name": "Keyword — control flow",
         "scope": ["keyword.control.flow", "keyword.control.return",
                   "keyword.control.trycatch"],
         "settings": {"foreground": ia, "fontStyle": "italic"}},
        {"name": "Keyword — operator",
         "scope": ["keyword.operator"],
         "settings": {"foreground": txt_s}},
        {"name": "Keyword — logical/comparison",
         "scope": ["keyword.operator.logical", "keyword.operator.comparison",
                   "keyword.operator.assignment"],
         "settings": {"foreground": ia}},

        # Strings
        {"name": "String",
         "scope": ["string", "string.quoted", "string.template"],
         "settings": {"foreground": succ}},
        {"name": "String — regexp",
         "scope": ["string.regexp"],
         "settings": {"foreground": succ_vivid}},
        {"name": "String — escape",
         "scope": ["constant.character.escape"],
         "settings": {"foreground": info_light}},
        {"name": "String — interpolation",
         "scope": ["meta.interpolation",
                   "punctuation.definition.interpolation"],
         "settings": {"foreground": info}},

        # Numbers / constants
        {"name": "Number",
         "scope": ["constant.numeric"],
         "settings": {"foreground": warn}},
        {"name": "Boolean / built-in",
         "scope": ["constant.language"],
         "settings": {"foreground": warn, "fontStyle": "italic"}},
        {"name": "Constant — other",
         "scope": ["constant.other", "variable.other.constant"],
         "settings": {"foreground": hi}},

        # Functions
        {"name": "Function definition",
         "scope": ["entity.name.function",
                   "meta.function entity.name.function"],
         "settings": {"foreground": info}},
        {"name": "Function call",
         "scope": ["meta.function-call entity.name.function",
                   "meta.function-call.generic"],
         "settings": {"foreground": info_light}},
        {"name": "Function parameter",
         "scope": ["variable.parameter"],
         "settings": {"foreground": txt_s, "fontStyle": "italic"}},

        # Types / classes
        {"name": "Type / class",
         "scope": ["entity.name.type", "entity.name.class",
                   "entity.name.struct", "entity.name.enum",
                   "entity.name.interface", "entity.name.trait",
                   "support.type", "support.class",
                   "support.type.primitive"],
         "settings": {"foreground": ia_light}},
        {"name": "Inherited class",
         "scope": ["entity.other.inherited-class"],
         "settings": {"foreground": ia_light, "fontStyle": "italic"}},

        # Variables
        {"name": "Variable",
         "scope": ["variable", "variable.other"],
         "settings": {"foreground": txt_p}},
        {"name": "Variable — language (this/self)",
         "scope": ["variable.language"],
         "settings": {"foreground": ia, "fontStyle": "italic"}},
        {"name": "Property",
         "scope": ["variable.other.property",
                   "support.variable.property"],
         "settings": {"foreground": txt_s}},
        {"name": "Object key / attribute name",
         "scope": ["meta.object-literal.key",
                   "entity.other.attribute-name"],
         "settings": {"foreground": info}},

        # Punctuation
        {"name": "Punctuation",
         "scope": ["punctuation", "punctuation.separator",
                   "punctuation.terminator", "punctuation.accessor"],
         "settings": {"foreground": txt_d}},
        {"name": "Brackets",
         "scope": ["punctuation.definition.brackets",
                   "punctuation.section", "meta.brace"],
         "settings": {"foreground": txt_s}},

        # Decorators / annotations
        {"name": "Decorator",
         "scope": ["meta.decorator",
                   "entity.name.function.decorator",
                   "punctuation.decorator"],
         "settings": {"foreground": fin_light}},

        # Modules / namespaces
        {"name": "Module / namespace",
         "scope": ["entity.name.namespace", "entity.name.module",
                   "support.module"],
         "settings": {"foreground": info}},
        {"name": "Import path",
         "scope": ["meta.import string", "meta.require string"],
         "settings": {"foreground": succ}},

        # HTML
        {"name": "HTML tag",
         "scope": ["entity.name.tag"],
         "settings": {"foreground": ia}},
        {"name": "HTML attribute",
         "scope": ["entity.other.attribute-name.html"],
         "settings": {"foreground": info}},
        {"name": "HTML attribute value",
         "scope": ["string.quoted.html",
                   "meta.attribute.html string"],
         "settings": {"foreground": succ}},
        {"name": "HTML entity",
         "scope": ["constant.character.entity"],
         "settings": {"foreground": warn}},
        {"name": "HTML/XML tag punctuation",
         "scope": ["punctuation.definition.tag"],
         "settings": {"foreground": p["border"]}},

        # CSS
        {"name": "CSS selector",
         "scope": ["entity.name.tag.css",
                   "entity.other.attribute-name.class.css",
                   "entity.other.attribute-name.id.css"],
         "settings": {"foreground": ia}},
        {"name": "CSS property",
         "scope": ["support.type.property-name.css"],
         "settings": {"foreground": info}},
        {"name": "CSS value",
         "scope": ["meta.property-value.css",
                   "support.constant.property-value.css"],
         "settings": {"foreground": txt_s}},
        {"name": "CSS color / unit",
         "scope": ["constant.other.color.rgb-value.css",
                   "constant.numeric.css",
                   "keyword.other.unit.css"],
         "settings": {"foreground": warn}},
        {"name": "CSS custom property",
         "scope": ["variable.css", "variable.scss",
                   "variable.other.less"],
         "settings": {"foreground": hi}},
        {"name": "CSS at-rule",
         "scope": ["keyword.control.at-rule"],
         "settings": {"foreground": fin_light}},

        # Markdown
        {"name": "Markdown heading",
         "scope": ["markup.heading",
                   "punctuation.definition.heading.markdown"],
         "settings": {"foreground": ia, "fontStyle": "bold"}},
        {"name": "Markdown bold",
         "scope": ["markup.bold"],
         "settings": {"foreground": txt_p, "fontStyle": "bold"}},
        {"name": "Markdown italic",
         "scope": ["markup.italic"],
         "settings": {"foreground": txt_p, "fontStyle": "italic"}},
        {"name": "Markdown code",
         "scope": ["markup.inline.raw", "markup.fenced_code"],
         "settings": {"foreground": succ}},
        {"name": "Markdown link",
         "scope": ["markup.underline.link",
                   "string.other.link.title.markdown"],
         "settings": {"foreground": info}},
        {"name": "Markdown blockquote",
         "scope": ["markup.quote"],
         "settings": {"foreground": txt_d, "fontStyle": "italic"}},

        # JSON
        {"name": "JSON property key",
         "scope": ["support.type.property-name.json"],
         "settings": {"foreground": info}},

        # Invalid
        {"name": "Invalid",
         "scope": ["invalid"],
         "settings": {"foreground": err}},
        {"name": "Deprecated",
         "scope": ["invalid.deprecated"],
         "settings": {"foreground": warn, "fontStyle": "strikethrough"}},
    ]


def _token_colors_light(p):
    """Syntax token color rules for the light theme."""
    txt_p = p["text_primary"]
    txt_s = p["text_secondary"]
    txt_d = p["text_disabled"]
    ia    = p["interactive"]        # dark shade for light bg
    info  = p["info_dark"]
    succ  = p["success_dark"]
    warn  = p["warning"]
    err   = p["error_dark"]
    hi    = p["highlight_dark"]
    fin   = p["move_finish_dark"]

    return [
        {"name": "Text base",
         "scope": ["source", "text"],
         "settings": {"foreground": txt_p}},
        {"name": "Comment",
         "scope": ["comment", "punctuation.definition.comment"],
         "settings": {"foreground": txt_d, "fontStyle": "italic"}},
        {"name": "Keyword",
         "scope": ["keyword", "keyword.control", "storage",
                   "storage.type", "storage.modifier"],
         "settings": {"foreground": ia}},
        {"name": "Keyword — control flow",
         "scope": ["keyword.control.flow", "keyword.control.return"],
         "settings": {"foreground": ia, "fontStyle": "italic"}},
        {"name": "Keyword — operator",
         "scope": ["keyword.operator"],
         "settings": {"foreground": txt_s}},
        {"name": "String",
         "scope": ["string", "string.quoted", "string.template"],
         "settings": {"foreground": succ}},
        {"name": "String — regexp",
         "scope": ["string.regexp"],
         "settings": {"foreground": succ}},
        {"name": "String — escape",
         "scope": ["constant.character.escape"],
         "settings": {"foreground": info}},
        {"name": "Number",
         "scope": ["constant.numeric"],
         "settings": {"foreground": "#e65100"}},
        {"name": "Boolean / built-in",
         "scope": ["constant.language"],
         "settings": {"foreground": "#e65100", "fontStyle": "italic"}},
        {"name": "Constant — other",
         "scope": ["constant.other", "variable.other.constant"],
         "settings": {"foreground": "#bf360c"}},
        {"name": "Function definition",
         "scope": ["entity.name.function"],
         "settings": {"foreground": info}},
        {"name": "Function call",
         "scope": ["meta.function-call entity.name.function"],
         "settings": {"foreground": info}},
        {"name": "Function parameter",
         "scope": ["variable.parameter"],
         "settings": {"foreground": txt_s, "fontStyle": "italic"}},
        {"name": "Type / class",
         "scope": ["entity.name.type", "entity.name.class",
                   "support.type", "support.class"],
         "settings": {"foreground": p["ia_dark"]}},
        {"name": "Variable",
         "scope": ["variable", "variable.other"],
         "settings": {"foreground": txt_p}},
        {"name": "Variable — language",
         "scope": ["variable.language"],
         "settings": {"foreground": ia, "fontStyle": "italic"}},
        {"name": "Property",
         "scope": ["variable.other.property"],
         "settings": {"foreground": txt_s}},
        {"name": "Object key / attribute",
         "scope": ["meta.object-literal.key",
                   "entity.other.attribute-name"],
         "settings": {"foreground": info}},
        {"name": "Decorator",
         "scope": ["meta.decorator",
                   "entity.name.function.decorator"],
         "settings": {"foreground": fin}},
        {"name": "HTML tag",
         "scope": ["entity.name.tag"],
         "settings": {"foreground": ia}},
        {"name": "HTML attribute",
         "scope": ["entity.other.attribute-name"],
         "settings": {"foreground": info}},
        {"name": "CSS selector",
         "scope": ["entity.name.tag.css",
                   "entity.other.attribute-name.class.css"],
         "settings": {"foreground": ia}},
        {"name": "CSS property",
         "scope": ["support.type.property-name.css"],
         "settings": {"foreground": info}},
        {"name": "Markdown heading",
         "scope": ["markup.heading"],
         "settings": {"foreground": ia, "fontStyle": "bold"}},
        {"name": "Markdown code",
         "scope": ["markup.inline.raw"],
         "settings": {"foreground": succ}},
        {"name": "Markdown link",
         "scope": ["markup.underline.link"],
         "settings": {"foreground": info}},
        {"name": "JSON property key",
         "scope": ["support.type.property-name.json"],
         "settings": {"foreground": info}},
        {"name": "Invalid",
         "scope": ["invalid"],
         "settings": {"foreground": err}},
    ]


def _semantic_dark(p):
    ia        = p["interactive"]
    info      = p["info"]
    succ      = p["success"]
    warn      = p["warning"]
    err       = p["error"]
    hi        = p["highlight"]
    ia_light  = p.get("ia_light",   "#29B6F6")
    info_lt   = p.get("info_light", "#4DD0E1")
    fin_light = p.get("fin_light",  "#CE93D8")
    txt_s     = p["text_secondary"]
    txt_d     = p["text_disabled"]

    return {
        "class":                   ia_light,
        "class.declaration":       {"foreground": ia_light, "bold": True},
        "interface":               ia_light,
        "enum":                    ia_light,
        "enumMember":              hi,
        "struct":                  ia_light,
        "typeParameter":           ia_light,
        "function":                info,
        "function.declaration":    {"foreground": info},
        "method":                  info_lt,
        "method.declaration":      {"foreground": info_lt},
        "property":                txt_s,
        "property.declaration":    {"foreground": txt_s},
        "variable":                p["text_primary"],
        "variable.defaultLibrary": ia,
        "parameter":               {"foreground": txt_s, "italic": True},
        "keyword":                 ia,
        "modifier":                ia,
        "number":                  warn,
        "string":                  succ,
        "regexp":                  p.get("succ_vivid", "#4CAF50"),
        "namespace":               info,
        "decorator":               fin_light,
        "comment":                 {"foreground": txt_d, "italic": True},
        "operator":                txt_s,
        "macro":                   fin_light,
        "type":                    ia_light,
        "selfParameter":           {"foreground": ia, "italic": True},
    }


def _semantic_light(p):
    ia   = p["interactive"]
    info = p["info_dark"]
    succ = p["success_dark"]
    warn = p["warning"]
    err  = p["error_dark"]
    fin  = p["move_finish_dark"]

    return {
        "class":              p["ia_dark"],
        "interface":          p["ia_dark"],
        "enum":               p["ia_dark"],
        "enumMember":         "#bf360c",
        "function":           info,
        "method":             info,
        "property":           p["text_secondary"],
        "variable":           p["text_primary"],
        "variable.defaultLibrary": ia,
        "parameter":          {"foreground": p["text_secondary"], "italic": True},
        "keyword":            ia,
        "number":             "#e65100",
        "string":             succ,
        "namespace":          info,
        "decorator":          fin,
        "comment":            {"foreground": p["text_disabled"], "italic": True},
        "type":               p["ia_dark"],
    }


# ─── Public API ──────────────────────────────────────────────────────────────

def build_dark_palette(
    bg="#121212",
    text_primary="#E0E0E0",
    text_secondary="#B0B0B0",
    text_disabled="#757575",
    border="#3d3d3d",
    border_subtle="#2a2a2a",
    interactive="#03A9F4",
    interactive_hover="#0288d1",
    interactive_active="#0277bd",
    info="#00BCD4",
    success="#8BC34A",
    warning="#FFC107",
    error="#F44336",
    highlight="#FFEB3B",
    move_start="#4CAF50",
    move_hand="#03A9F4",
    move_foot="#FFEB3B",
    move_finish="#9C27B0",
    # Derived dark surface layers (computed by caller if absent)
    layer01="#1e1e1e",
    layer02="#262626",
    layer03="#333333",
    activity_bar_bg="#0d0d0d",
):
    """Assemble the full dark palette dict including derived/computed values."""
    return {
        "bg":              bg,
        "layer01":         layer01,
        "layer02":         layer02,
        "layer03":         layer03,
        "activity_bar_bg": activity_bar_bg,
        "text_primary":    text_primary,
        "text_secondary":  text_secondary,
        "text_disabled":   text_disabled,
        "border":          border,
        "border_subtle":   border_subtle,
        "interactive":     interactive,
        "interactive_hover":   interactive_hover,
        "interactive_active":  interactive_active,
        "info":            info,
        "success":         success,
        "warning":         warning,
        "error":           error,
        "highlight":       highlight,
        "move_start":      move_start,
        "move_hand":       move_hand,
        "move_foot":       move_foot,
        "move_finish":     move_finish,
        # Derived syntax shades (lighter for dark bg context)
        "ia_light":        "#29B6F6",
        "info_light":      "#4DD0E1",
        "succ_vivid":      "#4CAF50",
        "fin_light":       "#CE93D8",
        # Terminal ANSI 0-7 (normal — slightly muted)
        "ansi_black":      bg,
        "ansi_red":        error,
        "ansi_green":      success,
        "ansi_yellow":     warning,
        "ansi_blue":       interactive,
        "ansi_magenta":    move_finish,
        "ansi_cyan":       info,
        "ansi_white":      text_secondary,
        # Terminal ANSI 8-15 (bright — vivid palette values)
        "ansi_bright_black":   layer03,
        "ansi_bright_red":     "#EF5350",
        "ansi_bright_green":   move_start,
        "ansi_bright_yellow":  highlight,
        "ansi_bright_blue":    "#29B6F6",
        "ansi_bright_magenta": "#CE93D8",
        "ansi_bright_cyan":    "#4DD0E1",
        "ansi_bright_white":   text_primary,
    }


def build_light_palette(
    bg="#f4f4f4",
    layer01="#ffffff",
    layer02="#f4f4f4",
    layer03="#e8e8e8",
    text_primary="#161616",
    text_secondary="#525252",
    text_disabled="#8d8d8d",
    border="#c6c6c6",
    border_subtle="#e0e0e0",
    # Light theme uses dark shades of vivid colors for contrast
    interactive="#0288d1",
    interactive_hover="#0277bd",
    interactive_active="#01579b",
    info="#00838f",
    success="#558b2f",
    warning="#e6ac00",
    error="#c62828",
    highlight="#e6ac00",
    move_start="#2e7d32",
    move_hand="#0277bd",
    move_foot="#e6ac00",
    move_finish="#6a1b9a",
    # Full-vivid versions used in bright ANSI slots
    vivid_interactive="#03A9F4",
    vivid_info="#00BCD4",
    vivid_success="#8BC34A",
    vivid_warning="#FFC107",
    vivid_error="#F44336",
    vivid_finish="#9C27B0",
):
    """Assemble the full light palette dict."""
    return {
        "bg":              bg,
        "layer01":         layer01,
        "layer02":         layer02,
        "layer03":         layer03,
        "text_primary":    text_primary,
        "text_secondary":  text_secondary,
        "text_disabled":   text_disabled,
        "border":          border,
        "border_subtle":   border_subtle,
        "interactive":     interactive,
        "interactive_hover":   interactive_hover,
        "interactive_active":  interactive_active,
        # Dark shades for syntax on light bg
        "info_dark":       info,
        "success_dark":    success,
        "warning":         warning,
        "error_dark":      error,
        "highlight_dark":  highlight,
        "ia_dark":         interactive_active,
        "move_finish_dark": move_finish,
        # Terminal ANSI 0-7 (dark/muted for light bg readability)
        "ansi_black":      text_primary,
        "ansi_red":        error,
        "ansi_green":      success,
        "ansi_yellow":     warning,
        "ansi_blue":       interactive,
        "ansi_magenta":    move_finish,
        "ansi_cyan":       info,
        "ansi_white":      text_secondary,
        # Terminal ANSI 8-15 (vivid — full palette values)
        "ansi_bright_black":   text_disabled,
        "ansi_bright_red":     vivid_error,
        "ansi_bright_green":   vivid_success,
        "ansi_bright_yellow":  vivid_warning,
        "ansi_bright_blue":    vivid_interactive,
        "ansi_bright_magenta": vivid_finish,
        "ansi_bright_cyan":    vivid_info,
        "ansi_bright_white":   "#ffffff",
    }


def create_vscode_dark_theme(palette=None, **palette_kwargs):
    """
    Return a VS Code dark color theme JSON string.

    Usage:
        p = build_dark_palette(bg="#121212", ...)
        json_str = create_vscode_dark_theme(palette=p)

    Or pass keyword args directly:
        json_str = create_vscode_dark_theme(bg="#121212", interactive="#03A9F4")
    """
    if palette is None:
        palette = build_dark_palette(**palette_kwargs)

    theme = {
        "name": "Monad Dark",
        "type": "dark",
        "$schema": "vscode://schemas/color-theme",
        "colors": _workbench_dark(palette),
        "tokenColors": _token_colors_dark(palette),
        "semanticHighlighting": True,
        "semanticTokenColors": _semantic_dark(palette),
    }
    return json.dumps(theme, indent=2)


def create_vscode_light_theme(palette=None, **palette_kwargs):
    """
    Return a VS Code light color theme JSON string.
    """
    if palette is None:
        palette = build_light_palette(**palette_kwargs)

    theme = {
        "name": "Monad Light",
        "type": "light",
        "$schema": "vscode://schemas/color-theme",
        "colors": _workbench_light(palette),
        "tokenColors": _token_colors_light(palette),
        "semanticHighlighting": True,
        "semanticTokenColors": _semantic_light(palette),
    }
    return json.dumps(theme, indent=2)


def create_vscode_package_json(
    version="1.0.0",
    publisher="monad-system",
    repository_url="",
):
    """
    Return the VS Code extension manifest (package.json) string.

    Includes all fields required for VS Code Marketplace publication:
    galleryBanner, icon reference, license, repository, etc.

    Args:
        version:        semver string, e.g. "1.0.0"
        publisher:      your marketplace publisher ID (create at
                        https://marketplace.visualstudio.com/manage)
        repository_url: optional GitHub URL for the repo
    """
    manifest = {
        "name": "monad-system-theme",
        "displayName": "Monad System",
        "description": (
            "Dark and light color themes derived from the Monad System design "
            "language. Engineered precision — every color earns its place."
        ),
        "version": version,
        "publisher": publisher,
        "license": "MIT",
        "icon": "icon.png",
        "engines": {"vscode": "^1.60.0"},
        "categories": ["Themes"],
        "keywords": [
            "theme", "dark", "light", "minimal", "monad",
            "design system", "flat", "high contrast",
        ],
        "galleryBanner": {
            "color": "#121212",
            "theme": "dark",
        },
        "contributes": {
            "themes": [
                {
                    "label": "Monad Dark",
                    "uiTheme": "vs-dark",
                    "path": "./monad-dark-color-theme.json",
                },
                {
                    "label": "Monad Light",
                    "uiTheme": "vs",
                    "path": "./monad-light-color-theme.json",
                },
            ]
        },
    }

    if repository_url:
        manifest["repository"] = {
            "type": "git",
            "url": repository_url,
        }
        manifest["bugs"] = {"url": repository_url.rstrip("/") + "/issues"}
        manifest["homepage"] = repository_url
    else:
        # Provide a placeholder so vsce doesn't warn about missing repository.
        # Replace with real URL before publishing.
        manifest["repository"] = {
            "type": "git",
            "url": "https://github.com/monad-system/monad-system-theme",
        }

    # Explicit file list — prevents vsce from bundling unintended files
    # and suppresses the .vscodeignore warning.
    manifest["files"] = [
        "monad-dark-color-theme.json",
        "monad-light-color-theme.json",
        "package.json",
        "README.md",
        "LICENSE",
        "icon.png",
    ]

    return json.dumps(manifest, indent=2)


def create_vscode_readme(dark_palette, light_palette):
    """
    Return a Marketplace-ready README.md string for the extension.

    Includes color swatches rendered as inline SVG badges so the
    marketplace page shows the actual palette at a glance.
    """
    dp = dark_palette
    lp = light_palette

    def swatch(hex_color, label):
        """Return a small inline HTML color swatch."""
        safe = hex_color.lstrip("#")
        return (
            f'<img src="https://placehold.co/14x14/{safe}/{safe}.png" '
            f'width="14" height="14" alt="{label}" title="{label} {hex_color}"> '
            f'`{hex_color}`'
        )

    return f"""\
# Monad System

> **Form follows Function.** Every color earns its place.

A dark and light theme pair derived from the **Monad System** — a precision
design language built on a single `colors.json` source of truth. Every color
in this theme is generated programmatically; nothing is hand-tweaked.

---

## Variants

| Theme | Type | Background | Foreground |
|---|---|---|---|
| **Monad Dark** | Dark | {swatch(dp['bg'], 'Background')} | {swatch(dp['text_primary'], 'Text')} |
| **Monad Light** | Light | {swatch(lp['bg'], 'Background')} | {swatch(lp['text_primary'], 'Text')} |

---

## Dark Palette

| Role | Color |
|---|---|
| Background | {swatch(dp['bg'], 'bg')} |
| Layer 01 | {swatch(dp['layer01'], 'layer01')} |
| Layer 02 | {swatch(dp['layer02'], 'layer02')} |
| Layer 03 | {swatch(dp['layer03'], 'layer03')} |
| Primary Text | {swatch(dp['text_primary'], 'text_primary')} |
| Secondary Text | {swatch(dp['text_secondary'], 'text_secondary')} |
| Disabled Text | {swatch(dp['text_disabled'], 'text_disabled')} |
| Interactive (blue) | {swatch(dp['interactive'], 'interactive')} |
| Info (cyan) | {swatch(dp['info'], 'info')} |
| Success (green) | {swatch(dp['success'], 'success')} |
| Warning (amber) | {swatch(dp['warning'], 'warning')} |
| Error (red) | {swatch(dp['error'], 'error')} |
| Highlight (yellow) | {swatch(dp['highlight'], 'highlight')} |

### Domain Colors (Movement)

| Role | Color |
|---|---|
| Start | {swatch(dp['move_start'], 'start')} |
| Hand | {swatch(dp['move_hand'], 'hand')} |
| Foot | {swatch(dp['move_foot'], 'foot')} |
| Finish | {swatch(dp['move_finish'], 'finish')} |

---

## Design Principles

- **No border-radius** — orthogonal, structural, undecorated
- **No box-shadow depth** — layering via 1px borders and background steps
- **No gradients** — flat fills only; color is information, not texture
- **Haptic transitions** — 80ms linear; motion is predictable, not expressive
- **Mono for data** — numeric values, labels, and overlines use JetBrains Mono

---

## Installation

Search **"Monad System"** in the VS Code Extension Marketplace, or install via CLI:

```bash
code --install-extension monad-system.monad-system-theme
```

Then open the theme picker:

```
Cmd+K  Cmd+T  →  Monad Dark  /  Monad Light
```

---

## Source

This theme is **generated** from `colors.json` — the single source of truth
for the entire Monad System (CSS, C#, Python/seaborn, Ghostty, and VS Code).

To regenerate after editing colors:

```bash
make install
```
"""


def create_vscode_license():
    """Return an MIT LICENSE file string."""
    return """\
MIT License

Copyright (c) 2026 Monad System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
