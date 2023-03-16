from src.model import data_issued as di
from src.model import author as at


class Result:
    def __init__(self, result):
        self.urlToImage = result['urlToImage']
        self.credibility = result['credibility']
        self.metadata = result['metadata']
        self.authors = [at.Author(author) for author in self.metadata['author']]
        self.collectionEditor = self.metadata['collectionEditor']
        self.composer = self.metadata['composer']
        self.issued = di.DateIssued(self.metadata['issued'])
        self.containerTitle = self.metadata['containerTitle']
        self.publisher = self.metadata['publisher']
        self.title = self.metadata['title'] if self.metadata['title'] is not None else ''
        self.url = self.metadata['url']
        self.chapterNumber = self.metadata['chapterNumber']

    def get_sort_key(self):
        author = self.authors[0].family if len(self.authors) > 0 else None
        title = self.title
        return author if author is not None else title
