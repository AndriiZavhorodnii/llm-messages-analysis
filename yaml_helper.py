from ruamel.yaml import YAML

class YamlParser:
    def __init__(self, path: str):
        self.path = path
        self.yaml = YAML(typ='safe')

    def read(self):
        with open(self.path, "r") as file:
            return self.yaml.load(file)

    def write(self, new_config: dict):
        with open(self.path, 'w') as file:
            self.yaml.dump(data=new_config, stream=file)
