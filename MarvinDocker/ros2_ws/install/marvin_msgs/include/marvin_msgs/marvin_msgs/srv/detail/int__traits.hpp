// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from marvin_msgs:srv/Int.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__INT__TRAITS_HPP_
#define MARVIN_MSGS__SRV__DETAIL__INT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "marvin_msgs/srv/detail/int__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace marvin_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const Int_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: data
  {
    out << "data: ";
    rosidl_generator_traits::value_to_yaml(msg.data, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Int_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data: ";
    rosidl_generator_traits::value_to_yaml(msg.data, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Int_Request & msg, bool use_flow_style = false)
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
  const marvin_msgs::srv::Int_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::srv::Int_Request & msg)
{
  return marvin_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::srv::Int_Request>()
{
  return "marvin_msgs::srv::Int_Request";
}

template<>
inline const char * name<marvin_msgs::srv::Int_Request>()
{
  return "marvin_msgs/srv/Int_Request";
}

template<>
struct has_fixed_size<marvin_msgs::srv::Int_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<marvin_msgs::srv::Int_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<marvin_msgs::srv::Int_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace marvin_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const Int_Response & msg,
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
  const Int_Response & msg,
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

inline std::string to_yaml(const Int_Response & msg, bool use_flow_style = false)
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
  const marvin_msgs::srv::Int_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::srv::Int_Response & msg)
{
  return marvin_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::srv::Int_Response>()
{
  return "marvin_msgs::srv::Int_Response";
}

template<>
inline const char * name<marvin_msgs::srv::Int_Response>()
{
  return "marvin_msgs/srv/Int_Response";
}

template<>
struct has_fixed_size<marvin_msgs::srv::Int_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<marvin_msgs::srv::Int_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<marvin_msgs::srv::Int_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<marvin_msgs::srv::Int>()
{
  return "marvin_msgs::srv::Int";
}

template<>
inline const char * name<marvin_msgs::srv::Int>()
{
  return "marvin_msgs/srv/Int";
}

template<>
struct has_fixed_size<marvin_msgs::srv::Int>
  : std::integral_constant<
    bool,
    has_fixed_size<marvin_msgs::srv::Int_Request>::value &&
    has_fixed_size<marvin_msgs::srv::Int_Response>::value
  >
{
};

template<>
struct has_bounded_size<marvin_msgs::srv::Int>
  : std::integral_constant<
    bool,
    has_bounded_size<marvin_msgs::srv::Int_Request>::value &&
    has_bounded_size<marvin_msgs::srv::Int_Response>::value
  >
{
};

template<>
struct is_service<marvin_msgs::srv::Int>
  : std::true_type
{
};

template<>
struct is_service_request<marvin_msgs::srv::Int_Request>
  : std::true_type
{
};

template<>
struct is_service_response<marvin_msgs::srv::Int_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // MARVIN_MSGS__SRV__DETAIL__INT__TRAITS_HPP_
