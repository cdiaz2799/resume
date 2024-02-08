---
title: etc - Website (GCP/Pulumi/Docker)
category: cloud
category_slug: f-cloud
type: content
image: https://storage.googleapis.com/production-website-assets/sites/1/2023/11/ETC-logo.png
button_url: https://github.com/etcollective/etc-website
---
A local theatre company startup needed a cost-effective yet reliable and scalable WordPress site. I combined my knowledge of cloud architecture, Docker, and Google Cloud Platform to deliver a highly reliable website to seamlessly handle the influx of traffic immediately prior to shows.
## WordPress Image
To provide the fastest and most consistent delivery of the website container, all fonts, themes, and plugins utlized for this site is packaged in a single Docker image. This ensures when the deployment is scaled up, containers can start serving traffic immediately.

[View Dockerfile here](https://github.com/etcollective/etc-website/blob/production/Dockerfile)

## Google Cloud Platform
### Cloud Run
The base site is served via Google Cloud Run to allow for many of the benefits of Kubernetes, but saving compute costs rather than running an actual Kubernetes cluster. The site typically sits at one pod, but seamlessly scales up to serve additional traffic (ticket sales immediately before a show). Through their first season, etc has reported no issues with website scalability and has handled traffic influx without issue.  
[View Cloud Run IaC here](https://github.com/etcollective/etc-website/blob/production/infra/cloud_run.py)
### Google Cloud Storage
Static images and fonts are automatically synced from WordPress into Google Cloud Storage, where it is served by Google's Cloud CDN. This significantly reduced the Largest Contentful Paint (LCP) metric.  
[View Cloud Storage IaC here](https://github.com/etcollective/etc-website/blob/production/infra/storage.py)
### Cloud SQL
Cloud SQL is utilized for the WordPress backend, and has effectively served the website's needs using the lowest price class available.  
[View Cloud SQL IaC here](https://github.com/etcollective/etc-website/blob/production/infra/db.py)
### Artifact Registry
For deployment, the image is build by Pulumi on GitHub actions and pushed to Google Artifact Registry, where it is directly consumed by Google Cloud Run.  
[View Artifact Registry IaC here](https://github.com/etcollective/etc-website/blob/production/infra/repo.py)

## Cloudflare
While all traffic and infrastructure is hosted by Google Cloud Platform, content is served via the Cloudflare Proxy. This allows etc to utilize the CDN and performance of the Cloudflare Network without potentially incurring costs utilizing Google's CDNs and simplifying the infrasturcture/deployment. Cloudflare automatically handles caching assets and site content, while also minifying CSS and JS. 