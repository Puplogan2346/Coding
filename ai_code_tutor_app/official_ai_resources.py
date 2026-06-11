from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


STATUS_OPTIONS = ["Not started", "Queued", "In progress", "Completed", "Skipped"]


@dataclass(frozen=True)
class OfficialAIResource:
    id: str
    provider: str
    title: str
    resource_type: str
    level: str
    time_commitment: str
    url: str
    certificate: str
    summary: str
    why_it_matters: str
    recommended_when: str
    tags: tuple[str, ...]


OFFICIAL_AI_RESOURCES: tuple[OfficialAIResource, ...] = (
    OfficialAIResource(
        id="anthropic_academy",
        provider="Anthropic / Claude",
        title="Anthropic Academy",
        resource_type="Course hub",
        level="Beginner to advanced",
        time_commitment="Pick courses as needed",
        url="https://www.anthropic.com/learn",
        certificate="Certificates listed for completed Academy courses",
        summary=(
            "Official Anthropic learning hub for AI fluency, Claude API development, "
            "Model Context Protocol, and Claude Code."
        ),
        why_it_matters=(
            "Best official starting point for learning Claude as a user, builder, and coding partner."
        ),
        recommended_when="Start after Python lesson 1 or whenever you want a Claude-specific path.",
        tags=("claude", "prompting", "api", "mcp", "coding"),
    ),
    OfficialAIResource(
        id="anthropic_prompt_engineering_overview",
        provider="Anthropic / Claude",
        title="Claude prompt engineering overview",
        resource_type="Docs and tutorial",
        level="Beginner to intermediate",
        time_commitment="1-3 focused sessions",
        url="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview",
        certificate="No certificate listed",
        summary=(
            "Official Claude guide that frames prompt engineering around success criteria, "
            "evaluation, best practices, and interactive tutorials."
        ),
        why_it_matters=(
            "Pairs directly with this app's Prompt Lab so you can compare your prompts against official guidance."
        ),
        recommended_when="Use while doing the Prompt Lab or debugging AI responses.",
        tags=("claude", "prompting", "evaluation", "tutorial"),
    ),
    OfficialAIResource(
        id="anthropic_intro_to_claude",
        provider="Anthropic / Claude",
        title="Intro to Claude for developers",
        resource_type="Developer docs",
        level="Beginner developer",
        time_commitment="1-2 sessions",
        url="https://platform.claude.com/docs/en/intro",
        certificate="No certificate listed",
        summary=(
            "Official path for making a first API call, understanding the Messages API, "
            "choosing a model, and exploring Claude features."
        ),
        why_it_matters=(
            "Gives you a second model provider to compare with the OpenAI-powered tutor in this starter app."
        ),
        recommended_when="Start after Python functions and dictionaries feel comfortable.",
        tags=("claude", "api", "developer", "models"),
    ),
    OfficialAIResource(
        id="anthropic_claude_code_docs",
        provider="Anthropic / Claude",
        title="Claude Code overview",
        resource_type="Developer docs",
        level="Intermediate",
        time_commitment="1-2 sessions plus practice",
        url="https://docs.anthropic.com/en/docs/claude-code/overview",
        certificate="No certificate listed",
        summary=(
            "Official Claude Code documentation for using Claude as an agentic coding tool in the terminal, "
            "IDE, desktop, and browser workflows."
        ),
        why_it_matters=(
            "Useful once you want to compare this app's AI tutor with a professional coding-agent workflow."
        ),
        recommended_when="Use after you understand functions, files, debugging, and GitHub basics.",
        tags=("claude", "claude code", "agentic coding", "developer", "terminal"),
    ),
    OfficialAIResource(
        id="anthropic_interactive_prompt_tutorial",
        provider="Anthropic / Claude",
        title="Anthropic interactive prompt engineering tutorial",
        resource_type="Hands-on tutorial",
        level="Beginner to advanced",
        time_commitment="9 chapters plus exercises",
        url="https://github.com/anthropics/prompt-eng-interactive-tutorial",
        certificate="No certificate listed",
        summary=(
            "Official Anthropic tutorial repository covering prompt structure, clarity, roles, examples, "
            "hallucination reduction, and complex prompts."
        ),
        why_it_matters=(
            "This is the most hands-on Claude prompting practice to pair with your coding lessons."
        ),
        recommended_when="Use as a weekly practice track alongside this app's Prompt Lab.",
        tags=("claude", "prompting", "exercises", "github"),
    ),
    OfficialAIResource(
        id="gumloop_university",
        provider="Gumloop",
        title="Gumloop University",
        resource_type="Course hub",
        level="Beginner",
        time_commitment="Short lessons",
        url="https://university.gumloop.com",
        certificate="No certificate listed on hub",
        summary=(
            "Official Gumloop learning hub for becoming a Gumloop and AI automation builder, "
            "with no prior knowledge required."
        ),
        why_it_matters=(
            "Strong bridge from learning Python and prompting into no-code/low-code AI agents and workflows."
        ),
        recommended_when="Start early if your goal is automations, operations, sales, marketing, or internal tools.",
        tags=("gumloop", "automation", "agents", "workflow", "no-code"),
    ),
    OfficialAIResource(
        id="gumloop_getting_started",
        provider="Gumloop",
        title="Getting Started with Gumloop",
        resource_type="Course",
        level="Beginner",
        time_commitment="6 lessons",
        url="https://university.gumloop.com/getting-started-with-gumloop/what-is-gumloop",
        certificate="Credits listed; certificate not listed for this course page",
        summary=(
            "Official Gumloop course for building and deploying an agent step by step, "
            "including tools, models, instructions, skills, triggers, Slack, and email."
        ),
        why_it_matters=(
            "Lets you turn what you learn about prompts into working agents that connect to real tools."
        ),
        recommended_when="Use after you finish Python basics or whenever you want an automation project.",
        tags=("gumloop", "agents", "instructions", "skills", "triggers"),
    ),
    OfficialAIResource(
        id="gumloop_ai_fundamentals",
        provider="Gumloop",
        title="AI Fundamentals",
        resource_type="Course collection",
        level="Beginner",
        time_commitment="7 lessons listed on Gumloop University hub",
        url="https://university.gumloop.com/ai-fundamentals/what-is-an-ai-model",
        certificate="No certificate listed on sampled lesson",
        summary=(
            "Official Gumloop AI fundamentals lessons covering AI models, tokens, context, tools, "
            "instructions, MCP, and Gumstack concepts."
        ),
        why_it_matters=(
            "Good plain-English foundation for understanding what an AI automation platform is doing behind the scenes."
        ),
        recommended_when="Start before building your first serious Gumloop workflow.",
        tags=("gumloop", "ai fundamentals", "models", "tokens", "mcp"),
    ),
    OfficialAIResource(
        id="gumloop_learning_cohorts",
        provider="Gumloop",
        title="Gumloop Learning Cohorts",
        resource_type="Live cohort",
        level="Beginner to intermediate",
        time_commitment="1 week",
        url="https://www.gumloop.com/cohorts",
        certificate="Certificates listed for completing cohort challenges",
        summary=(
            "Official guided cohort with live sessions, practical challenges, community support, "
            "and agent/automation projects."
        ),
        why_it_matters=(
            "Useful when you want accountability, feedback, and a real project deadline."
        ),
        recommended_when="Join after you have one automation idea you care about.",
        tags=("gumloop", "cohort", "certificate", "agents", "automation"),
    ),
    OfficialAIResource(
        id="openai_academy",
        provider="OpenAI",
        title="OpenAI Academy",
        resource_type="Learning hub and events",
        level="Beginner to advanced",
        time_commitment="Ongoing",
        url="https://academy.openai.com/",
        certificate="No certification claim listed on homepage",
        summary=(
            "Official OpenAI learning community with events, content, communities, and expert-led AI learning."
        ),
        why_it_matters=(
            "Keeps your AI skills current while you are building this app and learning to prompt."
        ),
        recommended_when="Use for current OpenAI product learning and live sessions.",
        tags=("openai", "academy", "events", "community"),
    ),
    OfficialAIResource(
        id="openai_prompting_guide",
        provider="OpenAI",
        title="OpenAI prompting guide",
        resource_type="Developer docs",
        level="Beginner to intermediate",
        time_commitment="1-2 sessions",
        url="https://developers.openai.com/api/docs/guides/prompting",
        certificate="No certificate listed",
        summary=(
            "Official OpenAI developer guide for writing clearer prompts and improving model outputs."
        ),
        why_it_matters=(
            "Pairs with this app's OpenAI-powered tutor and Prompt Lab."
        ),
        recommended_when="Use whenever you ask the AI tutor for code, debugging, or project help.",
        tags=("openai", "prompting", "developer", "api"),
    ),
    OfficialAIResource(
        id="google_intro_gen_ai",
        provider="Google Cloud / Gemini",
        title="Beginner: Introduction to Generative AI",
        resource_type="Learning path",
        level="Beginner",
        time_commitment="5 activities listed",
        url="https://www.skills.google/paths/118",
        certificate="Google Skills achievements may vary by activity",
        summary=(
            "Official Google Skills path introducing generative AI, large language models, and responsible AI principles."
        ),
        why_it_matters=(
            "Good vendor-neutral foundation before deeper Gemini or Google Cloud work."
        ),
        recommended_when="Use after this app's first AI/prompting lessons.",
        tags=("google", "gemini", "gen ai", "responsible ai"),
    ),
    OfficialAIResource(
        id="google_generative_ai_leader",
        provider="Google Cloud / Gemini",
        title="Google Cloud Generative AI Leader",
        resource_type="Certification",
        level="Beginner to intermediate",
        time_commitment="90 minute exam plus prep",
        url="https://cloud.google.com/learn/certification/generative-ai-leader",
        certificate="Official Google Cloud certification exam",
        summary=(
            "Official Google Cloud certification for explaining generative AI concepts, business value, "
            "Google Cloud AI products, implementation techniques, and responsible AI."
        ),
        why_it_matters=(
            "A practical first Google Cloud AI credential before advanced ML engineering targets."
        ),
        recommended_when="Use after Python basics, prompt fundamentals, and one hands-on AI workflow project.",
        tags=("google", "gemini", "certification", "gen ai", "cloud"),
    ),
    OfficialAIResource(
        id="google_professional_ml_engineer",
        provider="Google Cloud / Gemini",
        title="Google Professional Machine Learning Engineer",
        resource_type="Certification",
        level="Advanced",
        time_commitment="Exam plus prep path",
        url="https://cloud.google.com/learn/certification/machine-learning-engineer",
        certificate="Official proctored certification exam",
        summary=(
            "Official Google Cloud certification for building, evaluating, productionizing, and optimizing AI solutions, "
            "including generative AI solutions."
        ),
        why_it_matters=(
            "A serious long-term target after Python, APIs, data, and ML foundations."
        ),
        recommended_when="Do not start as a beginner; use as a 6-12 month target.",
        tags=("google", "certification", "machine learning", "cloud", "gen ai"),
    ),
    OfficialAIResource(
        id="microsoft_azure_ai_fundamentals",
        provider="Microsoft / Azure AI",
        title="Microsoft Azure AI Fundamentals",
        resource_type="Certification",
        level="Beginner",
        time_commitment="Exam plus prep",
        url="https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-fundamentals/",
        certificate="Official Microsoft certification; verify AI-900 retirement/replacement details before scheduling",
        summary=(
            "Official Microsoft credential for proving understanding of AI workloads, ML principles, computer vision, "
            "NLP, and generative AI workloads on Azure. Microsoft currently lists AI-900 as retiring June 30, 2026."
        ),
        why_it_matters=(
            "Good first cloud AI credential for technical and non-technical learners."
        ),
        recommended_when="Use after you understand Python basics and core AI terms.",
        tags=("microsoft", "azure", "certification", "ai fundamentals"),
    ),
    OfficialAIResource(
        id="microsoft_get_started_ai_agents",
        provider="Microsoft / Azure AI",
        title="Get started with AI applications and agents on Azure",
        resource_type="Learning path",
        level="Beginner",
        time_commitment="6 modules listed",
        url="https://learn.microsoft.com/en-us/training/paths/get-started-ai-apps-agents/",
        certificate="Microsoft Learn achievement code available when supported",
        summary=(
            "Official Microsoft Learn path for AI workloads and solutions in Microsoft Foundry, including agents, "
            "text, speech, vision, and information extraction."
        ),
        why_it_matters=(
            "Useful comparison point for Gumloop-style agents and Python client apps."
        ),
        recommended_when="Use after Python functions, dictionaries, and APIs.",
        tags=("microsoft", "azure", "agents", "foundry", "learning path"),
    ),
    OfficialAIResource(
        id="aws_ai_practitioner",
        provider="AWS",
        title="AWS Certified AI Practitioner",
        resource_type="Certification",
        level="Foundational",
        time_commitment="90 minute exam plus prep plan",
        url="https://aws.amazon.com/certification/certified-ai-practitioner/",
        certificate="Official AWS certification",
        summary=(
            "Official AWS certification validating AI, ML, generative AI concepts, and use cases."
        ),
        why_it_matters=(
            "Career-friendly foundational credential if you may use AWS AI tools later."
        ),
        recommended_when="Use after core AI terms and one cloud intro path.",
        tags=("aws", "certification", "foundational", "gen ai", "cloud"),
    ),
    OfficialAIResource(
        id="aws_ml_engineer_associate",
        provider="AWS",
        title="AWS Certified Machine Learning Engineer - Associate",
        resource_type="Certification",
        level="Intermediate",
        time_commitment="130 minute exam plus prep plan",
        url="https://aws.amazon.com/certification/certified-machine-learning-engineer-associate/",
        certificate="Official AWS certification",
        summary=(
            "Official AWS certification validating technical ability to implement and operationalize ML workloads on AWS."
        ),
        why_it_matters=(
            "A later cloud/ML engineering goal after you can build Python apps, work with APIs, and understand ML basics."
        ),
        recommended_when="Use after several projects and at least basic AWS experience.",
        tags=("aws", "certification", "machine learning", "cloud", "engineering"),
    ),
    OfficialAIResource(
        id="hugging_face_learn",
        provider="Hugging Face",
        title="Hugging Face Learn",
        resource_type="Course hub",
        level="Intermediate",
        time_commitment="Course dependent",
        url="https://huggingface.co/learn",
        certificate="No certification claim listed on hub",
        summary=(
            "Official Hugging Face course hub for LLMs, agents, context engineering, diffusion, audio, vision, and more."
        ),
        why_it_matters=(
            "Best open-source AI path once you want to understand models, datasets, agents, and deployment options."
        ),
        recommended_when="Use after Python fundamentals and API basics.",
        tags=("hugging face", "open source", "llm", "agents", "models"),
    ),
    OfficialAIResource(
        id="hugging_face_agents_course",
        provider="Hugging Face",
        title="Hugging Face Agents Course",
        resource_type="Course and certificate",
        level="Beginner to intermediate",
        time_commitment="Self-paced units and assignments",
        url="https://huggingface.co/learn/agents-course/unit0/introduction",
        certificate="Certificate of completion listed through assignments",
        summary=(
            "Official Hugging Face course for learning AI agents from beginner foundations to hands-on frameworks, "
            "assignments, and a final project."
        ),
        why_it_matters=(
            "A strong open-source follow-up after Gumloop, because it helps you understand what agent platforms automate."
        ),
        recommended_when="Use after Python functions, dictionaries, APIs, and at least one Gumloop or Streamlit project.",
        tags=("hugging face", "agents", "certificate", "open source", "assignments"),
    ),
    OfficialAIResource(
        id="nvidia_dli",
        provider="NVIDIA",
        title="NVIDIA Deep Learning Institute",
        resource_type="Training and certification",
        level="Intermediate to advanced",
        time_commitment="Course dependent",
        url="https://www.nvidia.com/en-us/training/",
        certificate="Training and certification hub",
        summary=(
            "Official NVIDIA training hub for AI, accelerated computing, data science, inference, robotics, and related skills."
        ),
        why_it_matters=(
            "Useful later if you move into GPU-based AI, deep learning, data science, or deployment."
        ),
        recommended_when="Use after Python, data structures, and basic ML concepts.",
        tags=("nvidia", "deep learning", "certification", "gpu", "data science"),
    ),
    OfficialAIResource(
        id="agentic_engineer_principled_ai_coding",
        provider="Agentic Engineer (IndyDevDan)",
        title="Principled AI Coding",
        resource_type="Paid course",
        level="Intermediate",
        time_commitment="Self-paced course",
        url="https://agenticengineer.com/principled-ai-coding",
        certificate="No certificate listed",
        summary=(
            "IndyDevDan's course on the foundations of AI coding: managing context, writing "
            "effective prompts, and selecting the right model for each job."
        ),
        why_it_matters=(
            "Pairs directly with this app's lessons 22-23 — the 'big three' of context, prompt, "
            "and model come from this school of thought."
        ),
        recommended_when="Use after lessons 10 (prompting) and 22-23 (agents and directing them).",
        tags=("agentic", "prompting", "context", "ai coding", "indydevdan"),
    ),
    OfficialAIResource(
        id="agentic_engineer_tactical_agentic_coding",
        provider="Agentic Engineer (IndyDevDan)",
        title="Tactical Agentic Coding",
        resource_type="Paid course",
        level="Intermediate to advanced",
        time_commitment="Self-paced course",
        url="https://agenticengineer.com",
        certificate="No certificate listed",
        summary=(
            "The follow-up course on building autonomous agentic systems: specs and plans as "
            "durable artifacts, verification loops, and workflows where agents build systems."
        ),
        why_it_matters=(
            "The natural next step after lesson 24 if you want to go deep on agentic workflows "
            "and automating real engineering work."
        ),
        recommended_when="Use after finishing the agentic coding arc (lessons 22-24).",
        tags=("agentic", "agents", "workflows", "verification", "indydevdan"),
    ),
)


