import pyrealsense2 as rs
ctx = rs.context()
devices = ctx.query_devices()
print(f"发现 {len(devices)} 台设备")
for d in devices:
    print(d.get_info(rs.camera_info.name))