// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from marvin_msgs:srv/MotorErrCode.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__TRAITS_HPP_
#define MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "marvin_msgs/srv/detail/motor_err_code__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace marvin_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MotorErrCode_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorErrCode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorErrCode_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace marvin_msgs

namespace rosidl_generator_traits
{

[[deprecated("use marvin_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const marvin_msgs::srv::MotorErrCode_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::srv::MotorErrCode_Request & msg)
{
  return marvin_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::srv::MotorErrCode_Request>()
{
  return "marvin_msgs::srv::MotorErrCode_Request";
}

template<>
inline const char * name<marvin_msgs::srv::MotorErrCode_Request>()
{
  return "marvin_msgs/srv/MotorErrCode_Request";
}

template<>
struct has_fixed_size<marvin_msgs::srv::MotorErrCode_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<marvin_msgs::srv::MotorErrCode_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<marvin_msgs::srv::MotorErrCode_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace marvin_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const MotorErrCode_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: error_code
  {
    if (msg.error_code.size() == 0) {
      out << "error_code: []";
    } else {
      out << "error_code: [";
      size_t pending_items = msg.error_code.size();
      for (auto item : msg.error_code) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MotorErrCode_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: error_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.error_code.size() == 0) {
      out << "error_code: []\n";
    } else {
      out << "error_code:\n";
      for (auto item : msg.error_code) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MotorErrCode_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace marvin_msgs

namespace rosidl_generator_traits
{

[[deprecated("use marvin_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const marvin_msgs::srv::MotorErrCode_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::srv::MotorErrCode_Response & msg)
{
  return marvin_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::srv::MotorErrCode_Response>()
{
  return "marvin_msgs::srv::MotorErrCode_Response";
}

template<>
inline const char * name<marvin_msgs::srv::MotorErrCode_Response>()
{
  return "marvin_msgs/srv/MotorErrCode_Response";
}

template<>
struct has_fixed_size<marvin_msgs::srv::MotorErrCode_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<marvin_msgs::srv::MotorErrCode_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<marvin_msgs::srv::MotorErrCode_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<marvin_msgs::srv::MotorErrCode>()
{
  return "marvin_msgs::srv::MotorErrCode";
}

template<>
inline const char * name<marvin_msgs::srv::MotorErrCode>()
{
  return "marvin_msgs/srv/MotorErrCode";
}

template<>
struct has_fixed_size<marvin_msgs::srv::MotorErrCode>
  : std::integral_constant<
    bool,
    has_fixed_size<marvin_msgs::srv::MotorErrCode_Request>::value &&
    has_fixed_size<marvin_msgs::srv::MotorErrCode_Response>::value
  >
{
};

template<>
struct has_bounded_size<marvin_msgs::srv::MotorErrCode>
  : std::integral_constant<
    bool,
    has_bounded_size<marvin_msgs::srv::MotorErrCode_Request>::value &&
    has_bounded_size<marvin_msgs::srv::MotorErrCode_Response>::value
  >
{
};

template<>
struct is_service<marvin_msgs::srv::MotorErrCode>
  : std::true_type
{
};

template<>
struct is_service_request<marvin_msgs::srv::MotorErrCode_Request>
  : std::true_type
{
};

template<>
struct is_service_response<marvin_msgs::srv::MotorErrCode_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__TRAITS_HPP_
