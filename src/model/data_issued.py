class DateIssued:

    def __init__(self, json):
        self.year = json['year']
        self.month = json['month']
        self.day = json['day']

    def get_year(self):
        return self.year if self.year is not None else 'n.d.'
