import rclpy
from rclpy.node import Node
from dynamixel_sdk_custom_interfaces.msg import SetPosition
from std_msgs.msg import Float64

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('conversion_node')
        self.subscribers = []
        self.float_publishers = []  # Corrected variable name

        for i in range(1, 10):
            topic_name = f"Robot/Cable{i}/state/displacement"
            subscriber = self.create_subscription(SetPosition, topic_name, self.set_position_callback, 10)
            self.subscribers.append(subscriber)

            float_topic_name = f"Sim/Cable{i}/state/displacement"
            float_publisher = self.create_publisher(Float64, float_topic_name, 10)
            self.float_publishers.append(float_publisher)

    def set_position_callback(self, msg):
        self.get_logger().info(f"Received: ID = {msg.id}, Position = {msg.position}")

        # Convert and publish in Float64 form using rospy
        float_msg = Float64()
        float_msg.data = float(msg.position)
        
        # Get the corresponding float_publisher based on ID
        id_index = msg.id - 1
        if id_index >= 0 and id_index < len(self.float_publishers):
            float_publisher = self.float_publishers[id_index]
            float_publisher.publish(float_msg)
        else:
            self.get_logger().warn(f"No corresponding float_publisher for ID = {msg.id}")
        

def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