PROVIDER_ORDER = tuple(dict.fromkeys(resource.provider for resource in OFFICIAL_AI_RESOURCES))
RESOURCE_TYPES = tuple(sorted(set(resource.resource_type for resource in OFFICIAL_AI_RESOURCES)))


OFFICIAL_AI_STARTER_PATH = (
    "gumloop_ai_fundamentals",
    "gumloop_getting_started",
    "anthropic_academy",
)


OFFICIAL_AI_MILESTONES = (
    {
        "title": "Foundation",
        "goal": "Understand coding basics, prompts, models, and AI vocabulary.",
        "resource_ids": (
            "anthropic_academy",
            "gumloop_ai_fundamentals",
            "openai_prompting_guide",
            "google_intro_gen_ai",
        ),
    },
    {
        "title": "Build useful AI workflows",
        "goal": "Turn prompts into repeatable agents, workflows, and small apps.",
        "resource_ids": (
            "gumloop_getting_started",
            "gumloop_university",
            "microsoft_get_started_ai_agents",
            "anthropic_intro_to_claude",
            "anthropic_claude_code_docs",
        ),
    },
    {
        "title": "Credential targets",
        "goal": "Pick credentials only after you know why they support your goals.",
        "resource_ids": (
            "gumloop_learning_cohorts",
            "aws_ai_practitioner",
            "google_generative_ai_leader",
            "microsoft_azure_ai_fundamentals",
            "google_professional_ml_engineer",
        ),
    },
    {
        "title": "Open-source and advanced AI",
        "goal": "Learn models, datasets, agents, GPUs, and deeper engineering concepts.",
        "resource_ids": (
            "hugging_face_learn",
            "hugging_face_agents_course",
            "nvidia_dli",
            "anthropic_interactive_prompt_tutorial",
        ),
    },
)


