#!/bin/bash
# Pre-commit hook to prevent API keys from being committed
# Copy this file to .git/hooks/pre-commit and make it executable:
#   cp pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit

# Configuration: API key patterns to detect
# Update these patterns as API key formats change
GOOGLE_API_PATTERN="AIza[A-Za-z0-9_-]{35}"
OPENAI_API_PATTERN="sk-[A-Za-z0-9_-]{20,}"
GROQ_API_PATTERN="gsk_[A-Za-z0-9_-]{32,}"
GITHUB_TOKEN_PATTERN="ghp_[A-Za-z0-9]{36}"
GITLAB_TOKEN_PATTERN="glpat-[A-Za-z0-9_-]{20}"

# Combined pattern for grep
ALL_PATTERNS="${GOOGLE_API_PATTERN}|${OPENAI_API_PATTERN}|${GROQ_API_PATTERN}|${GITHUB_TOKEN_PATTERN}|${GITLAB_TOKEN_PATTERN}"

# Minimum length for API key values to check (reduces false positives)
MIN_KEY_LENGTH=15

echo "🔍 Running API key security check..."

# Check if .env file is being committed
if git diff --cached --name-only | grep -q "^\.env$"; then
    echo "❌ ERROR: Attempting to commit .env file!"
    echo "   .env should never be committed to Git."
    echo "   Run: git reset HEAD .env"
    exit 1
fi

# Check for common API key patterns in staged files
if git diff --cached | grep -qE "${ALL_PATTERNS}"; then
    echo "❌ ERROR: Potential API key detected in staged changes!"
    echo "   Found pattern matching: Google API, OpenAI, GROQ, GitHub, or GitLab token"
    echo ""
    echo "   Please review your changes and remove any API keys."
    echo "   API keys should be in .env file (which is gitignored)."
    echo ""
    echo "   To see what was detected, run:"
    echo "   git diff --cached | grep -E 'AIza|sk-|gsk_|ghp_|glpat'"
    exit 1
fi

# Check for hardcoded api_key assignments in Python files with reasonable length keys
if git diff --cached -- "*.py" | grep -qE "api_key\s*=\s*['\"][^'\"]{${MIN_KEY_LENGTH},}['\"]"; then
    echo "⚠️  WARNING: Potential hardcoded API key assignment detected!"
    echo "   Found pattern: api_key = \"...\" with what looks like a real key (${MIN_KEY_LENGTH}+ characters)"
    echo ""
    echo "   Please verify this is not a real API key."
    echo "   Use environment variables instead: api_key = os.getenv('API_KEY')"
    echo ""
    read -p "   Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for common secret file names
if git diff --cached --name-only | grep -qE "(secrets\.(txt|json|yaml)|API_KEYS\.txt|.*\.keys$|.*credential.*)"; then
    echo "❌ ERROR: Attempting to commit a file that may contain secrets!"
    echo "   Files matching secret patterns should not be committed."
    echo ""
    git diff --cached --name-only | grep -E "(secrets\.(txt|json|yaml)|API_KEYS\.txt|.*\.keys$|.*credential.*)"
    echo ""
    echo "   Add these files to .gitignore if they should be excluded."
    exit 1
fi

echo "✅ API key security check passed!"
exit 0
