// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from marvin_msgs:srv/MotorErrCode.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__STRUCT_HPP_
#define MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__marvin_msgs__srv__MotorErrCode_Request __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__srv__MotorErrCode_Request __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MotorErrCode_Request_
{
  using Type = MotorErrCode_Request_<ContainerAllocator>;

  explicit MotorErrCode_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit MotorErrCode_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__srv__MotorErrCode_Request
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__srv__MotorErrCode_Request
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorErrCode_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorErrCode_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorErrCode_Request_

// alias to use template instance with default allocator
using MotorErrCode_Request =
  marvin_msgs::srv::MotorErrCode_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace marvin_msgs


#ifndef _WIN32
# define DEPRECATED__marvin_msgs__srv__MotorErrCode_Response __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__srv__MotorErrCode_Response __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MotorErrCode_Response_
{
  using Type = MotorErrCode_Response_<ContainerAllocator>;

  explicit MotorErrCode_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit MotorErrCode_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _error_code_type =
    std::vector<int16_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int16_t>>;
  _error_code_type error_code;
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__error_code(
    const std::vector<int16_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int16_t>> & _arg)
  {
    this->error_code = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__srv__MotorErrCode_Response
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__srv__MotorErrCode_Response
    std::shared_ptr<marvin_msgs::srv::MotorErrCode_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorErrCode_Response_ & other) const
  {
    if (this->error_code != other.error_code) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorErrCode_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorErrCode_Response_

// alias to use template instance with default allocator
using MotorErrCode_Response =
  marvin_msgs::srv::MotorErrCode_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace marvin_msgs

namespace marvin_msgs
{

namespace srv
{

struct MotorErrCode
{
  using Request = marvin_msgs::srv::MotorErrCode_Request;
  using Response = marvin_msgs::srv::MotorErrCode_Response;
};

}  // namespace srv

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__SRV__DETAIL__MOTOR_ERR_CODE__STRUCT_HPP_