_RESOURCE_BY_ID = {resource.id: resource for resource in OFFICIAL_AI_RESOURCES}


def get_resource(resource_id: str) -> OfficialAIResource:
    return _RESOURCE_BY_ID[resource_id]


def resources_for_ids(resource_ids: Iterable[str]) -> list[OfficialAIResource]:
    return [get_resource(resource_id) for resource_id in resource_ids if resource_id in _RESOURCE_BY_ID]


def normalize_status(status: str | None) -> str:
    if status in STATUS_OPTIONS:
        return str(status)
    return STATUS_OPTIONS[0]


def resource_has_certificate(resource: OfficialAIResource) -> bool:
    """Return True only when the resource has an actual certificate, certification, credential, or exam path.

    Text such as "No certificate listed" should not count. The Streamlit app and stats use this
    shared helper so the UI filter and dashboard numbers stay consistent.
    """
    combined = f"{resource.resource_type} {resource.certificate}".lower()
    negative_markers = (
        "no certificate",
        "no certification",
        "no credential",
        "not listed",
        "no certification claim",
    )
    if any(marker in combined for marker in negative_markers):
        return False
    return any(word in combined for word in ("certificate", "certification", "credential", "exam"))


def credential_resources() -> list[OfficialAIResource]:
    return [resource for resource in OFFICIAL_AI_RESOURCES if resource_has_certificate(resource)]


