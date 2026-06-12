// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from marvin_msgs:msg/Extforce.idl
// generated code does not contain a copyright notice
#include "marvin_msgs/msg/detail/extforce__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"

bool
marvin_msgs__msg__Extforce__init(marvin_msgs__msg__Extforce * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    marvin_msgs__msg__Extforce__fini(msg);
    return false;
  }
  // joint_ext_force
  // eef_ext_force
  return true;
}

void
marvin_msgs__msg__Extforce__fini(marvin_msgs__msg__Extforce * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // joint_ext_force
  // eef_ext_force
}

bool
marvin_msgs__msg__Extforce__are_equal(const marvin_msgs__msg__Extforce * lhs, const marvin_msgs__msg__Extforce * rhs)
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
  // joint_ext_force
  for (size_t i = 0; i < 14; ++i) {
    if (lhs->joint_ext_force[i] != rhs->joint_ext_force[i]) {
      return false;
    }
  }
  // eef_ext_force
  for (size_t i = 0; i < 14; ++i) {
    if (lhs->eef_ext_force[i] != rhs->eef_ext_force[i]) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__msg__Extforce__copy(
  const marvin_msgs__msg__Extforce * input,
  marvin_msgs__msg__Extforce * output)
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
  // joint_ext_force
  for (size_t i = 0; i < 14; ++i) {
    output->joint_ext_force[i] = input->joint_ext_force[i];
  }
  // eef_ext_force
  for (size_t i = 0; i < 14; ++i) {
    output->eef_ext_force[i] = input->eef_ext_force[i];
  }
  return true;
}

marvin_msgs__msg__Extforce *
marvin_msgs__msg__Extforce__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Extforce * msg = (marvin_msgs__msg__Extforce *)allocator.allocate(sizeof(marvin_msgs__msg__Extforce), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(marvin_msgs__msg__Extforce));
  bool success = marvin_msgs__msg__Extforce__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
marvin_msgs__msg__Extforce__destroy(marvin_msgs__msg__Extforce * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    marvin_msgs__msg__Extforce__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
marvin_msgs__msg__Extforce__Sequence__init(marvin_msgs__msg__Extforce__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Extforce * data = NULL;

  if (size) {
    data = (marvin_msgs__msg__Extforce *)allocator.zero_allocate(size, sizeof(marvin_msgs__msg__Extforce), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = marvin_msgs__msg__Extforce__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        marvin_msgs__msg__Extforce__fini(&data[i - 1]);
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
marvin_msgs__msg__Extforce__Sequence__fini(marvin_msgs__msg__Extforce__Sequence * array)
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
      marvin_msgs__msg__Extforce__fini(&array->data[i]);
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

marvin_msgs__msg__Extforce__Sequence *
marvin_msgs__msg__Extforce__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Extforce__Sequence * array = (marvin_msgs__msg__Extforce__Sequence *)allocator.allocate(sizeof(marvin_msgs__msg__Extforce__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = marvin_msgs__msg__Extforce__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
marvin_msgs__msg__Extforce__Sequence__destroy(marvin_msgs__msg__Extforce__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    marvin_msgs__msg__Extforce__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
marvin_msgs__msg__Extforce__Sequence__are_equal(const marvin_msgs__msg__Extforce__Sequence * lhs, const marvin_msgs__msg__Extforce__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!marvin_msgs__msg__Extforce__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__msg__Extforce__Sequence__copy(
  const marvin_msgs__msg__Extforce__Sequence * input,
  marvin_msgs__msg__Extforce__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(marvin_msgs__msg__Extforce);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    marvin_msgs__msg__Extforce * data =
      (marvin_msgs__msg__Extforce *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!marvin_msgs__msg__Extforce__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          marvin_msgs__msg__Extforce__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!marvin_msgs__msg__Extforce__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
