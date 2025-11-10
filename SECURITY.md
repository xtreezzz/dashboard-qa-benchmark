# 🔒 Security Guidelines

## API Key Protection

**IMPORTANT:** Never commit your OpenAI API key to version control!

### ✅ Safe Practices

1. **Use .env file** (already in .gitignore):
   ```bash
   echo "OPENAI_API_KEY=your-key-here" > .env
   echo "BENCHMARK_MODEL=gpt-5-mini" >> .env
   echo "EVAL_MODEL=gpt-5-nano" >> .env
   ```

2. **Use environment variables**:
   ```bash
   export OPENAI_API_KEY='your-key-here'
   ```

3. **Pass via command line** (for testing only):
   ```bash
   python main.py --dataset iris --api-key your-key-here
   ```

### ❌ Never Do This

- ❌ Don't hardcode keys in Python files
- ❌ Don't commit .env to git
- ❌ Don't share .env file
- ❌ Don't include keys in documentation
- ❌ Don't push keys to GitHub/GitLab

### 🛡️ What's Protected

The following files are automatically ignored by git:

- `.env` - Your API keys (CRITICAL)
- `*.log` - May contain API responses
- `__pycache__/` - Python cache
- `.venv/` - Virtual environment
- `.idea/` - IDE configs

### ✅ Verification

Check if .env is ignored:
```bash
git status | grep .env
# Should show nothing or only .env.example
```

### 🔍 If You Accidentally Committed Keys

1. **Revoke the key immediately** at https://platform.openai.com/api-keys
2. Generate a new key
3. Remove from git history:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```
4. Force push (if already pushed):
   ```bash
   git push origin --force --all
   ```

### 📋 Checklist Before Pushing

- [ ] .env is in .gitignore
- [ ] No API keys in code
- [ ] No API keys in logs
- [ ] No API keys in documentation (use placeholders like `your-key-here`)
- [ ] Run: `git status` to verify .env is not tracked
