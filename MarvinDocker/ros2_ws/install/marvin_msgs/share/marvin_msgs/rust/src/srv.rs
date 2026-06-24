#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to marvin_msgs__srv__Int_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Int_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: i64,

}



impl Default for Int_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Int_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Int_Request {
  type RmwMsg = super::srv::rmw::Int_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      data: msg.data,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data,
    }
  }
}


// Corresponds to marvin_msgs__srv__Int_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Int_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for Int_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Int_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Int_Response {
  type RmwMsg = super::srv::rmw::Int_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        error_code: msg.error_code,
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      error_code: msg.error_code,
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      error_code: msg.error_code,
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to marvin_msgs__srv__Velratio_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Velratio_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub vel: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: i64,

}



impl Default for Velratio_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Velratio_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Velratio_Request {
  type RmwMsg = super::srv::rmw::Velratio_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel: msg.vel,
        acc: msg.acc,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      vel: msg.vel,
      acc: msg.acc,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel: msg.vel,
      acc: msg.acc,
    }
  }
}


// Corresponds to marvin_msgs__srv__Velratio_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Velratio_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for Velratio_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Velratio_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Velratio_Response {
  type RmwMsg = super::srv::rmw::Velratio_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        error_code: msg.error_code,
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      error_code: msg.error_code,
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      error_code: msg.error_code,
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to marvin_msgs__srv__MotorErrCode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotorErrCode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for MotorErrCode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MotorErrCode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MotorErrCode_Request {
  type RmwMsg = super::srv::rmw::MotorErrCode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to marvin_msgs__srv__MotorErrCode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotorErrCode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: Vec<i16>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for MotorErrCode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MotorErrCode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MotorErrCode_Response {
  type RmwMsg = super::srv::rmw::MotorErrCode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        error_code: msg.error_code.into(),
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        error_code: msg.error_code.as_slice().into(),
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      error_code: msg.error_code
          .into_iter()
          .collect(),
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__marvin_msgs__srv__Int() -> *const std::ffi::c_void;
}

// Corresponds to marvin_msgs__srv__Int
#[allow(missing_docs, non_camel_case_types)]
pub struct Int;

impl rosidl_runtime_rs::Service for Int {
    type Request = Int_Request;
    type Response = Int_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__marvin_msgs__srv__Int() }
    }
}




#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__marvin_msgs__srv__Velratio() -> *const std::ffi::c_void;
}

// Corresponds to marvin_msgs__srv__Velratio
#[allow(missing_docs, non_camel_case_types)]
pub struct Velratio;

impl rosidl_runtime_rs::Service for Velratio {
    type Request = Velratio_Request;
    type Response = Velratio_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__marvin_msgs__srv__Velratio() }
    }
}




#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__marvin_msgs__srv__MotorErrCode() -> *const std::ffi::c_void;
}

// Corresponds to marvin_msgs__srv__MotorErrCode
#[allow(missing_docs, non_camel_case_types)]
pub struct MotorErrCode;

impl rosidl_runtime_rs::Service for MotorErrCode {
    type Request = MotorErrCode_Request;
    type Response = MotorErrCode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__marvin_msgs__srv__MotorErrCode() }
    }
}


