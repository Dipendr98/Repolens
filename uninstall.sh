#!/usr/bin/env bash
# uninstall.sh — Remove GitHub Analyser skill from Claude Code
set -e

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
AGENTS_DIR="${CLAUDE_AGENTS_DIR:-$HOME/.claude/agents}"

echo ""
echo "🗑️  Uninstalling GitHub Analyser..."

rm -rf "$SKILLS_DIR/github"
rm -rf "$SKILLS_DIR/gh-overview"
rm -rf "$SKILLS_DIR/gh-activity"
rm -rf "$SKILLS_DIR/gh-contributors"
rm -rf "$SKILLS_DIR/gh-code-quality"
rm -rf "$SKILLS_DIR/gh-security"
rm -rf "$SKILLS_DIR/gh-compare"
rm -rf "$SKILLS_DIR/gh-report"
rm -rf "$SKILLS_DIR/gh-report-pdf"
rm -f  "$AGENTS_DIR/gh-"*.md
rm -rf "$HOME/.claude/scripts/github-analyser"
rm -rf "$HOME/.claude/templates/github-analyser"

echo "✅ GitHub Analyser uninstalled."
echo ""
