from scaling import build_agent

def test_semicolon_step_split():
    a = build_agent("scouty", "skills/default.yaml")
    out = a.solve("python result = '{"x":1}'; json")
    assert '"x": 1' in out["result"]