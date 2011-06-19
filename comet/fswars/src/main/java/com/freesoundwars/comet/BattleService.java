package com.freesoundwars.comet;

import java.io.IOException;
import java.util.Map;
import java.util.HashMap;

import org.cometd.bayeux.Message;
import org.cometd.bayeux.server.BayeuxServer;
import org.cometd.bayeux.server.ServerSession;
import org.cometd.server.AbstractService;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;

public class BattleService extends AbstractService
{

    ConnectionFactory factory;
    Connection conn;
    Channel channel;

    public BattleService(BayeuxServer bayeux) throws IOException
    {
        super(bayeux, "updates");
        addService("/service/updates", "processBattle");
    }

    public void processBattle(ServerSession remote, Message message) throws IOException, ShutdownSignalException, ConsumerCancelledException, InterruptedException
    {
        Map<String, Object> input = message.getDataAsMap();
        String battle_id = (String)input.get("battle_id");
        System.out.println(" [x] Opening event stream for battle id " + battle_id);

        factory = new ConnectionFactory();
        factory.setHost("127.0.0.1");
        conn = factory.newConnection();
        channel = conn.createChannel();

        String exchange = "fswars_" + battle_id;
        channel.exchangeDeclare(exchange, "fanout");
        String queue = channel.queueDeclare().getQueue();
        channel.queueBind(queue, exchange, "");

        QueueingConsumer consumer = new QueueingConsumer(channel);
        channel.basicConsume(queue, true, consumer);



        while (true) {
            QueueingConsumer.Delivery delivery = consumer.nextDelivery();
            String rabbit_message = new String(delivery.getBody());
            System.out.println(" [x] Received from RabbitMQ'" + rabbit_message + "'");

            Map<String, Object> output = new HashMap<String, Object>();
            output.put("command", rabbit_message);
            remote.deliver(getServerSession(), "/updates", output, null);
        }



    }
}
