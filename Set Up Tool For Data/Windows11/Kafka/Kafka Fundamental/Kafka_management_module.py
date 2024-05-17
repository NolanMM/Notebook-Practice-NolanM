"""
This module provides a class to manage Kafka topics. It allows you to create, list, and delete topics. NolanM 2024-05-16
pip install kafka-python
"""

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


class KafkaTopicManager:
    def __init__(self, bootstrap_servers):
        self.admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        topic_list = [NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        try:
            self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print(f"Topic '{topic_name}' created successfully.")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic_name}' already exists.")
        except Exception as e:
            print(f"An error occurred while creating topic '{topic_name}': {e}")

    def list_topics(self):
        topics = self.admin_client.list_topics()
        print("Current topics in Kafka:")
        for topic in topics:
            print(f"- {topic}")

    def delete_topic(self, topic_name):
        try:
            self.admin_client.delete_topics(topics=[topic_name])
            print(f"Topic '{topic_name}' deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting topic '{topic_name}': {e}")


if __name__ == "__main__":
    manager = KafkaTopicManager(bootstrap_servers='localhost:9092')

    # Create a new topic
    manager.create_topic(topic_name='second_topic', num_partitions=3, replication_factor=1)

    # List all topics
    manager.list_topics()

    # Print the list of topics
    print(manager.admin_client.list_topics())

    # Delete a topic
    # manager.delete_topic(topic_name='first_topic')
