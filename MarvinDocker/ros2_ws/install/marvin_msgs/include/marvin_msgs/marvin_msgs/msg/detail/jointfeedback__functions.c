// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from marvin_msgs:msg/Jointfeedback.idl
// generated code does not contain a copyright notice
#include "marvin_msgs/msg/detail/jointfeedback__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
marvin_msgs__msg__Jointfeedback__init(marvin_msgs__msg__Jointfeedback * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    marvin_msgs__msg__Jointfeedback__fini(msg);
    return false;
  }
  // positions
  // velocities
  // efforts
  return true;
}

void
marvin_msgs__msg__Jointfeedback__fini(marvin_msgs__msg__Jointfeedback * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // positions
  // velocities
  // efforts
}

bool
marvin_msgs__msg__Jointfeedback__are_equal(const marvin_msgs__msg__Jointfeedback * lhs, const marvin_msgs__msg__Jointfeedback * rhs)
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
  // positions
  for (size_t i = 0; i < 14; ++i) {
    if (lhs->positions[i] != rhs->positions[i]) {
      return false;
    }
  }
  // velocities
  for (size_t i = 0; i < 14; ++i) {
    if (lhs->velocities[i] != rhs->velocities[i]) {
      return false;
    }
  }
  // efforts
  for (size_t i = 0; i < 14; ++i) {
    if (lhs->efforts[i] != rhs->efforts[i]) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__msg__Jointfeedback__copy(
  const marvin_msgs__msg__Jointfeedback * input,
  marvin_msgs__msg__Jointfeedback * output)
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
  // positions
  for (size_t i = 0; i < 14; ++i) {
    output->positions[i] = input->positions[i];
  }
  // velocities
  for (size_t i = 0; i < 14; ++i) {
    output->velocities[i] = input->velocities[i];
  }
  // efforts
  for (size_t i = 0; i < 14; ++i) {
    output->efforts[i] = input->efforts[i];
  }
  return true;
}

marvin_msgs__msg__Jointfeedback *
marvin_msgs__msg__Jointfeedback__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Jointfeedback * msg = (marvin_msgs__msg__Jointfeedback *)allocator.allocate(sizeof(marvin_msgs__msg__Jointfeedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(marvin_msgs__msg__Jointfeedback));
  bool success = marvin_msgs__msg__Jointfeedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
marvin_msgs__msg__Jointfeedback__destroy(marvin_msgs__msg__Jointfeedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    marvin_msgs__msg__Jointfeedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
marvin_msgs__msg__Jointfeedback__Sequence__init(marvin_msgs__msg__Jointfeedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Jointfeedback * data = NULL;

  if (size) {
    data = (marvin_msgs__msg__Jointfeedback *)allocator.zero_allocate(size, sizeof(marvin_msgs__msg__Jointfeedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = marvin_msgs__msg__Jointfeedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        marvin_msgs__msg__Jointfeedback__fini(&data[i - 1]);
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
marvin_msgs__msg__Jointfeedback__Sequence__fini(marvin_msgs__msg__Jointfeedback__Sequence * array)
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
      marvin_msgs__msg__Jointfeedback__fini(&array->data[i]);
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

marvin_msgs__msg__Jointfeedback__Sequence *
marvin_msgs__msg__Jointfeedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Jointfeedback__Sequence * array = (marvin_msgs__msg__Jointfeedback__Sequence *)allocator.allocate(sizeof(marvin_msgs__msg__Jointfeedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = marvin_msgs__msg__Jointfeedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
marvin_msgs__msg__Jointfeedback__Sequence__destroy(marvin_msgs__msg__Jointfeedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    marvin_msgs__msg__Jointfeedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
marvin_msgs__msg__Jointfeedback__Sequence__are_equal(const marvin_msgs__msg__Jointfeedback__Sequence * lhs, const marvin_msgs__msg__Jointfeedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!marvin_msgs__msg__Jointfeedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__msg__Jointfeedback__Sequence__copy(
  const marvin_msgs__msg__Jointfeedback__Sequence * input,
  marvin_msgs__msg__Jointfeedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(marvin_msgs__msg__Jointfeedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    marvin_msgs__msg__Jointfeedback * data =
      (marvin_msgs__msg__Jointfeedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!marvin_msgs__msg__Jointfeedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          marvin_msgs__msg__Jointfeedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!marvin_msgs__msg__Jointfeedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
