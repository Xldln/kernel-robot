// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from marvin_msgs:srv/Velratio.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__VELRATIO__FUNCTIONS_H_
#define MARVIN_MSGS__SRV__DETAIL__VELRATIO__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "marvin_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "marvin_msgs/srv/detail/velratio__struct.h"

/// Initialize srv/Velratio message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * marvin_msgs__srv__Velratio_Request
 * )) before or use
 * marvin_msgs__srv__Velratio_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Request__init(marvin_msgs__srv__Velratio_Request * msg);

/// Finalize srv/Velratio message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Request__fini(marvin_msgs__srv__Velratio_Request * msg);

/// Create srv/Velratio message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * marvin_msgs__srv__Velratio_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
marvin_msgs__srv__Velratio_Request *
marvin_msgs__srv__Velratio_Request__create();

/// Destroy srv/Velratio message.
/**
 * It calls
 * marvin_msgs__srv__Velratio_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Request__destroy(marvin_msgs__srv__Velratio_Request * msg);

/// Check for srv/Velratio message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Request__are_equal(const marvin_msgs__srv__Velratio_Request * lhs, const marvin_msgs__srv__Velratio_Request * rhs);

/// Copy a srv/Velratio message.
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
marvin_msgs__srv__Velratio_Request__copy(
  const marvin_msgs__srv__Velratio_Request * input,
  marvin_msgs__srv__Velratio_Request * output);

/// Initialize array of srv/Velratio messages.
/**
 * It allocates the memory for the number of elements and calls
 * marvin_msgs__srv__Velratio_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Request__Sequence__init(marvin_msgs__srv__Velratio_Request__Sequence * array, size_t size);

/// Finalize array of srv/Velratio messages.
/**
 * It calls
 * marvin_msgs__srv__Velratio_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Request__Sequence__fini(marvin_msgs__srv__Velratio_Request__Sequence * array);

/// Create array of srv/Velratio messages.
/**
 * It allocates the memory for the array and calls
 * marvin_msgs__srv__Velratio_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
marvin_msgs__srv__Velratio_Request__Sequence *
marvin_msgs__srv__Velratio_Request__Sequence__create(size_t size);

/// Destroy array of srv/Velratio messages.
/**
 * It calls
 * marvin_msgs__srv__Velratio_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Request__Sequence__destroy(marvin_msgs__srv__Velratio_Request__Sequence * array);

/// Check for srv/Velratio message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Request__Sequence__are_equal(const marvin_msgs__srv__Velratio_Request__Sequence * lhs, const marvin_msgs__srv__Velratio_Request__Sequence * rhs);

/// Copy an array of srv/Velratio messages.
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
marvin_msgs__srv__Velratio_Request__Sequence__copy(
  const marvin_msgs__srv__Velratio_Request__Sequence * input,
  marvin_msgs__srv__Velratio_Request__Sequence * output);

/// Initialize srv/Velratio message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * marvin_msgs__srv__Velratio_Response
 * )) before or use
 * marvin_msgs__srv__Velratio_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Response__init(marvin_msgs__srv__Velratio_Response * msg);

/// Finalize srv/Velratio message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Response__fini(marvin_msgs__srv__Velratio_Response * msg);

/// Create srv/Velratio message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * marvin_msgs__srv__Velratio_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
marvin_msgs__srv__Velratio_Response *
marvin_msgs__srv__Velratio_Response__create();

/// Destroy srv/Velratio message.
/**
 * It calls
 * marvin_msgs__srv__Velratio_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Response__destroy(marvin_msgs__srv__Velratio_Response * msg);

/// Check for srv/Velratio message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Response__are_equal(const marvin_msgs__srv__Velratio_Response * lhs, const marvin_msgs__srv__Velratio_Response * rhs);

/// Copy a srv/Velratio message.
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
marvin_msgs__srv__Velratio_Response__copy(
  const marvin_msgs__srv__Velratio_Response * input,
  marvin_msgs__srv__Velratio_Response * output);

/// Initialize array of srv/Velratio messages.
/**
 * It allocates the memory for the number of elements and calls
 * marvin_msgs__srv__Velratio_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Response__Sequence__init(marvin_msgs__srv__Velratio_Response__Sequence * array, size_t size);

/// Finalize array of srv/Velratio messages.
/**
 * It calls
 * marvin_msgs__srv__Velratio_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Response__Sequence__fini(marvin_msgs__srv__Velratio_Response__Sequence * array);

/// Create array of srv/Velratio messages.
/**
 * It allocates the memory for the array and calls
 * marvin_msgs__srv__Velratio_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
marvin_msgs__srv__Velratio_Response__Sequence *
marvin_msgs__srv__Velratio_Response__Sequence__create(size_t size);

/// Destroy array of srv/Velratio messages.
/**
 * It calls
 * marvin_msgs__srv__Velratio_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
void
marvin_msgs__srv__Velratio_Response__Sequence__destroy(marvin_msgs__srv__Velratio_Response__Sequence * array);

/// Check for srv/Velratio message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_marvin_msgs
bool
marvin_msgs__srv__Velratio_Response__Sequence__are_equal(const marvin_msgs__srv__Velratio_Response__Sequence * lhs, const marvin_msgs__srv__Velratio_Response__Sequence * rhs);

/// Copy an array of srv/Velratio messages.
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
marvin_msgs__srv__Velratio_Response__Sequence__copy(
  const marvin_msgs__srv__Velratio_Response__Sequence * input,
  marvin_msgs__srv__Velratio_Response__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MARVIN_MSGS__SRV__DETAIL__VELRATIO__FUNCTIONS_H_
