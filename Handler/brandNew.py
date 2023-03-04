from .dbOperations import DatabaseOperations
from Data.topic import Topics
from Handler import cursor, commit
from datetime import datetime
from logs.logger import addLog


class BrandNew(DatabaseOperations):
    """
    Class to represent the operations to add brand-new topics.
    Attributes:
        - topics(list[Topics]) : Contains topics object.
        - currentTopic(Topics) : Contains the current `topics` object working on.
    """

    def __init__(self):
        self.topics = []
        self.currentTopic = None

    @staticmethod
    def needBreak(value: str):
        if value == 'q':
            return True
        else:
            return False

    def executeQuery(self, query: str) -> None:
        """To execute queries with try and except block."""
        try:
            cursor.execute(query)
        except Exception as error:
            addLog(error)

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
        """Add external resources includes blog, YouTube links to the `currentTopic.externalResource`."""
        while True:
            resource = input('External resource : ')
            if self.needBreak(resource):
                break
            self.currentTopic.externalResourceLinks.append(resource)

    def updateDb(self) -> None:
        currentDate = datetime.strftime(datetime.now(), '%m/%d/%Y')
        for topic in self.topics:

            # Insert the values into the table 'topics'.
            query = "INSERT INTO topics(date, name, complexity_level, confidence_level, times_revised, test_resource, " \
                    "notes_name, page_no, reference_book)VALUES('{}', '{}', '{}', '{}', {}, '{}', '{}', {}, '{}')"\
                                                                                    .format(currentDate, topic.name,
                                                                                      topic.complexityLevel,
                                                                                      topic.confidenceLevel,
                                                                                      topic.timesRevised,
                                                                                      topic.testResources,
                                                                                      topic.notesName,
                                                                                      topic.pageNo,
                                                                                      topic.referenceBook)

            self.executeQuery(query)

            # Insert the values into the table 'sub_topics'.
            # Fetch the unique id of the current topic to store it in the sub_topics table.
            query = "SELECT id FROM topics WHERE name='{}'".format(topic.name)
            self.executeQuery(query)

            uniqueId = cursor.fetchone()[0]

            # Store all the sub topics.
            for subTopic in topic.subTopics:
                query = "INSERT INTO sub_topics(id, sub_topic_name)VALUES({}, '{}')".format(uniqueId, subTopic)
                self.executeQuery(query)

            # Insert the values into the table 'vocabularies'.
            for vocabulary, meaning in topic.vocabularies.items():
                query = "INSERT INTO vocabularies(id, vocabulary, meaning)VALUES({}, '{}', '{}')".format(uniqueId,
                                                                                                        vocabulary,
                                                                                                        meaning)
                self.executeQuery(query)

            # Insert the values into the table 'external_resources'.
            for resource in topic.externalResourceLinks:
                query = "INSERT INTO external_resources(id, resource)VALUES({}, '{}')".format(uniqueId, resource)

                self.executeQuery(query)

        commit()


if __name__ == '__main__':
    new = BrandNew()
    new.addTopic()
    new.updateDb()
