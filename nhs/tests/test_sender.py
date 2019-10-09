import pytest
import document_sender.sender


def test_do_nthing():
    pass

@pytest.mark.parametrize("num_items, bulk_size, expected", [
    (19, 5, 4),
    (20, 5, 4),
    (5, 5, 1),
    (3, 5, 1),
    (0, 5, 0)
])
def test_send_in_bulk(monkeypatch, num_items, bulk_size, expected):

    def MockMessageProducer(**configs):
        class MockProducer(object):

            def send(topic, value):
                pass

        return MockProducer

    monkeypatch.setattr(document_sender.sender, 'KafkaProducer', MockMessageProducer)

    kafka_host = 'host'
    kafka_port = 9999
    topic = 'topic'
    # bulk_size = 5
    documents = list(range(num_items))
    mp = document_sender.sender.MessageProducer(kafka_host, kafka_port, topic)
    num_chunks = mp.send_in_bluk(documents, bulk_size, 'filename')
    assert num_chunks == expected