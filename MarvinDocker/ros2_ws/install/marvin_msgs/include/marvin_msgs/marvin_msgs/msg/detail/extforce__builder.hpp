// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from marvin_msgs:msg/Extforce.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__EXTFORCE__BUILDER_HPP_
#define MARVIN_MSGS__MSG__DETAIL__EXTFORCE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "marvin_msgs/msg/detail/extforce__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace marvin_msgs
{

namespace msg
{

namespace builder
{

class Init_Extforce_eef_ext_force
{
public:
  explicit Init_Extforce_eef_ext_force(::marvin_msgs::msg::Extforce & msg)
  : msg_(msg)
  {}
  ::marvin_msgs::msg::Extforce eef_ext_force(::marvin_msgs::msg::Extforce::_eef_ext_force_type arg)
  {
    msg_.eef_ext_force = std::move(arg);
    return std::move(msg_);
  }

private:
  ::marvin_msgs::msg::Extforce msg_;
};

class Init_Extforce_joint_ext_force
{
public:
  explicit Init_Extforce_joint_ext_force(::marvin_msgs::msg::Extforce & msg)
  : msg_(msg)
  {}
  Init_Extforce_eef_ext_force joint_ext_force(::marvin_msgs::msg::Extforce::_joint_ext_force_type arg)
  {
    msg_.joint_ext_force = std::move(arg);
    return Init_Extforce_eef_ext_force(msg_);
  }

private:
  ::marvin_msgs::msg::Extforce msg_;
};

class Init_Extforce_header
{
public:
  Init_Extforce_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Extforce_joint_ext_force header(::marvin_msgs::msg::Extforce::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Extforce_joint_ext_force(msg_);
  }

private:
  ::marvin_msgs::msg::Extforce msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::msg::Extforce>()
{
  return marvin_msgs::msg::builder::Init_Extforce_header();
}

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__EXTFORCE__BUILDER_HPP_
