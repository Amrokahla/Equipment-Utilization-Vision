Kafka topic names for local development live in `src/dev/kafka/topics.txt`. That directory is mounted into the `kafka-init` container by `docker-compose.yml`.

Do not duplicate topic lists here; update `src/dev/kafka/topics.txt` instead.
