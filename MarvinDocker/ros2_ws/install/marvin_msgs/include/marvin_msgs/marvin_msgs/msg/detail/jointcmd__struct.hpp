// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from marvin_msgs:msg/Jointcmd.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTCMD__STRUCT_HPP_
#define MARVIN_MSGS__MSG__DETAIL__JOINTCMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__marvin_msgs__msg__Jointcmd __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__msg__Jointcmd __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Jointcmd_
{
  using Type = Jointcmd_<ContainerAllocator>;

  explicit Jointcmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 7>::iterator, double>(this->positions.begin(), this->positions.end(), 0.0);
    }
  }

  explicit Jointcmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    positions(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 7>::iterator, double>(this->positions.begin(), this->positions.end(), 0.0);
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _positions_type =
    std::array<double, 7>;
  _positions_type positions;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__positions(
    const std::array<double, 7> & _arg)
  {
    this->positions = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    marvin_msgs::msg::Jointcmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::msg::Jointcmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Jointcmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Jointcmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__msg__Jointcmd
    std::shared_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__msg__Jointcmd
    std::shared_ptr<marvin_msgs::msg::Jointcmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Jointcmd_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->positions != other.positions) {
      return false;
    }
    return true;
  }
  bool operator!=(const Jointcmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Jointcmd_

// alias to use template instance with default allocator
using Jointcmd =
  marvin_msgs::msg::Jointcmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTCMD__STRUCT_HPP_
