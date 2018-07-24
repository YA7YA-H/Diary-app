blacklist = []
class Blacklist:
    """users class"""

    def __init__(self, token):
        global blacklist
        self.token = token

    def save_blacklist(self):
        blacklist.append(self.token)