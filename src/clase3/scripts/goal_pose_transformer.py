#!/usr/bin/env python3

import rclpy

from rclpy.node import Node

from geometry_msgs.msg import PoseStamped

from tf2_ros import Buffer, TransformListener
from tf2_ros import TransformException

from tf2_geometry_msgs import do_transform_pose_stamped


class GoalPoseTransformer(Node):

    def __init__(self):
        super().__init__("goal_pose_transformer")

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.subscription = self.create_subscription(
            PoseStamped,
            "/goal_pose",
            self.callback,
            10
        )

    def callback(self, msg):

        try:
            transform = self.tf_buffer.lookup_transform(
                "world",                 # frame destino
                msg.header.frame_id,     # frame origen
                rclpy.time.Time()        # última transformación disponible
            )

            pose_world = do_transform_pose_stamped(msg, transform)

            p = pose_world.pose.position
            q = pose_world.pose.orientation

            self.get_logger().info(
                f"Posición en world : ({p.x:.3f}, {p.y:.3f}, {p.z:.3f})"
            )

            self.get_logger().info(
                f"Cuaternión en world: ({q.x:.4f}, {q.y:.4f}, {q.z:.4f}, {q.w:.4f})"
            )

        except TransformException as ex:
            self.get_logger().warn(str(ex))


def main():
    rclpy.init()

    node = GoalPoseTransformer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()