#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Int_Request() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__srv__Int_Request__init(msg: *mut Int_Request) -> bool;
    fn marvin_msgs__srv__Int_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Int_Request>, size: usize) -> bool;
    fn marvin_msgs__srv__Int_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Int_Request>);
    fn marvin_msgs__srv__Int_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Int_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Int_Request>) -> bool;
}

// Corresponds to marvin_msgs__srv__Int_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Int_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: i64,

}



impl Default for Int_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__srv__Int_Request__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__srv__Int_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Int_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Int_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Int_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Int_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Int_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Int_Request where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/srv/Int_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Int_Request() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Int_Response() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__srv__Int_Response__init(msg: *mut Int_Response) -> bool;
    fn marvin_msgs__srv__Int_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Int_Response>, size: usize) -> bool;
    fn marvin_msgs__srv__Int_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Int_Response>);
    fn marvin_msgs__srv__Int_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Int_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Int_Response>) -> bool;
}

// Corresponds to marvin_msgs__srv__Int_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub message: rosidl_runtime_rs::String,

}



impl Default for Int_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__srv__Int_Response__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__srv__Int_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Int_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Int_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Int_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Int_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Int_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Int_Response where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/srv/Int_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Int_Response() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Velratio_Request() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__srv__Velratio_Request__init(msg: *mut Velratio_Request) -> bool;
    fn marvin_msgs__srv__Velratio_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Velratio_Request>, size: usize) -> bool;
    fn marvin_msgs__srv__Velratio_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Velratio_Request>);
    fn marvin_msgs__srv__Velratio_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Velratio_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Velratio_Request>) -> bool;
}

// Corresponds to marvin_msgs__srv__Velratio_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__srv__Velratio_Request__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__srv__Velratio_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Velratio_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Velratio_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Velratio_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Velratio_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Velratio_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Velratio_Request where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/srv/Velratio_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Velratio_Request() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Velratio_Response() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__srv__Velratio_Response__init(msg: *mut Velratio_Response) -> bool;
    fn marvin_msgs__srv__Velratio_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Velratio_Response>, size: usize) -> bool;
    fn marvin_msgs__srv__Velratio_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Velratio_Response>);
    fn marvin_msgs__srv__Velratio_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Velratio_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Velratio_Response>) -> bool;
}

// Corresponds to marvin_msgs__srv__Velratio_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub message: rosidl_runtime_rs::String,

}



impl Default for Velratio_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__srv__Velratio_Response__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__srv__Velratio_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Velratio_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Velratio_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Velratio_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__Velratio_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Velratio_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Velratio_Response where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/srv/Velratio_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__Velratio_Response() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__MotorErrCode_Request() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__srv__MotorErrCode_Request__init(msg: *mut MotorErrCode_Request) -> bool;
    fn marvin_msgs__srv__MotorErrCode_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotorErrCode_Request>, size: usize) -> bool;
    fn marvin_msgs__srv__MotorErrCode_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotorErrCode_Request>);
    fn marvin_msgs__srv__MotorErrCode_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotorErrCode_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MotorErrCode_Request>) -> bool;
}

// Corresponds to marvin_msgs__srv__MotorErrCode_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotorErrCode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for MotorErrCode_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__srv__MotorErrCode_Request__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__srv__MotorErrCode_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotorErrCode_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__MotorErrCode_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__MotorErrCode_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__MotorErrCode_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotorErrCode_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotorErrCode_Request where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/srv/MotorErrCode_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__MotorErrCode_Request() }
  }
}


#[link(name = "marvin_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__MotorErrCode_Response() -> *const std::ffi::c_void;
}

#[link(name = "marvin_msgs__rosidl_generator_c")]
extern "C" {
    fn marvin_msgs__srv__MotorErrCode_Response__init(msg: *mut MotorErrCode_Response) -> bool;
    fn marvin_msgs__srv__MotorErrCode_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotorErrCode_Response>, size: usize) -> bool;
    fn marvin_msgs__srv__MotorErrCode_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotorErrCode_Response>);
    fn marvin_msgs__srv__MotorErrCode_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotorErrCode_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MotorErrCode_Response>) -> bool;
}

// Corresponds to marvin_msgs__srv__MotorErrCode_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotorErrCode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub error_code: rosidl_runtime_rs::Sequence<i16>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for MotorErrCode_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !marvin_msgs__srv__MotorErrCode_Response__init(&mut msg as *mut _) {
        panic!("Call to marvin_msgs__srv__MotorErrCode_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotorErrCode_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__MotorErrCode_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__MotorErrCode_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { marvin_msgs__srv__MotorErrCode_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotorErrCode_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotorErrCode_Response where Self: Sized {
  const TYPE_NAME: &'static str = "marvin_msgs/srv/MotorErrCode_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__marvin_msgs__srv__MotorErrCode_Response() }
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


