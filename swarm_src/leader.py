import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import SetBool
import time

class LeaderController(Node):
    def __init__(self):
        super().__init__('leader_controller')

        # /red/cmd_vel 퍼블리셔
        self.publisher = self.create_publisher(Twist, '/red/cmd_vel', 10)

        # 모터 전원 켜기
        self.motor_cli = self.create_client(SetBool, '/red/motor_power')
        self.enable_motor_power()

        self.start_time = time.time()
        self.timer = self.create_timer(0.1, self.control_loop)

    def enable_motor_power(self):
        if not self.motor_cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn("/red/motor_power 서비스 없음: 이미 ON이거나 네임스페이스 확인 필요.")
            return
        req = SetBool.Request()
        req.data = True
        fut = self.motor_cli.call_async(req)
        rclpy.spin_until_future_complete(self, fut, timeout_sec=2.0)
        if fut.result() and fut.result().success:
            self.get_logger().info("✅ 리더봇 모터 전원 ON")
        else:
            self.get_logger().warn("⚠️ 리더봇 모터 전원 ON 실패")

    def control_loop(self):
        msg = Twist()
        elapsed = time.time() - self.start_time

        # 0~5초: 직진
        if 0 <= elapsed < 5:
            msg.linear.x = 0.08
        else:
            # 이후: 정지
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LeaderController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()