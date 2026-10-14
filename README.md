# zellij-config

My zellij config: the `pills` layout plus the [zjstatus](https://github.com/dj95/zjstatus) status bar, with a Dracula-based theme (`themes/dracula-pills.kdl`).

## Install (WSL / Linux / macOS)

Clone straight into place:

```sh
git clone git@github.com:bm611/zellij-config.git ~/.config/zellij
python3 ~/.config/zellij/scripts/sync-zjstatus.py
```

Or clone anywhere and run `./install.sh`, which backs up any existing `~/.config/zellij` and copies the config there.

Either way, `sync-zjstatus.py` regenerates the status bar block in the layouts so its paths point at your `$HOME`.

## Editing the status bar

The zjstatus settings (colors, mode key hints, widgets) live in `scripts/sync-zjstatus.py`, not in the layouts. Edit it, then run:

```sh
python3 ~/.config/zellij/scripts/sync-zjstatus.py
```

It rewrites the zjstatus block in `layouts/pills.kdl`, `layouts/pills.swap.kdl` and `layouts/dev.kdl`.

Needs a Nerd Font for the pill edges and icons.
