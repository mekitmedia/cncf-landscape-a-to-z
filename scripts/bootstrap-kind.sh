#!/bin/bash
set -e

# Create a Kind cluster
echo "Creating Kind cluster..."
kind create cluster --name d2-fleet-test || true

# Wait for nodes to be ready
kubectl wait --for=condition=Ready nodes --all --timeout=300s

echo "Installing Flux..."
flux install

echo "Bootstrapping Flux OCI Reference Architecture (D2)..."
# Apply the OCIRepository pointing to a public demo d2-fleet artifact
cat <<'YAML' | kubectl apply -f -
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: OCIRepository
metadata:
  name: d2-fleet
  namespace: flux-system
spec:
  interval: 5m
  url: oci://ghcr.io/controlplaneio-fluxcd/d2-fleet
  ref:
    tag: latest
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: d2-fleet
  namespace: flux-system
spec:
  interval: 10m
  sourceRef:
    kind: OCIRepository
    name: d2-fleet
  path: ./clusters/management
  prune: true
  wait: true
YAML

echo "Kind cluster setup complete with Flux D2 (OCI) bootstrap!"
