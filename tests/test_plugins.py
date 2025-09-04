from scaling import build_agent

def test_math_plugin_basic():
    a = build_agent("scouty", "skills/default.yaml")
    # math tool not registered by default, ensure graceful fallback
    out = a.solve("calc 3*7")
    assert out["transcript"], "no transcript"