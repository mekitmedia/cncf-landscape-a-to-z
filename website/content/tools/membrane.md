---
title: "Membrane"
date: '2026-10-31'
layout: single
letter: M
lifecycle_stage: first_pass
status: completed
project_name: "Membrane"
homepage_url: "https://www.membrane-api.io/"
repo_url: "https://github.com/membrane/api-gateway"
cncf_status: "non-cncf"
---

## Summary
Membrane is an open-source API gateway that speaks both REST and SOAP. It allows you to deploy APIs directly from OpenAPI, secure them with OAuth2 and JWT, or turn legacy SOAP web services into JSON APIs with a few lines of YAML. It is lightweight and easy to run as a single container or Java application, requiring no database.

## Key Features
- Native OpenAPI Support: Deploy APIs from OpenAPI descriptions and use OpenAPI for message validation (supports 3.0, 3.1, and 3.2).
- Legacy XML and Web Services Integration: Expose existing SOAP web services as JSON APIs without changing the backend using wsdl2openapi.
- Protect APIs and Legacy Services: Validate messages against OpenAPI, JSON Schema, XSD, and WSDL. Secure APIs with API keys, OAuth2, JWT, and protect SOAP services with WS-Security.
- API Orchestration: Combine calls to multiple APIs in a single flow, process collections with loops, and control execution with conditions.
- Simple Configuration, Flexible Extensions: Configure with YAML, and for custom logic, use Groovy scripts or expressions with SpEL, JSONPath, and XPath.

## Recent Updates
Membrane recently achieved high throughput benchmarks, reaching 216,000 requests/sec for plain proxying and 167,000 requests/sec with OpenAPI validation enabled on a 16-vCPU Azure VM.

## Use Cases
Membrane can be used for proxying APIs, routing, rate limiting, load balancing, validating OpenAPI payloads, performing manual SOAP to REST conversion, acting as an OAuth2 authorization server, and protecting XML, JSON, JSON-RPC, and GraphQL payloads.

## Getting Started
Start Membrane via Docker: `docker run --rm -it -p 2000:2000 predic8/membrane`. To proxy your first API, create an `apis.yaml` and mount it: `docker run --rm -p 2000:2000 -v "$(pwd)/apis.yaml:/opt/membrane/conf/apis.yaml" predic8/membrane`.

## Interesting Facts
Membrane can act as its own OAuth 2.0 authorization server and provides a free 'API Gateway Handbook' eBook.
