#!/bin/sh
cwd_path=$PWD
case "$cwd_path" in
  "$HOME") cwd_path="~" ;;
  "$HOME"/*) cwd_path="~${cwd_path#"$HOME"}" ;;
esac
printf '%s' "$cwd_path"
