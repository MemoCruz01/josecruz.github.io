# SharedNav System Architecture

## Overview

SharedNav implements a **centralized coordination** architecture for multi-robot exploration. Two independent robots communicate through a shared coordinator node that manages frontier allocation and maintains a collective world model.

```
                    ┌─────────────────────────┐
                    │  Shared Coordinator     │
                    ├─────────────────────────┤
                    │ • Robot state tracking  │
                    │ • Frontier allocation   │
                    │ • Goal assignment       │
                    │ • Conflict handling*    │
                    └────────────┬────────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
        ┌─────────▼────────┐ ┌──────────────┐ ┌─────────▼────────┐
        │    Robot 1       │ │ World Model  │ │    Robot 2       │
        ├──────────────────┤ ├──────────────┤ ├──────────────────┤
        │ • LiDAR          │ │ • Maps       │ │ • LiDAR          │
        │ • Odometry       │ │ • Poses      │ │ • Odometry       │
        │ • SLAM (local)   │ │ • Frontiers  │ │ • SLAM (local)   │
        │ • Nav2           │ │ • Objects*   │ │ • Nav2           │
        │ • TF tree        │ │ • Metadata   │ │ • TF tree        │
        └──────────────────┘ └──────────────┘ └──────────────────┘
                  │              │              │
                  └──────────────┴──────────────┘
                         shared topics
```

*= optional/stretch features

---

## Component Breakdown

### 1. Gazebo Simulator

**Purpose:** Physics simulation environment

**Node:** `/gazebo`  
**Role:** 
- Provides physics simulation
- Hosts spawn service for robots
- Publishes clock for `/use_sim_time`

**Key Interfaces:**
- Service: `/spawn_entity` (robot spawning)
- Topic: `/clock` (simulation time)

---

### 2. Robot 1 & Robot 2

Each robot runs independently under its namespace.

#### Robot State Publisher

**Nodes:**
- `/robot1/robot_state_publisher`
- `/robot2/robot_state_publisher`

**Role:**
- Broadcasts TF tree for each robot
- Converts URDF to TF transforms

**Parameters:**
- `robot_description` — URDF/xacro
- `frame_prefix` — Namespace prefix
- `use_sim_time` — Synchronized with simulation

**Publishes:**
- `/tf` (shared channel, but prefixed frames)
- `/tf_static` (static transforms)

#### Robot Sensors (Phase 3+)

**Odometry:**
- `/robot1/odom` → nav_msgs/Odometry
- `/robot2/odom` → nav_msgs/Odometry

**LiDAR:**
- `/robot1/scan` → sensor_msgs/LaserScan
- `/robot2/scan` → sensor_msgs/LaserScan

**Camera** (Robot 2, Phase 7 optional):
- `/robot2/camera/image_raw` → sensor_msgs/Image
- `/robot2/camera/depth/image_raw` → sensor_msgs/Image

---

### 3. Coordinate Frames & TF Trees

#### Robot 1 TF Tree

```
map
  └── robot1/odom
        └── robot1/base_link
              ├── robot1/base_scan (LiDAR)
              └── robot1/imu_link
```

#### Robot 2 TF Tree

```
map
  └── robot2/odom
        └── robot2/base_link
              ├── robot2/base_scan (LiDAR)
              ├── robot2/camera_link (Phase 7+)
              └── robot2/imu_link
```

#### Future: Global Frame Hierarchy (Phase 6+)

```
global_map
  ├── robot1/map
  │     └── robot1/odom
  │           └── robot1/base_link
  │
  └── robot2/map
        └── robot2/odom
              └── robot2/base_link
```

**Notes:**
- Each robot maintains local `map→odom→base_link` chain
- SLAM produces `map` for each robot independently
- Phase 6 aligns robot maps under global frame
- TF prefixes prevent frame name collisions

---

## Navigation Stack (Phase 2) ✅ COMPLETE

### Per-Robot Nav2 Stack

Each robot runs an independent Navigation2 stack under its namespace for autonomous motion control.

