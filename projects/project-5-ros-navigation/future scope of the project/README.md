# SharedNav: Collaborative Multi-Robot Navigation in ROS 2

Autonomous exploration of unknown environments using two TurtleBot3 robots with shared environmental awareness.

## Project Overview

**SharedNav** demonstrates multi-robot cooperation through:
- Independent navigation under separate ROS 2 namespaces
- SLAM-based mapping (one per robot)
- Frontier-based exploration with centralized coordination
- Shared world model for collective perception
- Heterogeneous sensor information sharing (optional)

**Research Questions:**
- Can two robots explore more efficiently by sharing environmental information?
- Can heterogeneous sensor data improve the shared world representation?

---

## Quick Start

### Prerequisites
- **OS:** Ubuntu Linux (WSL2 on Windows supported)
- **ROS 2:** Humble
- **Simulator:** Gazebo
- **Packages:** TurtleBot3, Nav2, slam_toolbox
- **Python:** 3.10+

### Run Simulation

```bash
wsl bash -c "source /opt/ros/humble/setup.bash && \
export TURTLEBOT3_MODEL=burger && \
export AMENT_PREFIX_PATH=/mnt/d/Ubuntu_ROS2_Env/ros2_projects/sharednav/install/sharednav_bringup:/opt/ros/humble && \
source /mnt/d/Ubuntu_ROS2_Env/ros2_projects/sharednav/install/local_setup.bash && \
ros2 launch sharednav_bringup simulation.launch.py"
```

Or use the convenience script:
```bash
bash run_sim.sh
```

---

## Project Structure

```
sharednav/
├── README.md                          # This file
├── PROJECT_CONTEXT.txt                # Master specification (AI reference)
├── run_sim.sh                         # Simulation launcher script
│
├── docs/
│   ├── architecture.md                # System design & components
│   └── ros_graph.md                   # Topics, services, TF tree
│
├── src/
│   └── sharednav_bringup/
│       ├── package.xml                # ROS 2 package metadata
│       ├── CMakeLists.txt             # Build configuration
│       ├── setup.py                   # Python package setup
│       │
│       ├── launch/
│       │   ├── simulation.launch.py   # Main simulator launcher
│       │   └── robot.launch.py        # Individual robot bringup
│       │
│       ├── config/
       │   ├── multi_robot.rviz            # RViz visualization config
       │   ├── nav2_params_base.yaml       # Shared Nav2 configuration
       │   ├── robot1_nav2.yaml            # Robot 1 Nav2 overrides
       │   └── robot2_nav2.yaml            # Robot 2 Nav2 overrides
│       │
│       ├── worlds/
│       │   └── empty_world.world      # Gazebo simulation world
│       │
│       └── sharednav_bringup/         # Python package (empty, extensible)
│
└── results/                           # Experiment logs & metrics (Phase 10)
```

---

## Development Phases

| Phase | Status | Description |
|-------|--------|-------------|
| **0** | ✅ Complete | Environment verification |
| **1** | ✅ Complete | Two robots, namespaces, TF trees |
| **2** | ✅ Complete | Nav2 for independent navigation |
| **3** | ⬜ Planned | SLAM per robot |
| **4** | ⬜ Planned | Frontier detection |
| **5** | ⬜ Planned | Centralized frontier allocation |
| **6** | ⬜ Planned | Shared world model |
| **7** | ⬜ Planned | Heterogeneous sensor fusion (optional) |
| **8** | ⬜ Planned | Cross-robot semantic action (optional) |
| **9** | ⬜ Planned | Route conflict handling (optional) |
| **10** | ⬜ Planned | Metrics & experiments |

---

## Current System Architecture

### Active Nodes (Phase 1)

```
/gazebo
├── Gazebo simulator (headless)
│
/robot1
├── robot_state_publisher      [TF broadcaster]
│
/robot2
├── robot_state_publisher      [TF broadcaster]
```

### Topics (Phase 1)

