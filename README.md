# EcoInference Gateway

**Semantic inference interception for reducing redundant AI computation.**

EcoInference Gateway is an AWS-deployed middleware layer that checks whether an incoming AI request is semantically similar to a previously processed request before it reaches the inference layer.

The goal is simple: **avoid computation when an equivalent result can already be reused.**

---

## The Problem

Most caching relies on exact request matching.

```text
"A futuristic city at sunset"
"A futuristic city during sunset"

Different strings. Potentially the same intent.

If both requests reach inference independently, the second request may perform computation that could have been avoided.

EcoInference moves the optimization point before inference.

How It Works
Request
   │
   ▼
API Gateway
   │
   ▼
Lambda
   │
   ▼
Semantic Embedding
   │
   ▼
Cosine Similarity
   │
   ├── ≥ 0.92 ──► Cache HIT ──► Reuse S3 Result
   │
   └── < 0.92 ──► Cache MISS ─► Inference Path

The prototype uses all-MiniLM-L6-v2 to generate embeddings and cosine similarity to determine whether a request is sufficiently similar to a cached request.

Example

Cached

A futuristic city at sunset

Incoming

A futuristic city during sunset

Result

Similarity     0.9897
Decision       CACHE HIT
Compute        Bypassed

An unrelated request:

A red sports car driving through a mountain road

Similarity     0.1576
Decision       CACHE MISS
Compute        Inference path
AWS Architecture
                    ┌─────────────────┐
                    │ React Dashboard │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  API Gateway    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  AWS Lambda     │
                    │ Semantic Cache  │
                    └───────┬─────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                   HIT             MISS
                    │               │
                    ▼               ▼
              Amazon S3       Inference Path
                    │               │
                    └───────┬───────┘
                            ▼
                     Impact Engine

AWS: Lambda · API Gateway · ECR · S3 · CloudWatch · CloudFormation

The ML model is packaged into the Lambda container and deployed through Amazon ECR.

Why It Is Different

The usual question is:

How do we make inference more efficient?

EcoInference asks:

Does this inference need to happen at all?

This places the optimization decision before the inference workload, using semantic similarity rather than exact-string matching.

Impact Estimation

The prototype estimates the potential impact of avoided computation using configurable assumptions:

Parameter	Prototype value
GPU power	350 W
Inference time	12 s
WUE	1.8 L/kWh

A 12-second assumed inference corresponds to:

4200 J ≈ 0.001167 kWh ≈ 2.1 mL estimated water impact

These are scenario estimates, not direct measurements of GPU power or datacenter water consumption.

Current Prototype
Semantic request matching
Configurable similarity threshold (0.92)
Cache HIT / MISS routing
S3 cached-result retrieval
FastAPI gateway
React dashboard
Containerized Lambda deployment
Live API Gateway endpoint
CloudWatch logging
CloudFormation infrastructure

The current MISS path represents the downstream inference path; it does not yet execute a production generative AI model.

Stack

ML: Sentence Transformers · PyTorch · scikit-learn
Backend: Python · FastAPI
Frontend: React · Vite
AWS: Lambda · API Gateway · ECR · S3 · CloudWatch · CloudFormation
Deployment: Docker

AWS First Commit

EcoInference Gateway

Don't cool computation you didn't need to perform.

Built by Shreesha Kumar P.


This reads much more like a **real technical project README** than a generated marketing page. The judge can understand the novelty in three places immediately: **The Problem → How It Works → Why It Is Different.**
