---
title: "Cruising through the 'A's (Part 2): AI Agents, Streaming Big Data, and Serverless"
date: 2027-01-11T09:00:00Z
draft: true
letter: "A"
week: 2
---

Welcome back to Week 2 of our 52-week cloud-native journey! In [Part 1](/posts/2027-a1-cloud-platforms-and-security/), we explored 33 foundational infrastructure projects covering GitOps, Kubernetes orchestration, networking, and zero-trust security.

This week, we dive into the second half of **Letter A**: 37 projects powering **Generative AI, Autonomous Agent Frameworks, Distributed Big Data, and Event-Driven Serverless Compute**.

While traditional big data stalwarts anchor the data tier, the defining frontier of this week's catalog is the emergence of agentic infrastructure. We have structured this edition into four distinct, thematic sections:

1. **Featured: The Agent Game Changers** — The groundbreaking frameworks and protocols defining the autonomous AI agent revolution.
2. **Worth Discovering** — Modern, high-impact innovations in LLM inference, specialized fine-tuning, streaming storage, and reactive microservices.
3. **The Apache Ecosystem** — A dedicated exploration of the vibrant, self-contained sub-landscape created by the Apache Software Foundation starting with 'A'.
4. **On the Shoulders of Giants** — Cloud-provider-specific serverless runtimes and evaluation suites from AWS and Azure, placed lower in the catalog.

### Featured Projects this Week: The Agent Game Changers

Over the next seven days, we spotlight four transformative projects at the forefront of the agentic AI landscape, along with a nod to the pioneering framework that started the wave:

1.  **[Agent Substrate](/tools/agent_substrate/)**: A security-hardened, zero-trust execution sandbox engineered with gVisor, Cloud Hypervisor, and SPIFFE identity to safely run millions of autonomous agents and untrusted tools with 10x higher density than standard containers.
2.  **[Agentgateway](/tools/agentgateway/)**: A cloud-native traffic controller and protocol gateway designed specifically for agent workloads, handling dynamic agent discovery, streaming inference routing, rate-limiting, and stateful sessions.
3.  **[Agent Development Kit (ADK)](/tools/agent_development_kit/)**: Google's extensible toolkit providing production-grade, modular building blocks to construct, run, and scale agentic software in Python.
4.  **[Agent2agent (A2A)](/tools/agent2agent/)**: The open communication protocol that enables heterogeneous agents built on different frameworks to discover each other, negotiate capabilities, and collaborate on complex multi-agent workflows.

---

### The Curated Listicle: 37 AI, Big Data & Serverless Projects

Below is our complete guide to the 37 projects across our four designated sections.

---

## Part One: The Agent Game Changers

These projects are setting the architectural foundations for autonomous AI agents, multi-agent coordination, and secure sandbox execution.

#### [Agent Substrate](https://github.com/agent-substrate/substrate)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/agent-substrate/substrate)

A security-hardened, zero-trust runtime for sandboxed agents, engineered to safely run millions of agents and tools with 10x higher density than standard containers.

**Key Capabilities:**
- Always sandboxed, VM-grade boundaries with gVisor or Cloud Hypervisor
- Per-agent cryptographic identity using SPIFFE X.509 certificates
- Zero credentials in the sandbox via atenet-egress

[Explore full Agent Substrate tool profile & getting started guide →](/tools/agent_substrate/)

---

---

---

#### [Agentgateway](https://agentgateway.dev/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/agentgateway/agentgateway)

Agentgateway is an open source proxy built on AI-native protocols that provides drop-in security, observability, and governance for agent-to-LLM, agent-to-tool, and agent-to-agent communication.

**Key Capabilities:**
- LLM Gateway: Route traffic to major LLM providers through a unified OpenAI-compatible API with budget controls, load balancing, and failover.
- MCP Gateway: Connect LLMs to tools and external data sources via MCP with tool federation, OpenAPI integration, and OAuth authentication.
- A2A Gateway: Secure agent-to-agent communication using A2A with capability discovery and task collaboration.

[Explore full Agentgateway tool profile & getting started guide →](/tools/agentgateway/)

---

---

---

#### [Agent Development Kit](https://google.github.io/adk-docs/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/google/adk-python)

