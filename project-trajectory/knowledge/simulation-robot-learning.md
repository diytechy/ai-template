---
domains: [hardware]
researched: 2026-07-09
source: ClaudeGuardChecks/skill-knowledge-library
---
# Simulation & robot learning

Curated research pack imported from the staged skill/knowledge library. Verify version-sensitive examples against the linked current documentation before shipping.

### Core references
- **[MuJoCo](https://mujoco.readthedocs.io/)** — best physics fidelity for contact-rich manipulation;
  **[MJX](https://mujoco.readthedocs.io/en/stable/mjx.html)** gives JAX-accelerated parallel sim. The
  backbone of most academic sim-to-real and VLA evaluation.
- **[Isaac Lab](https://isaac-sim.github.io/IsaacLab/)** on **[Isaac Sim](https://developer.nvidia.com/isaac/sim)** — massively parallel GPU RL (thousands of envs; ~150K steps/s on an RTX 4090) for locomotion/whole-body.
- **[Gazebo Sim](https://gazebosim.org/)** — the ROS-native simulator; best for navigation/SLAM/multi-robot with tight ROS 2 integration.
- **[Genesis](https://github.com/Genesis-Embodied-AI/Genesis)** — fast multi-physics newcomer (rigid/soft/fluid). **[PyBullet](https://pybullet.org/)** — lightweight, great for quick prototyping. **[Drake](https://drake.mit.edu/)** — high-fidelity model-based.
- **Robot learning:** **[LeRobot (Hugging Face)](https://github.com/huggingface/lerobot)** — the 2026
  default for imitation + RL: record demos → `LeRobotDataset` → train (ACT, SmolVLA, diffusion) →
  deploy, with low-cost arm support (SO-100/101, Koch, ALOHA). Foundation policies:
  **[OpenVLA](https://openvla.github.io/)**, **[π0 / openpi](https://github.com/Physical-Intelligence/openpi)**,
  **[Open X-Embodiment](https://robotics-transformer-x.github.io/)** (cross-robot dataset).

### Actionable techniques
1. **Match the sim to the job:** contact-rich manipulation & sim-to-real → MuJoCo/MJX; large-scale RL
   locomotion → Isaac Lab; ROS navigation/SLAM in a world → Gazebo. Many teams run **dual-sim
   validation** in 2026 — train in Isaac Lab for throughput, then re-score checkpoints in MuJoCo MJX
   with system-identified parameters before touching hardware.
2. **Close the sim-to-real gap two ways:** (a) **domain randomization** — randomize mass, friction,
   latency, lighting, textures so the policy can't overfit one exact world; (b) **system
   identification** — calibrate joint friction, rotor inertia, actuator delay against real logs so the
   nominal sim is *right*. Randomize what you can't identify; identify what you can.
3. **Bootstrap manipulation with imitation, not RL from scratch.** Teleoperate ~50 demos, record to a
   `LeRobotDataset`, train an ACT/diffusion policy, evaluate in sim, then on hardware. Far cheaper than
   reward-engineering an RL policy for a bringup task.

```xml
<!-- MuJoCo MJCF: a one-joint arm segment with a position actuator. -->
<mujoco model="gilbert_arm">
  <worldbody>
    <body name="link1" pos="0 0 0.1">
      <joint name="j1" type="hinge" axis="0 0 1" range="-3.14 3.14"/>
      <geom type="capsule" fromto="0 0 0  0 0 0.3" size="0.03" mass="0.5"/>
    </body>
  </worldbody>
  <actuator><position joint="j1" kp="50" ctrlrange="-3.14 3.14"/></actuator>
</mujoco>
```

```bash
# LeRobot: record teleop demos, then train an imitation policy on them.
python -m lerobot.record  --robot.type=so101_follower --dataset.repo_id=me/gilbert_pick --dataset.num_episodes=50
python -m lerobot.scripts.train --policy.type=act --dataset.repo_id=me/gilbert_pick
```

### Gotchas
- Physics engines disagree on contact — a policy that works in one sim may fail in another; validate
  across engines before hardware (the dual-sim pattern exists for this reason).
- Domain randomization too wide hurts as much as too narrow (unlearnable task); tune the ranges.
- Keep the **same URDF/description** driving sim and real (B2); divergence there is a top sim-to-real bug.

---
