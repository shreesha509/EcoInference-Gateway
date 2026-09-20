# EcoInference Gateway

> **Stopping AI's environmental footprint before the GPU spins up.**

EcoInference Gateway is a thermal-aware AI middleware prototype that identifies **semantically similar AI requests before unnecessary inference is performed**.

Instead of asking only:

> How can we make AI inference more efficient?

EcoInference asks:

> **Does this inference need to happen at all?**

---

## The Problem

AI applications can receive many requests that are different in wording but similar in meaning.

For example:

- `A futuristic city at sunset`
- `A futuristic city during sunset`
- `Create an image of a futuristic city during sunset`

A traditional exact-match cache may treat these as three different requests.

That can result in repeated computation even when a useful result may already exist.

At scale, unnecessary computation can contribute to:

- Higher compute usage
- Additional energy consumption
- Higher GPU utilization
- Additional cooling requirements
- Increased infrastructure cost

Most AI optimization approaches focus on making the **inference itself** more efficient.

EcoInference explores a different opportunity:

### Prevent unnecessary inference before it reaches the inference layer.

---

# The Gap

There are many techniques for optimizing AI inference:

- Model compression
- Quantization
- Hardware optimization
- Kernel optimization
- Inference acceleration
- Batching
- Smaller models

These approaches primarily ask:

> **How can we make required inference cheaper or faster?**

EcoInference focuses on an earlier decision:

> **Can we avoid performing the inference in the first place?**

This creates an optimization layer **before the inference workload begins**.

---

# Our Approach

EcoInference sits between an application and its AI inference layer.

For every incoming request, the gateway:

1. Converts the request into a semantic embedding.
2. Compares it with previously processed requests.
3. Calculates semantic similarity using cosine similarity.
4. Checks the similarity against a configurable threshold.
5. Reuses a cached result when the request is sufficiently similar.
6. Otherwise allows the request to continue through the inference path.
7. Estimates the potential energy and cooling-water impact.

### Core Decision

