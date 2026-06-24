// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from marvin_msgs:srv/Velratio.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__VELRATIO__TRAITS_HPP_
#define MARVIN_MSGS__SRV__DETAIL__VELRATIO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "marvin_msgs/srv/detail/velratio__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace marvin_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const Velratio_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: vel
  {
    out << "vel: ";
    rosidl_generator_traits::value_to_yaml(msg.vel, out);
    out << ", ";
  }

  // member: acc
  {
    out << "acc: ";
    rosidl_generator_traits::value_to_yaml(msg.acc, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Velratio_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: vel
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "vel: ";
    rosidl_generator_traits::value_to_yaml(msg.vel, out);
    out << "\n";
  }

  // member: acc
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "acc: ";
    rosidl_generator_traits::value_to_yaml(msg.acc, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Velratio_Request & msg, bool use_flow_style = false)
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
  const marvin_msgs::srv::Velratio_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::srv::Velratio_Request & msg)
{
  return marvin_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::srv::Velratio_Request>()
{
  return "marvin_msgs::srv::Velratio_Request";
}

template<>
inline const char * name<marvin_msgs::srv::Velratio_Request>()
{
  return "marvin_msgs/srv/Velratio_Request";
}

template<>
struct has_fixed_size<marvin_msgs::srv::Velratio_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<marvin_msgs::srv::Velratio_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<marvin_msgs::srv::Velratio_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace marvin_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const Velratio_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: error_code
  {
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
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
  const Velratio_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: error_code
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "error_code: ";
    rosidl_generator_traits::value_to_yaml(msg.error_code, out);
    out << "\n";
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

inline std::string to_yaml(const Velratio_Response & msg, bool use_flow_style = false)
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
  const marvin_msgs::srv::Velratio_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::srv::Velratio_Response & msg)
{
  return marvin_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::srv::Velratio_Response>()
{
  return "marvin_msgs::srv::Velratio_Response";
}

template<>
inline const char * name<marvin_msgs::srv::Velratio_Response>()
{
  return "marvin_msgs/srv/Velratio_Response";
}

template<>
struct has_fixed_size<marvin_msgs::srv::Velratio_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<marvin_msgs::srv::Velratio_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<marvin_msgs::srv::Velratio_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<marvin_msgs::srv::Velratio>()
{
  return "marvin_msgs::srv::Velratio";
}

template<>
inline const char * name<marvin_msgs::srv::Velratio>()
{
  return "marvin_msgs/srv/Velratio";
}

template<>
struct has_fixed_size<marvin_msgs::srv::Velratio>
  : std::integral_constant<
    bool,
    has_fixed_size<marvin_msgs::srv::Velratio_Request>::value &&
    has_fixed_size<marvin_msgs::srv::Velratio_Response>::value
  >
{
};

template<>
struct has_bounded_size<marvin_msgs::srv::Velratio>
  : std::integral_constant<
    bool,
    has_bounded_size<marvin_msgs::srv::Velratio_Request>::value &&
    has_bounded_size<marvin_msgs::srv::Velratio_Response>::value
  >
{
};

template<>
struct is_service<marvin_msgs::srv::Velratio>
  : std::true_type
{
};

template<>
struct is_service_request<marvin_msgs::srv::Velratio_Request>
  : std::true_type
{
};

template<>
struct is_service_response<marvin_msgs::srv::Velratio_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MARVIN_MSGS__SRV__DETAIL__VELRATIO__TRAITS_HPP_
