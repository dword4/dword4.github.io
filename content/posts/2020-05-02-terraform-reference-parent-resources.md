---
Title: Terraform – Reference parent resources
Author: dword
Date: 2020-05-02
Category: cloud
Tags: aws, cloud, terraform
Slug: reference-parent-resource-tf
Summary: How to reference a parent resource in Terraform
---
Sometimes things get complicated in Terraform, like when I touch it and make a proper mess of the code. Here is a fairly straight forward example of how to reference parent resources in a child.

```
├── Child
│   └── main.tf
└── main.tf

1 directory, 2 files
$ pwd
/Users/dword4/Terraform
```

First lets look at what should be in the top level main.tf file, the substance of which is not super important other than to have a rough idea of what you want/need

```terraform
provider "aws" {
  region = "us-east-2"
  profile = "lab-profile"
}

terraform {
  backend "s3" {}
}

# lets create an ECS cluster

resource "aws_ecs_cluster" "goats" {
  name = "goat-herd"
}

output "ecs_cluster_id" {
  value = aws_ecs_cluster.goats.id
}
```

What this does simply is create an ECS cluster with the name "goat-herd" in us-east-2 and then outputs ecs\_cluster\_id which contains the ID of the cluster. While we don't necessarily need the value outputted visually to us, we need the output because it makes the data available to other modules including child objects. Now lets take a look at what should be in Child/main.tf

```terraform
provider "aws" {
  region = "us-east-2"
  profile = "lab-profile"
}

terraform {
  backend "s3" {}
}
module "res" {
  source = "../../Terraform"
}
output "our_cluster_id" {
  value = "${module.res.ecs_cluster_id}"
}
```

What is going on in this file is that it creates a module called res and sources it from the parent directory where the other main.tf file resides. This allows us to reference the module and the outputs it houses, enabling us to access the ecs\_cluster\_id value and use it within other resources as necessary.
