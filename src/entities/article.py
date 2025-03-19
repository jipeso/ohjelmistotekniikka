import uuid


class Article:
    def __init__(self, title, content, article_id=None):
        self.title = title
        self.content = content
        self.id = article_id or str(uuid.uuid4())