def next_recommended_resource(progress_data: dict[str, Any]) -> OfficialAIResource | None:
    """Choose the next official AI resource for a learner based on saved status.

    The order starts with the beginner-friendly Gumloop + Claude starter path, then falls
    through the broader milestone tracks. Completed and skipped resources are ignored.
    """
    statuses = progress_data.get("official_ai_status", {}) or {}

    ordered_ids: list[str] = []
    for resource_id in OFFICIAL_AI_STARTER_PATH:
        if resource_id not in ordered_ids:
            ordered_ids.append(resource_id)
    for milestone in OFFICIAL_AI_MILESTONES:
        for resource_id in milestone["resource_ids"]:
            if resource_id not in ordered_ids:
                ordered_ids.append(resource_id)

    for resource_id in ordered_ids:
        status = normalize_status(statuses.get(resource_id))
        if status not in {"Completed", "Skipped"}:
            return get_resource(resource_id)
    return None


def official_resource_stats(progress_data: dict[str, Any]) -> dict[str, int]:
    statuses = progress_data.get("official_ai_status", {}) or {}
    valid_ids = {resource.id for resource in OFFICIAL_AI_RESOURCES}
    tracked = {
        resource_id: normalize_status(status)
        for resource_id, status in statuses.items()
        if resource_id in valid_ids
    }
    started = [status for status in tracked.values() if status in {"Queued", "In progress", "Completed"}]
    completed = [status for status in tracked.values() if status == "Completed"]
    return {
        "total": len(OFFICIAL_AI_RESOURCES),
        "started": len(started),
        "completed": len(completed),
        "certificate_options": len(credential_resources()),
    }


def provider_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for resource in OFFICIAL_AI_RESOURCES:
        counts[resource.provider] = counts.get(resource.provider, 0) + 1
    return counts
