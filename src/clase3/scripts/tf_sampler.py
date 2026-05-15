import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

import time
import matplotlib.pyplot as plt


class FrameListener(Node):
    def __init__(self):
        super().__init__('tf2_sampler')

        self.target_frame = 'tool0'
        self.source_frame = 'base_link'

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # parámetros de muestreo
        self.dt = 0.1
        self.duration = 10.0
        self.start_time = time.time()

        # almacenamiento de datos
        self.t_data = []
        self.x_data = []
        self.y_data = []
    
        self.timer = self.create_timer(self.dt, self.on_timer)

    def on_timer(self):

        elapsed = time.time() - self.start_time

        # Condición de corte
        if elapsed > self.duration:
            self.get_logger().info("Fin de adquisición. Graficando...")
            self.plot_data()
            rclpy.shutdown()
            return
        
        # Como el TF puede no estar disponible inmediatamente, verificamos antes de intentar obtenerlo
        if not self.tf_buffer.can_transform(
            self.source_frame,
            self.target_frame,
            rclpy.time.Time()
        ):
            self.get_logger().warn("Esperando TF...")
            return

        try:
            transform = self.tf_buffer.lookup_transform(
                self.source_frame,
                self.target_frame,
                rclpy.time.Time()
            )
            trans = transform.transform.translation

            # guardar datos
            self.t_data.append(elapsed)
            self.x_data.append(trans.x)
            self.y_data.append(trans.y)

        except TransformException as ex:
            self.get_logger().warn(f'No transform: {ex}')

    def plot_data(self):
        plt.plot(self.t_data, self.x_data, label='x')
        plt.plot(self.t_data, self.y_data, label='y')

        plt.xlabel('Tiempo [s]')
        plt.ylabel('Posición [m]')
        plt.legend()
        plt.title('tool0 respecto a base_link')
        plt.show()


def main():
    rclpy.init()
    node = FrameListener()
    rclpy.spin(node)


if __name__ == '__main__':
    main()