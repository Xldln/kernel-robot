// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from marvin_msgs:msg/Extforce.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__EXTFORCE__TRAITS_HPP_
#define MARVIN_MSGS__MSG__DETAIL__EXTFORCE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "marvin_msgs/msg/detail/extforce__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace marvin_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Extforce & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: joint_ext_force
  {
    if (msg.joint_ext_force.size() == 0) {
      out << "joint_ext_force: []";
    } else {
      out << "joint_ext_force: [";
      size_t pending_items = msg.joint_ext_force.size();
      for (auto item : msg.joint_ext_force) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: eef_ext_force
  {
    if (msg.eef_ext_force.size() == 0) {
      out << "eef_ext_force: []";
    } else {
      out << "eef_ext_force: [";
      size_t pending_items = msg.eef_ext_force.size();
      for (auto item : msg.eef_ext_force) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Extforce & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: joint_ext_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.joint_ext_force.size() == 0) {
      out << "joint_ext_force: []\n";
    } else {
      out << "joint_ext_force:\n";
      for (auto item : msg.joint_ext_force) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: eef_ext_force
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.eef_ext_force.size() == 0) {
      out << "eef_ext_force: []\n";
    } else {
      out << "eef_ext_force:\n";
      for (auto item : msg.eef_ext_force) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Extforce & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace marvin_msgs

namespace rosidl_generator_traits
{

[[deprecated("use marvin_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const marvin_msgs::msg::Extforce & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::msg::Extforce & msg)
{
  return marvin_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::msg::Extforce>()
{
  return "marvin_msgs::msg::Extforce";
}

template<>
inline const char * name<marvin_msgs::msg::Extforce>()
{
  return "marvin_msgs/msg/Extforce";
}

template<>
struct has_fixed_size<marvin_msgs::msg::Extforce>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<marvin_msgs::msg::Extforce>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<marvin_msgs::msg::Extforce>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MARVIN_MSGS__MSG__DETAIL__EXTFORCE__TRAITS_HPP_
