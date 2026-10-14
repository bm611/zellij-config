#!/bin/sh
# Installs this zellij config into ~/.config/zellij and regenerates the zjstatus bar
# in the layouts so its plugin/script paths point at your $HOME.
# Not needed if you cloned straight into ~/.config/zellij; then just run
# scripts/sync-zjstatus.py.
set -e
src=$(cd "$(dirname "$0")" && pwd)
dest="$HOME/.config/zellij"
if [ "$src" != "$dest" ]; then
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    backup="$dest.backup-$(date +%Y%m%d-%H%M%S)"
    mv "$dest" "$backup"
    echo "Backed up existing config to $backup"
  fi
  mkdir -p "$dest/layouts" "$dest/plugins" "$dest/scripts" "$dest/themes"
  cp "$src/config.kdl" "$dest/"
  cp "$src/plugins/zjstatus.wasm" "$dest/plugins/"
  cp "$src"/scripts/* "$dest/scripts/"
  cp "$src"/themes/*.kdl "$dest/themes/"
  cp "$src"/layouts/*.kdl "$dest/layouts/"
fi
chmod +x "$dest"/scripts/*.sh "$dest"/scripts/*.py
python3 "$dest/scripts/sync-zjstatus.py"
echo "Installed zellij config to $dest"
