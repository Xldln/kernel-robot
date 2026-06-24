// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from marvin_msgs:srv/Velratio.idl
// generated code does not contain a copyright notice
#include "marvin_msgs/srv/detail/velratio__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
marvin_msgs__srv__Velratio_Request__init(marvin_msgs__srv__Velratio_Request * msg)
{
  if (!msg) {
    return false;
  }
  // vel
  // acc
  return true;
}

void
marvin_msgs__srv__Velratio_Request__fini(marvin_msgs__srv__Velratio_Request * msg)
{
  if (!msg) {
    return;
  }
  // vel
  // acc
}

bool
marvin_msgs__srv__Velratio_Request__are_equal(const marvin_msgs__srv__Velratio_Request * lhs, const marvin_msgs__srv__Velratio_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // vel
  if (lhs->vel != rhs->vel) {
    return false;
  }
  // acc
  if (lhs->acc != rhs->acc) {
    return false;
  }
  return true;
}

bool
marvin_msgs__srv__Velratio_Request__copy(
  const marvin_msgs__srv__Velratio_Request * input,
  marvin_msgs__srv__Velratio_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // vel
  output->vel = input->vel;
  // acc
  output->acc = input->acc;
  return true;
}

marvin_msgs__srv__Velratio_Request *
marvin_msgs__srv__Velratio_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__srv__Velratio_Request * msg = (marvin_msgs__srv__Velratio_Request *)allocator.allocate(sizeof(marvin_msgs__srv__Velratio_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(marvin_msgs__srv__Velratio_Request));
  bool success = marvin_msgs__srv__Velratio_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
marvin_msgs__srv__Velratio_Request__destroy(marvin_msgs__srv__Velratio_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    marvin_msgs__srv__Velratio_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
marvin_msgs__srv__Velratio_Request__Sequence__init(marvin_msgs__srv__Velratio_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__srv__Velratio_Request * data = NULL;

  if (size) {
    data = (marvin_msgs__srv__Velratio_Request *)allocator.zero_allocate(size, sizeof(marvin_msgs__srv__Velratio_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = marvin_msgs__srv__Velratio_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        marvin_msgs__srv__Velratio_Request__fini(&data[i - 1]);
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
marvin_msgs__srv__Velratio_Request__Sequence__fini(marvin_msgs__srv__Velratio_Request__Sequence * array)
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
      marvin_msgs__srv__Velratio_Request__fini(&array->data[i]);
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

marvin_msgs__srv__Velratio_Request__Sequence *
marvin_msgs__srv__Velratio_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__srv__Velratio_Request__Sequence * array = (marvin_msgs__srv__Velratio_Request__Sequence *)allocator.allocate(sizeof(marvin_msgs__srv__Velratio_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = marvin_msgs__srv__Velratio_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
marvin_msgs__srv__Velratio_Request__Sequence__destroy(marvin_msgs__srv__Velratio_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    marvin_msgs__srv__Velratio_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
marvin_msgs__srv__Velratio_Request__Sequence__are_equal(const marvin_msgs__srv__Velratio_Request__Sequence * lhs, const marvin_msgs__srv__Velratio_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!marvin_msgs__srv__Velratio_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__srv__Velratio_Request__Sequence__copy(
  const marvin_msgs__srv__Velratio_Request__Sequence * input,
  marvin_msgs__srv__Velratio_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(marvin_msgs__srv__Velratio_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    marvin_msgs__srv__Velratio_Request * data =
      (marvin_msgs__srv__Velratio_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!marvin_msgs__srv__Velratio_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          marvin_msgs__srv__Velratio_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!marvin_msgs__srv__Velratio_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
marvin_msgs__srv__Velratio_Response__init(marvin_msgs__srv__Velratio_Response * msg)
{
  if (!msg) {
    return false;
  }
  // error_code
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    marvin_msgs__srv__Velratio_Response__fini(msg);
    return false;
  }
  return true;
}

void
marvin_msgs__srv__Velratio_Response__fini(marvin_msgs__srv__Velratio_Response * msg)
{
  if (!msg) {
    return;
  }
  // error_code
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
marvin_msgs__srv__Velratio_Response__are_equal(const marvin_msgs__srv__Velratio_Response * lhs, const marvin_msgs__srv__Velratio_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // error_code
  if (lhs->error_code != rhs->error_code) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
marvin_msgs__srv__Velratio_Response__copy(
  const marvin_msgs__srv__Velratio_Response * input,
  marvin_msgs__srv__Velratio_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // error_code
  output->error_code = input->error_code;
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

marvin_msgs__srv__Velratio_Response *
marvin_msgs__srv__Velratio_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__srv__Velratio_Response * msg = (marvin_msgs__srv__Velratio_Response *)allocator.allocate(sizeof(marvin_msgs__srv__Velratio_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(marvin_msgs__srv__Velratio_Response));
  bool success = marvin_msgs__srv__Velratio_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
marvin_msgs__srv__Velratio_Response__destroy(marvin_msgs__srv__Velratio_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    marvin_msgs__srv__Velratio_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
marvin_msgs__srv__Velratio_Response__Sequence__init(marvin_msgs__srv__Velratio_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__srv__Velratio_Response * data = NULL;

  if (size) {
    data = (marvin_msgs__srv__Velratio_Response *)allocator.zero_allocate(size, sizeof(marvin_msgs__srv__Velratio_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = marvin_msgs__srv__Velratio_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        marvin_msgs__srv__Velratio_Response__fini(&data[i - 1]);
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
marvin_msgs__srv__Velratio_Response__Sequence__fini(marvin_msgs__srv__Velratio_Response__Sequence * array)
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
      marvin_msgs__srv__Velratio_Response__fini(&array->data[i]);
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

marvin_msgs__srv__Velratio_Response__Sequence *
marvin_msgs__srv__Velratio_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  marvin_msgs__srv__Velratio_Response__Sequence * array = (marvin_msgs__srv__Velratio_Response__Sequence *)allocator.allocate(sizeof(marvin_msgs__srv__Velratio_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = marvin_msgs__srv__Velratio_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
marvin_msgs__srv__Velratio_Response__Sequence__destroy(marvin_msgs__srv__Velratio_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    marvin_msgs__srv__Velratio_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
marvin_msgs__srv__Velratio_Response__Sequence__are_equal(const marvin_msgs__srv__Velratio_Response__Sequence * lhs, const marvin_msgs__srv__Velratio_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!marvin_msgs__srv__Velratio_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
marvin_msgs__srv__Velratio_Response__Sequence__copy(
  const marvin_msgs__srv__Velratio_Response__Sequence * input,
  marvin_msgs__srv__Velratio_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(marvin_msgs__srv__Velratio_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    marvin_msgs__srv__Velratio_Response * data =
      (marvin_msgs__srv__Velratio_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!marvin_msgs__srv__Velratio_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          marvin_msgs__srv__Velratio_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!marvin_msgs__srv__Velratio_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
