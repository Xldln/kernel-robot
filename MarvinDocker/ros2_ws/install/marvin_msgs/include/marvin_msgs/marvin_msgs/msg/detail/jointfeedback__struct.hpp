// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from marvin_msgs:msg/Jointfeedback.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__STRUCT_HPP_
#define MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__STRUCT_HPP_

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
# define DEPRECATED__marvin_msgs__msg__Jointfeedback __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__msg__Jointfeedback __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Jointfeedback_
{
  using Type = Jointfeedback_<ContainerAllocator>;

  explicit Jointfeedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 14>::iterator, double>(this->positions.begin(), this->positions.end(), 0.0);
      std::fill<typename std::array<double, 14>::iterator, double>(this->velocities.begin(), this->velocities.end(), 0.0);
      std::fill<typename std::array<double, 14>::iterator, double>(this->efforts.begin(), this->efforts.end(), 0.0);
    }
  }

  explicit Jointfeedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    positions(_alloc),
    velocities(_alloc),
    efforts(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 14>::iterator, double>(this->positions.begin(), this->positions.end(), 0.0);
      std::fill<typename std::array<double, 14>::iterator, double>(this->velocities.begin(), this->velocities.end(), 0.0);
      std::fill<typename std::array<double, 14>::iterator, double>(this->efforts.begin(), this->efforts.end(), 0.0);
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _positions_type =
    std::array<double, 14>;
  _positions_type positions;
  using _velocities_type =
    std::array<double, 14>;
  _velocities_type velocities;
  using _efforts_type =
    std::array<double, 14>;
  _efforts_type efforts;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__positions(
    const std::array<double, 14> & _arg)
  {
    this->positions = _arg;
    return *this;
  }
  Type & set__velocities(
    const std::array<double, 14> & _arg)
  {
    this->velocities = _arg;
    return *this;
  }
  Type & set__efforts(
    const std::array<double, 14> & _arg)
  {
    this->efforts = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    marvin_msgs::msg::Jointfeedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::msg::Jointfeedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Jointfeedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Jointfeedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__msg__Jointfeedback
    std::shared_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__msg__Jointfeedback
    std::shared_ptr<marvin_msgs::msg::Jointfeedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Jointfeedback_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->positions != other.positions) {
      return false;
    }
    if (this->velocities != other.velocities) {
      return false;
    }
    if (this->efforts != other.efforts) {
      return false;
    }
    return true;
  }
  bool operator!=(const Jointfeedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Jointfeedback_

// alias to use template instance with default allocator
using Jointfeedback =
  marvin_msgs::msg::Jointfeedback_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__JOINTFEEDBACK__STRUCT_HPP_
