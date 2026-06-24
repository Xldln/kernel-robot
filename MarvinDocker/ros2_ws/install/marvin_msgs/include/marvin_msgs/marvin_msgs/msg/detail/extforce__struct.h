// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from marvin_msgs:msg/Extforce.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__EXTFORCE__STRUCT_H_
#define MARVIN_MSGS__MSG__DETAIL__EXTFORCE__STRUCT_H_

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

/// Struct defined in msg/Extforce in the package marvin_msgs.
typedef struct marvin_msgs__msg__Extforce
{
  /// order L1,L2,L3,L4,L5,L6,L7,R1,R2,R3,R4,R5,R6,R7
  std_msgs__msg__Header header;
  double joint_ext_force[14];
  double eef_ext_force[14];
} marvin_msgs__msg__Extforce;

// Struct for a sequence of marvin_msgs__msg__Extforce.
typedef struct marvin_msgs__msg__Extforce__Sequence
{
  marvin_msgs__msg__Extforce * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} marvin_msgs__msg__Extforce__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MARVIN_MSGS__MSG__DETAIL__EXTFORCE__STRUCT_H_