**Nodes** (for each robot):
```
/robot1/
  ├── lifecycle_manager_navigation
  │   └── [Manages component lifecycle: configure → activate → deactivate]
  │
  ├── planner_server
  │   └── [NavfnPlanner: A* path planning with 0.5m tolerance]
  │
  ├── controller_server
  │   ├── RegulatedPurePursuitController
  │   └── [Generates velocity commands toward goal]
  │
  ├── global_costmap
  │   ├── StaticLayer [from SLAM map - Phase 3]
  │   └── InflationLayer [0.25m buffer around obstacles]
  │
  └── local_costmap
      ├── VoxelLayer [from LiDAR scan]
      └── InflationLayer [local obstacle padding]

/robot2/
  └── [identical stack]
```

### Configuration Architecture

**Modular Parameter Hierarchy:**

1. **nav2_params_base.yaml** (Shared - All Robots)
   - Global costmap: StaticLayer + InflationLayer
   - Local costmap: VoxelLayer + InflationLayer (0.25m inflation)
   - Planner: NavfnPlanner with A* enabled, 0.5m goal tolerance
   - Controller: RegulatedPurePursuitController with velocity limits
   - Behavior Tree: Full recovery sequence
   - Lifecycle manager: node_names list (planner, controller, bt_navigator)
   - `use_sim_time: true` for Gazebo synchronization

2. **robot1_nav2.yaml** (Robot 1 Overrides)
   - `desired_linear_vel: 0.4` (conservative velocity)
   - Load order: base file → robot-specific → merged into nodes

3. **robot2_nav2.yaml** (Robot 2 Overrides)
   - `desired_linear_vel: 0.5` (standard velocity)
   - Load order: base file → robot-specific → merged into nodes

**Parameter Merge Strategy:**
```
NavfnPlanner + RegulatedPurePursuit loaded with:
  1. nav2_params_base.yaml (shared parameters)
  2. robot1_nav2.yaml or robot2_nav2.yaml (overrides)
  = Resulting config affects each robot independently
```

**Benefits:**
- ✅ DRY principle: shared config defined once
- ✅ Per-robot tuning: velocity, thresholds customized
- ✅ Maintainability: global changes propagate to both robots
- ✅ Experimentation: swap config files for A/B testing

### Navigation Action & Services

**BT Navigator Actions (Goal Execution):**
- `/robot1/navigate_to_pose` → nav2_msgs/NavigateToPose.action
- `/robot2/navigate_to_pose` → nav2_msgs/NavigateToPose.action

**Planner Server Services:**
- `/robot1/compute_path_to_pose` → nav2_msgs/ComputePathToPose.srv
- `/robot2/compute_path_to_pose` → nav2_msgs/ComputePathToPose.srv

**Controller Server Services:**
- `/robot1/compute_path_to_pose` → nav2_msgs/ComputePathToPose.srv
- `/robot2/compute_path_to_pose` → nav2_msgs/ComputePathToPose.srv

**Lifecycle Transitions (Orchestration):**
- `/robot1/lifecycle_manager_navigation/manage_entities` → rcl_lifecycle_msgs/ChangeState.srv
- `/robot2/lifecycle_manager_navigation/manage_entities` → rcl_lifecycle_msgs/ChangeState.srv

**Independent Costmaps:**
- Each robot maintains separate local/global costmaps
- No interference between costmap updates
- Separate planner instances per robot

---

## SLAM (Phase 3+)

### Per-Robot SLAM with slam_toolbox

**Nodes:**
```
/robot1/
  └── slam_toolbox (async_slam_toolbox_node)

/robot2/
  └── slam_toolbox (async_slam_toolbox_node)
```

**Subscriptions:**
- `/robot1/scan` → laser scan input
- `/robot1/tf` → odometry transforms

**Publishes:**
- `/robot1/map` → nav_msgs/OccupancyGrid
- `/robot1/map_metadata` → nav_msgs/MapMetaData
- `/robot1/tf` → map→odom transform

