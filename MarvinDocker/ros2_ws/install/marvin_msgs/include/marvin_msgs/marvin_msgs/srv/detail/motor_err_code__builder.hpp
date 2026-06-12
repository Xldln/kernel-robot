// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from marvin_msgs:srv/MotorErrCode.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__BUILDER_HPP_
#define MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "marvin_msgs/srv/detail/motor_err_code__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace marvin_msgs
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::srv::MotorErrCode_Request>()
{
  return ::marvin_msgs::srv::MotorErrCode_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace marvin_msgs


namespace marvin_msgs
{

namespace srv
{

namespace builder
{

class Init_MotorErrCode_Response_message
{
public:
  explicit Init_MotorErrCode_Response_message(::marvin_msgs::srv::MotorErrCode_Response & msg)
  : msg_(msg)
  {}
  ::marvin_msgs::srv::MotorErrCode_Response message(::marvin_msgs::srv::MotorErrCode_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::marvin_msgs::srv::MotorErrCode_Response msg_;
};

class Init_MotorErrCode_Response_success
{
public:
  explicit Init_MotorErrCode_Response_success(::marvin_msgs::srv::MotorErrCode_Response & msg)
  : msg_(msg)
  {}
  Init_MotorErrCode_Response_message success(::marvin_msgs::srv::MotorErrCode_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MotorErrCode_Response_message(msg_);
  }

private:
  ::marvin_msgs::srv::MotorErrCode_Response msg_;
};

class Init_MotorErrCode_Response_error_code
{
public:
  Init_MotorErrCode_Response_error_code()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorErrCode_Response_success error_code(::marvin_msgs::srv::MotorErrCode_Response::_error_code_type arg)
  {
    msg_.error_code = std::move(arg);
    return Init_MotorErrCode_Response_success(msg_);
  }

private:
  ::marvin_msgs::srv::MotorErrCode_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::marvin_msgs::srv::MotorErrCode_Response>()
{
  return marvin_msgs::srv::builder::Init_MotorErrCode_Response_error_code();
}

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__BUILDER_HPP_
