// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from marvin_msgs:msg/Collimarker.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "marvin_msgs/msg/detail/collimarker__rosidl_typesupport_introspection_c.h"
#include "marvin_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "marvin_msgs/msg/detail/collimarker__functions.h"
#include "marvin_msgs/msg/detail/collimarker__struct.h"


// Include directives for member types
// Member `vectors`
#include "geometry_msgs/msg/vector3.h"
// Member `vectors`
#include "geometry_msgs/msg/detail/vector3__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  marvin_msgs__msg__Collimarker__init(message_memory);
}

void marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_fini_function(void * message_memory)
{
  marvin_msgs__msg__Collimarker__fini(message_memory);
}

size_t marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__size_function__Collimarker__vectors(
  const void * untyped_member)
{
  const geometry_msgs__msg__Vector3__Sequence * member =
    (const geometry_msgs__msg__Vector3__Sequence *)(untyped_member);
  return member->size;
}

const void * marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__get_const_function__Collimarker__vectors(
  const void * untyped_member, size_t index)
{
  const geometry_msgs__msg__Vector3__Sequence * member =
    (const geometry_msgs__msg__Vector3__Sequence *)(untyped_member);
  return &member->data[index];
}

void * marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__get_function__Collimarker__vectors(
  void * untyped_member, size_t index)
{
  geometry_msgs__msg__Vector3__Sequence * member =
    (geometry_msgs__msg__Vector3__Sequence *)(untyped_member);
  return &member->data[index];
}

void marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__fetch_function__Collimarker__vectors(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const geometry_msgs__msg__Vector3 * item =
    ((const geometry_msgs__msg__Vector3 *)
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__get_const_function__Collimarker__vectors(untyped_member, index));
  geometry_msgs__msg__Vector3 * value =
    (geometry_msgs__msg__Vector3 *)(untyped_value);
  *value = *item;
}

void marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__assign_function__Collimarker__vectors(
  void * untyped_member, size_t index, const void * untyped_value)
{
  geometry_msgs__msg__Vector3 * item =
    ((geometry_msgs__msg__Vector3 *)
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__get_function__Collimarker__vectors(untyped_member, index));
  const geometry_msgs__msg__Vector3 * value =
    (const geometry_msgs__msg__Vector3 *)(untyped_value);
  *item = *value;
}

bool marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__resize_function__Collimarker__vectors(
  void * untyped_member, size_t size)
{
  geometry_msgs__msg__Vector3__Sequence * member =
    (geometry_msgs__msg__Vector3__Sequence *)(untyped_member);
  geometry_msgs__msg__Vector3__Sequence__fini(member);
  return geometry_msgs__msg__Vector3__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_member_array[1] = {
  {
    "vectors",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__msg__Collimarker, vectors),  // bytes offset in struct
    NULL,  // default value
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__size_function__Collimarker__vectors,  // size() function pointer
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__get_const_function__Collimarker__vectors,  // get_const(index) function pointer
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__get_function__Collimarker__vectors,  // get(index) function pointer
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__fetch_function__Collimarker__vectors,  // fetch(index, &value) function pointer
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__assign_function__Collimarker__vectors,  // assign(index, value) function pointer
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__resize_function__Collimarker__vectors  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_members = {
  "marvin_msgs__msg",  // message namespace
  "Collimarker",  // message name
  1,  // number of fields
  sizeof(marvin_msgs__msg__Collimarker),
  marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_member_array,  // message members
  marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_init_function,  // function to initialize message memory (memory has to be allocated)
  marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_type_support_handle = {
  0,
  &marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_marvin_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, msg, Collimarker)() {
  marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Vector3)();
  if (!marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_type_support_handle.typesupport_identifier) {
    marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &marvin_msgs__msg__Collimarker__rosidl_typesupport_introspection_c__Collimarker_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
