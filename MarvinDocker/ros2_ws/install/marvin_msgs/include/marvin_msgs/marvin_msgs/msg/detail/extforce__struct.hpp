// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from marvin_msgs:msg/Extforce.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__EXTFORCE__STRUCT_HPP_
#define MARVIN_MSGS__MSG__DETAIL__EXTFORCE__STRUCT_HPP_

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
# define DEPRECATED__marvin_msgs__msg__Extforce __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__msg__Extforce __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Extforce_
{
  using Type = Extforce_<ContainerAllocator>;

  explicit Extforce_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 14>::iterator, double>(this->joint_ext_force.begin(), this->joint_ext_force.end(), 0.0);
      std::fill<typename std::array<double, 14>::iterator, double>(this->eef_ext_force.begin(), this->eef_ext_force.end(), 0.0);
    }
  }

  explicit Extforce_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    joint_ext_force(_alloc),
    eef_ext_force(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 14>::iterator, double>(this->joint_ext_force.begin(), this->joint_ext_force.end(), 0.0);
      std::fill<typename std::array<double, 14>::iterator, double>(this->eef_ext_force.begin(), this->eef_ext_force.end(), 0.0);
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _joint_ext_force_type =
    std::array<double, 14>;
  _joint_ext_force_type joint_ext_force;
  using _eef_ext_force_type =
    std::array<double, 14>;
  _eef_ext_force_type eef_ext_force;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__joint_ext_force(
    const std::array<double, 14> & _arg)
  {
    this->joint_ext_force = _arg;
    return *this;
  }
  Type & set__eef_ext_force(
    const std::array<double, 14> & _arg)
  {
    this->eef_ext_force = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    marvin_msgs::msg::Extforce_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::msg::Extforce_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Extforce_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Extforce_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__msg__Extforce
    std::shared_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__msg__Extforce
    std::shared_ptr<marvin_msgs::msg::Extforce_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Extforce_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->joint_ext_force != other.joint_ext_force) {
      return false;
    }
    if (this->eef_ext_force != other.eef_ext_force) {
      return false;
    }
    return true;
  }
  bool operator!=(const Extforce_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Extforce_

// alias to use template instance with default allocator
using Extforce =
  marvin_msgs::msg::Extforce_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__EXTFORCE__STRUCT_HPP_
