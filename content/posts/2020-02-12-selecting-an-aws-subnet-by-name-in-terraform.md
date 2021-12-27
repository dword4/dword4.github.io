---
Title: Selecting an AWS subnet by name in Terraform
Authors: dword
Date: 2020-02-12
Category: cloud
Tags: aws, terraform
Slug: aws-subnet-by-name
Summary: Selecting an AWS Subnet by name using Terraform
---
One of my recent challenges has been to write tf code to select existing [subnets][1] and use them in new blocks of code (specifically in this case to create a Directory, Workspaces and add a few Security Group entries). Since I am relatively new to using Terraform to do this it took far longer to figure out than I would care to say and I figured it would be best to document what finally worked and had the concept click for me in my mind. 

```terraform
provider "aws" {
  region = "us-east-1"
}
variable "subnet_name" {
  default = "workspaces-private-us-east-1c"
}
data "aws_subnet" "selected" {
  filter {
    name = "tag:Name"
    values = ["${var.subnet_name}"]
  }
}

output "vpcid" {
  value = "${data.aws_subnet.selected.vpc_id}"
}

output "subnet_name" {
  value = "${var.subnet_name}"
}
output "subnet_id" {
  value = "${data.aws_subnet.selected.id}"
}
```

This will look up the named subnet &#8220;workspaces-private-us-east-1c&#8221; and obtain not only the VPC ID associated with it but the unique subnet id as well, the output should look something like the below sample provided the name you are looking up is unique

```shell
data.aws_subnet.selected: Refreshing state...

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

subnet_id = subnet-0299e079c90b20ea6
subnet_name = workspaces-private-us-east-1c
vpcid = vpc-04066bef0a56ebcc2
```

This is of course specific to things as of Terraform 0.12.20 and provider.aws 2.48.0 so naturally things may change over time, however this will get you close and provide you enough of a starting point to use these subnets in other things.

 [1]: https://www.terraform.io/docs/providers/aws/d/subnet.html
