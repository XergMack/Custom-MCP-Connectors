# Infrastructure

Put the reproducible Azure deployment definition here.

Recommended contents:

- main.bicep or equivalent IaC
- parameters.example.json
- deploy.ps1
- app settings template
- notes on managed identity, ingress, port, and registry/image

The goal is that Azure can be recreated from GitHub without relying on memory.
