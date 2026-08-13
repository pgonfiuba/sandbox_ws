#include <geometry_msgs/msg/pose_stamped.hpp>
#include <memory>
#include <string>
#include <vector>
#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.hpp>
#include <moveit/planning_scene_interface/planning_scene_interface.hpp>
#include <moveit_msgs/msg/collision_object.hpp>
#include <shape_msgs/msg/solid_primitive.hpp>

// =====================================================================
// GOAL - modificar estos valores
// =====================================================================
static constexpr char PLANNING_GROUP[] = "arm";
static constexpr char EE_LINK[] = "tool0";
static constexpr char REF_FRAME[] = "base_link";

static constexpr double GOAL_X  = 0.261;
static constexpr double GOAL_Y  = -0.176;
static constexpr double GOAL_Z  = 0.168;
static constexpr double GOAL_QX = 1.0;
static constexpr double GOAL_QY = 0.0;
static constexpr double GOAL_QZ = 0.0;
static constexpr double GOAL_QW = 0.0;
// =====================================================================

// =====================================================================
// OBSTACLES - modificar / agregar / borrar entradas libremente.
//   type: 'b' = box (dims = {sx, sy, sz})
//         's' = sphere (dims = {radius})
//   pose está en el frame REF_FRAME, orientación identidad.
// =====================================================================
struct Obstacle
{
  std::string id;
  char type;
  double x, y, z;
  std::vector<double> dims;
};

static const std::vector<Obstacle> OBSTACLES = {
  {"mesa",   'b', 0.20,  0.00, 0.02, {0.30, 0.30, 0.02}},
  {"pilar",  'b', 0.15, -0.10, 0.15, {0.03, 0.03, 0.20}},
  {"pelota", 's', 0.05, -0.15, 0.20, {0.04}},
};
// =====================================================================

static moveit_msgs::msg::CollisionObject make_collision_object(
  const Obstacle & o, const std::string & frame_id)
{
  moveit_msgs::msg::CollisionObject co;
  co.header.frame_id = frame_id;
  co.id = o.id;

  shape_msgs::msg::SolidPrimitive prim;
  if (o.type == 's') {
    prim.type = shape_msgs::msg::SolidPrimitive::SPHERE;
    prim.dimensions = {o.dims.at(0)};
  } else {
    prim.type = shape_msgs::msg::SolidPrimitive::BOX;
    prim.dimensions = {o.dims.at(0), o.dims.at(1), o.dims.at(2)};
  }

  geometry_msgs::msg::Pose pose;
  pose.position.x = o.x;
  pose.position.y = o.y;
  pose.position.z = o.z;
  pose.orientation.w = 1.0;

  co.primitives.push_back(prim);
  co.primitive_poses.push_back(pose);
  co.operation = moveit_msgs::msg::CollisionObject::ADD;
  return co;
}

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  auto const node = std::make_shared<rclcpp::Node>(
    "hello_moveit_obstacles",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true)
  );

  auto const logger = rclcpp::get_logger("hello_moveit_obstacles");

  using moveit::planning_interface::MoveGroupInterface;
  using moveit::planning_interface::PlanningSceneInterface;

  auto arm_group_interface = MoveGroupInterface(node, PLANNING_GROUP);

  arm_group_interface.setPlanningPipelineId("ompl");
  arm_group_interface.setPlannerId("RRTConnectkConfigDefault");
  arm_group_interface.setPlanningTime(5.0);
  arm_group_interface.setMaxVelocityScalingFactor(1.0);
  arm_group_interface.setMaxAccelerationScalingFactor(1.0);
  arm_group_interface.setPoseReferenceFrame(REF_FRAME);
  arm_group_interface.setEndEffectorLink(EE_LINK);

  RCLCPP_INFO(logger, "Planning pipeline: %s", arm_group_interface.getPlanningPipelineId().c_str());
  RCLCPP_INFO(logger, "Planner ID: %s", arm_group_interface.getPlannerId().c_str());
  RCLCPP_INFO(logger, "Planning time: %.2f", arm_group_interface.getPlanningTime());

  PlanningSceneInterface psi;
  std::vector<moveit_msgs::msg::CollisionObject> objects;
  objects.reserve(OBSTACLES.size());
  for (auto const & o : OBSTACLES) {
    objects.push_back(make_collision_object(o, REF_FRAME));
  }
  bool const scene_ok = psi.applyCollisionObjects(objects);
  RCLCPP_INFO(logger, "Obstáculos publicados: %zu (ok=%s)",
              objects.size(), scene_ok ? "true" : "false");

  auto const target_pose = [&node]{
    geometry_msgs::msg::PoseStamped msg;
    msg.header.frame_id = REF_FRAME;
    msg.header.stamp = node->now();
    msg.pose.position.x = GOAL_X;
    msg.pose.position.y = GOAL_Y;
    msg.pose.position.z = GOAL_Z;
    msg.pose.orientation.x = GOAL_QX;
    msg.pose.orientation.y = GOAL_QY;
    msg.pose.orientation.z = GOAL_QZ;
    msg.pose.orientation.w = GOAL_QW;
    return msg;
  }();
  arm_group_interface.setPoseTarget(target_pose);

  auto const [success, plan] = [&arm_group_interface] {
    moveit::planning_interface::MoveGroupInterface::Plan msg;
    auto const ok = static_cast<bool>(arm_group_interface.plan(msg));
    return std::make_pair(ok, msg);
  }();

  if (success)
  {
    RCLCPP_INFO(logger, "Plan encontrado, ejecutando...");
    arm_group_interface.execute(plan);
  }
  else
  {
    RCLCPP_ERROR(logger, "Planning failed!");
  }

  rclcpp::shutdown();
  return 0;
}
