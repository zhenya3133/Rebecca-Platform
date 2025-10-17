class SecurityMemory:
    def __init__(self):
        self.audits = []

    def store_audit(self, audit):
        self.audits.append(audit)

    def get_audits(self):
        return self.audits
