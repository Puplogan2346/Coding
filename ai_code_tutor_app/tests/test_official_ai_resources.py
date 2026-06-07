from official_ai_resources import (
    OFFICIAL_AI_MILESTONES,
    OFFICIAL_AI_RESOURCES,
    OFFICIAL_AI_STARTER_PATH,
    PROVIDER_ORDER,
    STATUS_OPTIONS,
    credential_resources,
    next_recommended_resource,
    official_resource_stats,
    resource_has_certificate,
    resources_for_ids,
)
from progress import (
    default_progress,
    official_ai_completed_count,
    record_official_ai_resource,
)


def test_official_ai_resources_have_required_metadata():
    assert len(OFFICIAL_AI_RESOURCES) >= 18
    ids = [resource.id for resource in OFFICIAL_AI_RESOURCES]
    assert len(ids) == len(set(ids))
    for resource in OFFICIAL_AI_RESOURCES:
        assert resource.id
        assert resource.provider
        assert resource.title
        assert resource.url.startswith("https://")
        assert resource.summary
        assert resource.why_it_matters
        assert resource.tags


def test_user_requested_providers_are_included():
    providers = {resource.provider for resource in OFFICIAL_AI_RESOURCES}
    assert "Gumloop" in providers
    assert "Anthropic / Claude" in providers
    assert "OpenAI" in providers
    assert "Google Cloud / Gemini" in providers
    assert "AWS" in providers
    assert "Microsoft / Azure AI" in providers
    assert "Hugging Face" in providers
    assert "NVIDIA" in providers

    gumloop_resources = [resource for resource in OFFICIAL_AI_RESOURCES if resource.provider == "Gumloop"]
    claude_resources = [resource for resource in OFFICIAL_AI_RESOURCES if resource.provider == "Anthropic / Claude"]
    assert len(gumloop_resources) >= 3
    assert len(claude_resources) >= 4


def test_certification_and_certificate_options_are_trackable():
    stats = official_resource_stats({})
    assert stats["total"] == len(OFFICIAL_AI_RESOURCES)
    assert stats["certificate_options"] >= 7

    progress = default_progress(["lesson-one"], profile_name="Ava")
    record_official_ai_resource(progress, "gumloop_learning_cohorts", "In progress", "Apply after one workflow.")
    record_official_ai_resource(progress, "aws_ai_practitioner", "Completed", "Add badge link later.")

    stats = official_resource_stats(progress)
    assert stats["started"] == 2
    assert stats["completed"] == 1
    assert official_ai_completed_count(progress) == 1
    assert progress["official_ai_notes"]["gumloop_learning_cohorts"].startswith("Apply")


def test_credential_filter_excludes_no_certificate_resources():
    no_certificate_titles = {
        resource.title
        for resource in OFFICIAL_AI_RESOURCES
        if "No certificate" in resource.certificate or "not listed" in resource.certificate.lower()
    }
    credential_titles = {resource.title for resource in credential_resources()}
    assert no_certificate_titles
    assert not no_certificate_titles.intersection(credential_titles)

    no_certificate_resource = next(resource for resource in OFFICIAL_AI_RESOURCES if resource.id == "openai_academy")
    assert resource_has_certificate(no_certificate_resource) is False

    certification_resource = next(resource for resource in OFFICIAL_AI_RESOURCES if resource.id == "aws_ai_practitioner")
    assert resource_has_certificate(certification_resource) is True


def test_starter_path_prioritizes_gumloop_and_claude():
    assert OFFICIAL_AI_STARTER_PATH == (
        "gumloop_ai_fundamentals",
        "gumloop_getting_started",
        "anthropic_academy",
    )
    starter_resources = resources_for_ids(OFFICIAL_AI_STARTER_PATH)
    assert len(starter_resources) == 3
    assert starter_resources[0].provider == "Gumloop"
    assert starter_resources[1].provider == "Gumloop"
    assert starter_resources[2].provider == "Anthropic / Claude"


def test_next_recommended_resource_advances_after_starter_path():
    progress = default_progress(["lesson-one"], profile_name="Ava")
    assert next_recommended_resource(progress).id == "gumloop_ai_fundamentals"

    for resource_id in OFFICIAL_AI_STARTER_PATH:
        record_official_ai_resource(progress, resource_id, "Completed")

    recommendation = next_recommended_resource(progress)
    assert recommendation is not None
    assert recommendation.id == "openai_prompting_guide"

    for milestone in OFFICIAL_AI_MILESTONES:
        for resource_id in milestone["resource_ids"]:
            record_official_ai_resource(progress, resource_id, "Skipped")

    assert next_recommended_resource(progress) is None


def test_milestone_track_ids_exist():
    all_ids = {resource.id for resource in OFFICIAL_AI_RESOURCES}
    for milestone in OFFICIAL_AI_MILESTONES:
        assert milestone["title"]
        assert milestone["goal"]
        assert milestone["resource_ids"]
        assert set(milestone["resource_ids"]).issubset(all_ids)
        assert resources_for_ids(milestone["resource_ids"])


def test_provider_order_and_status_options_are_stable():
    assert PROVIDER_ORDER[0] == OFFICIAL_AI_RESOURCES[0].provider
    assert STATUS_OPTIONS == ["Not started", "Queued", "In progress", "Completed", "Skipped"]