```text
                    Incoming AI Request
                            |
                            v
                  Semantic Embedding
                            |
                            v
                  Similarity Analysis
                            |
                     Threshold >= 0.92
                       /           \
                     HIT           MISS
                      |              |
                      v              v
                Reuse Result    Inference Path
                      |              |
                      +------+-------+
                             |
                             v
                          Response


hy Semantic Matching?

The important difference is that EcoInference does not depend only on exact string matching.

Our deployed prototype contains:

Cached prompt:
"A futuristic city at sunset"

A user can submit:

"A futuristic city during sunset"

The wording is different, but the semantic meaning is similar.

The prototype produces:

Similarity: 0.9897
Decision: CACHE HIT
GPU Compute: Bypassed

This demonstrates the core idea:

Reuse computation based on meaning, not just identical text.

Live Prototype
Semantic Cache HIT
Cached request
A futuristic city at sunset
New request
A futuristic city during sunset
Result
Similarity: 0.9897
Decision: CACHE HIT
GPU Compute: Bypassed

The cached asset is retrieved from Amazon S3 using a presigned URL.

Under the current prototype assumptions, the system estimates:

Energy avoided: 4200 J
Estimated cooling-water impact avoided: 2.1 mL
Semantic Cache MISS
New request
A red sports car driving through a mountain road
Result
Similarity: 0.1576
Decision: CACHE MISS
GPU Compute: Inference Path

The system does not reuse an unrelated cached result.

This is important because an environmental optimization should not sacrifice correctness.

How It Works
                    User / Application
                           |
                           v
                  +------------------+
                  |  API Gateway     |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |   AWS Lambda     |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  | Semantic Model   |
                  | MiniLM-L6-v2     |
                  +--------+---------+
                           |
                           v
                  +------------------+
                  | Cosine Similarity|
                  +--------+---------+
                           |
                    +------+------+
                    |             |
                   HIT           MISS
                    |             |
                    v             v
                S3 Result    Inference Path
                    |             |
                    +------+------+
                           |
                           v
                  +------------------+
                  | Impact Engine    |
                  +--------+---------+
                           |
                           v
                      Dashboard
AWS Architecture

EcoInference is deployed using AWS services.

AWS Service	Purpose
Amazon API Gateway	Exposes the inference gateway API
AWS Lambda	Runs the gateway and semantic matching logic
Amazon ECR	Stores the Lambda container image
Amazon S3	Stores cached inference assets
Amazon CloudWatch	Application and Lambda logging
AWS CloudFormation	Infrastructure deployment

The application and ML model are packaged into a Docker container and deployed to AWS Lambda.

Machine Learning

The semantic matching engine uses:

Sentence Transformers — all-MiniLM-L6-v2

The incoming prompt is converted into a vector representation.

EcoInference then calculates cosine similarity between the incoming request and cached requests.

Current prototype threshold:

0.92

Decision logic:

Similarity >= 0.92
        |
        v
   CACHE HIT
        |
        v
Reuse cached result
Similarity < 0.92
        |
        v
   CACHE MISS
        |
        v
Continue to inference path

The threshold is configurable and can be tuned according to the application's reuse and accuracy requirements.

Environmental Impact Estimation

The prototype includes an impact calculation engine to make the potential effect of avoided computation visible.

Current scenario assumptions:

GPU Power      = 350 W
Inference Time = 12 seconds
WUE            = 1.8 L/kWh

Energy calculation:

Energy = Power x Time

       = 350 W x 12 seconds

       = 4200 J

Equivalent energy:

4200 J ~= 0.001167 kWh

Using the configured WUE assumption:

0.001167 kWh x 1.8 L/kWh
~= 0.0021 L
~= 2.1 mL

Therefore, under the current prototype assumptions, bypassing one 12-second inference represents:

4200 J

of estimated avoided computation energy and approximately:

2.1 mL

of estimated cooling-water impact.

Measurement Boundary

These values are estimates based on configured assumptions.

They are not direct measurements of:

GPU power consumption
Datacenter electricity consumption
Physical cooling-water usage

A future production implementation would replace these assumptions with real infrastructure telemetry.

What We Built

The current working prototype includes:

Semantic prompt matching
all-MiniLM-L6-v2 embeddings
Cosine similarity
Configurable similarity threshold
Semantic cache HIT/MISS decisions
Cached asset retrieval from Amazon S3
Presigned S3 URLs
Energy impact estimation
Cooling-water impact estimation
FastAPI gateway
React dashboard
Dockerized deployment
AWS Lambda deployment
Amazon API Gateway integration
Amazon ECR container registry
CloudWatch logging
CloudFormation infrastructure deployment
Technology Stack
Backend
Python 3.11
FastAPI
Pydantic
Uvicorn
boto3
Machine Learning
Sentence Transformers
all-MiniLM-L6-v2
PyTorch
scikit-learn
NumPy
SciPy
Frontend
React
Vite
JavaScript
CSS
Infrastructure
Docker
AWS Lambda
Amazon API Gateway
Amazon ECR
Amazon S3
Amazon CloudWatch
AWS CloudFormation
Project Structure
EcoInference-Gateway/
|
+-- gateway/
|   +-- app.py
|   +-- cache.py
|   +-- impact.py
|   +-- s3_storage.py
|
+-- dashboard/
|   +-- src/
|       +-- App.jsx
|       +-- App.css
|
+-- data/
|   +-- sample_cache.json
|
+-- models/
|   +-- all-MiniLM-L6-v2/
|
+-- aws-deployment/
|   +-- template.yaml
|   +-- samconfig.toml
|
+-- lambda_handler.py
+-- Dockerfile
+-- requirements.txt
+-- README.md
Current Prototype Boundary

EcoInference is currently a working proof of concept.

The current prototype intentionally has a limited scope:

The semantic cache uses a small demonstration dataset.
The MISS path represents the downstream inference path but does not currently execute a production generative AI model.
Environmental values are estimates rather than direct datacenter measurements.
The current cache is not yet a distributed production-scale cache.
The similarity threshold is currently configured at 0.92.

These limitations define the boundary between the current proof of concept and a future production implementation.

Future Direction

The architecture can evolve toward a production-scale system with:

Real Inference Integration

Connect the MISS path to an actual inference provider or model-serving infrastructure.

Real Infrastructure Telemetry

Replace assumed GPU power and WUE values with measured infrastructure data.

Distributed Semantic Cache

Support large-scale applications with persistent, distributed cache storage.

Adaptive Thresholds

Tune semantic similarity thresholds based on application-specific accuracy and reuse requirements.

Model-Aware Impact Estimation

Estimate environmental impact across different models, hardware configurations, and inference workloads.

Why This Approach Matters

AI sustainability is often discussed in terms of making computation more efficient.

EcoInference explores another dimension:

Avoid computation that does not need to happen.

If an application already has a sufficiently similar result, the gateway can attempt to reuse it instead of sending another request through the inference pipeline.

The concept is simple:

              BEFORE

User -> Inference -> GPU -> Result


              ECOINFERENCE

User -> Semantic Check
             |
          +--+--+
          |     |
         HIT   MISS
          |     |
          v     v
        Reuse  Inference

The optimization therefore happens before inference, rather than only inside it.

Built on AWS

EcoInference was built and deployed using AWS infrastructure.

The project demonstrates how AWS serverless services can be combined with an ML-powered middleware layer to create an AI efficiency gateway.

AWS Components
Amazon API Gateway
AWS Lambda
Amazon ECR
Amazon S3
Amazon CloudWatch
AWS CloudFormation
AWS First Commit Hackathon

Built for the AWS First Commit Hackathon.

Project

EcoInference Gateway

Core Idea

Semantic interception of AI requests to identify opportunities to reuse existing computation before new inference occurs.

Tagline

Stopping AI's environmental footprint before the GPU spins up.

Author

Shreesha Kumar P

Built as an independent project for the AWS First Commit Hackathon.

The Idea in One Sentence

EcoInference Gateway asks one question before every inference request: Do we really need to compute this again?


**Use this exact version.** It avoids the weird formatting/path issue from the previo
