# robot_control — Task 7.1: Your First Robot Control

**MIA Robotics — Electrical Training 2026/27**
Individual Task 7.1: A ROS2 package that launches `turtlesim`, provides keyboard-controlled movement, and simultaneously reads and processes color sensor data from the turtle's environment.

## Overview

This package contains a single ROS2 node (`NODE`) that handles both:
- **Movement**: reads keyboard input (W/A/S/D) and publishes `geometry_msgs/msg/Twist` commands to drive the turtle under non-holonomic constraints (forward/backward + rotation only — no sideways strafing).
- **Perception**: subscribes to the turtle's color sensor, calculates the dominant background color (Red/Green/Blue), logs it, and republishes it on a custom topic.

## Package Structure

```
robot_control/
├── robot_control/
│   ├── __init__.py
│   └── NODES.py              # main node: teleop + color sensor logic
├── launch/
│   └── robot_control_launch.py
├── resource/
├── test/
├── package.xml
├── setup.py
└── setup.cfg
```

## Node Details

### Topics

| Topic                     | Type                        | Direction  | Purpose                                  |
|----------------------------|------------------------------|-----------|-------------------------------------------|
| `/turtle1/cmd_vel`         | `geometry_msgs/msg/Twist`    | Publish   | Drives the turtle (linear.x, angular.z)   |
| `/turtle1/color_sensor`    | `turtlesim/msg/Color`        | Subscribe | Reads background r/g/b under the turtle   |
| `/dominant_color`          | `std_msgs/msg/String`        | Publish   | Broadcasts the calculated major color     |

All three topic names are exposed as **ROS2 parameters** (not hardcoded), so they can be remapped at runtime.

### Parameters

| Parameter name          | Default value            |
|--------------------------|---------------------------|
| `cmd_vel_topic`           | `/turtle1/cmd_vel`        |
| `color_sensor_topic`      | `/turtle1/color_sensor`   |
| `dominant_color_topic`    | `/dominant_color`         |

Example override:
```bash
ros2 run robot_control NODE --ros-args -p cmd_vel_topic:=/my_custom_topic
```

### Keyboard Controls

| Key | Action                  |
|-----|--------------------------|
| `W` | Move forward             |
| `S` | Move backward             |
| `A` | Rotate counter-clockwise |
| `D` | Rotate clockwise          |

Keys are read via raw terminal mode (non-blocking), checked every 0.1s by a ROS2 timer.

### Color Detection Logic

On every message from `/turtle1/color_sensor`, the node compares the `r`, `g`, `b` values (0–255) and determines the dominant channel:
- Ties are broken in the order Red → Green → Blue (i.e. Red wins on a Red/Green tie, etc.).

The result is:
1. Logged to console via `self.get_logger().info(...)`
2. Published as a `String` message to `/dominant_color`

## Setup & Installation

Requires ROS2 Jazzy Jalisco on Ubuntu 24.04, with `turtlesim` installed.

```bash
# Clone into your workspace's src folder
cd ~/robot/src
git clone <this-repo-url> robot_control

# Build
cd ~/robot
colcon build --packages-select robot_control
source install/setup.bash
```

> **Note:** `source install/setup.bash` must be re-run in every new terminal session before using `ros2 run`/`ros2 launch` with this package.

## Running

### Option 1 — Launch file (recommended, starts both nodes together)

```bash
ros2 launch robot_control robot_control_launch.py
```

This starts `turtlesim_node` and the custom control node simultaneously.

> **Known limitation:** Due to how `ros2 launch` spawns subprocesses, raw-terminal keyboard reading (`termios`) may not receive proper terminal access when run this way, causing the control node to exit. If WASD control doesn't respond after launching, use Option 2 below, or add `prefix='xterm -e'` to the node entry in the launch file so it spawns its own terminal window.

### Option 2 — Manual (two terminals, guaranteed to work)

```bash
# Terminal 1
ros2 run turtlesim turtlesim_node

# Terminal 2 (in the same workspace, sourced)
ros2 run robot_control NODE
```

Click into Terminal 2 to give it keyboard focus, then use W/A/S/D to drive the turtle.

## Verifying It Works

While running, open a third terminal to inspect the topics:
```bash
ros2 topic list
ros2 topic echo /dominant_color
```
You should see color labels appear as the turtle crosses different background colors.

## Non-Holonomic Constraint

The turtle (like a car or differential-drive robot) cannot move sideways — it can only move along its current heading (`linear.x`) or rotate in place (`angular.z`). This is why WASD control maps to forward/backward + rotation rather than direct X/Y translation.

## Author

Mohammed — Mechatronics and Robotics Engineering, Alexandria University
Electrical Team Training 2026/27, MIA Robotics
