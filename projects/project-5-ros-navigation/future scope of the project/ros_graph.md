# SharedNav ROS 2 Computational Graph

Complete list of nodes, topics, services, actions, and TF frames as of **Phase 2** ✅ COMPLETE.

---

## Node Graph (Phase 1 + Phase 2)

```
NODES:
├── /gazebo
│   └── [Gazebo simulator - physics & spawning]
│
├── /robot1
│   ├── robot_state_publisher
│   │   └── [TF broadcaster for robot1]
│   │
│   └── nav2 stack (Phase 2) ✅
│       ├── lifecycle_manager_navigation
│       │   └── [Orchestrates planner → controller → bt_navigator startup]
│       ├── planner_server
│       │   ├── global_costmap [StaticLayer (Phase 3+) + InflationLayer]
│       │   └── [NavfnPlanner: A* path planning]
│       ├── controller_server
│       │   ├── local_costmap [VoxelLayer + InflationLayer]
│       │   └── [RegulatedPurePursuitController: velocity generation]
│       └── bt_navigator
│           └── [Behavior Tree: goal orchestration + recovery]
│
└── /robot2
    ├── robot_state_publisher
    │   └── [TF broadcaster for robot2]
    │
    └── nav2 stack (Phase 2) ✅
        ├── lifecycle_manager_navigation
        ├── planner_server
        │   └── global_costmap
        ├── controller_server
        │   └── local_costmap
        └── bt_navigator


TOPICS (Phase 1 + 2):
├── /clock                          [rosgraph_msgs/Clock]
│   Publisher: /gazebo | Subscribers: all nodes (use_sim_time=true)
│
├── /robot1/odom                    [nav_msgs/Odometry]
│   Publisher: Gazebo physics plugin
├── /robot2/odom                    [nav_msgs/Odometry]
│   Publisher: Gazebo physics plugin
│
├── /robot1/cmd_vel                 [geometry_msgs/Twist] (Phase 2)
│   Publisher: /robot1/controller_server | Subscriber: Gazebo (base controller)
├── /robot2/cmd_vel                 [geometry_msgs/Twist] (Phase 2)
│   Publisher: /robot2/controller_server | Subscriber: Gazebo (base controller)
│
├── /robot1/scan                    [sensor_msgs/LaserScan]
│   Publisher: Gazebo LiDAR plugin | Subscribers: /robot1/local_costmap
├── /robot2/scan                    [sensor_msgs/LaserScan]
│   Publisher: Gazebo LiDAR plugin | Subscribers: /robot2/local_costmap
│
└── /tf, /tf_static                 [tf2_msgs/TFMessage]
    Publishers: /robot1/robot_state_publisher, /robot2/robot_state_publisher
    (+ /robot1/planner_server, /robot1/controller_server publishing static costmap TFs - Phase 2)


SERVICES (Phase 1 + 2):
├── /spawn_entity                   [gazebo_msgs/SpawnEntity] (Phase 1)
│   Server: /gazebo
│
├── /robot1/lifecycle_manager_navigation/manage_entities    [rcl_lifecycle_msgs/ChangeState] (Phase 2)
│   Server: /robot1/lifecycle_manager_navigation
├── /robot2/lifecycle_manager_navigation/manage_entities    [rcl_lifecycle_msgs/ChangeState] (Phase 2)
│   Server: /robot2/lifecycle_manager_navigation
│
├── /robot1/planner_server/compute_path_to_pose            [nav2_msgs/ComputePathToPose] (Phase 2)
│   Server: /robot1/planner_server
├── /robot2/planner_server/compute_path_to_pose            [nav2_msgs/ComputePathToPose] (Phase 2)
│   Server: /robot2/planner_server
│
└── /robot1/controller_server/compute_path_to_pose          [nav2_msgs/ComputePathToPose] (Phase 2)
    Server: /robot1/controller_server (same as planner due to BT design)


ACTIONS (Phase 2):
├── /robot1/navigate_to_pose                [nav2_msgs/NavigateToPose.action]
│   Server: /robot1/bt_navigator
└── /robot2/navigate_to_pose                [nav2_msgs/NavigateToPose.action]
    Server: /robot2/bt_navigator
```

