// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from marvin_msgs:msg/Jointcmd.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTCMD__BUILDER_HPP_
#define MARVIN_MSGS__MSG__DETAIL__JOINTCMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "marvin_msgs/msg/detail/jointcmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace marvin_msgs
{

namespace msg
{

namespace builder
{

class Init_Jointcmd_positions
{
public:
  explicit Init_Jointcmd_positions(::marvin_msgs::msg::Jointcmd & msg)
  : msg_(msg)
  {}
  ::marvin_msgs::msg::Jointcmd positions(::marvin_msgs::msg::Jointcmd::_positions_type arg)
  {
    msg_.positions = std::move(arg);
    return std::move(msg_);
  }

private:
  ::marvin_msgs::msg::Jointcmd msg_;
};

class Init_Jointcmd_header
{
public:
  Init_Jointcmd_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Jointcmd_positions header(::marvin_msgs::msg::Jointcmd::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Jointcmd_positions(msg_);
  }

private:
  ::marvin_msgs::msg::Jointcmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::msg::Jointcmd>()
{
  return marvin_msgs::msg::builder::Init_Jointcmd_header();
}

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTCMD__BUILDER_HPP_
