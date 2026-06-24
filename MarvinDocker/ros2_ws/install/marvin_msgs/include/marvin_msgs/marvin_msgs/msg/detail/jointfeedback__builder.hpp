// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from marvin_msgs:msg/Jointfeedback.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__BUILDER_HPP_
#define MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "marvin_msgs/msg/detail/jointfeedback__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace marvin_msgs
{

namespace msg
{

namespace builder
{

class Init_Jointfeedback_efforts
{
public:
  explicit Init_Jointfeedback_efforts(::marvin_msgs::msg::Jointfeedback & msg)
  : msg_(msg)
  {}
  ::marvin_msgs::msg::Jointfeedback efforts(::marvin_msgs::msg::Jointfeedback::_efforts_type arg)
  {
    msg_.efforts = std::move(arg);
    return std::move(msg_);
  }

private:
  ::marvin_msgs::msg::Jointfeedback msg_;
};

class Init_Jointfeedback_velocities
{
public:
  explicit Init_Jointfeedback_velocities(::marvin_msgs::msg::Jointfeedback & msg)
  : msg_(msg)
  {}
  Init_Jointfeedback_efforts velocities(::marvin_msgs::msg::Jointfeedback::_velocities_type arg)
  {
    msg_.velocities = std::move(arg);
    return Init_Jointfeedback_efforts(msg_);
  }

private:
  ::marvin_msgs::msg::Jointfeedback msg_;
};

class Init_Jointfeedback_positions
{
public:
  explicit Init_Jointfeedback_positions(::marvin_msgs::msg::Jointfeedback & msg)
  : msg_(msg)
  {}
  Init_Jointfeedback_velocities positions(::marvin_msgs::msg::Jointfeedback::_positions_type arg)
  {
    msg_.positions = std::move(arg);
    return Init_Jointfeedback_velocities(msg_);
  }

private:
  ::marvin_msgs::msg::Jointfeedback msg_;
};

class Init_Jointfeedback_header
{
public:
  Init_Jointfeedback_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Jointfeedback_positions header(::marvin_msgs::msg::Jointfeedback::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Jointfeedback_positions(msg_);
  }

private:
  ::marvin_msgs::msg::Jointfeedback msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::msg::Jointfeedback>()
{
  return marvin_msgs::msg::builder::Init_Jointfeedback_header();
}

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__BUILDER_HPP_
