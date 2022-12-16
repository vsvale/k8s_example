def on_delivery_avro(err, msg, obj):

    if err is not None:
        print('message {} delivery failed for user {} with error {}'.format(obj, obj.name, err))
    else:
        print('message {} successfully produced to {} [{}] at offset {}'.format(obj, msg.topic(), msg.partition(), msg.offset()))