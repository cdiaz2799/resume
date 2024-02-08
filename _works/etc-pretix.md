---
title: etc - Pretix (Ansible/Pulumi)
category: cloud
category_slug: f-cloud
type: content
image: https://static.pretix.space/static/pretixeu/img/logo_dark.e848be43c07e.svg
button_url: https://github.com/etcollective/pretix-infra/tree/main
---
## Pretix Ticket Sales
### Infrastructure (Pulumi)
Pulumi is utilized to deploy required resources. Current deployment is installed directly on a single compute node (due to cost). Improvement plans involve containerization and migration to a more cost effective platform (i.e. DigitalOcean).  
Traffic is served via a Cloudflare Tunnel to allow banning all ingress to the compute instance, simplifying management and security.
[![Pretix Architecture Diagram](https://github.com/etcollective/pretix-infra/blob/main/architecture.jpg?raw=true)](https://github.com/etcollective/pretix-infra/blob/main/architecture.jpg)  
[View IaC Repo Here](https://github.com/etcollective/pretix-infra/tree/main)

### Deployment / Configuration (Ansible)
Application installation and configuration is managed via Ansible. I built a custom Ansible role to install and configure the application per documented requirements from the software vendor. 
Eventually, this will be depreciated once application is containerized.  
[View Ansible role here](https://github.com/etcollective/ansible/blob/main/roles/pretix/tasks/main.yml)