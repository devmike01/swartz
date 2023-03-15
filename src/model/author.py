
class Author:

    def __init__(self, author_json):
        self.given: str = author_json['given']
        self.family = author_json['family']
        self.literal = author_json['literal']
