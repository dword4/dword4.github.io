Title: My Homelab - Building a Production-Grade Network at Home
Date: 2026-06-08
Category: homelab
Slug: homelab-overview-infrastructure-tour
Authors: dword4
Summary: A tour of my home lab infrastructure — from Cisco switching and Ruckus APs through Proxmox/Unraid compute, VLAN segmentation, internal PKI, SSO with Authentik, a full Grafana/Loki observability stack, and GitOps-style CI/CD with Forgejo and Infisical. Built for learning, operated like production.


Over the years, my homelab has evolved from a few spare machines running random services into something that genuinely resembles enterprise infrastructure — complete with VLANs, SSO, internal PKI, CI/CD pipelines, and a full observability stack. Here's a tour of what I'm running and why.
 
---
 
## The Hardware
 
The foundation is a **Cisco C891F** router paired with a **Cisco C3560CX** switch, giving me proper enterprise-grade L3 switching at the edge. Wireless is handled by a pair of **Ruckus R710** access points running Unleashed firmware — these are enterprise APs and the Wi-Fi quality shows it.
 
For compute, I run two **Proxmox** hypervisor nodes and two **Unraid** servers alongside a bare metal Linux dev machine. A **Raspberry Pi 4** and **Pi 5** round out the fleet, handling lightweight workloads and edge tasks. It's more iron than most people have in a datacenter closet, but there's always something to run on it.
 
---
 
## Network Segmentation
 
The network is divided into four VLANs:
 
| VLAN | Name | Purpose |
|------|------|---------|
| 10 | Trusted | Daily drivers, workstations |
| 20 | IoT | Smart home devices, cameras |
| 30 | Guest | Visitor Wi-Fi |
| 99 | Management | Infrastructure access |
 
DNS is handled internally by **Technitium** at `192.168.99.3`, resolving the `int.itsn.network` domain for all internal services. This makes service discovery clean and consistent — every self-hosted app gets a proper hostname.
 
---
 
## Identity & PKI
 
One of the more "enterprise-y" things I've built is a proper identity layer. **Authentik** serves as my SSO/IdP — think of it as a self-hosted Okta portal. Services like Grafana and Netbox authenticate via OIDC, so there's a single login experience across the stack.
 
Certificates are managed by **Certwarden**, backed by an internal CA called **NestCA**. Every service on `*.int.itsn.network` gets a valid TLS cert via wildcard, which means no browser warnings and no `curl -k` shortcuts. Real TLS, internally.
 
---
 
## Observability
 
The observability stack centers on **Grafana** with **Prometheus** for metrics and **Loki + Promtail** for log aggregation. Logs flow in from Proxmox hypervisors, Ruckus APs (via rsyslog), and various services — all centralized and queryable from a single Grafana instance.
 
This isn't just a dashboard for show. When something breaks at 2am, the logs are there.
 
---
 
## CI/CD & Secrets
 
**Forgejo** (a self-hosted Gitea fork) hosts my code, and **Forgejo Actions** handles CI/CD — pipelines that build, test, and deploy against internal infrastructure with SSL trust properly configured against NestCA.
 
Secrets are managed by a self-hosted **Infisical** instance at `infisical.int.itsn.network`. Machine identities authenticate to pull secrets at runtime, keeping credentials out of repos and environment variables.
 
---
 
## Infrastructure as Code
 
VM provisioning on Proxmox is fully automated with **Terraform** (using the `bpg/proxmox` provider) and **Ansible** for configuration management. Cloud-init Ubuntu 24.04 templates make spinning up new VMs a single `terraform apply`. AWS infrastructure is also managed via Terraform.
 
---
 
## Self-Hosted Services
 
The application layer is dense. A sampling of what's running:
 
- **Nginx Proxy Manager** — reverse proxy and SSL termination
- **Netbox** — IPAM and network documentation
- **Bookstack** — internal wiki
- **Jellyfin + arr stack** — media server
- **Home Assistant** — home automation with Zigbee, Node-RED, Frigate NVR (object detection, LPR, face recognition), and SmartCast TV control
- **Meshtastic/LoRa** — off-grid mesh networking experiments
---
 
## Lessons Learned
 
Running homelab infrastructure at this scale teaches you things you can't get from a tutorial:
 
- **PKI is hard until it isn't.** Getting internal TLS right — CA trust, cert distribution, mTLS — is painful once and painless forever.
- **Secrets management matters even at home.** Hardcoded credentials in a `docker-compose.yml` are a bad habit at any scale.
- **Observability is not optional.** If you can't see what's happening, you're just guessing.
- **Automation compounds.** Every hour spent on Terraform and Ansible pays back many times over.
The homelab is never "done" — there's always another service to integrate, another pipeline to harden, another protocol to explore. That's the point.

