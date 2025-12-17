---
sidebar_position: 6
title: Connecting AI Agents to ROS Controllers
description: Using Python and rclpy to connect AI algorithms to ROS 2 systems
---

# Connecting Python AI Agents to ROS Controllers using rclpy

## Introduction to rclpy

`rclpy` is the Python client library for ROS 2, providing Python bindings for the ROS 2 client library (rcl). It enables Python-based AI agents to integrate with ROS 2-based robotic systems, creating a bridge between AI algorithms and robotic hardware control.

Python has become the dominant language for AI development due to its rich ecosystem of libraries like TensorFlow, PyTorch, and scikit-learn. `rclpy` leverages these advantages while maintaining compatibility with the broader ROS 2 ecosystem, making it ideal for integrating AI algorithms with robotic systems.

## Setting Up rclpy

`rclpy` is typically installed as part of a ROS 2 distribution. For most users, it's available after installing ROS 2 and sourcing the setup script:

```bash
source /opt/ros/humble/setup.bash  # or your ROS 2 distribution
```

A typical `rclpy` node follows this structure:

```python
import rclpy
from rclpy.node import Node

class AIControllerNode(Node):
    def __init__(self):
        super().__init__('ai_controller_node')
        # Initialize publishers, subscribers, services, etc.
        # Set up AI model if needed
        # Configure parameters

def main():
    rclpy.init()
    node = AIControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## Creating Publishers and Subscribers

### Subscribers for Sensor Data

AI agents need to receive sensor data to perceive the environment:

```python
from sensor_msgs.msg import Image, LaserScan, Imu, JointState
from std_msgs.msg import String

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')

        # Subscribe to camera data
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)  # QoS history depth

        # Subscribe to joint states
        self.joint_subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10)

        # Store the latest sensor data
        self.latest_image = None
        self.latest_joints = None

    def image_callback(self, msg):
        self.latest_image = msg
        # Process image data with AI algorithm

    def joint_callback(self, msg):
        self.latest_joints = msg
        # Process joint state data
```

### Publishers for Control Commands

AI agents publish commands to control the robot:

```python
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

