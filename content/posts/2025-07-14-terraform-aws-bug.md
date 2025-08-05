Title: Terraform & AWS Bug
Date: 2025-07-14
Category: programming
Slug: aws-terraform-bug
Authors: dword4
Summary: Detailing a long-standing bug with Terraform and AWS regarding handling of deletion of resources

### Background

If you're not a frequent AWS user, here's some quick context: AWS Firewall Manager is a service that allows centralized management of AWS WAFs (Web Application Firewalls) across multiple accounts. It's commonly used for enforcing global security policies like IP blocking rules. A few components are relevant to this issue:

- **IP Set**: A named list of CIDR-notated IP addresses.
    
- **Rule Group**: A collection of IP sets grouped together under a named rule with specified actions (e.g., allow, block).
    

As part of building out WAF controls, you might create several IP sets (e.g., for sanctioned countries or specific network ranges) and then reference them in rule groups.

Here are some sample IP sets used for testing:

```plain
ip_sets = {
  IP-Block = [
    "10.0.1.0/24",
    "10.2.0.0/24"
  ],
  IP-Sloth = [
    "192.168.2.0/24",
    "192.168.3.0/24"
  ],
  IP-Snake = [
    "172.22.0.32/32",
    "10.1.2.3/32"
  ]
}
```

And here's how they're referenced in a rule group:

```hcl
rule_groups = {
  NetworkRuleGroup = [
    {
      name     = "IP-Block",
      priority = 0,
      action   = "block",
      statement = {
        ip_set_reference_statement = ["IP-Block"]
      }
    },
    {
      name     = "IP-Allow",
      priority = 1,
      action   = "allow",
      statement = {
        ip_set_reference_statement = ["IP-Sloth", "IP-Snake"]
      }
    }
  ]
}
```

Pretty straightforward. These values live in a `tfvars` file, and Terraform uses some looping logic to construct the necessary resources.

The configuration plans and applies cleanly—no issues there. The problem arises when modifying an existing IP set or rule group. Let's say we want to remove the `IP-Sloth` set. You might expect that deleting it from the `tfvars` file would suffice. Not so fast.

### The Problem

After removing `IP-Sloth` from the `tfvars` file, Terraform's plan correctly reports that it will destroy one resource and modify another. So far, so good. But when applying the plan, Terraform attempts to destroy the `IP-Sloth` IP set _before_ updating the rule group that references it.

Naturally, this fails—Terraform can't delete an IP set that's still in use. The operation spins for a while and then throws an error about the resource being in use.

This behavior is puzzling. When I ran a full `terraform destroy` in my lab environment, everything worked as expected. Terraform deleted the rule groups first and then the IP sets.

To rule out version-specific issues, I tested with Terraform versions 1.9.7, 1.12.0, and 1.12.1. All exhibited the same behavior.

This strongly suggests a dependency ordering bug in Terraform when updating resource graphs involving WAF IP sets and rule groups.

### Solution

In order to cope with this issue it became necessary to create a much more cumbersome process for revising our WAF resources to be a multi-step hokey-pokey dance.

1. Remove IP Sets from any Rule Groups that use them
2. Commit, Push and Run
3. Remove actual IP Set from tfvars
4. Commit, Push and Run
