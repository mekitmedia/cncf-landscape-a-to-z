---
cncf_status: non-cncf
date: '2026-11-11T23:07:28.624710'
description: Authelia is an open-source authentication and authorization server providing
  single sign-on and multi-factor authentication for web apps, including OpenID Connect
  1.0 provider support and integration with common reverse proxies including most
  Kubernetes ingress controllers.
homepage_url: https://www.authelia.com
layout: single
letter: A
lifecycle_stage: first_pass
project_name: Authelia
repo_url: https://github.com/authelia/authelia
status: completed
title: Authelia
---



## Overview

Authelia is an open-source authentication and authorization server providing single sign-on and multi-factor authentication for web applications, with OpenID Connect 1.0 provider support and integration with common reverse proxies including Kubernetes ingress controllers.



## Key Features


- Multi-factor authentication supporting WebAuthn/FIDO2 hardware keys, TOTP (Google Authenticator), and Duo push notifications.

- Certified OpenID Connect (OIDC) 1.0 Provider for centralized identity federation.

- Reverse proxy integration with Traefik, NGINX, Envoy, Caddy, and HAProxy via ForwardAuth middleware.

- Granular access control rules allowing per-resource, per-user, and per-network authorization policies.

- Password reset and self-service credential management with identity verification via email.

- Multiple authentication backends including LDAP, Active Directory, and local file storage.




## Use Cases

Securing internal homelab and enterprise services behind reverse proxies with 2FA, enforcing zero-trust access control for web dashboards without native authentication, and providing OIDC identity federation.



{{< callout title="Getting Started" type="code" >}}
Authelia can be deployed via Docker Compose or Kubernetes Helm charts. Configure an authentication backend and wire Authelia's forward-auth endpoint into your ingress reverse proxy.
{{< /callout >}}



## Recent Updates

Authelia v4.38 expanded OpenID Connect 1.0 provider capabilities, enhanced WebAuthn workflows, improved structured configuration validation, and streamlined Kubernetes Helm deployments.



{{< callout title="Did You Know?" type="info" >}}
Authelia is derived from the Greek word for authority and self-determination. It is widely considered one of the most popular lightweight, self-hosted alternatives to complex identity providers like Keycloak.
{{< /callout >}}



## Related Tools


- [Keycloak](/tools/keycloak/)

- [Ory Hydra](/tools/ory_hydra/)

- [Dex](/tools/dex/)

- [Authentik](/tools/authentik/)

- [Pomerium](/tools/pomerium/)


