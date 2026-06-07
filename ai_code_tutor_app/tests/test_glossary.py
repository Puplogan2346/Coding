from curriculum import LESSONS
from glossary import GLOSSARY, define, vocab_for_terms


def test_every_key_term_has_a_real_definition():
    """Every key term in every lesson must have a real glossary definition."""
    fallback = define("___definitely_not_a_real_term___")
    missing = []
    for lesson in LESSONS:
        for term in lesson.key_terms:
            if define(term) == fallback:
                missing.append((lesson.id, term))
    assert not missing, f"Terms without a glossary definition: {missing}"


def test_vocab_for_terms_pairs_terms_with_definitions():
    pairs = vocab_for_terms(["function", "list"])
    assert pairs[0][0] == "function"
    assert "reusable" in pairs[0][1].lower()
    assert len(pairs) == 2


def test_glossary_lookup_is_case_insensitive():
    assert define("JSON") == define("json")
    assert define("ValueError") == GLOSSARY["valueerror"]
