#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Jointcmd() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__msg__Jointcmd__init(msg: *mut Jointcmd) -> bool;
    fn marvin_msgs__msg__Jointcmd__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Jointcmd>, size: usize) -> bool;
    fn marvin_msgs__msg__Jointcmd__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Jointcmd>);
    fn marvin_msgs__msg__Jointcmd__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Jointcmd>, out_seq: *mut rosidl_runtime_rs::Sequence<Jointcmd>) -> bool;
}

// Corresponds to marvin_msgs__msg__Jointcmd
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Jointcmd {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub positions: [f64; 7],

}



impl Default for Jointcmd {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__msg__Jointcmd__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__msg__Jointcmd__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Jointcmd {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Jointcmd__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Jointcmd__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Jointcmd__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Jointcmd {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Jointcmd where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/msg/Jointcmd";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Jointcmd() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Jointfeedback() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__msg__Jointfeedback__init(msg: *mut Jointfeedback) -> bool;
    fn marvin_msgs__msg__Jointfeedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Jointfeedback>, size: usize) -> bool;
    fn marvin_msgs__msg__Jointfeedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Jointfeedback>);
    fn marvin_msgs__msg__Jointfeedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Jointfeedback>, out_seq: *mut rosidl_runtime_rs::Sequence<Jointfeedback>) -> bool;
}

// Corresponds to marvin_msgs__msg__Jointfeedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Jointfeedback {
    /// order L1,L2,L3,L4,L5,L6,L7,R1,R2,R3,R4,R5,R6,R7
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub positions: [f64; 14],


    // This member is not documented.
    #[allow(missing_docs)]
    pub velocities: [f64; 14],


    // This member is not documented.
    #[allow(missing_docs)]
    pub efforts: [f64; 14],

}



impl Default for Jointfeedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__msg__Jointfeedback__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__msg__Jointfeedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Jointfeedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Jointfeedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Jointfeedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Jointfeedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Jointfeedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Jointfeedback where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/msg/Jointfeedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Jointfeedback() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Collimarker() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__msg__Collimarker__init(msg: *mut Collimarker) -> bool;
    fn marvin_msgs__msg__Collimarker__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Collimarker>, size: usize) -> bool;
    fn marvin_msgs__msg__Collimarker__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Collimarker>);
    fn marvin_msgs__msg__Collimarker__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Collimarker>, out_seq: *mut rosidl_runtime_rs::Sequence<Collimarker>) -> bool;
}

// Corresponds to marvin_msgs__msg__Collimarker
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Collimarker {

    // This member is not documented.
    #[allow(missing_docs)]
    pub vectors: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Vector3>,

}



impl Default for Collimarker {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__msg__Collimarker__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__msg__Collimarker__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Collimarker {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Collimarker__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Collimarker__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Collimarker__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Collimarker {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Collimarker where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/msg/Collimarker";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Collimarker() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__KeypointPose() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__msg__KeypointPose__init(msg: *mut KeypointPose) -> bool;
    fn marvin_msgs__msg__KeypointPose__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeypointPose>, size: usize) -> bool;
    fn marvin_msgs__msg__KeypointPose__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeypointPose>);
    fn marvin_msgs__msg__KeypointPose__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeypointPose>, out_seq: *mut rosidl_runtime_rs::Sequence<KeypointPose>) -> bool;
}

// Corresponds to marvin_msgs__msg__KeypointPose
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 用于描述一个关键点

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeypointPose {
    /// 关键点名称
    pub name: rosidl_runtime_rs::String,

    /// 使用的机械臂，left/right
    pub arm: rosidl_runtime_rs::String,

    /// 位姿信息
    pub poses: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Pose>,

    /// 约束和速度
    /// xyz旋转约束
    pub constraints: [f32; 3],

    /// 移动速度
    pub speed: f32,

    /// 手爪控制
    /// 手爪开闭程度
    pub gripper_value: f32,

}



impl Default for KeypointPose {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__msg__KeypointPose__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__msg__KeypointPose__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeypointPose {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__KeypointPose__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__KeypointPose__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__KeypointPose__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeypointPose {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeypointPose where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/msg/KeypointPose";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__KeypointPose() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__KeypointPoseArray() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__msg__KeypointPoseArray__init(msg: *mut KeypointPoseArray) -> bool;
    fn marvin_msgs__msg__KeypointPoseArray__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeypointPoseArray>, size: usize) -> bool;
    fn marvin_msgs__msg__KeypointPoseArray__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeypointPoseArray>);
    fn marvin_msgs__msg__KeypointPoseArray__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeypointPoseArray>, out_seq: *mut rosidl_runtime_rs::Sequence<KeypointPoseArray>) -> bool;
}

// Corresponds to marvin_msgs__msg__KeypointPoseArray
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 用于发送一帧的所有关键点

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeypointPoseArray {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub poses: rosidl_runtime_rs::Sequence<super::super::msg::rmw::KeypointPose>,

}



impl Default for KeypointPoseArray {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__msg__KeypointPoseArray__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__msg__KeypointPoseArray__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeypointPoseArray {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__KeypointPoseArray__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__KeypointPoseArray__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__KeypointPoseArray__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeypointPoseArray {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeypointPoseArray where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/msg/KeypointPoseArray";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__KeypointPoseArray() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Extforce() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__msg__Extforce__init(msg: *mut Extforce) -> bool;
    fn marvin_msgs__msg__Extforce__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Extforce>, size: usize) -> bool;
    fn marvin_msgs__msg__Extforce__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Extforce>);
    fn marvin_msgs__msg__Extforce__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Extforce>, out_seq: *mut rosidl_runtime_rs::Sequence<Extforce>) -> bool;
}

// Corresponds to marvin_msgs__msg__Extforce
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Extforce {
    /// order L1,L2,L3,L4,L5,L6,L7,R1,R2,R3,R4,R5,R6,R7
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_ext_force: [f64; 14],


    // This member is not documented.
    #[allow(missing_docs)]
    pub eef_ext_force: [f64; 14],

}



impl Default for Extforce {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__msg__Extforce__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__msg__Extforce__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Extforce {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Extforce__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Extforce__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__msg__Extforce__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Extforce {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Extforce where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/msg/Extforce";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__msg__Extforce() }
  }
}


