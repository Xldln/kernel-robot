// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from marvin_msgs:msg/Collimarker.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__STRUCT_H_
#define MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'vectors'
#include "geometry_msgs/msg/detail/vector3__struct.h"

/// Struct defined in msg/Collimarker in the package marvin_msgs.
typedef struct marvin_msgs__msg__Collimarker
{
  geometry_msgs__msg__Vector3__Sequence vectors;
} marvin_msgs__msg__Collimarker;

// Struct for a sequence of marvin_msgs__msg__Collimarker.
typedef struct marvin_msgs__msg__Collimarker__Sequence
{
  marvin_msgs__msg__Collimarker * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} marvin_msgs__msg__Collimarker__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__STRUCT_H_
