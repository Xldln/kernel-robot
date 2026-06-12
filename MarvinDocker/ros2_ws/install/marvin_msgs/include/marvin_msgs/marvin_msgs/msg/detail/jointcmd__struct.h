// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from marvin_msgs:msg/Jointcmd.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTCMD__STRUCT_H_
#define MARVIN_MSGS__MSG__DETAIL__JOINTCMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/Jointcmd in the package marvin_msgs.
typedef struct marvin_msgs__msg__Jointcmd
{
  std_msgs__msg__Header header;
  double positions[7];
} marvin_msgs__msg__Jointcmd;

// Struct for a sequence of marvin_msgs__msg__Jointcmd.
typedef struct marvin_msgs__msg__Jointcmd__Sequence
{
  marvin_msgs__msg__Jointcmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} marvin_msgs__msg__Jointcmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTCMD__STRUCT_H_
