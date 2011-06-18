import pika, json, time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def send_message(battle_id, obj):
    exc_name = 'fswars_%s' % battle_id

    channel.exchange_declare(exchange=exc_name, type='fanout')

#    result = channel.queue_declare(exclusive=True)
#    channel.queue_bind(exchange=exc_name,
#                       queue=result.method.queue)

    channel.basic_publish(exchange=exc_name,
                          routing_key='',
                          body=json.dumps(obj))

def test_messages(times, battle_id=1):
    for i in range(times):
        send_message(battle_id, i)
        time.sleep(0.5)
