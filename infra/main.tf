provider "aws" {
  region = "ap-south-1"
}

resource "aws_key_pair" "devops_key2" {
  key_name   = "devops-key2"
  public_key = file("/home/bhavesh/.ssh/devops-key2.pub")
}

resource "aws_security_group" "micro_sg" {
  name        = "microservices-sg"
  description = "allow ssh and service ports"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # user-service
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # order-service
  ingress {
    from_port   = 5001
    to_port     = 5001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # prometheus
  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # grafana
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 for user-service
resource "aws_instance" "user" {
  ami                    = "ami-02d26659fd82cf299"
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.devops_key2.key_name
  vpc_security_group_ids = [aws_security_group.micro_sg.id]
  tags = { Name = "user-service" }
}

# EC2 for order-service
resource "aws_instance" "order" {
  ami                    = "ami-02d26659fd82cf299"
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.devops_key2.key_name
  vpc_security_group_ids = [aws_security_group.micro_sg.id]
  tags = { Name = "order-service" }
}

# EC2 for monitoring (Prometheus + Grafana)
resource "aws_instance" "monitoring" {
  ami                    = "ami-02d26659fd82cf299"
  instance_type          = "t3.micro"
  key_name               = aws_key_pair.devops_key2.key_name
  vpc_security_group_ids = [aws_security_group.micro_sg.id]
  tags = { Name = "monitoring" }
}

output "user_ip" {
  value = aws_instance.user.public_ip
}
output "order_ip" {
  value = aws_instance.order.public_ip
}
output "monitor_ip" {
  value = aws_instance.monitoring.public_ip
}
