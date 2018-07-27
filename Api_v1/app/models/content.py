from Api_v1.Database.connector import DatabaseConnection
db = DatabaseConnection()


class Content:
    """Entry of user in diary"""

    def __init__(self, title, content, email):
        self.title = title
        self.content = content
        self.email = email

    def create(self):
        db.add_new_entry(self.email, self.content, self.title)