**Parameters (YAML):**
```yaml
slam_toolbox:
  use_sim_time: true
  base_frame: robot1/base_link
  odom_frame: robot1/odom
  map_frame: robot1/map
  scan_topic: /robot1/scan
```

---

## Frontier Detection (Phase 4+)

### Algorithm (Pure Python, then ROS wrapper)

**Input:** OccupancyGrid from SLAM  
**Output:** List of frontier centroids

**Process:**
1. Scan grid for free cells adjacent to unknown cells
2. Cluster connected frontier cells
3. Filter small clusters (< min_size)
4. Calculate centroid & information gain
5. Publish as visualization markers

**ROS Node:** `frontier_detector_node.py` (Phase 4)

**Publishes:**
- `/robot1/frontiers` → custom message or visualization_msgs/MarkerArray
- `/robot2/frontiers` → visualization_msgs/MarkerArray

---

## Coordinator (Phase 5+)

### Centralized Goal Allocation

**Node:** `/sharednav_coordinator`

**Subscriptions:**
- `/robot1/pose` (or TF)
- `/robot2/pose` (or TF)
- `/robot1/frontiers`
- `/robot2/frontiers`
- `/robot1/nav2/feedback` (navigation status)
- `/robot2/nav2/feedback` (navigation status)

**Actions (Clients):**
- `/robot1/navigate_to_pose` (send goals)
- `/robot2/navigate_to_pose` (send goals)

**Publishes:**
- `/shared/assigned_goals` (for visualization)
- `/shared/robot_states` (aggregated status)

**Algorithm:**
```
For each unassigned frontier:
  cost_robot1 = distance(robot1, frontier) + conflict_penalty
  cost_robot2 = distance(robot2, frontier) + conflict_penalty
  
  if cost_robot1 < cost_robot2:
    assign frontier to robot1
  else:
    assign frontier to robot2
```

---

## Shared World Model (Phase 6+)

### World Model Node

**Node:** `/sharednav_world_model`

**Subscriptions:**
- `/robot1/map` → local occupancy grid
- `/robot2/map` → local occupancy grid
- `/robot1/pose` → robot pose
- `/robot2/pose` → robot pose

**Publishes:**
- `/shared/global_map` → merged OccupancyGrid
- `/shared/robot_states` → aggregated state
- `/shared/objects` (Phase 7+) → semantic detections

**Map Fusion Strategy (Phase 6):**

```python
global_map = empty OccupancyGrid(frame='global_map')

for each robot:
    transform robot_local_map to global_map frame
    for each cell in global_map:
        if robot.map[cell] == OCCUPIED:
            global_map[cell] = OCCUPIED
        elif robot.map[cell] == FREE:
            if global_map[cell] != OCCUPIED:
                global_map[cell] = FREE
        # else: leave as UNKNOWN
```

---

## Semantic Perception (Phase 7+ - Optional)

### Semantic Detector Node

**Node:** `/robot2/semantic_detector`

**Subscriptions:**
- `/robot2/camera/image_raw`
- `/robot2/camera/depth/image_raw` (if available)

**Publishes:**
- `/robot2/detections` → custom Detection message
- `/shared/objects` → shared semantic observations

**Detection Pipeline:**
```
Image → Neural Net → [class, bbox, confidence]
       → Depth Projection → 3D Position
       → TF Transform → Global Frame
       → Publish to shared world model
```

---

## Parameters & Configuration

### Global Parameters

**File:** `config/sharednav.yaml`

```yaml
sharednav:
  use_sim_time: true
  coordination_rate: 10.0  # Hz
  frontier_min_size: 5  # cells
  frontier_max_age: 30.0  # seconds
  goal_commitment_time: 5.0  # seconds
  conflict_distance_threshold: 1.5  # meters
```

### Robot-Specific Parameters

**Files:** 
- `config/robot1_nav2.yaml`
- `config/robot2_nav2.yaml`

