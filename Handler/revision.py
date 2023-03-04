from .dbOperations import DatabaseOperations
from Handler import cursor, commit
from datetime import datetime, timedelta
from logs.logger import addLog


class Revision(DatabaseOperations):

    def __init__(self):
        self.topics = []
        self.getTopics()

    def executeQuery(self, query):
        try:
            cursor.execute(query)
        except Exception as error:
            addLog(error)

    @staticmethod
    def getDates() -> list:
        """Calculate the dates to revise the topics studied on that date."""
        dates = []

        # Calculate the dates
        for day in [2, 10, 30, 60]:
            currentDate = datetime.strftime(datetime.now(), '%m/%d/%Y')
            currentDate = datetime.strptime(currentDate, '%m/%d/%Y')
            dates.append(datetime.strftime(currentDate - timedelta(days=day), '%m/%d/%Y'))
        return dates

    def getAllDetails(self, uniqueId: int):
        details = []
        query = "SELECT * FROM topics WHERE id={}".format(uniqueId)
        self.executeQuery(query)

        # Filter
        for detail in cursor.fetchall():
            details.append(detail)

        return details

    def getSubTopics(self, uniqueId: int) -> list:
        """Get the sub-topics of the topic based on the given unique id."""
        subTopics = []
        query = "SELECT sub_topic_name FROM sub_topics WHERE id={}".format(uniqueId)
        self.executeQuery(query)

        # Filter the sub-topics.
        for subTopic in cursor.fetchall():
            subTopics.append(subTopic[0])

        return subTopics

    def getVocabularies(self, uniqueId: int) -> dict:
        """Get vocabularies along with its meaning and return as `dict`."""
        vocabularies = {}
        query = "SELECT vocabulary, meaning FROM vocabularies WHERE id={}".format(uniqueId)
        self.executeQuery(query)

        # Filter
        for pair in cursor.fetchall():
            vocabularies[pair[0]] = pair[1]

        return vocabularies

    def getExternalResourceLinks(self, uniqueId: int) -> list:
        resources = []
        query = "SELECT resource FROM external_resources WHERE id={}".format(uniqueId)
        self.executeQuery(query)

        # Filter
        for resource in cursor.fetchall():
            resources.append(resource[0])

        return resources

    def getTopicByComplexityLevel(self, complexityLevel: str) -> list:
        topics = []
        query = "SELECT id, name FROM topics WHERE complexity_level='{}'".format(complexityLevel)
        self.executeQuery(query)

        # Filter
        for topic in cursor.fetchall():
            topics.append((topic[0], topic[1]))

        return topics

    def getTopicByConfidenceLevel(self, confidenceLevel: str) -> list:
        topics = []
        query = "SELECT id, name FROM topics WHERE confidence_level='{}'".format(confidenceLevel)
        self.executeQuery(query)

        # Filter
        for topic in cursor.fetchall():
            topics.append((topic[0], topic[1]))

        return topics

    def getTopicsByDate(self, date):
        topics = []
        query = 'SELECT id, name FROM topics WHERE date="' + date + '"'
        self.executeQuery(query)

        # Filter
        for topic in cursor.fetchall():
            topics.append((topic[0], topic[1]))

        return topics

    def getTopics(self):
        """Get the topics studied on the dates calculated by the `getDates()` method."""
        for date in self.getDates():
            query = "SELECT id, name FROM topics WHERE date='{}'".format(date)
            self.executeQuery(query)

            # Filter the topic name and id.
            for topic in cursor.fetchall():
                self.topics.append((topic[0], topic[1]))

    def reviseTopic(self):

        for pair in self.topics:
            identity, topic = pair

            with open('todo.txt', 'w') as todoFile:
                # Write all details to the top of the todoFile
                print(self.getAllDetails(identity), file=todoFile)
                print("\n\n", file=todoFile)

                # Write the topic and sub topics.
                print(topic.upper(), file=todoFile)
                print('\nSUB-TOPICS', file=todoFile)
                for number, subTopic in enumerate(self.getSubTopics(identity)):
                    todoFile.write(f"{number}. {subTopic}\n")

                # Write vocabularies to the todoFile.
                print("\nVOCABULARIES", file=todoFile)
                for number, pair in enumerate(self.getVocabularies(identity).items()):
                    vocabulary, meaning = pair
                    todoFile.write(f"{number}. {vocabulary} - {meaning}\n")

                # Write the external resources to the todoFile.
                print("\nEXTERNAL RESOURCES", file=todoFile)
                for number, resource in enumerate(self.getExternalResourceLinks(identity)):
                    todoFile.write(f"{number}. {resource}\n")

            print("Once you have completed.")
            input('Press Enter')

            # Update the 'times_revised' column
            self.updateDb(identity)

    def updateDb(self, identity: int):
        # Get the current value of the column 'times_revised'.
        query = "SELECT times_revised FROM topics WHERE id={}".format(identity)
        self.executeQuery(query)
        currentRevisionTimes = cursor.fetchone()[0]

        # Update the 'times_revised' column by 1.
        query = "UPDATE topics SET times_revised={} WHERE id={} ".format(currentRevisionTimes + 1, identity)
        self.executeQuery(query)


if __name__ == '__main__':
    r = Revision()
    r.reviseTopic()
    commit()
