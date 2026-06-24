// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from marvin_msgs:msg/Jointfeedback.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__FUNCTIONS_H_
#define MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "marvin_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "marvin_msgs/msg/detail/jointfeedback__struct.h"

/// Initialize msg/Jointfeedback message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * marvin_msgs__msg__Jointfeedback
 * )) before or use
 * marvin_msgs__msg__Jointfeedback__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__msg__Jointfeedback__init(marvin_msgs__msg__Jointfeedback * msg);

/// Finalize msg/Jointfeedback message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__msg__Jointfeedback__fini(marvin_msgs__msg__Jointfeedback * msg);

/// Create msg/Jointfeedback message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * marvin_msgs__msg__Jointfeedback__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
marvin_msgs__msg__Jointfeedback *
marvin_msgs__msg__Jointfeedback__create();

/// Destroy msg/Jointfeedback message.
/**
 * It calls
 * marvin_msgs__msg__Jointfeedback__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__msg__Jointfeedback__destroy(marvin_msgs__msg__Jointfeedback * msg);

/// Check for msg/Jointfeedback message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__msg__Jointfeedback__are_equal(const marvin_msgs__msg__Jointfeedback * lhs, const marvin_msgs__msg__Jointfeedback * rhs);

/// Copy a msg/Jointfeedback message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__msg__Jointfeedback__copy(
  const marvin_msgs__msg__Jointfeedback * input,
  marvin_msgs__msg__Jointfeedback * output);

/// Initialize array of msg/Jointfeedback messages.
/**
 * It allocates the memory for the number of elements and calls
 * marvin_msgs__msg__Jointfeedback__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__msg__Jointfeedback__Sequence__init(marvin_msgs__msg__Jointfeedback__Sequence * array, size_t size);

/// Finalize array of msg/Jointfeedback messages.
/**
 * It calls
 * marvin_msgs__msg__Jointfeedback__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__msg__Jointfeedback__Sequence__fini(marvin_msgs__msg__Jointfeedback__Sequence * array);

/// Create array of msg/Jointfeedback messages.
/**
 * It allocates the memory for the array and calls
 * marvin_msgs__msg__Jointfeedback__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
marvin_msgs__msg__Jointfeedback__Sequence *
marvin_msgs__msg__Jointfeedback__Sequence__create(size_t size);

/// Destroy array of msg/Jointfeedback messages.
/**
 * It calls
 * marvin_msgs__msg__Jointfeedback__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__msg__Jointfeedback__Sequence__destroy(marvin_msgs__msg__Jointfeedback__Sequence * array);

/// Check for msg/Jointfeedback message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__msg__Jointfeedback__Sequence__are_equal(const marvin_msgs__msg__Jointfeedback__Sequence * lhs, const marvin_msgs__msg__Jointfeedback__Sequence * rhs);

/// Copy an array of msg/Jointfeedback messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__msg__Jointfeedback__Sequence__copy(
  const marvin_msgs__msg__Jointfeedback__Sequence * input,
  marvin_msgs__msg__Jointfeedback__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__FUNCTIONS_H_
