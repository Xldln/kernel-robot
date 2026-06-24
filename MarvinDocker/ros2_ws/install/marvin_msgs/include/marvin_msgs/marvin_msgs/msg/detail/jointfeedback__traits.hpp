// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from marvin_msgs:msg/Jointfeedback.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__TRAITS_HPP_
#define MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "marvin_msgs/msg/detail/jointfeedback__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace marvin_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Jointfeedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: positions
  {
    if (msg.positions.size() == 0) {
      out << "positions: []";
    } else {
      out << "positions: [";
      size_t pending_items = msg.positions.size();
      for (auto item : msg.positions) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: velocities
  {
    if (msg.velocities.size() == 0) {
      out << "velocities: []";
    } else {
      out << "velocities: [";
      size_t pending_items = msg.velocities.size();
      for (auto item : msg.velocities) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: efforts
  {
    if (msg.efforts.size() == 0) {
      out << "efforts: []";
    } else {
      out << "efforts: [";
      size_t pending_items = msg.efforts.size();
      for (auto item : msg.efforts) {
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
  const Jointfeedback & msg,
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

  // member: positions
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.positions.size() == 0) {
      out << "positions: []\n";
    } else {
      out << "positions:\n";
      for (auto item : msg.positions) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: velocities
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.velocities.size() == 0) {
      out << "velocities: []\n";
    } else {
      out << "velocities:\n";
      for (auto item : msg.velocities) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: efforts
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.efforts.size() == 0) {
      out << "efforts: []\n";
    } else {
      out << "efforts:\n";
      for (auto item : msg.efforts) {
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

inline std::string to_yaml(const Jointfeedback & msg, bool use_flow_style = false)
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
  const marvin_msgs::msg::Jointfeedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  marvin_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use marvin_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const marvin_msgs::msg::Jointfeedback & msg)
{
  return marvin_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<marvin_msgs::msg::Jointfeedback>()
{
  return "marvin_msgs::msg::Jointfeedback";
}

template<>
inline const char * name<marvin_msgs::msg::Jointfeedback>()
{
  return "marvin_msgs/msg/Jointfeedback";
}

template<>
struct has_fixed_size<marvin_msgs::msg::Jointfeedback>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<marvin_msgs::msg::Jointfeedback>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<marvin_msgs::msg::Jointfeedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__TRAITS_HPP_
