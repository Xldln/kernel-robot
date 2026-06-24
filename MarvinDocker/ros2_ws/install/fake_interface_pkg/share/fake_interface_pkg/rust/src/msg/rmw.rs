#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "fake_interface_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__ObjectPose() -> *const std::ffi::c_void;
}

#[link(name = "fake_interface_pkg__rosidl_generator_c")]
extern "C" {
    fn fake_interface_pkg__msg__ObjectPose__init(msg: *mut ObjectPose) -> bool;
    fn fake_interface_pkg__msg__ObjectPose__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ObjectPose>, size: usize) -> bool;
    fn fake_interface_pkg__msg__ObjectPose__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ObjectPose>);
    fn fake_interface_pkg__msg__ObjectPose__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ObjectPose>, out_seq: *mut rosidl_runtime_rs::Sequence<ObjectPose>) -> bool;
}

// Corresponds to fake_interface_pkg__msg__ObjectPose
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ObjectPose.msg

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObjectPose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// 注意名字要和 Pose.msg 一致
    pub poses: rosidl_runtime_rs::Sequence<super::super::msg::rmw::Pose>,

}



impl Default for ObjectPose {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !fake_interface_pkg__msg__ObjectPose__init(&mut msg as *mut _) {
        panic!("Call to fake_interface_pkg__msg__ObjectPose__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ObjectPose {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__ObjectPose__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__ObjectPose__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__ObjectPose__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ObjectPose {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ObjectPose where Self: Sized {
  const TYPE_NAME: &'static str = "fake_interface_pkg/msg/ObjectPose";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__ObjectPose() }
  }
}


#[link(name = "fake_interface_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__Action() -> *const std::ffi::c_void;
}

#[link(name = "fake_interface_pkg__rosidl_generator_c")]
extern "C" {
    fn fake_interface_pkg__msg__Action__init(msg: *mut Action) -> bool;
    fn fake_interface_pkg__msg__Action__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Action>, size: usize) -> bool;
    fn fake_interface_pkg__msg__Action__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Action>);
    fn fake_interface_pkg__msg__Action__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Action>, out_seq: *mut rosidl_runtime_rs::Sequence<Action>) -> bool;
}

// Corresponds to fake_interface_pkg__msg__Action
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Action.msg

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Action {
    /// 动作描述
    pub description: rosidl_runtime_rs::String,

    /// 对应目标物体名称
    pub goal: rosidl_runtime_rs::String,

    /// 动作类型，例如 pick/open/place
    pub action: rosidl_runtime_rs::String,

}



impl Default for Action {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !fake_interface_pkg__msg__Action__init(&mut msg as *mut _) {
        panic!("Call to fake_interface_pkg__msg__Action__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Action {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__Action__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__Action__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__Action__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Action {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Action where Self: Sized {
  const TYPE_NAME: &'static str = "fake_interface_pkg/msg/Action";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__Action() }
  }
}


#[link(name = "fake_interface_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__Pose() -> *const std::ffi::c_void;
}

#[link(name = "fake_interface_pkg__rosidl_generator_c")]
extern "C" {
    fn fake_interface_pkg__msg__Pose__init(msg: *mut Pose) -> bool;
    fn fake_interface_pkg__msg__Pose__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Pose>, size: usize) -> bool;
    fn fake_interface_pkg__msg__Pose__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Pose>);
    fn fake_interface_pkg__msg__Pose__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Pose>, out_seq: *mut rosidl_runtime_rs::Sequence<Pose>) -> bool;
}

// Corresponds to fake_interface_pkg__msg__Pose
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Pose.msg

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Pose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: geometry_msgs::msg::rmw::Point,


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientation: geometry_msgs::msg::rmw::Quaternion,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obj_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obj_name: rosidl_runtime_rs::String,

}



impl Default for Pose {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !fake_interface_pkg__msg__Pose__init(&mut msg as *mut _) {
        panic!("Call to fake_interface_pkg__msg__Pose__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Pose {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__Pose__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__Pose__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__Pose__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Pose {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Pose where Self: Sized {
  const TYPE_NAME: &'static str = "fake_interface_pkg/msg/Pose";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__Pose() }
  }
}


#[link(name = "fake_interface_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__ActionPlan() -> *const std::ffi::c_void;
}

