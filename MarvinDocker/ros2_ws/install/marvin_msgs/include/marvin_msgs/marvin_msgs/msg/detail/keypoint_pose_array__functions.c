// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from marvin_msgs:msg/KeypointPoseArray.idl
// generated code does not contain a copyright notice
#include "marvin_msgs/msg/detail/keypoint_pose_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `poses`
#include "marvin_msgs/msg/detail/keypoint_pose__functions.h"

bool
marvin_msgs__msg__KeypointPoseArray__init(marvin_msgs__msg__KeypointPoseArray * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    marvin_msgs__msg__KeypointPoseArray__fini(msg);
    return false;
  }
  // poses
  if (!marvin_msgs__msg__KeypointPose__Sequence__init(&msg->poses, 0)) {
    marvin_msgs__msg__KeypointPoseArray__fini(msg);
    return false;
  }
  return true;
}

void
marvin_msgs__msg__KeypointPoseArray__fini(marvin_msgs__msg__KeypointPoseArray * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // poses
  marvin_msgs__msg__KeypointPose__Sequence__fini(&msg->poses);
}

bool
marvin_msgs__msg__KeypointPoseArray__are_equal(const marvin_msgs__msg__KeypointPoseArray * lhs, const marvin_msgs__msg__KeypointPoseArray * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // poses
  if (!marvin_msgs__msg__KeypointPose__Sequence__are_equal(
      &(lhs->poses), &(rhs->poses)))
  {
    return false;
  }
  return true;
}

bool
marvin_msgs__msg__KeypointPoseArray__copy(
  const marvin_msgs__msg__KeypointPoseArray * input,
  marvin_msgs__msg__KeypointPoseArray * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // poses
  if (!marvin_msgs__msg__KeypointPose__Sequence__copy(
      &(input->poses), &(output->poses)))
  {
    return false;
  }
  return true;
}

marvin_msgs__msg__KeypointPoseArray *
marvin_msgs__msg__KeypointPoseArray__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__KeypointPoseArray * msg = (marvin_msgs__msg__KeypointPoseArray *)allocator.allocate(sizeof(marvin_msgs__msg__KeypointPoseArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(marvin_msgs__msg__KeypointPoseArray));
  bool success = marvin_msgs__msg__KeypointPoseArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
marvin_msgs__msg__KeypointPoseArray__destroy(marvin_msgs__msg__KeypointPoseArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    marvin_msgs__msg__KeypointPoseArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
marvin_msgs__msg__KeypointPoseArray__Sequence__init(marvin_msgs__msg__KeypointPoseArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__KeypointPoseArray * data = NULL;

  if (size) {
    data = (marvin_msgs__msg__KeypointPoseArray *)allocator.zero_allocate(size, sizeof(marvin_msgs__msg__KeypointPoseArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = marvin_msgs__msg__KeypointPoseArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        marvin_msgs__msg__KeypointPoseArray__fini(&data[i - 1]);
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
marvin_msgs__msg__KeypointPoseArray__Sequence__fini(marvin_msgs__msg__KeypointPoseArray__Sequence * array)
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
      marvin_msgs__msg__KeypointPoseArray__fini(&array->data[i]);
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

marvin_msgs__msg__KeypointPoseArray__Sequence *
marvin_msgs__msg__KeypointPoseArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__KeypointPoseArray__Sequence * array = (marvin_msgs__msg__KeypointPoseArray__Sequence *)allocator.allocate(sizeof(marvin_msgs__msg__KeypointPoseArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = marvin_msgs__msg__KeypointPoseArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
marvin_msgs__msg__KeypointPoseArray__Sequence__destroy(marvin_msgs__msg__KeypointPoseArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    marvin_msgs__msg__KeypointPoseArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
marvin_msgs__msg__KeypointPoseArray__Sequence__are_equal(const marvin_msgs__msg__KeypointPoseArray__Sequence * lhs, const marvin_msgs__msg__KeypointPoseArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!marvin_msgs__msg__KeypointPoseArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__msg__KeypointPoseArray__Sequence__copy(
  const marvin_msgs__msg__KeypointPoseArray__Sequence * input,
  marvin_msgs__msg__KeypointPoseArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(marvin_msgs__msg__KeypointPoseArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    marvin_msgs__msg__KeypointPoseArray * data =
      (marvin_msgs__msg__KeypointPoseArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!marvin_msgs__msg__KeypointPoseArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          marvin_msgs__msg__KeypointPoseArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!marvin_msgs__msg__KeypointPoseArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
