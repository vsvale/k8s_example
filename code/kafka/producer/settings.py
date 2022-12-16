def producer_settings_avro(broker,schema_registry):
    avro = {
        "client.id":"sampledb-producer",
        "bootstrap.servers": broker,
        "schema.registry.url": schema_registry,
        "enable.idempotence":"true",
        "acks":"all",
        "retries": 100,
        "linger.ms":1000,
        "batch.num.messages": 1000,
        "queue.buffering.max.ms": 100,
        "queue.buffering.max.messages": 1000,
        "batch.size":16384,
        "compression.type":"gzip",
        "max.in.flight.requests.per.connection": 1
    }

    return dict(avro)