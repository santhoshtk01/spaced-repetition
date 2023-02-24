from dataclasses import dataclass


@dataclass
class Topics:
    def __init__(self, name: str = None):
        self.name = name
        self.subTopics = []
        self.vocabularies = {}
        self.complexityLevel = 'Easy'
        self.confidenceLevel = 'Weak'
        self.timesRevised = 0
        self.testResources = ''
        self.notesName = ''
        self.pageNo = None
        self.externalResourceLinks = []
        self.referenceBook = ''
