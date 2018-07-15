content_data = []


class Content:
    """Entry of user in diary"""
    contentID = 0

    def __init__(self, date_created, content):
        self.date_created = date_created
        self.content = content

    def create(self):
        my_diary = {
            "ContentID": Content.contentID,
            "Date": self.date_created,
            "Content": self.content
        }
        Content.contentID += 1
        return content_data.append(my_diary)
