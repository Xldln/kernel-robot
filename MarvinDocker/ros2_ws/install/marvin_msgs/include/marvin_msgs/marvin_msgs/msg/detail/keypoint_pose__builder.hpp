// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from marvin_msgs:msg/KeypointPose.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__KEYPOINT_POSE__BUILDER_HPP_
#define MARVIN_MSGS__MSG__DETAIL__KEYPOINT_POSE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "marvin_msgs/msg/detail/keypoint_pose__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace marvin_msgs
{

namespace msg
{

namespace builder
{

class Init_KeypointPose_gripper_value
{
public:
  explicit Init_KeypointPose_gripper_value(::marvin_msgs::msg::KeypointPose & msg)
  : msg_(msg)
  {}
  ::marvin_msgs::msg::KeypointPose gripper_value(::marvin_msgs::msg::KeypointPose::_gripper_value_type arg)
  {
    msg_.gripper_value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPose msg_;
};

class Init_KeypointPose_speed
{
public:
  explicit Init_KeypointPose_speed(::marvin_msgs::msg::KeypointPose & msg)
  : msg_(msg)
  {}
  Init_KeypointPose_gripper_value speed(::marvin_msgs::msg::KeypointPose::_speed_type arg)
  {
    msg_.speed = std::move(arg);
    return Init_KeypointPose_gripper_value(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPose msg_;
};

class Init_KeypointPose_constraints
{
public:
  explicit Init_KeypointPose_constraints(::marvin_msgs::msg::KeypointPose & msg)
  : msg_(msg)
  {}
  Init_KeypointPose_speed constraints(::marvin_msgs::msg::KeypointPose::_constraints_type arg)
  {
    msg_.constraints = std::move(arg);
    return Init_KeypointPose_speed(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPose msg_;
};

class Init_KeypointPose_poses
{
public:
  explicit Init_KeypointPose_poses(::marvin_msgs::msg::KeypointPose & msg)
  : msg_(msg)
  {}
  Init_KeypointPose_constraints poses(::marvin_msgs::msg::KeypointPose::_poses_type arg)
  {
    msg_.poses = std::move(arg);
    return Init_KeypointPose_constraints(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPose msg_;
};

class Init_KeypointPose_arm
{
public:
  explicit Init_KeypointPose_arm(::marvin_msgs::msg::KeypointPose & msg)
  : msg_(msg)
  {}
  Init_KeypointPose_poses arm(::marvin_msgs::msg::KeypointPose::_arm_type arg)
  {
    msg_.arm = std::move(arg);
    return Init_KeypointPose_poses(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPose msg_;
};

class Init_KeypointPose_name
{
public:
  Init_KeypointPose_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_KeypointPose_arm name(::marvin_msgs::msg::KeypointPose::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_KeypointPose_arm(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPose msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::msg::KeypointPose>()
{
  return marvin_msgs::msg::builder::Init_KeypointPose_name();
}

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__KEYPOINT_POSE__BUILDER_HPP_
