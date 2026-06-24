// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from marvin_msgs:msg/Jointfeedback.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "marvin_msgs/msg/detail/jointfeedback__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace marvin_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Jointfeedback_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) marvin_msgs::msg::Jointfeedback(_init);
}

void Jointfeedback_fini_function(void * message_memory)
{
  auto typed_message = static_cast<marvin_msgs::msg::Jointfeedback *>(message_memory);
  typed_message->~Jointfeedback();
}

size_t size_function__Jointfeedback__positions(const void * untyped_member)
{
  (void)untyped_member;
  return 14;
}

const void * get_const_function__Jointfeedback__positions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 14> *>(untyped_member);
  return &member[index];
}

void * get_function__Jointfeedback__positions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 14> *>(untyped_member);
  return &member[index];
}

void fetch_function__Jointfeedback__positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Jointfeedback__positions(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Jointfeedback__positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Jointfeedback__positions(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__Jointfeedback__velocities(const void * untyped_member)
{
  (void)untyped_member;
  return 14;
}

const void * get_const_function__Jointfeedback__velocities(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 14> *>(untyped_member);
  return &member[index];
}

void * get_function__Jointfeedback__velocities(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 14> *>(untyped_member);
  return &member[index];
}

void fetch_function__Jointfeedback__velocities(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Jointfeedback__velocities(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Jointfeedback__velocities(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Jointfeedback__velocities(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

size_t size_function__Jointfeedback__efforts(const void * untyped_member)
{
  (void)untyped_member;
  return 14;
}

const void * get_const_function__Jointfeedback__efforts(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 14> *>(untyped_member);
  return &member[index];
}

void * get_function__Jointfeedback__efforts(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 14> *>(untyped_member);
  return &member[index];
}

void fetch_function__Jointfeedback__efforts(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Jointfeedback__efforts(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Jointfeedback__efforts(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Jointfeedback__efforts(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Jointfeedback_message_member_array[4] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs::msg::Jointfeedback, header),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "positions",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    14,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs::msg::Jointfeedback, positions),  // bytes offset in struct
    nullptr,  // default value
    size_function__Jointfeedback__positions,  // size() function pointer
    get_const_function__Jointfeedback__positions,  // get_const(index) function pointer
    get_function__Jointfeedback__positions,  // get(index) function pointer
    fetch_function__Jointfeedback__positions,  // fetch(index, &value) function pointer
    assign_function__Jointfeedback__positions,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "velocities",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    14,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs::msg::Jointfeedback, velocities),  // bytes offset in struct
    nullptr,  // default value
    size_function__Jointfeedback__velocities,  // size() function pointer
    get_const_function__Jointfeedback__velocities,  // get_const(index) function pointer
    get_function__Jointfeedback__velocities,  // get(index) function pointer
    fetch_function__Jointfeedback__velocities,  // fetch(index, &value) function pointer
    assign_function__Jointfeedback__velocities,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "efforts",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    14,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs::msg::Jointfeedback, efforts),  // bytes offset in struct
    nullptr,  // default value
    size_function__Jointfeedback__efforts,  // size() function pointer
    get_const_function__Jointfeedback__efforts,  // get_const(index) function pointer
    get_function__Jointfeedback__efforts,  // get(index) function pointer
    fetch_function__Jointfeedback__efforts,  // fetch(index, &value) function pointer
    assign_function__Jointfeedback__efforts,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Jointfeedback_message_members = {
  "marvin_msgs::msg",  // message namespace
  "Jointfeedback",  // message name
  4,  // number of fields
  sizeof(marvin_msgs::msg::Jointfeedback),
  Jointfeedback_message_member_array,  // message members
  Jointfeedback_init_function,  // function to initialize message memory (memory has to be allocated)
  Jointfeedback_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Jointfeedback_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Jointfeedback_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace marvin_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<marvin_msgs::msg::Jointfeedback>()
{
  return &::marvin_msgs::msg::rosidl_typesupport_introspection_cpp::Jointfeedback_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, marvin_msgs, msg, Jointfeedback)() {
  return &::marvin_msgs::msg::rosidl_typesupport_introspection_cpp::Jointfeedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
