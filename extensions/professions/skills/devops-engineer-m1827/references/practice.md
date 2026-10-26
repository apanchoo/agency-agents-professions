# Methods and Validation

## Workflow

1. Define environments, dependencies, secrets and availability criteria.
2. Build and test a container image with a Dockerfile and service configuration.
3. Version the pipeline for building, testing, analyzing and publishing artifacts.
4. Prepare the infrastructure plan and automate configuration and deployment.
5. Verify health probes, observability, scaling and rollback.

## Technical Areas

Select techniques that fit the task and available resources.

- DevOps tools and methods
- Cloud Solutions
- Cloud ecosystem
- Containerization Fundamentals
- Containerized infrastructures
- Program your infrastructure
- DevOps tools
- Cloud computing
- Software architecture
- Mathematical modeling for communicating applications

## Validation Scenarios

Choose a scenario suited to the deliverable and specify inputs, constraints, expected results and checks.

- Manage the pipeline of a Cloud-oriented application
- Design a multi-site computer network hosting virtualized services
- Creation and deployment of application services
- Evolution of an infrastructure

## Deliverables

- Dockerfile and Docker Compose configuration or Kubernetes manifests, as appropriate
- GitLab CI or Jenkins pipeline and test reports
- Terraform or Pulumi infrastructure code and Ansible playbooks suited to the environment
- Deployment, monitoring and rollback procedure

## Acceptance Criteria

- The built image is identified and tested before publication
- The pipeline stops delivery when a required test or check fails
- Secrets are externalized and infrastructure changes are reviewed before application
- The deployment includes an availability check and a verifiable rollback scenario

Retain assumptions, units, inputs and intermediate results needed to reproduce the checks. Distinguish observed results from checks that still need to be performed.
