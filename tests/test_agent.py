from scaling import build_agent

def test_http_rule():
    a = build_agent("scouty", "skills/default.yaml")
    out = a.solve("fetch https://httpbin.org/json and json parse")
    assert out["transcript"], "no transcript"

def test_python_tool_simple_math():
    a = build_agent("scouty", "skills/default.yaml")
    out = a.solve("python result = 2 + 3")
    assert out["result"].strip() == "5"

def test_json_tool_with_context():
    a = build_agent("scouty", "skills/default.yaml")
    out = a.solve("python result = '{"a": 1}'; json")
    assert '"a": 1' in out["result"]