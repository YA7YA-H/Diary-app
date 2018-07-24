from Api_v1.Database.connector import DatabaseConnection
db = DatabaseConnection()


class Content:
    """Entry of user in diary"""

    def __init__(self, date_created, content):
        self.date_created = date_created
        self.content = content

    def create(self):
        db.add_new_entry(self.date_created, self.content)
