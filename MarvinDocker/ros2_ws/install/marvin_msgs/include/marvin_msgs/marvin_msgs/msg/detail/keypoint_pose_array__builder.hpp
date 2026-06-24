// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from marvin_msgs:msg/KeypointPoseArray.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__KEYPOINT_POSE_ARRAY__BUILDER_HPP_
#define MARVIN_MSGS__MSG__DETAIL__KEYPOINT_POSE_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "marvin_msgs/msg/detail/keypoint_pose_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace marvin_msgs
{

namespace msg
{

namespace builder
{

class Init_KeypointPoseArray_poses
{
public:
  explicit Init_KeypointPoseArray_poses(::marvin_msgs::msg::KeypointPoseArray & msg)
  : msg_(msg)
  {}
  ::marvin_msgs::msg::KeypointPoseArray poses(::marvin_msgs::msg::KeypointPoseArray::_poses_type arg)
  {
    msg_.poses = std::move(arg);
    return std::move(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPoseArray msg_;
};

class Init_KeypointPoseArray_header
{
public:
  Init_KeypointPoseArray_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_KeypointPoseArray_poses header(::marvin_msgs::msg::KeypointPoseArray::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_KeypointPoseArray_poses(msg_);
  }

private:
  ::marvin_msgs::msg::KeypointPoseArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::msg::KeypointPoseArray>()
{
  return marvin_msgs::msg::builder::Init_KeypointPoseArray_header();
}

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__KEYPOINT_POSE_ARRAY__BUILDER_HPP_
