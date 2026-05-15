import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    # Ruta al URDF
    urdf_file = os.path.join(
        get_package_share_directory('clase4'),
        'robots','mycobot_320_m5_2022',
        'mycobot_320_m5_2022.urdf'
    )

    # Leer contenido del URDF
    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description}
            ]
        ),

        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d',
                os.path.join(
                    get_package_share_directory('clase4'),
                    'config',
                    'display.rviz'
                )
            ]
        )
    ])