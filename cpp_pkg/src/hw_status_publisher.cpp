#include "rclcpp/rclcpp.hpp"
#include "robot_interface/msg/hardware_status.hpp"

class HardwareStatusPublisherNode : public rclcpp::Node // MODIFY NAME
{
public:
    HardwareStatusPublisherNode() : Node("hardware_status_publisher") // MODIFY NAME
    {
      this->declare_parameter("test123", 2);
      
      pub_ = this->create_publisher<robot_interface::msg::HardwareStatus>(
        "hardware_status", 10);

      timer_ = this->create_wall_timer(
        std::chrono::seconds(1),
        std::bind(&HardwareStatusPublisherNode::publishHardwareStatus, this)
      );

      RCLCPP_INFO(this->get_logger(), "Hardware status publisher has been started");
    }
 
private:
  rclcpp::Publisher<robot_interface::msg::HardwareStatus>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  
  void publishHardwareStatus()
  {
    auto msg = robot_interface::msg::HardwareStatus();
    msg.temperature = this->get_parameter("test123").as_int();
    msg.are_motors_ready = true;
    msg.debug_message = "Nothing special here";
    pub_->publish(msg);
  }
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HardwareStatusPublisherNode>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}