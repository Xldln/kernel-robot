// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from marvin_msgs:msg/Collimarker.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__BUILDER_HPP_
#define MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "marvin_msgs/msg/detail/collimarker__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace marvin_msgs
{

namespace msg
{

namespace builder
{

class Init_Collimarker_vectors
{
public:
  Init_Collimarker_vectors()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::marvin_msgs::msg::Collimarker vectors(::marvin_msgs::msg::Collimarker::_vectors_type arg)
  {
    msg_.vectors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::marvin_msgs::msg::Collimarker msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::msg::Collimarker>()
{
  return marvin_msgs::msg::builder::Init_Collimarker_vectors();
}

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__BUILDER_HPP_
