# Bug Fixes and Improvements QA Pass

Date: 2026-05-28

## Bugs fixed

1. **AI Certs tab runtime bug**
   - Problem: `app.py` called `provider_counts()` but did not import it from `official_ai_resources.py`.
   - Impact: opening or using the AI Certs tab could raise a `NameError` in a real Streamlit session.
   - Fix: imported `provider_counts` and added a static regression test so this specific issue is caught in future changes.

2. **Credential-only filter was too broad**
   - Problem: resources with text like `No certificate listed` still matched the word `certificate`.
   - Impact: the AI Certs credential filter could show non-credential resources.
   - Fix: moved certificate detection into a shared `resource_has_certificate()` helper that excludes negative phrases such as `No certificate`, `No certification`, and `not listed`.

3. **Duplicate import cleanup**
   - Problem: `record_official_ai_resource` was imported twice in `app.py`.
   - Impact: not a crash, but a maintenance smell.
   - Fix: removed the duplicate import and added an AST-based test that checks for duplicate imports from app dependencies.

4. **Outdated or redirecting resource URLs**
   - Problem: a couple of official resource URLs either redirected or were less stable than a deeper official page.
   - Fixes:
     - OpenAI prompting link now uses the current `developers.openai.com` docs URL.
     - Hugging Face Agents Course link now points to the course introduction page.
     - Gumloop AI Fundamentals time commitment now matches the current University hub wording.

## UX/UI improvements

1. Added a **Recommended next AI step** card in the AI Certs tab.
2. Centralized the starter path as `OFFICIAL_AI_STARTER_PATH` so the app and tests stay aligned.
3. Added `next_recommended_resource()` so the app can guide a new learner from Gumloop basics into Claude/Anthropic, OpenAI prompting, and later credential targets.
4. Kept the AI Certs tab focused on official links and private tracking rather than copying course content.

## New tests added

- Static app dependency check for missing imports.
- Duplicate import check for app dependency imports.
- Credential filter test that confirms `No certificate listed` does not count as a certificate option.
- Starter path test focused on Gumloop and Anthropic/Claude.
- Next-recommended-resource test that confirms the learner advances after completing the starter path.

## Current test status

```text
python -m pytest -q
28 passed in 2.14s
```

```text
python -m compileall -q .
completed successfully
```

## Fresh new-user QA result

```text
initial completion: 0.0
initial lessons remaining: 12
initial recommended ai: gumloop_ai_fundamentals
completion after one lesson: 0.083
lessons remaining after one lesson: 11
quiz percent: 100.0
code lab sample solution passed: True
prompt score: 10/10
ai resources started: 3
recommended ai after queuing starter: gumloop_ai_fundamentals
```

## Official AI tracker QA result

```text
catalog count: 21
credential count: 9
starter path: gumloop_ai_fundamentals, gumloop_getting_started, anthropic_academy
first recommendation: gumloop_ai_fundamentals
after starter complete: openai_prompting_guide
```

## Manual browser test limitation

This container does not have Streamlit installed, and package installation cannot reach PyPI from here. Because of that, I could not run a live browser-click test in this environment. The app was syntax-compiled, the core logic was tested directly, and the newly found app-level missing-import bug is now covered by static tests.
