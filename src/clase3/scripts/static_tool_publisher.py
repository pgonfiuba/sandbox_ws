import numpy as np
import rclpy
from rclpy.node import Node

from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class StaticToolPublisher(Node):

    def __init__(self):
        super().__init__('static_tool_publisher')
        self.broadcaster = StaticTransformBroadcaster(self)
        self.publish_static_tf()

    def publish_static_tf(self):
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'tool0'
        t.child_frame_id = 'tool'

        # 150 mm en X
        t.transform.translation.x = 0.15
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0

        # Z para abajo
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = np.sqrt(2)/2
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = np.sqrt(2)/2

        self.broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = StaticToolPublisher()

    # importante: dejar que el nodo viva un poco
    rclpy.spin_once(node, timeout_sec=0.5)

    rclpy.shutdown()


if __name__ == '__main__':
    main()