from scaling import build_agent

def test_default_route_python_when_unknown():
    a = build_agent("scouty", "skills/default.yaml")
    out = a.solve("compute 1+1")
    assert out["transcript"], "no transcript"