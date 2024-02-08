---
title: Homelab Kubernetes (Terraform)
category: cloud
category_slug: f-cloud
type: content
image: https://upload.wikimedia.org/wikipedia/commons/3/39/Kubernetes_logo_without_workmark.svg
button_url: https://gitlab.com/homelab-infrastructure/kubernetes
---
This project defines the Kubernetes infrastructure for my homelab environment. All services are defined via Terraform and deployed using GitLab CI/CD via their Kubernetes Agent. State is stored in the GitLab repo. 

Self-Hosted Services:
- [Actual Budget](https://github.com/actualbudget/actual)
- [Paperless-NGX](https://github.com/paperless-ngx/paperless-ngx)
- Home Automation stack
  - [Home Assistant](https://github.com/home-assistant)
  - [Eufy Security WS](https://github.com/bropat/eufy-security-ws) Bridge (allows Home Assistant to communicate with Eufy Security products)
  - [Ring-MQTT](https://github.com/tsightler/ring-mqtt) Bridge (connects Home Assistant to Ring Alarm)
- Cloudflared Tunnel (for ingress, cluster is not exposed to the internet)
- Media Stack
  - Plex (out of scope)
  - Overseerr
  - Radarr / Sonarr