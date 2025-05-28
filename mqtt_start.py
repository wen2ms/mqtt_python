from paho.mqtt.client import Client, MQTTMessage
from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(
        self,
        sub_topic: str,
        pub_topic: str,
        broker: str = "localhost",
        port: int = 1883,
    ):
        self.broker = broker
        self.port = port
        self.sub_topic = sub_topic
        self.pub_topic = pub_topic

        self.client: Client = mqtt.Client(CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(
        self,
        client: Client,
        userdata: object,
        flags: dict,
        reason_code: int,
        properties=None,
    ) -> None:
        print("Connected with result code", reason_code)
        client.subscribe(self.sub_topic)

    def on_message(self, client: Client, userdata: object, msg: MQTTMessage) -> None:
        payload: str = msg.payload.decode()
        print(f"Received message: '{payload}' on topic '{msg.topic}'")

        if payload == "ping":
            response: str = "pong"
            client.publish(self.pub_topic, response)

    def run(self) -> None:
        self.client.connect(self.broker, self.port)
        print("MQTT responder started. Waiting for messages...")
        self.client.loop_forever()


if __name__ == "__main__":
    responder = MQTTClient("test/topic", "test/response")

    responder.run()
