from agent import AGENTS
def test_scoutry():
    out = AGENTS['scouty'].act('ping')
    assert 'scouty' in out['result']
