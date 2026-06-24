// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from marvin_msgs:srv/Velratio.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "marvin_msgs/srv/detail/velratio__rosidl_typesupport_introspection_c.h"
#include "marvin_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "marvin_msgs/srv/detail/velratio__functions.h"
#include "marvin_msgs/srv/detail/velratio__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  marvin_msgs__srv__Velratio_Request__init(message_memory);
}

void marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_fini_function(void * message_memory)
{
  marvin_msgs__srv__Velratio_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_member_array[2] = {
  {
    "vel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__srv__Velratio_Request, vel),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "acc",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__srv__Velratio_Request, acc),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_members = {
  "marvin_msgs__srv",  // message namespace
  "Velratio_Request",  // message name
  2,  // number of fields
  sizeof(marvin_msgs__srv__Velratio_Request),
  marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_member_array,  // message members
  marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_type_support_handle = {
  0,
  &marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_marvin_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, srv, Velratio_Request)() {
  if (!marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_type_support_handle.typesupport_identifier) {
    marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &marvin_msgs__srv__Velratio_Request__rosidl_typesupport_introspection_c__Velratio_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "marvin_msgs/srv/detail/velratio__rosidl_typesupport_introspection_c.h"
// already included above
// #include "marvin_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "marvin_msgs/srv/detail/velratio__functions.h"
// already included above
// #include "marvin_msgs/srv/detail/velratio__struct.h"


// Include directives for member types
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  marvin_msgs__srv__Velratio_Response__init(message_memory);
}

void marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_fini_function(void * message_memory)
{
  marvin_msgs__srv__Velratio_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_member_array[3] = {
  {
    "error_code",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__srv__Velratio_Response, error_code),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__srv__Velratio_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(marvin_msgs__srv__Velratio_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_members = {
  "marvin_msgs__srv",  // message namespace
  "Velratio_Response",  // message name
  3,  // number of fields
  sizeof(marvin_msgs__srv__Velratio_Response),
  marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_member_array,  // message members
  marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_type_support_handle = {
  0,
  &marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_marvin_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, srv, Velratio_Response)() {
  if (!marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_type_support_handle.typesupport_identifier) {
    marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &marvin_msgs__srv__Velratio_Response__rosidl_typesupport_introspection_c__Velratio_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "marvin_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "marvin_msgs/srv/detail/velratio__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_service_members = {
  "marvin_msgs__srv",  // service namespace
  "Velratio",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_Request_message_type_support_handle,
  NULL  // response message
  // marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_Response_message_type_support_handle
};

static rosidl_service_type_support_t marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_service_type_support_handle = {
  0,
  &marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, srv, Velratio_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, srv, Velratio_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_marvin_msgs
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, srv, Velratio)() {
  if (!marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_service_type_support_handle.typesupport_identifier) {
    marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, srv, Velratio_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, marvin_msgs, srv, Velratio_Response)()->data;
  }

  return &marvin_msgs__srv__detail__velratio__rosidl_typesupport_introspection_c__Velratio_service_type_support_handle;
}
