#!/bin/sh
# Prints the git branch of the focused pane's cwd (zjstatus runs this with
# command_git_branch_cwd "{focused_pane_cwd}"). Prints nothing outside a repo.
branch=$(git symbolic-ref --short -q HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null) || exit 0
[ -n "$branch" ] && printf ' %s' "$branch"
