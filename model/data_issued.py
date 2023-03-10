class DateIssued:

    def __init__(self, json):
        self.year = json['year']
        self.month = json['month']
        self.day = json['day']