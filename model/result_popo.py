from model import data_issued as di


class Result:
    def __init__(self, result):
        self.urlToImage = result['urlToImage']
        self.credibility = result['credibility']
        self.metadata = result['metadata']
        self.author = self.metadata['author']
        self.collectionEditor = self.metadata['collectionEditor']
        self.composer = self.metadata['composer']
        self.issued = di.DateIssued(self.metadata['issued'])
        self.containerTitle = self.metadata['containerTitle']
        self.publisher = self.metadata['publisher']
        self.title = self.metadata['title']
        self.url = self.metadata['url']
        self.chapterNumber = self.metadata['chapterNumber']