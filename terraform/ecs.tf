# Create ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "pioneer-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "pioneer-cluster"
  }
}

# Create ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "pioneer-task"
  requires_compatibilities = ["FARGATE"]
  network_mode            = "awsvpc"
  cpu                     = 512
  memory                  = 1024
  execution_role_arn      = aws_iam_role.ecs_execution_role.arn
  task_role_arn           = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "pioneer-app"
      image     = "${data.aws_ecr_repository.app.repository_url}:latest"
      essential = true
      
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]

      environment = [
        {
          name  = "ENVIRONMENT"
          value = "staging"
        },
        {
          name  = "PORT"
          value = "8000"
        }
      ]

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/pioneer-app"
          "awslogs-region"        = "us-west-2"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])

  tags = {
    Name        = "pioneer-task"
    Environment = "staging"
  }
}

# Create CloudWatch Log Group
resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/pioneer-app"
  retention_in_days = 30

  tags = {
    Name = "pioneer-logs"
  }
}

# Use existing ECR Repository
data "aws_ecr_repository" "app" {
  name = "pioneer"
}

# Create VPC for ECS
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "pioneer-vpc"
  }
}

# Create Public Subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "pioneer-public-subnet-${count.index + 1}"
  }
}

# Create Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "pioneer-igw"
  }
}

# Create Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "pioneer-public-rt"
  }
}

# Associate Route Table with Subnets
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Create Security Group for ECS Tasks
resource "aws_security_group" "ecs_tasks" {
  name        = "pioneer-ecs-tasks-sg"
  description = "Allow inbound traffic for ECS tasks"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Allow inbound HTTP"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "pioneer-ecs-tasks-sg"
  }
}

# Create ECS Service
resource "aws_ecs_service" "app" {
  name            = "pioneer-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2  # Running two instances for high availability
  launch_type     = "FARGATE"

  deployment_controller {
    type = "ECS"
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [task_definition]
  }

  tags = {
    Name        = "pioneer-service"
    Environment = "staging"
  }
}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}