#[link(name = "fake_interface_pkg__rosidl_generator_c")]
extern "C" {
    fn fake_interface_pkg__msg__ActionPlan__init(msg: *mut ActionPlan) -> bool;
    fn fake_interface_pkg__msg__ActionPlan__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ActionPlan>, size: usize) -> bool;
    fn fake_interface_pkg__msg__ActionPlan__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ActionPlan>);
    fn fake_interface_pkg__msg__ActionPlan__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ActionPlan>, out_seq: *mut rosidl_runtime_rs::Sequence<ActionPlan>) -> bool;
}

// Corresponds to fake_interface_pkg__msg__ActionPlan
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// ActionPlan.msg

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ActionPlan {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// 动作列表
    pub action_plan: rosidl_runtime_rs::Sequence<super::super::msg::rmw::Action>,

}



impl Default for ActionPlan {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !fake_interface_pkg__msg__ActionPlan__init(&mut msg as *mut _) {
        panic!("Call to fake_interface_pkg__msg__ActionPlan__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ActionPlan {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__ActionPlan__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__ActionPlan__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__ActionPlan__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ActionPlan {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ActionPlan where Self: Sized {
  const TYPE_NAME: &'static str = "fake_interface_pkg/msg/ActionPlan";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__ActionPlan() }
  }
}


#[link(name = "fake_interface_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__KeypointPose() -> *const std::ffi::c_void;
}

#[link(name = "fake_interface_pkg__rosidl_generator_c")]
extern "C" {
    fn fake_interface_pkg__msg__KeypointPose__init(msg: *mut KeypointPose) -> bool;
    fn fake_interface_pkg__msg__KeypointPose__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeypointPose>, size: usize) -> bool;
    fn fake_interface_pkg__msg__KeypointPose__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeypointPose>);
    fn fake_interface_pkg__msg__KeypointPose__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeypointPose>, out_seq: *mut rosidl_runtime_rs::Sequence<KeypointPose>) -> bool;
}

// Corresponds to fake_interface_pkg__msg__KeypointPose
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
    pub gripper_value: rosidl_runtime_rs::Sequence<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub time: rosidl_runtime_rs::Sequence<f32>,

}



impl Default for KeypointPose {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !fake_interface_pkg__msg__KeypointPose__init(&mut msg as *mut _) {
        panic!("Call to fake_interface_pkg__msg__KeypointPose__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeypointPose {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__KeypointPose__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__KeypointPose__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__KeypointPose__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeypointPose {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeypointPose where Self: Sized {
  const TYPE_NAME: &'static str = "fake_interface_pkg/msg/KeypointPose";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__KeypointPose() }
  }
}


#[link(name = "fake_interface_pkg__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__KeypointPoseArray() -> *const std::ffi::c_void;
}

#[link(name = "fake_interface_pkg__rosidl_generator_c")]
extern "C" {
    fn fake_interface_pkg__msg__KeypointPoseArray__init(msg: *mut KeypointPoseArray) -> bool;
    fn fake_interface_pkg__msg__KeypointPoseArray__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KeypointPoseArray>, size: usize) -> bool;
    fn fake_interface_pkg__msg__KeypointPoseArray__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KeypointPoseArray>);
    fn fake_interface_pkg__msg__KeypointPoseArray__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KeypointPoseArray>, out_seq: *mut rosidl_runtime_rs::Sequence<KeypointPoseArray>) -> bool;
}

// Corresponds to fake_interface_pkg__msg__KeypointPoseArray
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
      if !fake_interface_pkg__msg__KeypointPoseArray__init(&mut msg as *mut _) {
        panic!("Call to fake_interface_pkg__msg__KeypointPoseArray__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KeypointPoseArray {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__KeypointPoseArray__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__KeypointPoseArray__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { fake_interface_pkg__msg__KeypointPoseArray__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KeypointPoseArray {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KeypointPoseArray where Self: Sized {
  const TYPE_NAME: &'static str = "fake_interface_pkg/msg/KeypointPoseArray";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__fake_interface_pkg__msg__KeypointPoseArray() }
  }
}


