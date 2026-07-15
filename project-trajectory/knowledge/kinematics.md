---
domains: [hardware]
researched: 2026-07-09
source: ClaudeGuardChecks/skill-knowledge-library
---
# Kinematics

Curated research pack imported from the staged skill/knowledge library. Verify version-sensitive examples against the linked current documentation before shipping.

### Core references
- **[Modern Robotics (Lynch & Park)](http://modernrobotics.org)** — *the* modern textbook; free
  preprint + **[video lectures](https://modernrobotics.northwestern.edu/nu-gm-book-resource/)** +
  **[code library `NxRLab/ModernRobotics`](https://github.com/NxRLab/ModernRobotics)** (Python/MATLAB).
  Learn the **screw-theory / Product-of-Exponentials** formulation — twists, wrenches, and the space/body Jacobian. This is the vocabulary gilbert's kinematics should be written in.
- **[Pinocchio](https://stack-of-tasks.github.io/pinocchio/)** — fast rigid-body dynamics + kinematics
  (FK, Jacobians, RNEA) in C++/Python; the backbone of modern optimization-based control.
- **IK solvers:** **[Pink](https://github.com/stephane-caron/pink)** (differential IK on Pinocchio),
  **[Mink](https://github.com/kevinzakka/mink)** (differential IK on MuJoCo), **[PyRoki](https://github.com/chungmin99/pyroki)** (modular kinematic optimization toolkit, 2025).
- **[MoveIt 2](https://moveit.picknik.ai/)** — planning framework; see the
  **[URDF & SRDF tutorial](https://moveit.picknik.ai/main/doc/examples/urdf_srdf/urdf_srdf_tutorial.html)** and the Setup Assistant. **[ros2_control](https://control.ros.org/)** bridges URDF joints to hardware.
- **[Drake](https://drake.mit.edu/)** — model-based design, optimization-based IK and planning with
  rigorous multibody dynamics; strong when you need constraints/guarantees.

### Actionable techniques
1. **Describe the robot once, in URDF, with a `ros2_control` block.** Everything (TF, MoveIt, sim,
   controllers) reads from that description. Keep link frames and joint axes honest — sim-to-real
   errors trace back here more than anywhere else.
2. **Compute FK with Product-of-Exponentials**, not hand-chained DH tables — one home configuration
   `M` plus a screw axis per joint. It's less error-prone and matches the textbook.
3. **Prefer differential (Jacobian) IK for smooth servoing / teleop** (Pink/Mink): solve for joint
   velocities that realize a desired end-effector twist, subject to limits, as a small QP each tick.
   Use analytic/global IK (MoveIt/IKFast) when you need *a* pose reached from scratch.

```xml
<!-- URDF: bind joints to hardware so one description drives sim and real. -->
<ros2_control name="GilbertArm" type="system">
  <hardware><plugin>gilbert_hardware/GilbertSystem</plugin></hardware>
  <joint name="shoulder_pan">
    <command_interface name="position"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
```

```python
# Forward kinematics via Product-of-Exponentials (Modern Robotics library).
import modern_robotics as mr
T_ee = mr.FKinSpace(M, Slist, thetalist)   # M: home SE(3); Slist: 6xn screw axes; thetalist: joints

# Differential IK for a desired end-effector pose (Pink, on Pinocchio).
from pink import solve_ik, Configuration
from pink.tasks import FrameTask
task = FrameTask("ee_link", position_cost=1.0, orientation_cost=1.0); task.set_target(T_desired)
cfg = Configuration(model, data, q)
q = pin.integrate(model, q, solve_ik([task], cfg, dt, solver="quadprog") * dt)
```

### Gotchas
- Watch joint-limit and singularity handling in differential IK — near a singularity the Jacobian
  inverse blows up; use damped least squares (Levenberg–Marquardt) and cap velocities.
- URDF has no closed-loop kinematics (only trees); parallel linkages need `<mimic>` joints or Drake/MuJoCo.
