#!/usr/bin/env python3
"""Writes the zjstatus plugin block into every layout that uses zjstatus.

Edit COLORS / HINTS / build_block() here, then run:
    python3 ~/.config/zellij/scripts/sync-zjstatus.py
Layouts are rewritten in place; only the `plugin location=".../zjstatus.wasm" { ... }`
block is replaced, so tab/pane definitions are left alone.
"""

import os
import re

ROOT = os.path.expanduser("~/.config/zellij")
LAYOUTS = ["layouts/pills.kdl", "layouts/pills.swap.kdl", "layouts/dev.kdl"]
WASM = f"file:{ROOT}/plugins/zjstatus.wasm"

# Dracula palette (https://draculatheme.com/contribute).
C = {
    "bg": "#282a36",
    "line": "#44475a",
    "fg": "#f8f8f2",
    "comment": "#6272a4",
    "cyan": "#8be9fd",
    "green": "#50fa7b",
    "orange": "#ffb86c",
    "pink": "#ff79c6",
    "purple": "#bd93f9",
    "red": "#ff5555",
    "yellow": "#f1fa8c",
}

# mode name -> (label, pill color, [(keys, description), ...]); keep in sync with config.kdl.
MODES = {
    "locked": ("LOCKED", "red", [("ctrl g", "unlock")]),
    "pane": ("PANE", "cyan", [
        ("hjkl", "focus"), ("n", "new"), ("d/r", "split ↓/→"), ("s", "stack"),
        ("x", "close"), ("f", "full"), ("e", "float"), ("w", "floats"), ("c", "rename"),
    ]),
    "tab": ("TAB", "cyan", [
        ("hjkl/1-9", "go"), ("n", "new"), ("x", "close"), ("r", "rename"),
        ("b/[/]", "break pane"), ("s", "sync"), ("tab", "last"),
    ]),
    "resize": ("RESIZE", "orange", [("hjkl", "grow"), ("HJKL", "shrink"), ("+/-", "size")]),
    "move": ("MOVE", "orange", [("hjkl", "move"), ("n/p", "cycle")]),
    "scroll": ("SCROLL", "yellow", [
        ("j/k", "line"), ("d/u", "half page"), ("[/]", "prompt"), ("s", "search"),
        ("e", "edit"), ("c", "copy output"),
    ]),
    "search": ("SEARCH", "yellow", [
        ("n/p", "next/prev"), ("c", "case"), ("w", "wrap"), ("o", "whole word"),
    ]),
    "enter_search": ("SEARCH", "yellow", [("enter", "search"), ("esc", "cancel")]),
    "session": ("SESSION", "cyan", [
        ("w", "sessions"), ("l", "layouts"), ("c", "config"), ("p", "plugins"),
        ("s", "share"), ("d", "detach"),
    ]),
    "rename_tab": ("RENAME", "pink", [("enter", "save"), ("esc", "cancel")]),
    "rename_pane": ("RENAME", "pink", [("enter", "save"), ("esc", "cancel")]),
    "tmux": ("TMUX", "cyan", [
        ('"/%', "split"), ("c", "tab"), ("n/p", "tab"), ("z", "full"),
        ("space", "swap layout"), ("[", "scroll"), ("d", "detach"),
    ]),
}


def mode_format(label, color, hints):
    pill = f"#[bg={C[color]},fg={C['bg']},bold] {label} "
    parts = [f"#[bg=default,fg={C['fg']},bold]{k}#[fg={C['comment']},nobold] {d}" for k, d in hints]
    sep = f"#[fg={C['line']}] · "
    return pill + "#[bg=default] " + sep.join(parts)


def build_block(indent):
    pad = " " * (indent + 4)
    opts = [
        ("format_left", f"#[fg={C['comment']},bg=default] {{session}}  {{tabs}}"),
        ("format_center", "{mode}"),
        ("format_right", "{notifications}{swap_layout}{command_git_branch}{command_cwd}{datetime}"),
        ("format_space", "#[bg=default]"),
        # Mode hints are the first thing dropped when the window is too narrow.
        ("format_hide_on_overlength", "true"),
        ("format_precedence", "lrc"),

        ("border_enabled", "false"),
        # Must stay false: when true, zjstatus turns frames back on as soon as a tab has 2+ panes.
        ("hide_frame_for_single_pane", "false"),

        ("tab_normal", f"#[fg={C['line']},bg=default]#[fg={C['fg']},bg={C['line']}] {{index}} {{name}}{{fullscreen_indicator}}{{sync_indicator}}{{floating_indicator}} #[fg={C['line']},bg=default]"),
        ("tab_active", f"#[fg={C['purple']},bg=default]#[fg={C['bg']},bg={C['purple']},bold] {{index}} {{name}}{{fullscreen_indicator}}{{sync_indicator}}{{floating_indicator}} #[fg={C['purple']},bg=default]"),
        ("tab_separator", "#[bg=default] "),
        ("tab_fullscreen_indicator", " 󰊓"),
        ("tab_sync_indicator", " ↔"),
        ("tab_floating_indicator", " 󰉈"),

        ("command_cwd_command", f"/bin/sh {ROOT}/scripts/status-cwd.sh"),
        ("command_cwd_format", f"#[fg={C['cyan']},bg=default] {{stdout}}"),
        ("command_cwd_interval", "1"),
        ("command_cwd_rendermode", "static"),
        ("command_cwd_cwd", "{focused_pane_cwd}"),

        ("command_git_branch_command", f"/bin/sh {ROOT}/scripts/status-git.sh"),
        ("command_git_branch_format", f"#[fg={C['purple']},bg=default] {{stdout}}"),
        ("command_git_branch_interval", "2"),
        ("command_git_branch_rendermode", "static"),
        ("command_git_branch_cwd", "{focused_pane_cwd}"),

        ("swap_layout_format", f"#[fg={C['comment']},bg=default] 󰕰 {{name}}"),
        ("swap_layout_hide_if_empty", "true"),

        ("datetime", f"#[fg={C['comment']},bg=default] {{format}} "),
        ("datetime_format", "%H:%M"),
        ("datetime_timezone", "Europe/Amsterdam"),

        # zellij pipe "zjstatus::notify::build done"
        ("notification_format_unread", f"#[fg={C['bg']},bg={C['yellow']},bold] 󰂞 {{message}} #[bg=default] "),
        ("notification_format_no_notifications", ""),
        ("notification_show_interval", "10"),

        ("mode_normal", ""),
    ]
    for name, (label, color, hints) in MODES.items():
        opts.append((f"mode_{name}", mode_format(label, color, hints)))

    lines = [" " * indent + f'plugin location="{WASM}" {{']
    for k, v in opts:
        v = v.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'{pad}{k} "{v}"')
    lines.append(" " * indent + "}")
    return "\n".join(lines)


def replace_block(text):
    m = re.search(r'^([ \t]*)plugin location="[^"]*zjstatus\.wasm"\s*\{', text, re.M)
    if not m:
        raise SystemExit("no zjstatus block found")
    depth, i = 0, m.end() - 1
    in_str = False
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 1
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    return text[: m.start()] + build_block(len(m.group(1))) + text[i + 1 :]


if __name__ == "__main__":
    for rel in LAYOUTS:
        path = os.path.join(ROOT, rel)
        with open(path) as f:
            text = f.read()
        with open(path, "w") as f:
            f.write(replace_block(text))
        print(f"updated {rel}")
