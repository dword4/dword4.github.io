Title: Terraform Basics - Importing Existing Resources
Date: 2026-05-13
Category: programming
Slug: terraform-basics-importing
Authors: dword4
Summary: Very basic introduction to importing existing AWS resources


So you have inherited some AWS resources that are not yet in Terraform, but its not feasible to completely rebuild them from scratch without a huge interruption to services. This is where importing comes into play, its not always the most elegant of processes but it helps avoid rebuilding things to get them into IaC.

Lets say we have a VPC that already exists in AWS
```bash
$> aws ec2 describe-vpcs 
{
    "Vpcs": [
        {
            "OwnerId": "123456789012",
            "InstanceTenancy": "default",
            "CidrBlockAssociationSet": [
                {
                    "AssociationId": "vpc-cidr-assoc-00000000",
                    "CidrBlock": "172.31.0.0/16",
                    "CidrBlockState": {
                        "State": "associated"
                    }
                }
            ],
            "IsDefault": true,
            "Tags": [],
            "VpcId": "vpc-00000000",
            "State": "available",
            "CidrBlock": "172.31.0.0/16",
            "DhcpOptionsId": "dopt-00000000"
        }
    ]
}
```

In order to do an import our code first has to have a very loose idea of what we are going to import, so lets setup for that in our main.tf file. We will assume safely that you have already run terraform init to setup everything.

```bash
resource "aws_vpc" "test_vpc" {
    # imported resource
}
```

If you were to run an init and plan on this it would want to create the resource named test-vpc, however we dont want to create anything we want to import. Remember the VpcId from earlier when we looked at the available VPCs? We need to use that with import, it should look like this

```bash
$> terraform import aws_vpc.test_vpc vpc-00000000
aws_vpc.test_vpc: Importing from ID "vpc-00000000"...
aws_vpc.test_vpc: Import prepared!
  Prepared aws_vpc for import
aws_vpc.test_vpc: Refreshing state... [id=vpc-00000000]

Import successful!
```

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.

If you look at the main.tf it still looks the same, nothing special about it but if we look at the actual terraform state we now see the test_vpc resource we imported.
```bash
$> terraform state list
aws_vpc.test_vpc
```
And to look at the contents of that resource

```bash
$> terraform state show aws_vpc.test_vpc
# aws_vpc.test_vpc:
resource "aws_vpc" "test_vpc" {
    arn                                  = "arn:aws:ec2:us-east-1:123456789012:vpc/vpc-00000000"
    assign_generated_ipv6_cidr_block     = false
    cidr_block                           = "172.31.0.0/16"
    default_network_acl_id               = "acl-00000000"
    default_route_table_id               = "rtb-00000000"
    default_security_group_id            = "sg-00000000"
    dhcp_options_id                      = "dopt-00000000"
    enable_dns_hostnames                 = true
    enable_dns_support                   = true
    enable_network_address_usage_metrics = false
    id                                   = "vpc-00000000"
    instance_tenancy                     = "default"
    ipv6_association_id                  = null
    ipv6_cidr_block                      = null
    ipv6_cidr_block_network_border_group = null
    ipv6_ipam_pool_id                    = null
    ipv6_netmask_length                  = 0
    main_route_table_id                  = "rtb-00000000"
    owner_id                             = "123456789012"
    region                               = "us-east-1"
    tags                                 = {}
    tags_all                             = {}
}
```

Now to get our main.tf to be more reasonable and show us some of the thing configured about the VPC we have to move the contents of that resource from the state file into main.tf which should look like the below. You may notice that some values are not brought over like arn, id, tags_all and a bunch of default_ items, the rule here is if its something that would be automatically decided based on the result of applying (aka not available until the vpc is created) then those values do not belong in main.tf and terraform will tell you as much if you run a plan with the values present in the file. Depending on the resource imported this can result in a little trial-and-error to find out what all is not needed.

```bash
resource "aws_vpc" "test_vpc" {
    assign_generated_ipv6_cidr_block     = false
    cidr_block                           = "172.31.0.0/16"
    enable_dns_hostnames                 = true
    enable_dns_support                   = true
    enable_network_address_usage_metrics = false
    instance_tenancy                     = "default"
    region                               = "us-east-1"
    tags                                 = {}
}
```

Once you have all the non-needed items removed from the terraform code you plan should come back looking clean like the output below

```bash
$> terraform plan
aws_vpc.test_vpc: Refreshing state... [id=vpc-00000000]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.
```

From here we can add resources, such as a subnet and the code treats it as if the item was always present in the state

```bash
$> cat main.tf
resource "aws_vpc" "test_vpc" {
    assign_generated_ipv6_cidr_block     = false
    cidr_block                           = "172.31.0.0/16"
    enable_dns_hostnames                 = true
    enable_dns_support                   = true
    enable_network_address_usage_metrics = false
    instance_tenancy                     = "default"
    region                               = "us-east-1"
    tags                                 = {}
}

resource "aws_subnet" "test_subnet" {
    vpc_id = aws_vpc.test_vpc.id
    cidr_block = "172.31.1.0/24"
    availability_zone = "us-east-1a"
    map_public_ip_on_launch = false

    tags = {
        Name = "test_subnet"
    }
}

$> terraform plan
aws_vpc.test_vpc: Refreshing state... [id=vpc-00000000]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_subnet.test_subnet will be created
  + resource "aws_subnet" "test_subnet" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "us-east-1a"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "172.31.1.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block                                = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + region                                         = "us-east-1"
      + tags                                           = {
          + "Name" = "test_subnet"
        }
      + tags_all                                       = {
          + "Name" = "test_subnet"
        }
      + vpc_id                                         = "vpc-00000000"
    }

Plan: 1 to add, 0 to change, 0 to destroy.

``` 
