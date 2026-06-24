// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from marvin_msgs:msg/Collimarker.idl
// generated code does not contain a copyright notice

#ifndef MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__STRUCT_HPP_
#define MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'vectors'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__marvin_msgs__msg__Collimarker __attribute__((deprecated))
#else
# define DEPRECATED__marvin_msgs__msg__Collimarker __declspec(deprecated)
#endif

namespace marvin_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Collimarker_
{
  using Type = Collimarker_<ContainerAllocator>;

  explicit Collimarker_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit Collimarker_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _vectors_type =
    std::vector<geometry_msgs::msg::Vector3_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Vector3_<ContainerAllocator>>>;
  _vectors_type vectors;

  // setters for named parameter idiom
  Type & set__vectors(
    const std::vector<geometry_msgs::msg::Vector3_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<geometry_msgs::msg::Vector3_<ContainerAllocator>>> & _arg)
  {
    this->vectors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    marvin_msgs::msg::Collimarker_<ContainerAllocator> *;
  using ConstRawPtr =
    const marvin_msgs::msg::Collimarker_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Collimarker_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      marvin_msgs::msg::Collimarker_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__marvin_msgs__msg__Collimarker
    std::shared_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__marvin_msgs__msg__Collimarker
    std::shared_ptr<marvin_msgs::msg::Collimarker_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Collimarker_ & other) const
  {
    if (this->vectors != other.vectors) {
      return false;
    }
    return true;
  }
  bool operator!=(const Collimarker_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Collimarker_

// alias to use template instance with default allocator
using Collimarker =
  marvin_msgs::msg::Collimarker_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace marvin_msgs

#endif  // MARVIN_MSGS__MSG__DETAIL__COLLIMARKER__STRUCT_HPP_