**Robot-Specific:**
- `/robot1/odom` → Robot 1 odometry
- `/robot1/base_scan` → Robot 1 LiDAR (when implemented)
- `/robot1/cmd_vel` → Robot 1 velocity commands
- `/robot2/odom` → Robot 2 odometry
- `/robot2/base_scan` → Robot 2 LiDAR (when implemented)
- `/robot2/cmd_vel` → Robot 2 velocity commands

**TF Frames:**
- `map` → Global reference frame
- `robot1/odom` → Robot 1 odometry frame
- `robot1/base_link` → Robot 1 base frame
- `robot1/base_scan` → Robot 1 LiDAR frame
- `robot2/odom` → Robot 2 odometry frame
- `robot2/base_link` → Robot 2 base frame
- `robot2/base_scan` → Robot 2 LiDAR frame

(See [docs/ros_graph.md](docs/ros_graph.md) for complete topic/service list.)

---

## Key Design Principles

1. **Modular Architecture** — Each phase is independent and testable
2. **Namespace Isolation** — `/robot1` and `/robot2` operate independently
3. **Standard ROS 2 Messages** — Uses nav_msgs, geometry_msgs, sensor_msgs
4. **Centralized Coordination** — Single coordinator node for task allocation
5. **Shared World Model** — Collective perception without individual control
6. **Clean Separation** — Algorithms independent from ROS interfaces
7. **Incremental Development** — Every phase has working acceptance criteria

---

## Running Experiments

### Check Nodes
```bash
wsl bash -c "source /opt/ros/humble/setup.bash && \
export AMENT_PREFIX_PATH=/mnt/d/Ubuntu_ROS2_Env/ros2_projects/sharednav/install/sharednav_bringup:/opt/ros/humble && \
source /mnt/d/Ubuntu_ROS2_Env/ros2_projects/sharednav/install/local_setup.bash && \
ros2 node list"
```

### Check Topics
```bash
ros2 topic list
ros2 topic echo /robot1/odom
```

### Check TF Tree
```bash
ros2 run tf2_tools view_frames
```

### Visualize (when RViz2 is available)
```bash
ros2 run rviz2 rviz2 -d src/sharednav_bringup/config/multi_robot.rviz
```

---

## Building & Cleaning

### Build
```bash
wsl bash -c "source /opt/ros/humble/setup.bash && \
cd /mnt/d/Ubuntu_ROS2_Env/ros2_projects/sharednav && \
python3 -m colcon build --symlink-install"
```

### Clean
```bash
wsl bash -c "cd /mnt/d/Ubuntu_ROS2_Env/ros2_projects/sharednav && \
rm -rf build install log"
```

---

## Contributing

- Follow the [PROJECT_CONTEXT.txt](PROJECT_CONTEXT.txt) specification
- Create feature branches for each phase
- Include unit tests for algorithms
- Update README and docs after each phase
- Use meaningful commit messages

---

## Known Limitations

- Gazebo runs headless (no GUI in WSL2) — see [docs/architecture.md](docs/architecture.md)
- Known initial robot poses used for map alignment (Phase 6)
- Centralized coordination (single point of failure)
- Simple occupancy fusion (not probabilistic)
- No formal safety guarantees

---

## Next Steps

**Phase 2:** Implement Nav2 for both robots
- Create `robot1_nav2.yaml` and `robot2_nav2.yaml`
- Launch Nav2 stacks independently
- Test independent goal navigation
- Verify costmap isolation

See [PROJECT_CONTEXT.txt](PROJECT_CONTEXT.txt) for full 4-day development plan.

---

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Nav2 Documentation](https://navigation.ros.org/)
- [slam_toolbox](https://github.com/StanleyInnovation/slam_toolbox)
- [TurtleBot3 Wiki](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)

---

**Last Updated:** 2026-08-20  
**Current Phase:** 1 (Complete)  
**Next Phase:** 2 (Nav2 Implementation)
