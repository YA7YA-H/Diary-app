content_data = []


class Content:
    """Entry of user in diary"""

    def __init__(self, date_created, content):
        self.date_created = date_created
        self.content = content

    def create(self):
        my_diary = {"Date": self.date_created, "Content": self.content}
        return content_data.append(my_diary)
