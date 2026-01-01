# 🔐 API Key Security Checklist

This checklist ensures that API keys are never exposed in your repository.

## ✅ Pre-Commit Checklist

Before committing any code, verify:

- [ ] `.env` file is NOT in the staging area (`git status` should not show `.env`)
- [ ] No hardcoded API keys in any Python files (search for `AIza`, `sk-`, `gsk_`)
- [ ] All API keys are loaded from environment variables using `os.getenv()` or `os.environ.get()`
- [ ] `.env.template` or `.env.example` only contain placeholder values
- [ ] `.gitignore` includes `.env` and related patterns
- [ ] No API keys in configuration files (YAML, JSON, etc.)
- [ ] No API keys in comments or documentation

## 🔍 How to Check for Exposed API Keys

### Check Git Status
```bash
git status --ignored
```
✅ Should show `.env` as ignored

### Search for Potential API Keys in Staged Files
```bash
# Search for common API key patterns (broad match for various key types)
git diff --cached | grep -E "AIza|sk-|gsk_|ghp_|glpat"

# Search for hardcoded assignments with minimum length
git diff --cached | grep -E "api_key\s*=\s*['\"][^'\"]{15,}['\"]"
```
✅ Should return no results

### Verify .env is in .gitignore
```bash
git check-ignore .env
```
✅ Should output: `.env`

### Check for API Keys in Commit History
```bash
# Check if .env was ever committed
git log --all --full-history -- .env
```
✅ Should return no results

## 🛡️ Security Best Practices

### 1. Environment Variables Only
```python
# ✅ CORRECT
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('USDA_API_KEY')

# ❌ WRONG
api_key = "AIzaSyXXXXXXXXXXXXXXXX"
```

### 2. Use Helper Functions
```python
# ✅ CORRECT - Use provided helper functions
from usda_api import get_usda_api
api = get_usda_api()  # Reads from environment automatically

# ❌ WRONG - Hardcoding in initialization
from usda_api import USDAFoodAPI
api = USDAFoodAPI("AIzaSyXXXXXXXX")
```

### 3. Template Files Only
- ✅ Commit: `.env.template`, `.env.example`
- ❌ Never commit: `.env`, `.env.local`, `.env.production`

### 4. Deployment Platforms
- Use platform's environment variable settings:
  - **Railway**: Environment Variables in Settings
  - **Render**: Environment tab in dashboard
  - **Heroku**: Config Vars in Settings
- Never hardcode API keys in `render.yaml`, `railway.json`, etc.

### 5. Pre-commit Hook (Recommended)
Install the pre-commit hook to automatically check for API keys:

```bash
# Copy the pre-commit hook
cp pre-commit-hook.sh .git/hooks/pre-commit

# Make it executable (Unix/Mac/Linux)
chmod +x .git/hooks/pre-commit

# On Windows with Git Bash
git update-index --chmod=+x .git/hooks/pre-commit
```

The hook will automatically run before each commit and prevent you from committing:
- The `.env` file
- Files with API key patterns
- Secret files
- Hardcoded API keys in Python files

## 🚨 If API Keys Were Exposed

If you accidentally committed API keys:

### 1. Remove from Git History
```bash
# Remove file from Git but keep locally
git rm --cached .env
git commit -m "Remove .env from repository"
git push
```

### 2. Rotate ALL API Keys Immediately

- **USDA API**: Get new key at https://fdc.nal.usda.gov/api-key-signup.html
- **Gemini API**: Revoke and create new at https://aistudio.google.com/app/apikey
- **Data.gov.in API**: Request new key at https://data.gov.in/
- **GROQ API**: Revoke and create new at https://console.groq.com/

### 3. Update .env with New Keys
```bash
# Update your local .env file with new keys
# DO NOT commit this file
```

### 4. Consider BFG Repo-Cleaner for History Cleanup
If keys are in commit history:
```bash
# Install BFG Repo-Cleaner
# Download from: https://rtyley.github.io/bfg-repo-cleaner/

# Remove all .env files from history
bfg --delete-files .env

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (WARNING: This rewrites history)
git push --force
```

## 📋 Files to Review

### Always Check These Files Before Committing:
- [ ] `usda_api.py` - No hardcoded API keys in examples
- [ ] `gemini_chatbot.py` - Using environment variables
- [ ] `ai_chatbot.py` - Using environment variables
- [ ] `mandi_price_api.py` - Using environment variables
- [ ] `db_config.py` - Using environment variables for DB credentials
- [ ] Any new Python files that use external APIs

### Configuration Files:
- [ ] `render.yaml` - Only has `sync: false` for API keys
- [ ] `.gitignore` - Includes all sensitive file patterns
- [ ] `.env.template` - Only placeholder values
- [ ] `.env.example` - Only placeholder values

## 🎯 Quick Security Audit

Run this command before every push:

```bash
# Search all tracked files for potential API keys (broad patterns)
git grep -E "AIza|sk-[A-Za-z0-9_-]{20,}|gsk_|ghp_|glpat|api_key\s*=\s*['\"][^'\"]{15,}['\"]" -- "*.py" "*.js" "*.json" "*.yaml"
```

✅ Should return no results (or only comments/placeholders)

## 📚 Additional Resources

- [SECURITY.md](SECURITY.md) - Comprehensive security guidelines
- [USDA_API_SETUP.md](USDA_API_SETUP.md) - How to set up USDA API key
- [.env.template](.env.template) - Template for environment variables

## ✅ Current Security Status

Your repository is secure when:
- ✅ `.env` is in `.gitignore`
- ✅ No `.env` file in Git history
- ✅ All API keys loaded from environment variables
- ✅ Template files contain only placeholders
- ✅ No hardcoded keys in any code files
- ✅ Deployment configs use platform environment variables

**Last Updated**: 2026-01-01
