#!/usr/bin/env bash
# install.sh — GitHub Analyser skill installer for Claude Code
set -e

SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
AGENTS_DIR="${CLAUDE_AGENTS_DIR:-$HOME/.claude/agents}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "🔧 Installing GitHub Analyser Skill Suite..."
echo ""

# Create directories
mkdir -p "$SKILLS_DIR"
mkdir -p "$AGENTS_DIR"

# Install main orchestrator
mkdir -p "$SKILLS_DIR/github"
cp "$SCRIPT_DIR/SKILL.md" "$SKILLS_DIR/github/SKILL.md"
echo "  ✅ Installed: github/SKILL.md (main orchestrator)"

# Install sub-skills
for skill_dir in "$SCRIPT_DIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$SKILLS_DIR/$skill_name"
    cp "$skill_dir/SKILL.md" "$SKILLS_DIR/$skill_name/SKILL.md"
    echo "  ✅ Installed: $skill_name/SKILL.md"
done

# Install agents
for agent_file in "$SCRIPT_DIR/agents"/*.md; do
    agent_name=$(basename "$agent_file")
    cp "$agent_file" "$AGENTS_DIR/$agent_name"
    echo "  ✅ Installed agent: $agent_name"
done

# Install scripts to ~/.claude/scripts/github-analyser/
SCRIPTS_DEST="$HOME/.claude/scripts/github-analyser"
mkdir -p "$SCRIPTS_DEST"
cp "$SCRIPT_DIR/scripts/"*.py "$SCRIPTS_DEST/"
echo "  ✅ Installed scripts to $SCRIPTS_DEST/"

# Install templates
TEMPLATES_DEST="$HOME/.claude/templates/github-analyser"
mkdir -p "$TEMPLATES_DEST"
cp "$SCRIPT_DIR/templates/"*.md "$TEMPLATES_DEST/" 2>/dev/null || true

echo ""
echo "📦 Installing Python dependencies..."
pip install requests matplotlib numpy reportlab --break-system-packages -q 2>/dev/null || \
pip install requests matplotlib numpy reportlab -q 2>/dev/null || \
echo "  ⚠️  Could not auto-install Python packages. Run manually:"
echo "     pip install requests matplotlib numpy reportlab"

echo ""
echo "✅ GitHub Analyser installed successfully!"
echo ""
echo "Usage in Claude Code:"
echo "  /github analyse https://github.com/owner/repo"
echo "  /github activity https://github.com/owner/repo"
echo "  /github contributors https://github.com/owner/repo"
echo "  /github security https://github.com/owner/repo"
echo "  /github compare <url1> <url2>"
echo "  /github report-pdf https://github.com/owner/repo"
echo ""
echo "Tip: Set GITHUB_TOKEN env var for higher API rate limits:"
echo "  export GITHUB_TOKEN=ghp_yourtoken"
echo ""
