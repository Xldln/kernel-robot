// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from marvin_msgs:msg/KeypointPose.idl
// generated code does not contain a copyright notice
#include "marvin_msgs/msg/detail/keypoint_pose__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `name`
// Member `arm`
#include "rosidl_runtime_c/string_functions.h"
// Member `poses`
#include "geometry_msgs/msg/detail/pose__functions.h"

bool
marvin_msgs__msg__KeypointPose__init(marvin_msgs__msg__KeypointPose * msg)
{
  if (!msg) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    marvin_msgs__msg__KeypointPose__fini(msg);
    return false;
  }
  // arm
  if (!rosidl_runtime_c__String__init(&msg->arm)) {
    marvin_msgs__msg__KeypointPose__fini(msg);
    return false;
  }
  // poses
  if (!geometry_msgs__msg__Pose__Sequence__init(&msg->poses, 0)) {
    marvin_msgs__msg__KeypointPose__fini(msg);
    return false;
  }
  // constraints
  // speed
  // gripper_value
  return true;
}

void
marvin_msgs__msg__KeypointPose__fini(marvin_msgs__msg__KeypointPose * msg)
{
  if (!msg) {
    return;
  }
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // arm
  rosidl_runtime_c__String__fini(&msg->arm);
  // poses
  geometry_msgs__msg__Pose__Sequence__fini(&msg->poses);
  // constraints
  // speed
  // gripper_value
}

bool
marvin_msgs__msg__KeypointPose__are_equal(const marvin_msgs__msg__KeypointPose * lhs, const marvin_msgs__msg__KeypointPose * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // arm
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->arm), &(rhs->arm)))
  {
    return false;
  }
  // poses
  if (!geometry_msgs__msg__Pose__Sequence__are_equal(
      &(lhs->poses), &(rhs->poses)))
  {
    return false;
  }
  // constraints
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->constraints[i] != rhs->constraints[i]) {
      return false;
    }
  }
  // speed
  if (lhs->speed != rhs->speed) {
    return false;
  }
  // gripper_value
  if (lhs->gripper_value != rhs->gripper_value) {
    return false;
  }
  return true;
}

bool
marvin_msgs__msg__KeypointPose__copy(
  const marvin_msgs__msg__KeypointPose * input,
  marvin_msgs__msg__KeypointPose * output)
{
  if (!input || !output) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // arm
  if (!rosidl_runtime_c__String__copy(
      &(input->arm), &(output->arm)))
  {
    return false;
  }
  // poses
  if (!geometry_msgs__msg__Pose__Sequence__copy(
      &(input->poses), &(output->poses)))
  {
    return false;
  }
  // constraints
  for (size_t i = 0; i < 3; ++i) {
    output->constraints[i] = input->constraints[i];
  }
  // speed
  output->speed = input->speed;
  // gripper_value
  output->gripper_value = input->gripper_value;
  return true;
}

marvin_msgs__msg__KeypointPose *
marvin_msgs__msg__KeypointPose__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__KeypointPose * msg = (marvin_msgs__msg__KeypointPose *)allocator.allocate(sizeof(marvin_msgs__msg__KeypointPose), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(marvin_msgs__msg__KeypointPose));
  bool success = marvin_msgs__msg__KeypointPose__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
marvin_msgs__msg__KeypointPose__destroy(marvin_msgs__msg__KeypointPose * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    marvin_msgs__msg__KeypointPose__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
marvin_msgs__msg__KeypointPose__Sequence__init(marvin_msgs__msg__KeypointPose__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__KeypointPose * data = NULL;

  if (size) {
    data = (marvin_msgs__msg__KeypointPose *)allocator.zero_allocate(size, sizeof(marvin_msgs__msg__KeypointPose), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = marvin_msgs__msg__KeypointPose__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        marvin_msgs__msg__KeypointPose__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
marvin_msgs__msg__KeypointPose__Sequence__fini(marvin_msgs__msg__KeypointPose__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      marvin_msgs__msg__KeypointPose__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

marvin_msgs__msg__KeypointPose__Sequence *
marvin_msgs__msg__KeypointPose__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__KeypointPose__Sequence * array = (marvin_msgs__msg__KeypointPose__Sequence *)allocator.allocate(sizeof(marvin_msgs__msg__KeypointPose__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = marvin_msgs__msg__KeypointPose__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
marvin_msgs__msg__KeypointPose__Sequence__destroy(marvin_msgs__msg__KeypointPose__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    marvin_msgs__msg__KeypointPose__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
marvin_msgs__msg__KeypointPose__Sequence__are_equal(const marvin_msgs__msg__KeypointPose__Sequence * lhs, const marvin_msgs__msg__KeypointPose__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!marvin_msgs__msg__KeypointPose__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__msg__KeypointPose__Sequence__copy(
  const marvin_msgs__msg__KeypointPose__Sequence * input,
  marvin_msgs__msg__KeypointPose__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(marvin_msgs__msg__KeypointPose);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    marvin_msgs__msg__KeypointPose * data =
      (marvin_msgs__msg__KeypointPose *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!marvin_msgs__msg__KeypointPose__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          marvin_msgs__msg__KeypointPose__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!marvin_msgs__msg__KeypointPose__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
