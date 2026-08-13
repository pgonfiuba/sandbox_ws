# Clase 7

## Objetivo

Ejecutar la simulación en Gazebo con ROS 2, MoveIt y visualización en RViz/PlotJuggler, mostrando cómo se articula la descripción del robot, el control y la planificación del

- doble péndulo
- cobot myCobot 300

![Cobot esquivando obstaculos](docs/mycobot_plan.png)
![Cobot esquivando obstaculos](docs/mycobot_execute.png)

## Contenido

- `launch/mycobot_launch.py`: arranca Gazebo, publica el URDF generado por Xacro, spawnea el robot en el mundo, lanza los controladores y MoveIt, y abre RViz y PlotJuggler.
- `launch/dp_launch.py`: ejemplo adicional de doble péndulo con Gazebo, `robot_state_publisher` y control ros2_control.
- `robot_description/mycobot_320_m5_2022/mycobot_320_m5_2022.xacro`: definición del robot myCobot 320 M5 con componentes visuales, cinemática y configuración de control.
- `config/mycobot_320_m5_2022/ros2_controllers.yaml`: parámetros de los controladores que se cargan en el launch.
- `config/display.rviz`: configuración de RViz usada por el launch principal.
- `config/plotjuggler_layout.xml`: layout de PlotJuggler para monitoreo de topics.
- `worlds/`: mundos disponibles para Gazebo, incluyendo `mundo_escritorio.world` usado por defecto.
- `src/hello_moveit.cpp`: ejemplo mínimo en C++ que usa `MoveGroupInterface` para planificar y ejecutar una pose con MoveIt.
- `scripts/hello_moveit.py`: mismo ejemplo en Python usando el cliente de acción `/move_action`. Ambos apuntan al grupo `arm` del myCobot y envían la misma pose objetivo, para comparar las dos APIs.
- `src/hello_moveit_obstacles.cpp`: variante en C++ que además publica un `PlanningScene` con obstáculos (caja de mesa, pilar y esfera) usando `PlanningSceneInterface`. El planner OMPL/RRTConnect debe rodearlos para llegar a la misma pose objetivo.
- `scripts/hello_moveit_obstacles.py`: equivalente en Python; publica los mismos obstáculos mediante el servicio `/apply_planning_scene`. Editá el bloque `OBSTACLES` (arriba de cada archivo) para agregar/mover/quitar cajas y esferas.

## Compilación

```bash
colcon build --packages-select clase7 --symlink-install
source install/setup.bash
```bash

## Ejecución

- Simulación principal del myCobot con Gazebo, MoveIt, RViz y PlotJuggler:

```bash
  ros2 launch clase7 mycobot_launch.py
```

- Cambiar el mundo de Gazebo:

```bash
  ros2 launch clase7 mycobot_launch.py world_name:=mundo_obstaculos.world
```  

- En otra terminal, enviar la pose objetivo con MoveIt desde C++ (usa `MoveGroupInterface`, necesita que la launch le cargue `robot_description*` y `kinematics.yaml`):

```bash
  ros2 launch clase7 hello_moveit.launch.py
```

- Equivalente en Python (habla directo con la acción `/move_action`, no requiere parámetros de MoveIt):

```bash
  ros2 run clase7 hello_moveit.py
```

- Versión con obstáculos en C++ (misma pose objetivo pero el planner tiene que rodear cajas y esferas):

```bash
  ros2 launch clase7 hello_moveit_obstacles.launch.py
```

- Versión con obstáculos en Python:

```bash
  ros2 run clase7 hello_moveit_obstacles.py
```

## Qué explorar

- `launch/mycobot_launch.py`: cómo se arma el flujo completo de Gazebo, controladores, MoveIt y visualización.
- `robot_description/mycobot_320_m5_2022/mycobot_320_m5_2022.xacro`: estructura del robot y parámetros de los links/joints.
- `config/mycobot_320_m5_2022/ros2_controllers.yaml`: definición de los controladores que se cargan en `controller_manager`.
- `config/mycobot_320_m5_2022/moveit`: configuraciones varias de la planificación de trayectorias.
- `worlds/mundo_escritorio.world` y `worlds/mundo_obstaculos.world`: el entorno físico de la simulación.
- `src/hello_moveit.cpp` y `scripts/hello_moveit.py`: dos implementaciones equivalentes del mismo ejemplo de MoveIt, una en C++ (API `MoveGroupInterface`) y otra en Python (cliente de acción `/move_action`).
- `src/hello_moveit_obstacles.cpp` y `scripts/hello_moveit_obstacles.py`: variantes que suman obstáculos al `PlanningScene`. Comparar con `diff` contra las versiones sin obstáculos aísla exactamente el código nuevo (helper + bloque `OBSTACLES` + llamada a `PlanningSceneInterface` / `/apply_planning_scene`).