---

## Phase 2: Navigation Stack (✅ COMPLETE)

### Nav2 Command & Control Topics

#### Velocity Commands (Phase 2)

| Topic | Type | Publisher | Subscriber | Frequency | Description |
|-------|------|-----------|------------|-----------|-------------|
| `/robot1/cmd_vel` | `geometry_msgs/Twist` | controller_server | Gazebo base_controller | 50 Hz | Velocity target for Robot 1 |
| `/robot2/cmd_vel` | `geometry_msgs/Twist` | controller_server | Gazebo base_controller | 50 Hz | Velocity target for Robot 2 |

**Message Structure:**
```yaml
linear:
  x: 0.5      # m/s forward (max 0.4 for robot1, 0.5 for robot2)
  y: 0.0      # m/s lateral (always 0 for differential drive)
  z: 0.0      # m/s vertical (always 0)

angular:
  x: 0.0      # rad/s roll (always 0)
  y: 0.0      # rad/s pitch (always 0)
  z: 0.2      # rad/s yaw (rotation rate)
```

### Nav2 Services (Phase 2)

#### Lifecycle Management

| Service | Type | Server | Purpose |
|---------|------|--------|---------|
| `/robot1/lifecycle_manager_navigation/manage_entities` | `rcl_lifecycle_msgs/ChangeState` | lifecycle_manager | Configure/Activate/Deactivate nodes |
| `/robot2/lifecycle_manager_navigation/manage_entities` | `rcl_lifecycle_msgs/ChangeState` | lifecycle_manager | Configure/Activate/Deactivate nodes |

**State Machine:**
```
Unconfigured ──configure──> Inactive ──activate──> Active
                                ▲                      │
                                └────deactivate────────┘
```

#### Path Planning

| Service | Type | Server | Purpose |
|---------|------|--------|---------|
| `/robot1/planner_server/compute_path_to_pose` | `nav2_msgs/ComputePathToPose` | planner_server | Get collision-free path |
| `/robot2/planner_server/compute_path_to_pose` | `nav2_msgs/ComputePathToPose` | planner_server | Get collision-free path |

**Request Structure:**
```yaml
start:
  header:
    frame_id: "robot1/map"
  pose:
    position: {x: 0.0, y: 0.0}
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}

goal:
  header:
    frame_id: "robot1/map"
  pose:
    position: {x: 3.0, y: 4.0}
    orientation: {x: 0.0, y: 0.0, z: 0.707, w: 0.707}

planner_id: "GridBased"
```

**Response Structure:**
```yaml
path:
  header:
    frame_id: "robot1/map"
  poses:
    - pose: {position: {x: 0.0, y: 0.0}, orientation: ...}
    - pose: {position: {x: 1.0, y: 0.5}, orientation: ...}
    - pose: {position: {x: 3.0, y: 4.0}, orientation: ...}
```

### Nav2 Actions (Phase 2)

#### Navigate To Pose Action

| Action | Type | Server | Purpose |
|--------|------|--------|---------|
| `/robot1/navigate_to_pose` | `nav2_msgs/NavigateToPose` | bt_navigator | Execute full navigation goal |
| `/robot2/navigate_to_pose` | `nav2_msgs/NavigateToPose` | bt_navigator | Execute full navigation goal |

**Goal Structure:**
```yaml
pose:
  header:
    frame_id: "robot1/map"
  pose:
    position: {x: 2.0, y: 3.0, z: 0.0}
    orientation: {x: 0.0, y: 0.0, z: 0.707, w: 0.707}

behavior_tree_id: ""  # Empty = use default BT
```

**Feedback Structure:**
```yaml
current_pose:
  header:
    frame_id: "robot1/map"
  pose:
    position: {x: 0.1, y: 0.2, z: 0.0}
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}

navigation_time: 0.5  # seconds elapsed
estimated_time_remaining: 4.5  # seconds
number_of_recoveries: 0
```

