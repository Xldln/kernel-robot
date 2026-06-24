// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from marvin_msgs:msg/Collimarker.idl
// generated code does not contain a copyright notice
#include "marvin_msgs/msg/detail/collimarker__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `vectors`
#include "geometry_msgs/msg/detail/vector3__functions.h"

bool
marvin_msgs__msg__Collimarker__init(marvin_msgs__msg__Collimarker * msg)
{
  if (!msg) {
    return false;
  }
  // vectors
  if (!geometry_msgs__msg__Vector3__Sequence__init(&msg->vectors, 0)) {
    marvin_msgs__msg__Collimarker__fini(msg);
    return false;
  }
  return true;
}

void
marvin_msgs__msg__Collimarker__fini(marvin_msgs__msg__Collimarker * msg)
{
  if (!msg) {
    return;
  }
  // vectors
  geometry_msgs__msg__Vector3__Sequence__fini(&msg->vectors);
}

bool
marvin_msgs__msg__Collimarker__are_equal(const marvin_msgs__msg__Collimarker * lhs, const marvin_msgs__msg__Collimarker * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // vectors
  if (!geometry_msgs__msg__Vector3__Sequence__are_equal(
      &(lhs->vectors), &(rhs->vectors)))
  {
    return false;
  }
  return true;
}

bool
marvin_msgs__msg__Collimarker__copy(
  const marvin_msgs__msg__Collimarker * input,
  marvin_msgs__msg__Collimarker * output)
{
  if (!input || !output) {
    return false;
  }
  // vectors
  if (!geometry_msgs__msg__Vector3__Sequence__copy(
      &(input->vectors), &(output->vectors)))
  {
    return false;
  }
  return true;
}

marvin_msgs__msg__Collimarker *
marvin_msgs__msg__Collimarker__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Collimarker * msg = (marvin_msgs__msg__Collimarker *)allocator.allocate(sizeof(marvin_msgs__msg__Collimarker), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(marvin_msgs__msg__Collimarker));
  bool success = marvin_msgs__msg__Collimarker__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
marvin_msgs__msg__Collimarker__destroy(marvin_msgs__msg__Collimarker * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    marvin_msgs__msg__Collimarker__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
marvin_msgs__msg__Collimarker__Sequence__init(marvin_msgs__msg__Collimarker__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Collimarker * data = NULL;

  if (size) {
    data = (marvin_msgs__msg__Collimarker *)allocator.zero_allocate(size, sizeof(marvin_msgs__msg__Collimarker), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = marvin_msgs__msg__Collimarker__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        marvin_msgs__msg__Collimarker__fini(&data[i - 1]);
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
marvin_msgs__msg__Collimarker__Sequence__fini(marvin_msgs__msg__Collimarker__Sequence * array)
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
      marvin_msgs__msg__Collimarker__fini(&array->data[i]);
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

marvin_msgs__msg__Collimarker__Sequence *
marvin_msgs__msg__Collimarker__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__msg__Collimarker__Sequence * array = (marvin_msgs__msg__Collimarker__Sequence *)allocator.allocate(sizeof(marvin_msgs__msg__Collimarker__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = marvin_msgs__msg__Collimarker__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
marvin_msgs__msg__Collimarker__Sequence__destroy(marvin_msgs__msg__Collimarker__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    marvin_msgs__msg__Collimarker__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
marvin_msgs__msg__Collimarker__Sequence__are_equal(const marvin_msgs__msg__Collimarker__Sequence * lhs, const marvin_msgs__msg__Collimarker__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!marvin_msgs__msg__Collimarker__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__msg__Collimarker__Sequence__copy(
  const marvin_msgs__msg__Collimarker__Sequence * input,
  marvin_msgs__msg__Collimarker__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(marvin_msgs__msg__Collimarker);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    marvin_msgs__msg__Collimarker * data =
      (marvin_msgs__msg__Collimarker *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!marvin_msgs__msg__Collimarker__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          marvin_msgs__msg__Collimarker__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!marvin_msgs__msg__Collimarker__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
