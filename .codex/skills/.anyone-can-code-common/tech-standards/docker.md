# Docker / Kubernetes Standards

These rules apply to any lab containing Dockerfiles, Compose files, or Kubernetes YAML. Read and apply them when writing or reviewing infrastructure demo files.

---

## Dockerfile

- Must build successfully: `docker build -t test-lab . 2>&1`
- Use official base images with explicit version tags — never `latest` unless intentional
- Add a comment above each `RUN` instruction explaining what it does
- Multi-stage builds preferred for any image serving production traffic

---

## Docker Compose

- File must be named `compose.yaml` (not `docker-compose.yml`)
- Must start cleanly: `docker compose up -d 2>&1`
- Must stop cleanly: `docker compose down`
- Every service has a comment explaining its role in the demo

---

## Kubernetes YAML

- Apply dry-run must succeed: `kubectl apply -f [file] --dry-run=client 2>&1`
- Every manifest has a comment block explaining what it is and why it exists
- Specify namespace explicitly — never rely on the default namespace implicitly

---

## Config files (nginx.conf, etc.)

- Validate with the tool if it's available locally (e.g., `nginx -t`)
- Add section comments explaining each configuration block's purpose

---

## Exit codes

All `docker build` and `docker compose up` commands must succeed (exit 0) before the lab is committed. Verify:

```bash
docker build -t test-lab . 2>&1; echo "Exit: $?"
docker compose up -d 2>&1; echo "Exit: $?"
```
