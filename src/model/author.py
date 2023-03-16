
class Author:

    def __init__(self, author_json):
        self.given: str = author_json['given']
        self.family = author_json['family']
        self.literal = author_json['literal']

    def get_given(self):
        return '{}. '.format(self.given) if self.given is not None else ''

    def get_family(self):
        return '{}, '.format(self.family) if self.family is not None else ''
