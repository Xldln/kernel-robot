#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to fake_interface_pkg__msg__ObjectPose
/// ObjectPose.msg

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ObjectPose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// 注意名字要和 Pose.msg 一致
    pub poses: Vec<super::msg::Pose>,

}



impl Default for ObjectPose {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ObjectPose::default())
  }
}

impl rosidl_runtime_rs::Message for ObjectPose {
  type RmwMsg = super::msg::rmw::ObjectPose;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        poses: msg.poses
          .into_iter()
          .map(|elem| super::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        poses: msg.poses
          .iter()
          .map(|elem| super::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      poses: msg.poses
          .into_iter()
          .map(super::msg::Pose::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to fake_interface_pkg__msg__Action
/// Action.msg

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Action {
    /// 动作描述
    pub description: std::string::String,

    /// 对应目标物体名称
    pub goal: std::string::String,

    /// 动作类型，例如 pick/open/place
    pub action: std::string::String,

}



impl Default for Action {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Action::default())
  }
}

impl rosidl_runtime_rs::Message for Action {
  type RmwMsg = super::msg::rmw::Action;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        description: msg.description.as_str().into(),
        goal: msg.goal.as_str().into(),
        action: msg.action.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        description: msg.description.as_str().into(),
        goal: msg.goal.as_str().into(),
        action: msg.action.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      description: msg.description.to_string(),
      goal: msg.goal.to_string(),
      action: msg.action.to_string(),
    }
  }
}


// Corresponds to fake_interface_pkg__msg__Pose
/// Pose.msg

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Pose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position: geometry_msgs::msg::Point,


    // This member is not documented.
    #[allow(missing_docs)]
    pub orientation: geometry_msgs::msg::Quaternion,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obj_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub obj_name: std::string::String,

}



impl Default for Pose {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Pose::default())
  }
}

impl rosidl_runtime_rs::Message for Pose {
  type RmwMsg = super::msg::rmw::Pose;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.position)).into_owned(),
        orientation: geometry_msgs::msg::Quaternion::into_rmw_message(std::borrow::Cow::Owned(msg.orientation)).into_owned(),
        obj_id: msg.obj_id,
        obj_name: msg.obj_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.position)).into_owned(),
        orientation: geometry_msgs::msg::Quaternion::into_rmw_message(std::borrow::Cow::Borrowed(&msg.orientation)).into_owned(),
      obj_id: msg.obj_id,
        obj_name: msg.obj_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      position: geometry_msgs::msg::Point::from_rmw_message(msg.position),
      orientation: geometry_msgs::msg::Quaternion::from_rmw_message(msg.orientation),
      obj_id: msg.obj_id,
      obj_name: msg.obj_name.to_string(),
    }
  }
}


// Corresponds to fake_interface_pkg__msg__ActionPlan
/// ActionPlan.msg

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ActionPlan {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// 动作列表
    pub action_plan: Vec<super::msg::Action>,

}



impl Default for ActionPlan {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ActionPlan::default())
  }
}

impl rosidl_runtime_rs::Message for ActionPlan {
  type RmwMsg = super::msg::rmw::ActionPlan;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        action_plan: msg.action_plan
          .into_iter()
          .map(|elem| super::msg::Action::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        action_plan: msg.action_plan
          .iter()
          .map(|elem| super::msg::Action::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      action_plan: msg.action_plan
          .into_iter()
          .map(super::msg::Action::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to fake_interface_pkg__msg__KeypointPose
/// 用于描述一个关键点

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeypointPose {
    /// 关键点名称
    pub name: std::string::String,

    /// 使用的机械臂，left/right
    pub arm: std::string::String,

    /// 位姿信息
    pub poses: Vec<geometry_msgs::msg::Pose>,

    /// 约束和速度
    /// xyz旋转约束
    pub constraints: [f32; 3],

    /// 移动速度
    pub speed: f32,

    /// 手爪控制
    /// 手爪开闭程度
    pub gripper_value: Vec<f32>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub time: Vec<f32>,

}



impl Default for KeypointPose {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::KeypointPose::default())
  }
}

impl rosidl_runtime_rs::Message for KeypointPose {
  type RmwMsg = super::msg::rmw::KeypointPose;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        arm: msg.arm.as_str().into(),
        poses: msg.poses
          .into_iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        constraints: msg.constraints,
        speed: msg.speed,
        gripper_value: msg.gripper_value.into(),
        time: msg.time.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        arm: msg.arm.as_str().into(),
        poses: msg.poses
          .iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        constraints: msg.constraints,
      speed: msg.speed,
        gripper_value: msg.gripper_value.as_slice().into(),
        time: msg.time.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      arm: msg.arm.to_string(),
      poses: msg.poses
          .into_iter()
          .map(geometry_msgs::msg::Pose::from_rmw_message)
          .collect(),
      constraints: msg.constraints,
      speed: msg.speed,
      gripper_value: msg.gripper_value
          .into_iter()
          .collect(),
      time: msg.time
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to fake_interface_pkg__msg__KeypointPoseArray
/// 用于发送一帧的所有关键点

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KeypointPoseArray {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub poses: Vec<super::msg::KeypointPose>,

}



impl Default for KeypointPoseArray {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::KeypointPoseArray::default())
  }
}

impl rosidl_runtime_rs::Message for KeypointPoseArray {
  type RmwMsg = super::msg::rmw::KeypointPoseArray;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        poses: msg.poses
          .into_iter()
          .map(|elem| super::msg::KeypointPose::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        poses: msg.poses
          .iter()
          .map(|elem| super::msg::KeypointPose::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      poses: msg.poses
          .into_iter()
          .map(super::msg::KeypointPose::from_rmw_message)
          .collect(),
    }
  }
}


