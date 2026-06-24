// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from marvin_msgs:srv/Int.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__SRV__DETAIL__INT__STRUCT_HPP_
#define MARVIN_MSGS__SRV__DETAIL__INT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__marvin_msgs__srv__Int_Request __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__srv__Int_Request __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Int_Request_
{
  using Type = Int_Request_<ContainerAllocator>;

  explicit Int_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = 0ll;
    }
  }

  explicit Int_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = 0ll;
    }
  }

  // field types and members
  using _data_type =
    int64_t;
  _data_type data;

  // setters for named parameter idiom
  Type & set__data(
    const int64_t & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    marvin_msgs::srv::Int_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::srv::Int_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::Int_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::Int_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__srv__Int_Request
    std::shared_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__srv__Int_Request
    std::shared_ptr<marvin_msgs::srv::Int_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Int_Request_ & other) const
  {
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const Int_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Int_Request_

// alias to use template instance with default allocator
using Int_Request =
  marvin_msgs::srv::Int_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace marvin_msgs


#ifndef _WIN32
# define DEPRECATED__marvin_msgs__srv__Int_Response __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__srv__Int_Response __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Int_Response_
{
  using Type = Int_Response_<ContainerAllocator>;

  explicit Int_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->error_code = 0ll;
      this->success = false;
      this->message = "";
    }
  }

  explicit Int_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->error_code = 0ll;
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _error_code_type =
    int64_t;
  _error_code_type error_code;
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__error_code(
    const int64_t & _arg)
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
    marvin_msgs::srv::Int_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::srv::Int_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::Int_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::srv::Int_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__srv__Int_Response
    std::shared_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__srv__Int_Response
    std::shared_ptr<marvin_msgs::srv::Int_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Int_Response_ & other) const
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
  bool operator!=(const Int_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Int_Response_

// alias to use template instance with default allocator
using Int_Response =
  marvin_msgs::srv::Int_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace marvin_msgs

namespace marvin_msgs
{

namespace srv
{

struct Int
{
  using Request = marvin_msgs::srv::Int_Request;
  using Response = marvin_msgs::srv::Int_Response;
};

}  // namespace srv

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__SRV__DETAIL__INT__STRUCT_HPP_