A toolkit for building, running, and managing agentic software at scale.

**Key Capabilities:**
- Provides building blocks for AI agents
- Scalable management of agent lifecycles
- Extensible Python API

[Explore full Agent Development Kit tool profile & getting started guide →](/tools/agent_development_kit/)

---

---

---

#### [Agent2agent](https://a2a-protocol.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/a2aproject/A2A)

Agent2Agent (A2A) is an open protocol enabling communication and interoperability between opaque agentic applications.

**Key Capabilities:**
- Standardized Communication: Defines standard message formats and protocols for AI agents to communicate and coordinate tasks.
- Interoperability: Enables agents built on different frameworks or by different organizations to interact seamlessly.
- Extensibility: Designed to allow developers to define custom capabilities and schemas for their specific use cases while maintaining compatibility.

[Explore full Agent2agent tool profile & getting started guide →](/tools/agent2agent/)

---

## Part Two: Worth Discovering

These high-impact projects bring specialized innovation to model serving, LLM fine-tuning, cloud-native streaming, and reactive microservices.

#### [AIBrix](https://aibrix.github.io/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/vllm-project/aibrix)

AIBrix is an open-source, cost-efficient, scalable, and pluggable cloud-native infrastructure for GenAI applications, tailored specifically to enterprise needs for deploying, managing, and scaling large language model (LLM) inference.

**Key Capabilities:**
- High-Density LoRA Management: Streamlined support for lightweight, low-rank adaptations of models.
- LLM Gateway and Routing: Efficiently manage and direct traffic across multiple models and replicas.
- LLM App-Tailored Autoscaler: Dynamically scale inference resources based on real-time demand.

[Explore full AIBrix tool profile & getting started guide →](/tools/aibrix/)

---

---

---

#### [Agno](https://www.agno.com/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/agno-agi/agno)

Agno is a framework and runtime for agent platforms, allowing you to build, run, and manage agentic software at scale while maintaining control of your data, memory, and security posture.

**Key Capabilities:**
- Production API with over 50 endpoints, SSE, and websockets.
- Built-in storage for sessions, memory, knowledge, and traces.
- More than 100 integrations including GitHub, Slack, and Postgres.

[Explore full Agno tool profile & getting started guide →](/tools/agno/)

---

---

---

#### [Axolotl](https://docs.axolotl.ai)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/axolotl-ai-cloud/axolotl)

Axolotl is a free and open-source tool designed to streamline post-training and fine-tuning for the latest large language models (LLMs).

**Key Capabilities:**
- Multiple Model Support: Train various models like GPT-OSS, LLaMA, Mistral, Mixtral, Pythia, and many more models available on the Hugging Face Hub.
- Multimodal Training: Fine-tune vision-language models (VLMs) and audio models.
- Training Methods: Full fine-tuning, LoRA, QLoRA, GPTQ, QAT, FP8 mixed-precision training, NVFP4/MXFP4 MoE LoRA, Preference Tuning, RL, and Reward Modelling.

[Explore full Axolotl tool profile & getting started guide →](/tools/axolotl/)

---

### Streaming, Message Queuing & Event Routers

---

---

#### [Astron Agent](http://astron.ai/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/iflytek/astron-agent)

Astron Agent is an enterprise-grade, commercial-friendly agentic workflow development platform that integrates AI workflow orchestration, model management, AI and MCP tool integration, RPA automation, and team collaboration features.

**Key Capabilities:**
- AI workflow orchestration and model management
- AI and MCP tool integration
- Native intelligent RPA integration for connecting enterprise systems

[Explore full Astron Agent tool profile & getting started guide →](/tools/astron_agent/)

---

---

---

#### [AutoMQ](https://www.automq.com/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/AutoMQ/automq)

AutoMQ is a cloud-native, diskless alternative to Apache Kafka® on S3 or any S3-compatible storage. It is designed to offer 10x cost savings, scale in seconds, and eliminate cross-AZ traffic costs while maintaining 100% Kafka compatibility.

**Key Capabilities:**
- Stateless broker architecture leveraging object storage (S3) instead of local disk storage.
- 100% Apache Kafka® compatible (retention of Kafka API, protocol, and ecosystem).
- Autoscale in seconds without data rebalancing.

