import pika, json, time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def send_message(battle_id, obj, already_json_dumped=False):
    exc_name = str('fswars_%s' % battle_id)
    channel.exchange_declare(exchange=exc_name, type='fanout')
    channel.basic_publish(exchange=exc_name,
                          routing_key='',
                          body=obj if already_json_dumped else json.dumps(obj))

def test_messages(times, battle_id=1):
    for i in range(times):
        send_message(battle_id, i)
        time.sleep(0.5)
