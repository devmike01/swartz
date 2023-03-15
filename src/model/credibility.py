class Credibility:

    def __int__(self, json):
        self.score = json['score']
        self.comment = json['comment']