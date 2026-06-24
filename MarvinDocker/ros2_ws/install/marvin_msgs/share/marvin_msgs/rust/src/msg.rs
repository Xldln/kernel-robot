#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to marvin_msgs__msg__Jointcmd

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Jointcmd {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub positions: [f64; 7],

}



impl Default for Jointcmd {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Jointcmd::default())
  }
}

impl rosidl_runtime_rs::Message for Jointcmd {
  type RmwMsg = super::msg::rmw::Jointcmd;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        positions: msg.positions,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        positions: msg.positions,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      positions: msg.positions,
    }
  }
}


// Corresponds to marvin_msgs__msg__Jointfeedback

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Jointfeedback {
    /// order L1,L2,L3,L4,L5,L6,L7,R1,R2,R3,R4,R5,R6,R7
    pub header: std_msgs::msg::Header,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Jointfeedback::default())
  }
}

impl rosidl_runtime_rs::Message for Jointfeedback {
  type RmwMsg = super::msg::rmw::Jointfeedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        positions: msg.positions,
        velocities: msg.velocities,
        efforts: msg.efforts,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        positions: msg.positions,
        velocities: msg.velocities,
        efforts: msg.efforts,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      positions: msg.positions,
      velocities: msg.velocities,
      efforts: msg.efforts,
    }
  }
}


// Corresponds to marvin_msgs__msg__Collimarker

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Collimarker {

    // This member is not documented.
    #[allow(missing_docs)]
    pub vectors: Vec<geometry_msgs::msg::Vector3>,

}



impl Default for Collimarker {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Collimarker::default())
  }
}

impl rosidl_runtime_rs::Message for Collimarker {
  type RmwMsg = super::msg::rmw::Collimarker;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vectors: msg.vectors
          .into_iter()
          .map(|elem| geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vectors: msg.vectors
          .iter()
          .map(|elem| geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vectors: msg.vectors
          .into_iter()
          .map(geometry_msgs::msg::Vector3::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to marvin_msgs__msg__KeypointPose
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
    pub gripper_value: f32,

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
        gripper_value: msg.gripper_value,
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
      gripper_value: msg.gripper_value,
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
      gripper_value: msg.gripper_value,
    }
  }
}


// Corresponds to marvin_msgs__msg__KeypointPoseArray
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


// Corresponds to marvin_msgs__msg__Extforce

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Extforce {
    /// order L1,L2,L3,L4,L5,L6,L7,R1,R2,R3,R4,R5,R6,R7
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_ext_force: [f64; 14],


    // This member is not documented.
    #[allow(missing_docs)]
    pub eef_ext_force: [f64; 14],

}



impl Default for Extforce {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Extforce::default())
  }
}

impl rosidl_runtime_rs::Message for Extforce {
  type RmwMsg = super::msg::rmw::Extforce;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        joint_ext_force: msg.joint_ext_force,
        eef_ext_force: msg.eef_ext_force,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        joint_ext_force: msg.joint_ext_force,
        eef_ext_force: msg.eef_ext_force,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      joint_ext_force: msg.joint_ext_force,
      eef_ext_force: msg.eef_ext_force,
    }
  }
}


