// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from marvin_msgs:msg/Jointfeedback.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__STRUCT_H_
#define MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__STRUCT_H_

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

/// Struct defined in msg/Jointfeedback in the package marvin_msgs.
typedef struct marvin_msgs__msg__Jointfeedback
{
  /// order L1,L2,L3,L4,L5,L6,L7,R1,R2,R3,R4,R5,R6,R7
  std_msgs__msg__Header header;
  double positions[14];
  double velocities[14];
  double efforts[14];
} marvin_msgs__msg__Jointfeedback;

// Struct for a sequence of marvin_msgs__msg__Jointfeedback.
typedef struct marvin_msgs__msg__Jointfeedback__Sequence
{
  marvin_msgs__msg__Jointfeedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} marvin_msgs__msg__Jointfeedback__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__STRUCT_H_
