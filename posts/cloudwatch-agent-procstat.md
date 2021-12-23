Title: Monitoring on AWS with CloudWatch Agent and Procstat
Date: 2020-08-26
Category: cloud-aws
Slug: monitoring-cloudwatch-agent-procstat
Authors: dword4
Tags: AWS, CloudWatch, procstat, EC2, monitoring
Summary: Install CloudWatch agent with procstat on an EC2 instance and configure a metric alarm in CloudWatch

One of the first issues I ran into was with IAM Policies, or lack thereof . Specifically it was the managed policy **CloudWatchAgentServerPolicy** which needed to be added. The telltale sign that you forgot to add this Policy is an error message in the Agent logs, seen below


```
2020-08-17T22:46:18Z E! refresh EC2 Instance Tags failed: NoCredentialProviders: no valid providers in chain<br>caused by: EnvAccessKeyNotFound: failed to find credentials in the environment.
```

The procstat plugin fortunately is already part of the Agent from install, but it still needs to be configured. In order to do this you have to add a configuration file specific to your monitoring needs. For old school admins the easiest way to think of procstat is that it basically ties into the ps tool. It’s like doing a `ps -ef | grep` to find something about a running process.

```
[root@lab-master amazon-cloudwatch-agent.d]# pwd
/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.d
[root@lab-master amazon-cloudwatch-agent.d]# cat processes
{
    "metrics": {
        "metrics_collected": {
            "procstat": [
                {
                    "pattern": "nginx: master process /usr/sbin/nginx",
                    "measurement": [
                        "pid_count"
                    ]
                }
            ]
        }
    }
}
```

This will get us far enough that now we can see values in the Metrics view of CloudWatch. Once we have data there its time to construct a metric alarm. My goal was to use Terraform however its less painful to do in the AWS console.

```
resource "aws_cloudwatch_metric_alarm" "nginx-master" {
  alarm_name = "nginx master alarm"
  comparison_operator = "LessThanThreshold"
  evaluation_periods = 1
  datapoints_to_alarm = 1
  metric_name = "procstat_lookup_pid_count"
  namespace = "CWAgent"
  period = "300"
  statistic = "Average"
  threshold = "1"
  alarm_description = "Checks for the presence of an nginx-master process"
  alarm_actions = [aws_sns_topic.pagerduty_standard_alarms.arn]
  insufficient_data_actions = []
  treat_missing_data = "missing"
  dimensions = {
    "AutoScalingGroupName" = "some-ASG-YXI8VDT6MBE3"
    "ImageId"       = "some-ami"
    "InstanceId"    = "some-instance-id"
    "InstanceType"  = "t3a.large"
    "pattern"       = "nginx: master process /usr/sbin/nginx"
    "pid_finder"    = "native"
  }
}
```

The alarm creation proved to be a lot harder than I had expected, taking up several hours. I had to re-create things in my lab setup twice and do a Terraform import. The problem turned out to be that the dimensions{} block is not optional despite what the Terraform docs say. Had it said the fields were all required I probably would have saved days of time

## Polish Work

In the process of working things out I hard coded a lot of values in the Dimensions {} block. Naturally that is not good practice, especially with IaaS so I will need to rework it to use variables instead. Also the alarm names should utilize the Terraform workspace values for better naming.