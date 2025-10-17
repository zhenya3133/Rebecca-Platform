class SemanticMemory:
    def __init__(self):
        self.concepts = {}

    def store_concept(self, name, description):
        self.concepts[name] = description

    def get_concept(self, name):
        return self.concepts.get(name)