[Explore full AutoMQ tool profile & getting started guide →](/tools/automq/)

---


---

## Part Two: Worth Discovering

These high-impact projects bring specialized innovation to autonomous agent orchestration, low-latency OLAP, LLM model serving, and reactive microservices.

---

#### [Alluxio](https://github.com/Alluxio/alluxio)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/Alluxio/alluxio)

An open-source data orchestration layer that bridges analytical and AI compute frameworks with distributed and cloud storage systems.

**Key Capabilities:**
- Memory-speed distributed caching across storage tiers (RAM, NVMe, SSD).
- Unified namespace aggregating AWS S3, HDFS, GCS, and Ceph.
- Transparent acceleration for PyTorch, TensorFlow, Spark, and Presto/Trino.

[Explore full Alluxio tool profile & getting started guide →](/tools/alluxio/)

---

---

---

#### [ArangoDB](https://www.arangodb.com/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/arangodb/arangodb)

A native multi-model database system supporting graph, document, and key-value data models with a unified declarative query language (AQL).

**Key Capabilities:**
- Unified multi-model engine allowing graph traversals, document queries, and search.
- ArangoDB Query Language (AQL) providing declarative syntax for joins and graph traversals.
- ArangoSearch engine integrating full-text search and similarity search with JSON documents.

[Explore full ArangoDB tool profile & getting started guide →](/tools/arangodb/)

---

---

---

#### [Akka](https://akka.io/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/akka/akka)

A toolkit and runtime for building concurrent, distributed, resilient, and message-driven applications using the Actor model on the JVM.

**Key Capabilities:**
- Actor-based concurrency eliminating explicit locking.
- Akka Cluster for decentralized node discovery and state management.
- Akka Persistence for event sourcing and CQRS.

[Explore full Akka tool profile & getting started guide →](/tools/akka/)

---

---

---

#### [ArkFlow](https://arkflow-rs.com/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/arkflow-rs/arkflow)

A high-performance Rust-based stream processing engine designed for real-time data stream transformation, routing, and event-driven computing.

**Key Capabilities:**
- Blazing fast stream processing built with Rust and Tokio for memory safety and low latency.
- Declarative stream pipeline definitions and modular event filters.
- High-throughput data routing across message brokers and storage sinks.

[Explore full ArkFlow tool profile & getting started guide →](/tools/arkflow/)

---

---

---

#### [Arks](https://www.scitix.ai)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/scitix/arks)

An end-to-end framework developed by Scitix for managing, serving, and orchestrating LLM-based applications and multi-agent systems within Kubernetes.

**Key Capabilities:**
- Kubernetes-native orchestration for large language models and multi-agent workflows.
- Optimized inference scheduling, batching, and GPU resource management.
- Seamless agent communication channels and tool invocation gateways.

[Explore full Arks tool profile & getting started guide →](/tools/arks/)

---

### Reactive Frameworks & WebAssembly Runtimes

---

---

#### [Asyncify](https://github.com/GoogleChromeLabs/asyncify)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/GoogleChromeLabs/asyncify)

A JavaScript wrapper intended to be used with the Asyncify feature of Binaryen. Together, they allow the use of asynchronous APIs (such as most Web APIs) from within WebAssembly written and compiled from any source language.

**Key Capabilities:**
- JavaScript wrapper for Binaryen's Asyncify feature.
- Enables using asynchronous APIs (like most Web APIs) within WebAssembly.
- Supports drop-in replacement APIs for the regular WebAssembly interface with added async support.

[Explore full Asyncify tool profile & getting started guide →](/tools/asyncify/)

---


---

## Part Three: On the Shoulders of Giants

Positioned lower in this catalog, these projects reflect cloud-provider-specific tools (from AWS and Azure) as well as foundational distributed computing engines from the Apache ecosystem. While essential in their respective environments, they are less universally central to independent open-source cloud-native architectures.

### Cloud Provider Platforms & Serverless Runtimes


---

## Part Three: The Apache Ecosystem

The Apache Software Foundation has contributed an extraordinary array of foundational technologies starting with the letter **A**. Spanning stream processing, real-time analytics, big data storage, compilers, and serverless runtimes, this sub-landscape is so vast and influential that it forms an entire ecosystem in its own right.

