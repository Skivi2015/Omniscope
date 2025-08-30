# Minimal agent registry and runner
import yaml, importlib, os
class Agent:
    def __init__(self, name, cfg):
        self.name = name
        self.cfg = cfg
    def act(self, task):
        return {'result': f'{self.name} completed: {task}'}
def load_agents(yaml_file):
    bots = yaml.safe_load(open(yaml_file))
    return {name: Agent(name, cfg) for name, cfg in bots.items()}
AGENTS = load_agents('bots.yaml')