**Result Structure:**
```yaml
result: "NavigateToPose.Result.UNKNOWN"  # or SUCCEEDED, CANCELED
```

---

### Simulation Time

| Topic | Type | Direction | Frequency | Description |
|-------|------|-----------|-----------|-------------|
| `/clock` | `rosgraph_msgs/Clock` | Pub (gazebo) | 100 Hz | Simulated time for `use_sim_time` |

---

### Odometry (Phase 1 - Minimal)

| Topic | Type | Direction | Frequency | Frame ID | Description |
|-------|------|-----------|-----------|----------|-------------|
| `/robot1/odom` | `nav_msgs/Odometry` | Pub (gazebo) | 50 Hz | `robot1/odom` | Robot 1 odometry |
| `/robot2/odom` | `nav_msgs/Odometry` | Pub (gazebo) | 50 Hz | `robot2/odom` | Robot 2 odometry |

**Message Structure (nav_msgs/Odometry):**
```
header
  seq: sequence number
  stamp: timestamp
  frame_id: "robot1/odom"  or  "robot2/odom"

child_frame_id: "robot1/base_link"  or  "robot2/base_link"

pose
  pose
    position: {x, y, z}
    orientation: {x, y, z, w}
  covariance: [36]

twist
  twist
    linear: {x, y, z}
    angular: {x, y, z}
  covariance: [36]
```

---

### Transforms (TF)

| Frame | Parent | Source Node | Type | Rate |
|-------|--------|-------------|------|------|
| `robot1/base_link` | `robot1/odom` | robot_state_publisher | Transform | 50 Hz |
| `robot1/base_scan` | `robot1/base_link` | robot_state_publisher | Transform (static from URDF) | - |
| `robot1/imu_link` | `robot1/base_link` | robot_state_publisher | Transform (static from URDF) | - |
| `robot2/base_link` | `robot2/odom` | robot_state_publisher | Transform | 50 Hz |
| `robot2/base_scan` | `robot2/base_link` | robot_state_publisher | Transform (static from URDF) | - |
| `robot2/imu_link` | `robot2/base_link` | robot_state_publisher | Transform (static from URDF) | - |

**TF Tree Visualization:**

```
robot1/odom
  └── robot1/base_link
        ├── robot1/base_scan
        ├── robot1/base_footprint
        └── robot1/imu_link

robot2/odom
  └── robot2/base_link
        ├── robot2/base_scan
        ├── robot2/base_footprint
        └── robot2/imu_link
```

---

## Phase 2+ Topics (Preview)

### Sensor Data (Phase 2+)

| Topic | Type | Publisher | Frequency | Frame ID |
|-------|------|-----------|-----------|----------|
| `/robot1/scan` | `sensor_msgs/LaserScan` | Gazebo plugin | 50 Hz | `robot1/base_scan` |
| `/robot2/scan` | `sensor_msgs/LaserScan` | Gazebo plugin | 50 Hz | `robot2/base_scan` |

### Navigation Commands (Phase 2+)

| Topic | Type | Subscriber | Latched |
|-------|------|-----------|---------|
| `/robot1/cmd_vel` | `geometry_msgs/Twist` | Controller | No |
| `/robot2/cmd_vel` | `geometry_msgs/Twist` | Controller | No |

**Example Message:**
```yaml
linear:
  x: 0.5      # m/s forward
  y: 0.0      # m/s lateral (usually 0 for diff drive)
  z: 0.0      # m/s vertical (always 0)

angular:
  x: 0.0      # rad/s roll
  y: 0.0      # rad/s pitch
  z: 0.1      # rad/s yaw
```

### Navigation Feedback (Phase 2+)

| Topic | Type | Publisher | Description |
|-------|------|-----------|-------------|
| `/robot1/nav2/amcl_pose` | `geometry_msgs/PoseWithCovarianceStamped` | Localization | Robot pose estimate |
| `/robot1/tf` | `tf2_msgs/TFMessage` | SLAM + state publisher | TF transforms |

