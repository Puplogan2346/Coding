# Official AI Lessons and Certifications Tracker

This app includes a private tracker for official AI learning resources. It does not copy or republish paid or third-party course content. It links to the original provider pages and lets you save your own status and notes.

## Included providers

- Anthropic / Claude: Anthropic Academy, Claude developer docs, Claude Code docs, Claude prompt engineering docs, and the official Anthropic prompt engineering tutorial.
- Gumloop: Gumloop University, Getting Started with Gumloop, AI Fundamentals, and Learning Cohorts.
- OpenAI: OpenAI Academy and the OpenAI prompting guide.
- Google Cloud / Gemini: Google Skills introductory generative AI path, Generative AI Leader certification, and Professional Machine Learning Engineer certification.
- Microsoft / Azure AI: Azure AI Fundamentals and the Microsoft Learn AI applications and agents path.
- AWS: AWS Certified AI Practitioner and AWS Certified Machine Learning Engineer - Associate.
- Hugging Face: Hugging Face Learn and the Hugging Face Agents Course.
- NVIDIA: NVIDIA Deep Learning Institute training and certification hub.

## How to use it

1. Open the app and go to **AI Certs**.
2. Start with the **Foundation** milestone.
3. Mark each resource as `Queued`, `In progress`, `Completed`, or `Skipped`.
4. Add private notes, such as exam goals, certificate links, or projects you want to build.
5. Re-check official provider pages before paying for exams, cohorts, or certificates.

## Suggested starter path

1. Finish Python lesson 1 in the main curriculum.
2. Queue **Gumloop AI Fundamentals**, **Getting Started with Gumloop**, and **Anthropic Academy**.
3. Follow the **Recommended next AI step** card in the AI Certs tab.
4. Use the OpenAI and Claude prompting docs while practicing in Prompt Lab.
5. Build one simple Gumloop workflow or agent.
6. Choose only one certification target at first, such as AWS Certified AI Practitioner, Google Cloud Generative AI Leader, or Microsoft Azure AI Fundamentals.

## Maintenance notes

The resource catalog lives in `official_ai_resources.py`. The app stores short summaries, provider names, official links, status, and private notes only. It does not scrape or embed the full lessons.

Before sharing publicly, review the links and update any certification notes, prices, exam codes, retirement dates, or cohort dates. The v5 QA pass fixed the credential-only filter so resources marked as `No certificate listed` do not appear as credential options. Then run:

```bash
pytest -q
python -m compileall .
```
