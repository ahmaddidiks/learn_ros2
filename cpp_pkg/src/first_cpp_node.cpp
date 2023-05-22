#include "rclcpp/rclcpp.hpp"

class MyNode: public rclcpp::Node
{
private:
  /* data */
  void timerCallback()
  {
    counter_++;
    RCLCPP_INFO(this->get_logger(), "Hello %d", counter_);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  int counter_;

public:
  MyNode(): Node("cpp_test"), counter_(0)
  {
    RCLCPP_INFO(this->get_logger(), "Hello Cpp node here");
    timer_ = this->create_wall_timer(std::chrono::milliseconds(100), std::bind(&MyNode::timerCallback, this));
  }
  
};

int main(int arg, char **argv)
{
  rclcpp::init(arg, argv);
  auto node = std::make_shared<MyNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}