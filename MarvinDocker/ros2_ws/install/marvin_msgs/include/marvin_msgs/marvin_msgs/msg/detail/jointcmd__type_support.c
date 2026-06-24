// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from marvin_msgs:msg/Jointcmd.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "marvin_msgs/msg/detail/jointcmd__rosidl_typesupport_introspection_c.h"
#include "marvin_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "marvin_msgs/msg/detail/jointcmd__functions.h"
#include "marvin_msgs/msg/detail/jointcmd__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  marvin_msgs__msg__Jointcmd__init(message_memory);
}

void marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_fini_function(void * message_memory)
{
  marvin_msgs__msg__Jointcmd__fini(message_memory);
}

size_t marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__size_function__Jointcmd__positions(
  const void * untyped_member)
{
  (void)untyped_member;
  return 7;
}

const void * marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__get_const_function__Jointcmd__positions(
  const void * untyped_member, size_t index)
{
  const double * member =
    (const double *)(untyped_member);
  return &member[index];
}

void * marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__get_function__Jointcmd__positions(
  void * untyped_member, size_t index)
{
  double * member =
    (double *)(untyped_member);
  return &member[index];
}

void marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__fetch_function__Jointcmd__positions(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__get_const_function__Jointcmd__positions(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__assign_function__Jointcmd__positions(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__get_function__Jointcmd__positions(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__msg__Jointcmd, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "positions",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    7,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__msg__Jointcmd, positions),  // bytes offset in struct
    NULL,  // default value
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__size_function__Jointcmd__positions,  // size() function pointer
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__get_const_function__Jointcmd__positions,  // get_const(index) function pointer
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__get_function__Jointcmd__positions,  // get(index) function pointer
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__fetch_function__Jointcmd__positions,  // fetch(index, &value) function pointer
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__assign_function__Jointcmd__positions,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_members = {
  "marvin_msgs__msg",  // message namespace
  "Jointcmd",  // message name
  2,  // number of fields
  sizeof(marvin_msgs__msg__Jointcmd),
  marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_member_array,  // message members
  marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_init_function,  // function to initialize message memory (memory has to be allocated)
  marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_type_support_handle = {
  0,
  &marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_marvin_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, msg, Jointcmd)() {
  marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_type_support_handle.typesupport_identifier) {
    marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &marvin_msgs__msg__Jointcmd__rosidl_typesupport_introspection_c__Jointcmd_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
