#!/bin/sh
# Installs this zellij config into ~/.config/zellij, rewriting __HOME__ to $HOME.
set -e
src=$(cd "$(dirname "$0")" && pwd)
dest="$HOME/.config/zellij"
if [ -e "$dest" ] && [ ! -L "$dest" ]; then
  backup="$dest.backup-$(date +%Y%m%d-%H%M%S)"
  mv "$dest" "$backup"
  echo "Backed up existing config to $backup"
fi
mkdir -p "$dest/layouts" "$dest/plugins" "$dest/scripts"
cp "$src/config.kdl" "$dest/"
cp "$src/plugins/zjstatus.wasm" "$dest/plugins/"
cp "$src/scripts/status-cwd.sh" "$dest/scripts/"
chmod +x "$dest/scripts/status-cwd.sh"
for f in "$src"/layouts/*.kdl; do
  sed "s#__HOME__#$HOME#g" "$f" > "$dest/layouts/$(basename "$f")"
done
echo "Installed zellij config to $dest"
