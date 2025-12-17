---
sidebar_position: 3
title: Nodes, Topics, and Services
description: Understanding the communication patterns in ROS 2
---

# Nodes, Topics, and Services in ROS 2

## Understanding ROS 2 Communication Patterns

ROS 2 implements three primary communication patterns that enable different types of interaction between robotic software components. Understanding these patterns is crucial for developing effective Physical AI systems that can coordinate complex behaviors.

The communication architecture in ROS 2 handles the diverse needs of robotic systems, from real-time sensor data streaming to reliable command execution. Each communication pattern serves specific purposes and has its own advantages and trade-offs. The architecture provides a flexible framework for humanoid robotics applications.

ROS 2's communication patterns are built on the Data Distribution Service (DDS) standard, which provides the underlying infrastructure for distributed communication. This ensures that the communication is both reliable and performant for real-time robotic systems.

DDS provides key capabilities that make it ideal for robotics:
- **Discovery**: Automatic discovery of nodes and their communication interfaces
- **Quality of Service (QoS)**: Configurable policies for reliability and history
- **Data Centricity**: Focus on the data being communicated rather than applications
- **Real-time Performance**: Optimized for time-critical applications

## Nodes: The Building Blocks

### What are Nodes?

Nodes are the fundamental execution units in ROS 2. Each node is a process that performs computation and communicates with other nodes. Think of nodes as specialized organs in the robotic nervous system, each responsible for a specific function:

- **Sensor nodes**: Collect data from cameras, LIDAR, IMUs, etc.
- **Controller nodes**: Execute control algorithms for robot joints
- **Perception nodes**: Process sensor data to recognize objects or understand the environment
- **Planning nodes**: Generate motion plans or high-level action sequences
- **Behavior nodes**: Implement high-level behaviors like walking or grasping

### Node Characteristics

Nodes in ROS 2 have important characteristics:

- **Language agnostic**: Nodes can be written in any supported language (C++, Python, etc.) and still communicate seamlessly
- **Process isolation**: Each node runs in its own process, providing fault tolerance
- **Lifecycle management**: Nodes can be configured with different lifecycle states (unconfigured, inactive, active, finalized)
- **Namespaces**: Nodes can be organized into namespaces to avoid naming conflicts
- **Parameters**: Nodes can be configured through parameters set at launch time or runtime

### Node Lifecycle

ROS 2 provides a lifecycle management system that allows nodes to transition between different states:

1. **Unconfigured**: Node has been created but not yet configured
2. **Inactive**: Node is configured but not executing
3. **Active**: Node is executing and participating in communication
4. **Finalized**: Node has been shut down and resources have been released

This lifecycle system is important for safety-critical robotic systems where proper initialization and shutdown procedures are essential.

### Creating Nodes

Nodes are created by inheriting from the Node class in your chosen programming language. The node constructor requires a name, and optionally a namespace and context. Once created, nodes can create publishers, subscribers, services, and other communication interfaces.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')

        # Create communication interfaces
        self.publisher = self.create_publisher(String, 'topic_name', 10)
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.callback,
            10)

        # Create timer
        self.timer = self.create_timer(0.1, self.timer_callback)

        # Declare parameters
        self.declare_parameter('param_name', 'default_value')

    def callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World'
        self.publisher.publish(msg)
```

## Topics: Publish-Subscribe Communication

### How Topics Work

Topics implement a publish-subscribe communication pattern. In this pattern:

- **Publishers** send messages to a topic
- **Subscribers** receive messages from a topic
- Communication is **asynchronous** and **non-blocking**
- Multiple publishers and subscribers can exist for the same topic

This pattern is well-suited for streaming data where the publisher doesn't need to know who is receiving the data, and subscribers don't need to know who is publishing. It enables loose coupling between different parts of the robotic system.

### Topic Characteristics

Topics are ideal for streaming data like sensor readings or robot states because:

- **Real-time**: Messages are sent as soon as they're available
- **Broadcast**: Multiple subscribers can receive the same data simultaneously
- **Decoupled**: Publishers and subscribers don't need to know about each other
- **Lossy**: If a subscriber isn't ready, messages may be lost (configurable with QoS settings)
- **Scalable**: New subscribers can join without affecting publishers

### Common Topic Use Cases in Humanoid Robotics

- `/joint_states`: Current positions, velocities, and efforts of robot joints
- `/camera/image_raw`: Raw image data from robot cameras
- `/imu/data`: Inertial measurement unit readings
- `/tf`: Transform data representing the relationship between different robot frames
- `/cmd_vel`: Velocity commands for robot base movement
- `/scan`: LIDAR range data for obstacle detection
- `/odom`: Odometry data for position tracking

### Quality of Service (QoS) Configuration

When creating publishers and subscribers, you can configure QoS settings to match your application's requirements:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy

# For critical control commands - reliable delivery
control_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST
)

# For high-frequency sensor data - best effort
sensor_qos = QoSProfile(
    depth=1,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST
)

# Create publisher with custom QoS
self.control_publisher = self.create_publisher(
    Twist,
    '/cmd_vel',
    qos_profile=control_qos
)
```

## Services: Request-Response Communication

### How Services Work

Services implement a request-response communication pattern. In this pattern:

- A **client** sends a request to a **server**
- The **server** processes the request and sends back a response
- Communication is **synchronous** and **blocking**
- There's a clear **one-to-one** relationship between client and server