#### [Apache Spark](https://spark.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/spark)

A unified multi-language engine for executing large-scale data engineering, data science, and machine learning on single-node machines or clusters.

**Key Capabilities:**
- In-memory distributed computing delivering up to 100x speed over MapReduce.
- Unified APIs in Python (PySpark), SQL, Scala, Java, and R.
- Built-in libraries: Spark SQL, Structured Streaming, MLlib, and GraphX.

[Explore full Apache Spark tool profile & getting started guide →](/tools/apache_spark/)

---

---

---

#### [Apache Flink](https://flink.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/flink)

An open-source distributed stream processing engine providing stateful computations over unbounded and bounded data streams with low latency.

**Key Capabilities:**
- Event-driven stream processing with exactly-once state consistency guarantees.
- Sub-millisecond latency with RocksDB state backend.
- Advanced event-time watermarking and windowing.

[Explore full Apache Flink tool profile & getting started guide →](/tools/apache_flink/)

---

---

---

#### [Apache Hadoop](https://hadoop.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/hadoop)

A foundational open-source framework that allows for the distributed processing and storage of large data sets across clusters of computers.

**Key Capabilities:**
- HDFS (Hadoop Distributed File System) for fault-tolerant distributed storage.
- YARN for cluster resource negotiation and workload scheduling.
- Hadoop MapReduce for parallel data computation.

[Explore full Apache Hadoop tool profile & getting started guide →](/tools/apache_hadoop/)

---

---

---

#### [Apache Pinot](https://pinot.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/pinot)

A real-time distributed OLAP datastore designed to execute low-latency analytical queries over streaming and historical data at massive scale.

**Key Capabilities:**
- Ultra-low latency SQL queries (sub-50ms) over billions of rows.
- Pluggable indexing (inverted, star-tree, range, text, JSON, geospatial).
- Real-time streaming ingestion from Kafka, Pulsar, and Kinesis.

[Explore full Apache Pinot tool profile & getting started guide →](/tools/apache_pinot/)

---

---

---

#### [Apache Druid](https://druid.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/druid)

A high-performance, real-time analytics database designed for sub-second OLAP queries on large volumes of event-driven data.

**Key Capabilities:**
- Sub-second query response times for multi-dimensional filtering and grouping.
- Native real-time streaming ingestion from Kafka and Kinesis.
- Columnar storage with dictionary encoding and bitmap indexing.

[Explore full Apache Druid tool profile & getting started guide →](/tools/apache_druid/)

---

---

---

#### [Apache NiFi](https://nifi.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/nifi)

An easy-to-use, powerful, and reliable system to process, transform, and distribute data across distributed enterprise systems.

**Key Capabilities:**
- Web-based visual canvas for designing and monitoring real-time dataflows.
- Complete data provenance tracking every transformation of every FlowFile.
- Guaranteed delivery with configurable backpressure and queuing.

[Explore full Apache NiFi tool profile & getting started guide →](/tools/apache_nifi/)

---

---

---

#### [Apache RocketMQ](https://rocketmq.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/rocketmq)

A distributed messaging and streaming data platform offering low latency, high throughput, high reliability, and ultra-large capacity.

**Key Capabilities:**
- Strict message ordering and transactional message guarantees.
- Massive topic scalability supporting tens of thousands of topics per cluster.
- Configurable message delay and scheduled delivery.

[Explore full Apache RocketMQ tool profile & getting started guide →](/tools/apache_rocketmq/)

---

---

---

#### [Apache Camel K](https://camel.apache.org)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/camel-k)

A lightweight, serverless cloud-native integration framework built on Apache Camel, designed to run integrations directly on Kubernetes and OpenShift.

**Key Capabilities:**
- Sub-second deployment of Enterprise Integration Patterns (EIPs) on Kubernetes.
- Serverless integration powered by Knative scaling down to zero.
- Polyglot DSL support (Java, JS, Groovy, Kotlin, YAML).

[Explore full Apache Camel K tool profile & getting started guide →](/tools/apache_camel_k/)

---

---

---

#### [Apache TVM](https://tvm.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/tvm)

