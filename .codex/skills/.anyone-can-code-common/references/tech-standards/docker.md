# Docker And Kubernetes Standards

Apply these rules when a lab includes infrastructure files.

## Dockerfile

- use explicit base image tags
- comment non-obvious build steps
- require `docker build` to succeed

## Compose

- prefer `compose.yaml`
- require clean `docker compose up -d` and `docker compose down`
- explain each service briefly

## Kubernetes

- require `kubectl apply --dry-run=client`
- specify namespace explicitly
- explain each manifest's purpose

## Verification

Infrastructure demos must pass their validation command before the lab is accepted.