class AIControllerNode(Node):
    def __init__(self):
        super().__init__('ai_controller')

        # Publisher for robot velocity commands
        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        # Publisher for joint position commands
        self.joint_cmd_publisher = self.create_publisher(
            JointState,
            '/joint_group_position_controller/commands',
            10)

    def send_velocity_command(self, linear_x, linear_y, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.linear.y = linear_y
        msg.angular.z = angular_z
        self.cmd_vel_publisher.publish(msg)

    def send_joint_positions(self, joint_names, positions):
        msg = JointState()
        msg.name = joint_names
        msg.position = positions
        self.joint_cmd_publisher.publish(msg)
```

### Quality of Service (QoS) Configuration

Configure QoS settings to match your application's requirements:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy

# For critical control commands - reliable delivery
control_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST
)

# Create publisher with custom QoS
self.control_publisher = self.create_publisher(
    Twist,
    '/cmd_vel',
    qos_profile=control_qos
)
```

## Integrating AI Models with ROS 2

### Loading AI Models

AI models can be loaded within ROS 2 nodes for real-time inference:

```python
import tensorflow as tf
import torch
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class AIInferenceNode(Node):
    def __init__(self):
        super().__init__('ai_inference_node')

        # Initialize OpenCV bridge for image conversion
        self.bridge = CvBridge()

        # Load pre-trained models
        self.load_models()

        # Subscribe to sensor data
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.inference_callback,
            10)

        # Publisher for inference results
        self.result_publisher = self.create_publisher(
            String,
            '/ai/inference_result',
            10)

    def load_models(self):
        """Load AI models during initialization"""
        try:
            # Load TensorFlow/Keras model
            self.detection_model = tf.keras.models.load_model('/path/to/detection_model')
            self.get_logger().info('AI model loaded successfully')
        except Exception as e:
            self.get_logger().error(f'Failed to load AI model: {e}')

    def inference_callback(self, msg):
        """Process incoming sensor data with AI models"""
        try:
            # Convert ROS image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Preprocess image for model
            processed_image = self.preprocess_image(cv_image)

            # Run inference
            with torch.no_grad():  # For PyTorch models
                prediction = self.classification_model(processed_image)

            # Publish results
            result_msg = String()
            result_msg.data = str(prediction.cpu().numpy().tolist())
            self.result_publisher.publish(result_msg)
        except Exception as e:
            self.get_logger().error(f'Inference error: {e}')

    def preprocess_image(self, image):
        """Preprocess image for AI model input"""
        # Resize, normalize, convert to tensor as needed by your model
        resized = cv2.resize(image, (224, 224))
        normalized = resized / 255.0
        tensor = torch.tensor(normalized, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)
        return tensor
```

### Real-time Performance Considerations

**Threading**: Use separate threads for AI inference to avoid blocking the ROS communication loop:

```python
import threading
import queue

class ThreadedAINode(Node):
    def __init__(self):
        super().__init__('threaded_ai_node')

        # Queue for passing data between threads
        self.data_queue = queue.Queue(maxsize=10)

        # Start AI processing thread
        self.ai_thread = threading.Thread(target=self.ai_processing_loop)
        self.ai_thread.daemon = True
        self.ai_thread.start()

        # Subscribe to sensor data
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.sensor_callback,
            10)

    def sensor_callback(self, msg):
        """Called in main thread - just queue the data"""
        try:
            self.data_queue.put_nowait(msg)
        except queue.Full:
            self.get_logger().warn('Data queue full, dropping frame')

    def ai_processing_loop(self):
        """Run in separate thread - handles AI processing"""
        while rclpy.ok():
            try:
                # Get data from queue (blocks until available)
                msg = self.data_queue.get(timeout=0.1)

                # Process with AI model
                result = self.process_with_ai(msg)

                # Publish result in main thread using call later
                self.call_in_main_thread(result)

            except queue.Empty:
                continue
            except Exception as e:
                self.get_logger().error(f'AI processing error: {e}')
```

## Services for Synchronous Operations

AI agents can provide services to other nodes:

```python
from example_interfaces.srv import SetBool, Trigger

class AIServiceNode(Node):
    def __init__(self):
        super().__init__('ai_service_node')

        # Service to enable/disable AI processing
        self.enable_service = self.create_service(
            SetBool,
            'enable_ai_processing',
            self.enable_callback)

        self.ai_enabled = True

    def enable_callback(self, request, response):
        """Handle enable/disable request"""
        self.ai_enabled = request.data
        response.success = True
        response.message = f"AI processing {'enabled' if self.ai_enabled else 'disabled'}"
        self.get_logger().info(response.message)
        return response
```

## Actions for Long-Running Tasks

For tasks that take significant time, ROS 2 actions are more appropriate:

```python
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci

class AIActionServer(Node):
    def __init__(self):
        super().__init__('ai_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,
            'ai_fibonacci',
            execute_callback=self.execute_callback)

    async def execute_callback(self, goal_handle):
        """Execute the goal (runs in separate thread)"""
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            # Simulate AI processing time
            time.sleep(0.1)

            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])

            # Publish feedback
            goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info('Goal succeeded')

        return result
```

## Example: Complete AI-ROS Integration

Here's an example showing an AI agent controlling a humanoid robot:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Image, Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import numpy as np
import tensorflow as tf
import threading
import queue
from cv_bridge import CvBridge

class HumanoidAIController(Node):
    def __init__(self):
        super().__init__('humanoid_ai_controller')

        # Initialize components
        self.bridge = CvBridge()
        self.data_queue = queue.Queue(maxsize=5)

        # Load AI model for movement planning
        try:
            self.movement_model = tf.keras.models.load_model('/path/to/movement_model')
            self.get_logger().info('Movement model loaded successfully')
        except Exception as e:
            self.get_logger().error(f'Failed to load movement model: {e}')
            self.movement_model = None

        # Subscribe to sensor data
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)

        # Publishers for control commands
        self.cmd_vel_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.status_pub = self.create_publisher(
            String,
            '/ai/status',
            10)

        # Timer for periodic AI decision making
        self.control_timer = self.create_timer(0.1, self.ai_control_loop)

        # Store current sensor data
        self.current_joint_positions = None

    def joint_state_callback(self, msg):
        """Store current joint positions"""
        self.current_joint_positions = np.array(msg.position)

    def ai_control_loop(self):
        """Main control loop running at 10Hz"""
        if self.current_joint_positions is not None and self.movement_model is not None:
            try:
                # Prepare input for movement model
                input_data = self.prepare_movement_input()

                # Get AI prediction for next movement
                target_positions = self.movement_model.predict(
                    np.expand_dims(input_data, axis=0)
                )[0]

                # Send trajectory command (simplified)
                self.send_velocity_command(target_positions[0], 0, target_positions[1])

                # Publish status
                status_msg = String()
                status_msg.data = f"Controlling robot with AI"
                self.status_pub.publish(status_msg)

            except Exception as e:
                self.get_logger().error(f'Control loop error: {e}')

    def prepare_movement_input(self):
        """Prepare input data for movement model"""
        # Combine joint positions and other relevant information
        input_data = np.concatenate([
            self.current_joint_positions[:2],  # Using first 2 joints as example
        ])
        return input_data

    def send_velocity_command(self, linear_x, angular_z):
        """Send velocity command"""
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.cmd_vel_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    ai_controller = HumanoidAIController()

    # Use multi-threaded executor to handle callbacks and AI processing
    executor = MultiThreadedExecutor()
    executor.add_node(ai_controller)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        ai_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Best Practices for AI-ROS Integration

### Design Patterns

1. **Separation of Concerns**: Keep AI logic separate from ROS communication logic
   - Create dedicated classes for AI processing
   - Use ROS nodes primarily for communication and coordination
   - Implement clear interfaces between AI components and ROS components

2. **Error Handling**: Implement robust error handling for both AI and ROS components
   - Handle model loading failures gracefully
   - Implement fallback behaviors when AI models fail
   - Use ROS logging appropriately for debugging

3. **Resource Management**: Monitor and manage computational resources
   - Implement resource monitoring to detect system overload
   - Use appropriate QoS settings for different types of data
   - Consider computational requirements when designing AI models

### Performance Optimization

1. **Asynchronous Processing**: Use separate threads or async patterns for AI inference
   - Implement proper thread synchronization
   - Use queues for safe data passing between threads

2. **Message Filtering**: Only process messages at the required frequency
   - Implement message throttling when appropriate
   - Use time-based filtering to reduce processing load

3. **Model Optimization**: Optimize AI models for the target hardware
   - Use quantization to reduce model size and improve speed
   - Implement model pruning to remove unnecessary weights

## Summary

`rclpy` provides a powerful bridge between Python-based AI algorithms and ROS 2 robotic systems. By understanding how to create publishers, subscribers, services, and actions with `rclpy`, you can integrate sophisticated AI models with robotic hardware control. The key is to balance the computational requirements of AI algorithms with the real-time constraints of robotic systems.

In the next section, we'll explore URDF (Unified Robot Description Format) and how it describes the structure of humanoid robots.