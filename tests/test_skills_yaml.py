import yaml

def test_skills_yaml_parses():
    with open("skills/default.yaml", "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    assert isinstance(doc, dict) and "rules" in doc and isinstance(doc["rules"], list) and len(doc["rules"]) > 0