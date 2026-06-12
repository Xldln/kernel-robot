// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from marvin_msgs:srv/MotorErrCode.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__STRUCT_H_
#define MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/MotorErrCode in the package marvin_msgs.
typedef struct marvin_msgs__srv__MotorErrCode_Request
{
  uint8_t structure_needs_at_least_one_member;
} marvin_msgs__srv__MotorErrCode_Request;

// Struct for a sequence of marvin_msgs__srv__MotorErrCode_Request.
typedef struct marvin_msgs__srv__MotorErrCode_Request__Sequence
{
  marvin_msgs__srv__MotorErrCode_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} marvin_msgs__srv__MotorErrCode_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'error_code'
#include "rosidl_runtime_c/primitives_sequence.h"
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MotorErrCode in the package marvin_msgs.
typedef struct marvin_msgs__srv__MotorErrCode_Response
{
  rosidl_runtime_c__int16__Sequence error_code;
  bool success;
  rosidl_runtime_c__String message;
} marvin_msgs__srv__MotorErrCode_Response;

// Struct for a sequence of marvin_msgs__srv__MotorErrCode_Response.
typedef struct marvin_msgs__srv__MotorErrCode_Response__Sequence
{
  marvin_msgs__srv__MotorErrCode_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} marvin_msgs__srv__MotorErrCode_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__STRUCT_H_
