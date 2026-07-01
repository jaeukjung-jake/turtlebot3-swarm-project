import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_srvs.srv import SetBool
import math
import time

class BlueFollower(Node):
    def __init__(self):
        super().__init__('blue_follower')

        # 리더와 팔로워 odom 토픽
        self.leader_odom_topic = '/red/odom'
        self.follower_odom_topic = '/blue/odom'

        # 퍼블리셔 (/blue/cmd_vel)
        self.cmd_pub = self.create_publisher(Twist, '/blue/cmd_vel', 10)

        # 구독자 등록
        self.create_subscription(Odometry, self.leader_odom_topic, self.leader_cb, 10)
        self.create_subscription(Odometry, self.follower_odom_topic, self.follower_cb, 10)

        # 모터 전원 서비스 (/blue/motor_power)
        self.motor_cli = self.create_client(SetBool, '/blue/motor_power')
        self.enable_motor_power()

        # 제어 파라미터 (단순화)
        self.target_distance = 0.5
        self.k_lin = 0.8
        self.k_ang = 1.2
        self.max_lin = 0.15
        self.max_ang = 1.0

        self.leader_pose = None
        self.follower_pose = None
        self.last_cmd_time = time.time()

        # 제어 루프 (10Hz)
        self.create_timer(0.1, self.control_loop)

    def enable_motor_power(self):
        if not self.motor_cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn("⚠️ /blue/motor_power 서비스 없음: 이미 ON이거나 bringup 네임스페이스 확인 필요.")
            return
        req = SetBool.Request()
        req.data = True
        fut = self.motor_cli.call_async(req)
        rclpy.spin_until_future_complete(self, fut, timeout_sec=2.0)
        if fut.result() and fut.result().success:
            self.get_logger().info("✅ 팔로워봇 모터 전원 ON")
        else:
            self.get_logger().warn("⚠️ 팔로워봇 모터 전원 ON 실패")

    def leader_cb(self, msg: Odometry):
        self.leader_pose = msg.pose.pose

    def follower_cb(self, msg: Odometry):
        self.follower_pose = msg.pose.pose

    def control_loop(self):
        if self.leader_pose is None or self.follower_pose is None:
            self.safe_stop()
            return

        lx, ly = self.leader_pose.position.x, self.leader_pose.position.y
        fx, fy = self.follower_pose.position.x, self.follower_pose.position.y

        dx, dy = lx - fx, ly - fy
        distance = math.hypot(dx, dy)

        target_theta = math.atan2(dy, dx)
        yaw = self.quat_to_yaw(self.follower_pose.orientation)
        ang_err = math.atan2(math.sin(target_theta - yaw), math.cos(target_theta - yaw))
        lin_err = distance - self.target_distance

        cmd = Twist()
        cmd.angular.z = self.clamp(self.k_ang * ang_err, -self.max_ang, self.max_ang)

        # 각도 오차 작으면 앞으로 이동
        if abs(ang_err) < 0.5:
            cmd.linear.x = self.clamp(self.k_lin * lin_err, -self.max_lin, self.max_lin)
        else:
            cmd.linear.x = 0.0

        self.cmd_pub.publish(cmd)
        self.last_cmd_time = time.time()

    def safe_stop(self):
        if time.time() - self.last_cmd_time > 0.5:
            self.cmd_pub.publish(Twist())

    @staticmethod
    def quat_to_yaw(q):
        siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1.0 - 2.0 * (q.y*q.y + q.z*q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    @staticmethod
    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

def main(args=None):
    rclpy.init(args=args)
    node = BlueFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()