---

## Services (Detailed)

### Gazebo Services (Phase 1)

#### /spawn_entity

**Service Type:** `gazebo_msgs/SpawnEntity`

**Request:**
```yaml
name: "robot1"
xml: """<robot><link>...</link></robot>"""
initial_pose:
  position: {x: 0.0, y: 0.0, z: 0.0}
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
robot_namespace: "robot1"
```

**Response:**
```yaml
success: true
status_message: "Entity [robot1] successfully spawned."
```

---

## Actions (Phase 2+)

### Navigation To Pose

**Action:** `/robot1/navigate_to_pose`  
**Type:** `nav2_msgs/NavigateToPose`

**Goal:**
```yaml
pose:
  header:
    frame_id: "robot1/map"
  pose:
    position: {x: 2.0, y: 3.0, z: 0.0}
    orientation: {x: 0.0, y: 0.0, z: 0.707, w: 0.707}
behavior_tree_id: ""
```

**Feedback:**
```yaml
current_pose:
  pose:
    position: {x: 0.5, y: 0.3, z: 0.0}
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
navigation_time:
  sec: 5
  nsec: 234000000
estimated_time_remaining:
  sec: 10
  nsec: 0
number_of_recoveries: 0
recovery_status: "Not recovering"
```

**Result:**
```yaml
result: SUCCEEDED  # or FAILED, CANCELED, UNKNOWN
```

---

## Nav2 Stack Topics (Phase 2+)

### Costmap Layers

| Topic | Type | Publisher | Purpose |
|-------|------|-----------|---------|
| `/robot1/local_costmap/costmap` | `nav_msgs/OccupancyGrid` | local_costmap | Local navigation costmap |
| `/robot1/global_costmap/costmap` | `nav_msgs/OccupancyGrid` | global_costmap | Global navigation costmap |
| `/robot1/local_costmap/costmap_updates` | `map_msgs/OccupancyGridUpdate` | local_costmap | Incremental updates |
| `/robot1/global_costmap/costmap_updates` | `map_msgs/OccupancyGridUpdate` | global_costmap | Incremental updates |

### Planner & Controller Topics

| Topic | Type | Publisher | Subscriber |
|-------|------|-----------|-----------|
| `/robot1/plan` | `nav_msgs/Path` | planner_server | (visualization) |
| `/robot1/local_plan` | `nav_msgs/Path` | controller_server | (visualization) |

---

## SLAM Topics (Phase 3+)

| Topic | Type | Publisher | Frequency | Frame |
|-------|------|-----------|-----------|-------|
| `/robot1/map` | `nav_msgs/OccupancyGrid` | slam_toolbox | 1-10 Hz | `robot1/map` |
| `/robot1/map_metadata` | `nav_msgs/MapMetaData` | slam_toolbox | 1-10 Hz | - |

**Map Metadata:**
```yaml
map_load_time:
  sec: 1234567890
  nsec: 123456789
resolution: 0.05        # meters/cell
width: 2048             # cells
height: 2048            # cells
origin:
  position: {x: -51.2, y: -51.2, z: 0.0}
  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
```

---

## Frontier Topics (Phase 4+)

| Topic | Type | Publisher | Format |
|-------|------|-----------|--------|
| `/robot1/frontiers` | `visualization_msgs/MarkerArray` | frontier_detector | RViz markers |
| `/shared/frontiers` | Custom or MarkerArray | coordinator | Aggregated frontiers |

---

## Coordination Topics (Phase 5+)

| Topic | Type | Publisher | Subscribers |
|-------|------|-----------|-------------|
| `/shared/assigned_goals` | Custom Goal message | coordinator | (visualization) |
| `/shared/robot_states` | Custom RobotState[] | coordinator | (visualization, metrics) |

**Example Robot State:**
```yaml
robot_id: "robot1"
pose: {x: 1.5, y: 2.3, theta: 0.785}
status: "EXPLORING"
current_goal: {x: 3.0, y: 4.0}
battery: 85.5
```

