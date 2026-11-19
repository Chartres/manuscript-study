#!/bin/sh
# Link the skill into Claude Code's skills directory.
set -e
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$HOME/.claude/skills"
ln -sfn "$here/skill/manuscript-study" "$HOME/.claude/skills/manuscript-study"
echo "skill linked: ~/.claude/skills/manuscript-study (tools: $here/tools)"
