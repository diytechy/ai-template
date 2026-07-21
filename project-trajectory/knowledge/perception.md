---
domains: [hardware]
researched: 2026-07-09
source: curated from a private research library
---
# Perception

Curated research pack imported from the staged skill/knowledge library. Verify version-sensitive examples against the linked current documentation before shipping.

### Core references
- **[ROS 2 documentation](https://docs.ros.org/en/jazzy/)** — the platform. Anchor everything on TF2
  frames, `sensor_msgs`, and the node/topic model.
- **Point clouds:** **[PCL](https://pointclouds.org/)** + **[perception_pcl (ROS 2 interface)](https://github.com/ros-perception/perception_pcl)**, and **[Open3D](https://www.open3d.org/docs/release/)** for fast Python registration/segmentation/visualization.
- **SLAM & localization:** **[Nav2](https://docs.nav2.org/)** (navigation stack),
  **[slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)** (2D lifelong SLAM),
  **[robot_localization](https://github.com/cra-ros-pkg/robot_localization)** (EKF/UKF sensor fusion —
  the standard for IMU + wheel odom + GPS). EKF is the best default for 50–200 Hz odometry fusion.
- **Foundation-model perception (open-vocabulary):** **[SAM 2](https://github.com/facebookresearch/sam2)**
  (promptable segmentation + video tracking), **[Grounding DINO](https://github.com/IDEA-Research/GroundingDINO)**
  (text→boxes zero-shot detection), **[Grounded-SAM-2](https://github.com/IDEA-Research/Grounded-SAM-2)**
  (the detect→segment→track pipeline — enables "pick up the blue mug" without a trained detector).
- **Curated indexes:** **[awesome-ros2](https://github.com/fkromer/awesome-ros2)**, **[awesome-robotics-libraries](https://github.com/jslee02/awesome-robotics-libraries)**, **[ros-perception org](https://github.com/ros-perception)**.

### Actionable techniques
1. **Fuse pose with an EKF, don't trust one sensor.** Feed wheel odom + IMU (+ GPS/visual odom) into
   `robot_localization`; configure per-sensor which state dimensions to trust. Odom for local
   smoothness, IMU for orientation/yaw-rate, GPS for global drift correction.
2. **Open-vocabulary perception pipeline** for "find/grasp the X": text prompt → Grounding DINO boxes
   → SAM 2 masks → lift mask to 3D via the depth image + camera intrinsics → cluster to a grasp target.
   No per-object training; swap the noun in the prompt.
3. **Register point clouds with ICP** (align a new scan to a map / a model to an observation): coarse
   align (feature/global) then refine point-to-plane ICP. Point-to-plane converges faster than
   point-to-point on structured scenes.

```yaml
# robot_localization EKF (ekf.yaml): fuse wheel odometry + IMU into a smooth odom→base_link.
ekf_filter_node:
  ros__parameters:
    frequency: 30.0
    two_d_mode: false
    odom_frame: odom
    base_link_frame: base_link
    world_frame: odom
    odom0: /wheel/odometry
    odom0_config: [true, true, false,  false, false, true,   # x,y | yaw
                   true, false, false, false, false, true,   # vx  | vyaw
                   false, false, false]
    imu0: /imu/data
    imu0_config: [false, false, false, true, true, true,     # roll,pitch,yaw
                  false, false, false, true, true, true,     # angular vel
                  true, true, true]                          # linear accel
```

```python
# Open-vocabulary detect -> segment (Grounded-SAM-2 pattern), then lift to 3D.
boxes, labels = grounding_dino.predict(image, caption="blue mug . gripper .", box_threshold=0.35)
masks = sam2.predict(image, boxes=boxes)                     # promptable segmentation
pts3d = deproject(depth_image, masks[0], camera_intrinsics)  # mask + depth -> object point cloud
```

### Gotchas
- Perception lives or dies on **TF frames and time sync**; a wrong `base_link`→sensor transform makes
  everything downstream (SLAM, planning) silently wrong. Verify the TF tree first.
- Foundation-model inference (SAM 2 / DINO) is heavy — run it on a workstation/GPU node, not the
  robot's compute-constrained onboard, or use distilled variants.