An open-source machine learning compiler framework for CPUs, GPUs, and specialized hardware accelerators.

**Key Capabilities:**
- Automated compilation from PyTorch, TensorFlow, ONNX, and Keras.
- End-to-end compilation lowering computation graphs to hardware machine code.
- AutoTVM and Ansor auto-tuning finding optimal tensor scheduling.

[Explore full Apache TVM tool profile & getting started guide →](/tools/apache_tvm/)

---

---

---

#### [Apache AGE](https://age.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/age)

Apache AGE is a PostgreSQL Graph database extension that leverages graph data structures to analyze and use relationships and patterns in data. It adds graph data processing and analytics capability to relational databases.

**Key Capabilities:**
- Provides graph database functionality as a PostgreSQL extension.
- Read and write graph data in nodes and edges within an existing relational database.
- Supports variable length and edge traversal algorithms.

[Explore full Apache AGE tool profile & getting started guide →](/tools/apache_age/)

---

---

---

#### [Apache Avro](https://avro.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/avro)

Apache Avro is a data serialization system that provides rich data structures, a compact, fast, binary data format, and simple integration with dynamic languages.

**Key Capabilities:**
- Rich data structures defined using JSON.
- Compact, fast, binary data format.
- Container file format for storing persistent data.

[Explore full Apache Avro tool profile & getting started guide →](/tools/avro/)

---

### Distributed Big Data & Analytics Engines


---

---

#### [Apache HBase](https://hbase.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/hbase)

An open-source, distributed, versioned, column-oriented store modeled after Google's Bigtable, providing random real-time read/write access to big data on HDFS.

**Key Capabilities:**
- Linear horizontal scalability across commodity servers.
- Strictly consistent read and write operations at scale.
- Automatic sharding and region failover handling.

[Explore full Apache HBase tool profile & getting started guide →](/tools/apache_hbase/)

---

---

---

#### [Apache Storm](https://storm.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/storm)

A distributed, real-time computation system for processing unbounded streams of data reliably with high speed and low latency.

**Key Capabilities:**
- Real-time stream abstraction with Spouts and Bolts in Topologies.
- Guaranteed message processing semantics (at-least-once or Trident exactly-once).
- Fault-tolerant worker management with automatic task restarts.

[Explore full Apache Storm tool profile & getting started guide →](/tools/apache_storm/)

---

---

---

#### [Apache Ignite](https://ignite.apache.org)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/ignite)

A distributed in-memory database, caching layer, and computation platform designed to accelerate transactional and analytical workloads.

**Key Capabilities:**
- In-memory data grid and distributed cache with ANSI-99 SQL support.
- ACID-compliant distributed transactions across memory and disk tiers.
- Co-located distributed computing minimizing network serialization.

[Explore full Apache Ignite tool profile & getting started guide →](/tools/apache_ignite/)

---

---

---

#### [Apache CarbonData](https://carbondata.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/carbondata)

An indexed columnar data format for fast analytics on big data platforms, optimized for multi-dimensional point lookups and aggregations.

**Key Capabilities:**
- Multi-level indexing (min/max, inverted index, B-tree) for rapid point queries.
- Columnar storage with advanced encoding and compression.
- Integration with Spark, Presto, and Hive.

[Explore full Apache CarbonData tool profile & getting started guide →](/tools/apache_carbondata/)

---

### Serverless, Cloud Functions & Integration

---

---

#### [Apache Zeppelin](https://zeppelin.apache.org)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/zeppelin)

A web-based notebook that enables data-driven, interactive data analytics, visualization, and collaborative workflows across multiple backend engines.

**Key Capabilities:**
- Multi-language backend interpreter supporting Spark, SQL, Python, Scala, Shell, JDBC.
- Built-in data visualizations and pivot charts without front-end code.
- Dynamic forms allowing parameterized queries and interactive dashboarding.

[Explore full Apache Zeppelin tool profile & getting started guide →](/tools/apache_zeppelin/)

---

### Databases, Graph & Distributed Storage

---

---

#### [Apache StreamPipes](https://streampipes.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/streampipes)

A self-service Industrial IoT (IIoT) and streaming analytics platform designed to enable non-technical users to connect, analyze, and explore IoT data streams.