---

## World Model Topics (Phase 6+)

| Topic | Type | Publisher | Description |
|-------|------|-----------|-------------|
| `/shared/global_map` | `nav_msgs/OccupancyGrid` | world_model | Merged map from all robots |
| `/shared/objects` | Custom or Detection[] | world_model | Detected objects (Phase 7+) |

---

## Parameter Server (config/sharednav.yaml)

```yaml
use_sim_time: true
coordination_rate: 10.0
frontier:
  min_size: 5
  max_age: 30.0
goal:
  commitment_time: 5.0
collision:
  distance_threshold: 1.5
```

---

## ros2 Commands Reference

### List Everything

```bash
ros2 node list
ros2 topic list
ros2 service list
ros2 action list
ros2 param list
```

### Inspect a Topic

```bash
ros2 topic info /robot1/odom
ros2 topic echo /robot1/odom
ros2 interface show nav_msgs/msg/Odometry
```

### View TF Tree

```bash
ros2 run tf2_tools view_frames
evince frames.pdf
```

### Monitor Node

```bash
ros2 node info /gazebo
ros2 node info /robot1/robot_state_publisher
```

### List Subscriptions/Publications

```bash
ros2 node info /robot1/robot_state_publisher
```

---

## QoS Settings (Recommended)

| Category | Topic | Reliability | Durability | History |
|----------|-------|-------------|-----------|---------|
| **Sensor Data** | `/robot1/scan` | Best Effort | Volatile | Keep Last (1) |
| **Odometry** | `/robot1/odom` | Best Effort | Volatile | Keep Last (1) |
| **Commands** | `/robot1/cmd_vel` | Best Effort | Volatile | Keep Last (1) |
| **State** | `/robot1/map` | Reliable | Volatile | Keep Last (1) |
| **Configuration** | `/tf_static` | Reliable | Transient Local | Keep All |
| **Clock** | `/clock` | Best Effort | Volatile | Keep Last (1) |

---

## Expected Output During Startup

```
[INFO] [launch]: All log files can be found below /home/joseg/.ros/log/...
[INFO] [launch]: Default logging verbosity is set to INFO
[INFO] [gzserver-1]: process started with pid [5191]
[INFO] [gzclient-2]: process started with pid [5193]
[INFO] [ros2-3]: process started with pid [5195]
[INFO] [robot_state_publisher-4]: process started with pid [5197]
[INFO] [ros2-5]: process started with pid [5199]
[INFO] [robot_state_publisher-6]: process started with pid [5201]

[robot_state_publisher-6] [INFO] [...] [robot2.robot_state_publisher]: got segment base_footprint
[robot_state_publisher-6] [INFO] [...] [robot2.robot_state_publisher]: got segment base_link
...
[ros2-5] [INFO] [...] [spawn_entity]: Spawn status: SpawnEntity: Successfully spawned entity [robot2]
[ros2-3] [INFO] [...] [spawn_entity]: Spawn status: SpawnEntity: Successfully spawned entity [robot1]
```

---

## Troubleshooting

### Topic Not Found

```bash
ros2 topic list | grep robot1
```

If no topics appear:
- Check robot spawned successfully (look for "Successfully spawned" in output)
- Verify TF tree: `ros2 run tf2_tools view_frames`
- Check Gazebo is running: `ps aux | grep gzserver`

### TF Errors

```bash
ros2 run tf2_tools view_frames
# Check for cycles or missing transforms
```

### No Odometry Published

- Verify Gazebo physics running
- Check `use_sim_time: true` in all parameters
- Verify odometry plugin loaded in URDF

---

## Next Phase (Phase 2)

- Add Nav2 nodes (planner_server, controller_server, behavior_tree_navigator)
- Add new topics for costmaps and paths
- Add `/navigate_to_pose` action clients

---

**Last Updated:** 2026-08-20  
**Completeness:** Phase 1 only (will expand as phases complete)
