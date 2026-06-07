# Private GitHub Setup

Use this while the app is still being built. The goal is: private code, no committed secrets, tests running on every push, and no public deployment until the app is ready.

## Recommended repository settings

- Repository name: `ai-code-tutor`
- Visibility: **Private**
- Default branch: `main`
- Do not add API keys to any file in the repo.
- Keep `.env`, `.streamlit/secrets.toml`, and `data/progress_*.json` out of git.

The included `.gitignore` already excludes local secrets and learner progress files.

## Create the private repo from GitHub's website

1. On GitHub, choose **New repository**.
2. Name it `ai-code-tutor`.
3. Choose **Private** visibility.
4. Do not initialize it with a README, license, or gitignore because this folder already has project files.
5. Create the repository.

Then, from this app folder:

```bash
git init
git add .
git commit -m "Initial private AI Code Tutor app"
git branch -M main
git remote add origin git@github.com:YOUR-USERNAME/ai-code-tutor.git
git push -u origin main
```

If you use HTTPS instead of SSH, GitHub will show you the HTTPS remote URL on the new repository page.

## Create the private repo with GitHub CLI

If you have `gh` installed and authenticated:

```bash
gh repo create ai-code-tutor --private --source=. --remote=origin --push
```

## Confirm it stayed private

After pushing, open the repository page and confirm it says **Private** near the repository name.

## Optional: keep deployment private too

You can keep the GitHub repository private while still deploying to a private host later. Before any public deployment, finish these upgrades:

- Add real user authentication.
- Replace JSON progress files with a database.
- Keep `ALLOW_CODE_RUNNER=false` unless you add a real sandbox.
- Add production error logging.
- Test AI Tutor with a real API key stored only as a platform secret.