```yaml
robot1:
  base_frame: robot1/base_link
  odom_frame: robot1/odom
  map_frame: robot1/map
  scan_topic: /robot1/scan
  
  nav2:
    planner_type: GridBased
    controller_type: DWB
    local_costmap:
      width: 3.0
      height: 3.0
      resolution: 0.05
```

---

## Namespace & Remapping Strategy

### Why Namespaces?

1. **Isolation** — `/cmd_vel` sent to robot1 doesn't affect robot2
2. **Scalability** — Adding more robots is straightforward
3. **Clarity** — Topic names indicate source robot

### Remapping Strategy

```python
# TF must be shared globally (not namespaced)
remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')]

# Sensor data stays in namespace
# /robot1/scan  (not /robot1/base_scan -> /scan)
# /robot2/scan

# Commands in namespace
# /robot1/cmd_vel  (from controller)
# /robot2/cmd_vel
```

---

## Execution Flow (Simulation)

```
1. Launch: ros2 launch sharednav_bringup simulation.launch.py
   ├─ Start Gazebo (gzserver + libgazebo_ros_factory.so)
   ├─ Spawn Robot 1
   │  └─ Launch robot_state_publisher for robot1
   └─ Spawn Robot 2
      └─ Launch robot_state_publisher for robot2

2. Gazebo Physics Loop (1000 Hz)
   ├─ Update robot pose in physics engine
   ├─ Publish /clock
   └─ Broadcast odometry

3. Robot State Publisher (50 Hz, default)
   ├─ Read URDF
   ├─ Publish /tf with current joint state

4. (Phase 2+) Nav2 Lifecycle
   ├─ Activate costmap servers
   ├─ Activate planner server
   ├─ Listen for /navigate_to_pose actions

5. (Phase 3+) SLAM Loop
   ├─ Subscribe to /scan
   ├─ Update pose graph
   ├─ Publish updated map
   └─ Broadcast map→odom transform
```

---

## Known Limitations

### Current (Phase 1-2)

- ✅ Gazebo headless (WSL friendly)
- ✅ Each robot builds independent map
- ✅ Nav2 handles obstacle avoidance

### Phase 3-5

- ⚠️ Simple distance-based goal allocation
- ⚠️ No dynamic goal replanning
- ⚠️ No multi-robot path coordination

### Phase 6+

- ⚠️ Map fusion is conservative (doesn't handle contradictions)
- ⚠️ Centralized coordinator (single point of failure)
- ⚠️ No communication latency modeling
- ⚠️ Robots assume known initial poses

### Future Work

- Decentralized multi-robot SLAM
- Bayesian occupancy fusion
- Communication-aware planning
- Learning-based goal allocation
- Real hardware deployment

---

## Debugging Checklist

### Robot Not Moving?
- [ ] Check `/cmd_vel` topic
- [ ] Check Nav2 lifecycle state (should be "active")
- [ ] Check local costmap for inflation
- [ ] Verify TF tree is complete
- [ ] Check odometry publishing

### Map Not Appearing?
- [ ] Check `/robot1/scan` and `/robot2/scan` present
- [ ] Check TF scan→base_link exists
- [ ] Check slam_toolbox is running
- [ ] Check map→odom TF publishing

### Both Robots Interfering?
- [ ] Check namespaces in launch file
- [ ] Verify remappings for TF
- [ ] Check parameter file robot names
- [ ] Inspect `/robot1/` vs `/robot2/` topics

### Coordinator Not Assigning Goals?
- [ ] Check coordinator node running
- [ ] Verify frontiers being detected
- [ ] Check robot pose updates
- [ ] Inspect coordinator logs for errors

---

## References

- [ROS 2 Nodes & Executors](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Executors.html)
- [TF2 Frames](https://docs.ros.org/en/humble/Concepts/Intermediate/Tf2/Tf2-Main.html)
- [Nav2 Documentation](https://navigation.ros.org/)
- [slam_toolbox GitHub](https://github.com/StanleyInnovation/slam_toolbox)

---

**Last Updated:** 2026-08-20  
**Phase:** 1 Complete, Phase 2 in preparation