Services are appropriate for operations that require guaranteed delivery and a specific response. Unlike topics, services ensure that the client receives a response to their request.

### Service Characteristics

Services are appropriate for operations that require:

- **Guaranteed delivery**: The client knows when the server has processed the request
- **Immediate results**: The client receives a response with the result
- **State changes**: Operations that change system state or require acknowledgment
- **Task completion**: Operations that have a clear beginning and end
- **Configuration**: Setting parameters or system states

### Common Service Use Cases in Humanoid Robotics

- `/get_joint_positions`: Retrieve current joint positions
- `/set_joint_positions`: Command specific joint positions
- `/get_robot_state`: Retrieve comprehensive robot state
- `/load_map`: Load a navigation map from file
- `/save_calibration`: Save sensor calibration data
- `/set_parameters`: Update system parameters at runtime
- `/reset_robot`: Reset robot to a known state
- `/enable_motors`: Enable or disable robot motors

## Actions: Goal-Based Communication

Actions represent a third communication pattern in ROS 2 that's important for humanoid robotics:

- **Goal**: A request with a long-running execution
- **Feedback**: Continuous updates during execution
- **Result**: Final outcome when the goal is completed

Actions are perfect for tasks like:
- Moving the robot to a specific location
- Grasping an object
- Walking to a target
- Executing a complex manipulation sequence

Actions combine the best of both topics and services, providing the asynchronous nature of topics with the guaranteed completion of services.

### Common Action Use Cases in Humanoid Robotics

- `/move_base`: Navigate to a specified location
- `/pick_and_place`: Pick up an object and place it elsewhere
- `/follow_path`: Follow a predefined path
- `/speech_synthesis`: Synthesize and speak a text phrase
- `/object_detection`: Detect and classify objects in a scene

## Practical Example: AI-Agent to Robot Communication

Consider how an AI agent might communicate with a humanoid robot using these patterns:

### Perception Loop (Topics)
```
AI Perception Node → subscribes to → /camera/image_raw
                    subscribes to → /lidar/scan
                    subscribes to → /imu/data
                    publishes to  → /detected_objects
                    publishes to  → /environment_map
```

### Planning and Control Loop (Topics and Services)
```
AI Planning Node → subscribes to → /detected_objects
                   subscribes to → /environment_map
                   publishes to  → /motion_plan
                   publishes to  → /arm_controller/commands
                   calls service → /set_navigation_parameters
```

### High-Level Orchestration (Services and Actions)
```
AI Manager Node → calls action   → /move_to_location
                  calls action   → /grasp_object
                  calls service  → /get_robot_status
                  calls service  → /reset_robot
```

## Quality of Service (QoS) Settings

ROS 2 provides QoS settings that allow you to tune communication behavior:

### Reliability Policy
- **Reliable**: All messages are delivered (like TCP)
- **Best Effort**: Messages may be lost (like UDP)

Critical sensor data and control commands should use reliable delivery, while high-frequency sensor data might use best effort.

### Durability Policy
- **Transient Local**: Late-joining subscribers receive the last message
- **Volatile**: Late-joining subscribers receive no historical messages

Useful for state information that new nodes need immediately.

### History Policy
- **Keep Last**: Store the specified number of most recent messages
- **Keep All**: Store all messages (limited by memory)

Controls how many messages are kept in the queue.

## Best Practices for Communication Design

When designing communication patterns for Physical AI systems:

### Design Principles
1. **Use topics for streaming data** like sensor readings and state updates
2. **Use services for discrete operations** that require acknowledgment
3. **Use actions for long-running tasks** with feedback
4. **Consider real-time requirements** when choosing QoS settings
5. **Design message types carefully** to minimize communication overhead

### Performance Optimization
- **Minimize message size**: Only include necessary data in messages
- **Optimize message frequency**: Balance between information freshness and system load
- **Use appropriate QoS settings**: Match communication requirements to system needs

### Safety and Reliability
- **Implement timeouts**: Prevent indefinite waiting for responses
- **Handle failures gracefully**: Provide fallback behaviors when communication fails
- **Validate data**: Check message contents for reasonableness

## Debugging and Monitoring Communication

ROS 2 provides tools for monitoring and debugging communication:

### Command Line Tools
- `ros2 topic list`: Show all active topics
- `ros2 topic echo <topic_name>`: Display messages on a topic
- `ros2 service list`: Show all available services
- `ros2 node info <node_name>`: Show node's communication interfaces

### Visualization Tools
- **RViz**: Real-time visualization of robot state and sensor data
- **rqt**: Graphical tools for monitoring topics and services
- **ros2 bag**: Recording and playback of message data for analysis

## Summary

Nodes, topics, and services form the foundation of communication in ROS 2. Understanding these patterns is essential for developing AI systems that can effectively communicate with robotic hardware. The publish-subscribe model of topics is ideal for streaming sensor data, while the request-response model of services is perfect for discrete operations requiring confirmation. The goal-based model of actions is ideal for long-running tasks that require feedback during execution.

These communication patterns enable the complex coordination required for humanoid robots to operate effectively in the physical world. By properly designing communication interfaces and selecting appropriate QoS settings, you can create robust and efficient robotic systems that meet the demanding requirements of Physical AI applications.

In the next section, we'll explore how to connect Python AI agents specifically to ROS controllers using rclpy.