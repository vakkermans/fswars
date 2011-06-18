package com.freesoundwars.comet;

import java.io.IOException;

import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConsumerCancelledException;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.client.ShutdownSignalException;

public class RabbitMQTest {

    ConnectionFactory factory;
    Connection conn;
    Channel channel;

    private final static String username = "fswars";
    private final static String password = "fswars";
    private final static String virtualHost = "/";

    RabbitMQTest() {

    }

    public void startListening() throws IOException, ShutdownSignalException, ConsumerCancelledException, InterruptedException {
        factory = new ConnectionFactory();
        factory.setHost("127.0.0.1");
        conn = factory.newConnection();
        channel = conn.createChannel();
        channel.queueDeclare("fswars_1", false, false, false, null);

        QueueingConsumer consumer = new QueueingConsumer(channel);
        channel.basicConsume("fswars_1", true, consumer);

        while (true) {
            QueueingConsumer.Delivery delivery;
            delivery = consumer.nextDelivery();
            String message = new String(delivery.getBody());
            System.out.println(" [x] Received '" + message + "'");
        }

    }

    public static void main(String[] argv) throws ShutdownSignalException, ConsumerCancelledException, IOException, InterruptedException {
        RabbitMQTest test = new RabbitMQTest();
        test.startListening();
    }


}
