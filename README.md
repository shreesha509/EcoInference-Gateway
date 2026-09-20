# EcoInference Gateway

### Stopping unnecessary AI computation before the GPU spins up.

EcoInference Gateway is an **AWS-deployed semantic inference gateway** that checks whether a new AI request is sufficiently similar to a previously processed request **before sending it to inference**.

The key idea:

> **Don't optimize computation you never needed to perform.**

---

## The Gap

Most AI optimization happens **inside inference** — faster models, quantization, batching, hardware optimization, etc.

EcoInference targets an earlier layer:

**Can we prevent redundant inference from happening at all?**

Traditional caching often depends on exact request matching:

```text
"futuristic city at sunset"
        ≠
"futuristic city during sunset"

EcoInference compares meaning instead of strings.

How It Works
AI Request
    ↓
API Gateway
    ↓
AWS Lambda
    ↓
Semantic Embedding
    ↓
Cosine Similarity
    ↓
   ┌───────────────┐
   │ Similarity ≥  │
   │     0.92      │
   └───────┬───────┘
       ┌───┴───┐
      HIT     MISS
       ↓        ↓
    Reuse     Inference
    Result     Path
       ↓        ↓
       └───┬────┘
           ↓
      Impact Estimate
           ↓
        Response

The prototype uses all-MiniLM-L6-v2 for semantic embeddings and cosine similarity for matching.

Working Demonstration
Semantic HIT

Cached:

A futuristic city at sunset

Incoming:

A futuristic city during sunset

Result:

Similarity:       0.9897
Decision:         CACHE HIT
GPU computation:  Bypassed
Energy avoided:   4200 J*
Water avoided:    2.1 mL*
Semantic MISS

Incoming:

A red sports car driving through a mountain road

Result:

Similarity:       0.1576
Decision:         CACHE MISS
Inference:        Required

This demonstrates that the gateway can distinguish semantically reusable requests from unrelated requests.

AWS Architecture
React Dashboard
       ↓
Amazon API Gateway
       ↓
AWS Lambda
       ↓
Semantic Cache
   ↙           ↘
 HIT           MISS
  ↓             ↓
S3 Result   Inference Path
   ↘           ↙
    Impact Engine
         ↓
     Dashboard
AWS Services
Amazon API Gateway — inference API
AWS Lambda — semantic gateway
Amazon ECR — containerized ML runtime
Amazon S3 — cached assets
Amazon CloudWatch — logging
AWS CloudFormation — deployment

The ML model is packaged directly into the Lambda container rather than downloaded at runtime.

Environmental Impact

The prototype makes potential impact visible using configurable assumptions:

GPU power       = 350 W
Inference time  = 12 s
WUE             = 1.8 L/kWh

A 12-second assumed inference corresponds to:

4200 J
≈ 0.001167 kWh
≈ 2.1 mL estimated water impact

*These are scenario estimates, not direct measurements of GPU power or datacenter water consumption.

The architecture is designed so these assumptions can later be replaced with real infrastructure telemetry.

What Makes It Different
1. Optimization before inference

Instead of making inference cheaper, EcoInference first asks whether inference is necessary.

2. Semantic reuse

It can identify similar requests even when the wording changes.

3. Sustainability-aware middleware

The gateway exposes the estimated energy and cooling-water impact of the decision.

4. AWS-native deployment

The prototype is actually deployed using AWS serverless infrastructure rather than being only a local simulation.

Current Prototype

Built and deployed:

Semantic cache
all-MiniLM-L6-v2
Cosine similarity
Configurable 0.92 threshold
HIT/MISS routing
S3 cached asset retrieval
FastAPI gateway
React dashboard
Dockerized Lambda deployment
API Gateway
ECR
CloudWatch
CloudFormation
Current boundary

The MISS path currently represents the downstream inference path but does not execute a production generative AI model. Environmental values are estimates based on configurable assumptions.

Tech Stack

AI/ML: Sentence Transformers, PyTorch, scikit-learn

Backend: Python, FastAPI

Frontend: React, Vite

Cloud: AWS Lambda, API Gateway, ECR, S3, CloudWatch, CloudFormation

Deployment: Docker

Built for AWS First Commit

Project: EcoInference Gateway

Core idea:

Before spending compute, determine whether the useful computation already exists.

Tagline:

Stopping AI's environmental footprint before the GPU spins up.

Author

Shreesha Kumar P

Built for the AWS First Commit Hackathon.


### Why I prefer this version

A judge can scan the README and immediately get:

**Problem → Gap → Novel approach → Working evidence → AWS architecture → Impact → Limitations.**

And importantly, it doesn't claim that you have built a full production AI inference platform when you haven't. That makes the project technically credible while clearly showing what is unique about it.
