// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from marvin_msgs:msg/KeypointPoseArray.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "marvin_msgs/msg/detail/keypoint_pose_array__rosidl_typesupport_introspection_c.h"
#include "marvin_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "marvin_msgs/msg/detail/keypoint_pose_array__functions.h"
#include "marvin_msgs/msg/detail/keypoint_pose_array__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `poses`
#include "marvin_msgs/msg/keypoint_pose.h"
// Member `poses`
#include "marvin_msgs/msg/detail/keypoint_pose__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  marvin_msgs__msg__KeypointPoseArray__init(message_memory);
}

void marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_fini_function(void * message_memory)
{
  marvin_msgs__msg__KeypointPoseArray__fini(message_memory);
}

size_t marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__size_function__KeypointPoseArray__poses(
  const void * untyped_member)
{
  const marvin_msgs__msg__KeypointPose__Sequence * member =
    (const marvin_msgs__msg__KeypointPose__Sequence *)(untyped_member);
  return member->size;
}

const void * marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__get_const_function__KeypointPoseArray__poses(
  const void * untyped_member, size_t index)
{
  const marvin_msgs__msg__KeypointPose__Sequence * member =
    (const marvin_msgs__msg__KeypointPose__Sequence *)(untyped_member);
  return &member->data[index];
}

void * marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__get_function__KeypointPoseArray__poses(
  void * untyped_member, size_t index)
{
  marvin_msgs__msg__KeypointPose__Sequence * member =
    (marvin_msgs__msg__KeypointPose__Sequence *)(untyped_member);
  return &member->data[index];
}

void marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__fetch_function__KeypointPoseArray__poses(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const marvin_msgs__msg__KeypointPose * item =
    ((const marvin_msgs__msg__KeypointPose *)
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__get_const_function__KeypointPoseArray__poses(untyped_member, index));
  marvin_msgs__msg__KeypointPose * value =
    (marvin_msgs__msg__KeypointPose *)(untyped_value);
  *value = *item;
}

void marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__assign_function__KeypointPoseArray__poses(
  void * untyped_member, size_t index, const void * untyped_value)
{
  marvin_msgs__msg__KeypointPose * item =
    ((marvin_msgs__msg__KeypointPose *)
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__get_function__KeypointPoseArray__poses(untyped_member, index));
  const marvin_msgs__msg__KeypointPose * value =
    (const marvin_msgs__msg__KeypointPose *)(untyped_value);
  *item = *value;
}

bool marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__resize_function__KeypointPoseArray__poses(
  void * untyped_member, size_t size)
{
  marvin_msgs__msg__KeypointPose__Sequence * member =
    (marvin_msgs__msg__KeypointPose__Sequence *)(untyped_member);
  marvin_msgs__msg__KeypointPose__Sequence__fini(member);
  return marvin_msgs__msg__KeypointPose__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__msg__KeypointPoseArray, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "poses",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__msg__KeypointPoseArray, poses),  // bytes offset in struct
    NULL,  // default value
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__size_function__KeypointPoseArray__poses,  // size() function pointer
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__get_const_function__KeypointPoseArray__poses,  // get_const(index) function pointer
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__get_function__KeypointPoseArray__poses,  // get(index) function pointer
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__fetch_function__KeypointPoseArray__poses,  // fetch(index, &value) function pointer
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__assign_function__KeypointPoseArray__poses,  // assign(index, value) function pointer
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__resize_function__KeypointPoseArray__poses  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_members = {
  "marvin_msgs__msg",  // message namespace
  "KeypointPoseArray",  // message name
  2,  // number of fields
  sizeof(marvin_msgs__msg__KeypointPoseArray),
  marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_member_array,  // message members
  marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_init_function,  // function to initialize message memory (memory has to be allocated)
  marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_type_support_handle = {
  0,
  &marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_marvin_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, msg, KeypointPoseArray)() {
  marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, msg, KeypointPose)();
  if (!marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_type_support_handle.typesupport_identifier) {
    marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &marvin_msgs__msg__KeypointPoseArray__rosidl_typesupport_introspection_c__KeypointPoseArray_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
