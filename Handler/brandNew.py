from dbOperations import DatabaseOperations
from Data.topic import Topics
from Handler import cursor, commit
from datetime import datetime
import pickle


class BrandNew(DatabaseOperations):
    """
    Class to represent the operations to add brand new topics.
    Attributes:
        - topics(list[Topics]) : Contains topics object.
        - currentTopic(Topics) : Contains the current `topics` object working on.
    """

    def __init__(self):
        self.topics = [[], []]
        self.currentTopic = None

    @staticmethod
    def needBreak(value: str):
        if value == 'q':
            return True
        else:
            return False

    def addTopic(self):
        """Create a new topic and add the necessary data to the `self.currentTopic` object."""
        while True:
            name = input('Enter topic name : ')

            # Terminating while the user enters 'q'.
            if self.needBreak(name):
                break

            self.currentTopic = Topics(name)
            self.topics.append(self.currentTopic)

            # Getting some initial details.
            self.currentTopic.complexityLevel = input('Complexity level : ')
            self.currentTopic.notesName = input('Notes Name : ')
            self.currentTopic.pageNo = int(input('Enter page no of the notes : '))
            self.currentTopic.referenceBook = input('Reference book name : ')

            # Add other details
            self.addSubTopic()
            self.addVocabulary()
            self.addTestResource()
            self.addExternalResource()

    def addSubTopic(self):
        while True:
            subTopic = input(f"Enter sub topic of the {self.currentTopic.name} : ")
            # Terminating while the user enters 'q'.
            if self.needBreak(subTopic):
                break
            self.currentTopic.subTopics.append(subTopic)

    def addVocabulary(self):
        """Add vocabulary and its meaning to the `currentTopic.vocabularies`."""
        while True:
            vocabulary = input('Enter Vocabulary : ')
            if self.needBreak(vocabulary):
                break
            meaning = input(f'Meaning of {vocabulary} : ')
            self.currentTopic.vocabularies[vocabulary] = meaning

    def addTestResource(self):
        """Add test (Assessment) resources to the `currentTopic.testResource`."""
        resource = input('Test Resource : ')
        self.currentTopic.testResources = resource

    def addExternalResource(self):
        """Add external resources includes blog, Youtube links to the `currentTopic.externalResource`."""
        while True:
            resource = input('External resource : ')
            if self.needBreak(resource):
                break
            self.currentTopic.externalResourceLinks.append(resource)

    def updateDb(self):
        currentDate = datetime.strftime(datetime.now(), '%m/%d/%Y')
        for topic in self.topics:
            try:
                query = 'INSERT INTO topics(date, topic)VALUES("{}", "{}")'.format(currentDate, pickle.dumps(topic))
                cursor.execute(query)
            except Exception as error:
                print(error)
        commit()


if __name__ == '__main__':
    new = BrandNew()
    # new.addTopic()
    new.updateDb()



