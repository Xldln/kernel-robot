// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from marvin_msgs:msg/Jointcmd.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "marvin_msgs/msg/detail/jointcmd__struct.hpp"
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

void Jointcmd_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) marvin_msgs::msg::Jointcmd(_init);
}

void Jointcmd_fini_function(void * message_memory)
{
  auto typed_message = static_cast<marvin_msgs::msg::Jointcmd *>(message_memory);
  typed_message->~Jointcmd();
}

size_t size_function__Jointcmd__positions(const void * untyped_member)
{
  (void)untyped_member;
  return 7;
}

const void * get_const_function__Jointcmd__positions(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 7> *>(untyped_member);
  return &member[index];
}

void * get_function__Jointcmd__positions(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 7> *>(untyped_member);
  return &member[index];
}

void fetch_function__Jointcmd__positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__Jointcmd__positions(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__Jointcmd__positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__Jointcmd__positions(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Jointcmd_message_member_array[2] = {
  {
    "header",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<std_msgs::msg::Header>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs::msg::Jointcmd, header),  // bytes offset in struct
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
    7,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs::msg::Jointcmd, positions),  // bytes offset in struct
    nullptr,  // default value
    size_function__Jointcmd__positions,  // size() function pointer
    get_const_function__Jointcmd__positions,  // get_const(index) function pointer
    get_function__Jointcmd__positions,  // get(index) function pointer
    fetch_function__Jointcmd__positions,  // fetch(index, &value) function pointer
    assign_function__Jointcmd__positions,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Jointcmd_message_members = {
  "marvin_msgs::msg",  // message namespace
  "Jointcmd",  // message name
  2,  // number of fields
  sizeof(marvin_msgs::msg::Jointcmd),
  Jointcmd_message_member_array,  // message members
  Jointcmd_init_function,  // function to initialize message memory (memory has to be allocated)
  Jointcmd_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Jointcmd_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Jointcmd_message_members,
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
get_message_type_support_handle<marvin_msgs::msg::Jointcmd>()
{
  return &::marvin_msgs::msg::rosidl_typesupport_introspection_cpp::Jointcmd_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, marvin_msgs, msg, Jointcmd)() {
  return &::marvin_msgs::msg::rosidl_typesupport_introspection_cpp::Jointcmd_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