**Key Capabilities:**
- Drag-and-drop web pipeline editor for building stream workflows without coding.
- Pre-built library of pipeline elements (adapters, processors, sinks).
- Live data explorer and customizable dashboards for sensor monitoring.

[Explore full Apache StreamPipes tool profile & getting started guide →](/tools/apache_streampipes/)

---

---

---

#### [Apache OpenWhisk](https://openwhisk.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/openwhisk)

An open-source, distributed serverless cloud platform that executes code in response to events at any scale.

**Key Capabilities:**
- Event-driven architecture with Triggers, Rules, and Actions model.
- Polyglot containerized function execution across major languages.
- Sub-second auto-scaling from zero to thousands of concurrent invocations.

[Explore full Apache OpenWhisk tool profile & getting started guide →](/tools/apache_openwhisk/)

---

---

---

#### [Apache OpenServerless](https://openserverless.apache.org/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/apache/openserverless)

An open-source serverless platform built on Kubernetes and Apache OpenWhisk designed to simplify serverless computing across multi-cloud environments.

**Key Capabilities:**
- Turnkey deployment of serverless execution on any Kubernetes cluster.
- Integrated API gateway, cron scheduling, and web asset hosting.
- Polyglot runtime support (Node.js, Python, Java, Go, Rust, PHP).

[Explore full Apache OpenServerless tool profile & getting started guide →](/tools/apache_openserverless/)

---

---


---

## Part Four: On the Shoulders of Giants

Positioned lower in this catalog, these projects reflect cloud-provider-specific tools and evaluation suites from AWS and Azure. While valuable for teams locked into specific hyperscale platforms, they are less universally central to independent open-source cloud-native architectures.

#### [AWS Server Application Model (SAM)](https://aws.amazon.com/serverless/sam/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/aws/serverless-application-model)

An open-source framework and CLI for building, testing, and deploying serverless applications on AWS using declarative templates.

**Key Capabilities:**
- Shorthand syntax extending AWS CloudFormation for defining functions, APIs, and databases.
- Local emulation and testing of Lambda functions and API Gateway with Docker.
- Step-through debugging in local IDEs.

[Explore full AWS Server Application Model (SAM) tool profile & getting started guide →](</tools/aws_server_application_model_(sam)/>)

---

---

---

#### [Azure Functions](https://azure.microsoft.com/en-us/services/functions/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/Azure/azure-functions-host)

An event-driven serverless compute platform that helps developers develop more efficiently.

**Key Capabilities:**
- Serverless architecture
- Event-driven programming model
- Supports multiple programming languages

[Explore full Azure Functions tool profile & getting started guide →](/tools/azure_functions/)

---

---

---

#### [Agent Evaluation](https://awslabs.github.io/agent-evaluation/)

**Status:** `Non-cncf` | **Code:** [GitHub Repository](https://github.com/awslabs/agent-evaluation)

A generative AI-powered framework for testing virtual agents.

**Key Capabilities:**
- Built-in support for popular AWS services like Amazon Bedrock, Amazon Q Business, and Amazon SageMaker
- Orchestrate concurrent, multi-turn conversations with your agent while evaluating its responses
- Define hooks to perform additional tasks such as integration testing

[Explore full Agent Evaluation tool profile & getting started guide →](/tools/agent_evaluation/)

---


---

### Distributed Systems & Specialized Data Foundations


---

### What's Next in the Journey?

With Week 2 concluded, we have completed our 360-degree survey of **all 70 projects in Letter A**!
- From **Part 1**'s infrastructure behemoths ([Argo](/tools/argo/), [Atlantis](/tools/atlantis/), [Artifact Hub](/tools/artifact_hub/))
- To **Part 2**'s agent game changers ([Agent Substrate](/tools/agent_substrate/), [Agentgateway](/tools/agentgateway/), [ADK](/tools/agent_development_kit/), [A2A](/tools/agent2agent/)) and the expansive Apache ecosystem ([Spark](/tools/apache_spark/), [Flink](/tools/apache_flink/)).

Next week, we turn the page to **Letter B**, exploring cloud-native service meshes, eBPF telemetry, and developer portals like Backstage, BIRD, and Buildpacks. Stay tuned!
