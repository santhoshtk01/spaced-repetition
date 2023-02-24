import pickle
from pickle import UnpicklingError
import ast
from dbOperations import DatabaseOperations
from Handler import cursor
from datetime import datetime, timedelta


class Revision(DatabaseOperations):

    def __init__(self):
        self.topics = []

    def getDates(self) -> list:
        """Calculate the dates to revise the topics studied on that date."""
        dates = []

        # Calculate the dates
        for day in [2, 10, 30, 60]:
            currentDate = datetime.strftime(datetime.now(), '%m/%d/%Y')
            currentDate = datetime.strptime(currentDate, '%m/%d/%Y')
            dates.append(datetime.strftime(currentDate - timedelta(days=day), '%m/%d/%Y'))
        return dates

    def __unPickle(self, topics):
        """Un-Pickle the bytes into actual objects."""
        topics = topics
        for index, topic in enumerate(topics):
            try:
                data = pickle.loads(topic)
                topics[index] = data
            except UnpicklingError as error:
                print(error)
            except Exception:
                pass

        return topics

    def getTopics(self):
        """Get the topics studied on the dates calculated by the `getDates()` method."""
        topics = []
        for date in self.getDates():
            # query = 'SELECT topic FROM topics WHERE date="' + date + '"'
            query = 'SELECT * FROM topics'
            cursor.execute(query)

        # Unpack the topics form the tuple.
        for topic in cursor.fetchall():
            topics.append(topic[1])

        return self.__unPickle(topics)

    def reviseTopic(self, topics):
        pass

    def getTopicByComplexityLevel(self, complexityLevel: str) -> list:
        pass

    def getTopicByConfidenceLevel(self, confidenceLevel: str) -> list:
        pass

    def getTopicsByDate(self, date):
        topics = []
        query = 'SELECT topic FROM topics WHERE date="' + date + '"'
        cursor.execute(query)

        # Unpack the tuple.
        for topic in cursor.fetchall():
            topics.append(topic[0])

        return topics

    def updateDb(self):
        pass


if __name__ == '__main__':
    r = Revision()
    print(r.getDates())
    print(r.getTopics())


