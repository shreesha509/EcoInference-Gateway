from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from gateway.cache import find_similar_prompt, save_to_cache
from gateway.impact import calculate_impact, estimate_inference_time
from gateway.s3_storage import generate_presigned_url


app = FastAPI(
    title="EcoInference Gateway",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


STANDARD_INFERENCE_TIME_SECONDS = 15.0


class InferenceRequest(BaseModel):
    prompt: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "EcoInference Gateway",
        "version": "0.1.0",
    }


@app.post("/v1/inference/generate")
def generate(request: InferenceRequest):

    cache_result = find_similar_prompt(request.prompt)

    if cache_result["cache_hit"]:

        impact = calculate_impact(0)

        standard_impact = calculate_impact(
            STANDARD_INFERENCE_TIME_SECONDS
        )

        asset_url = generate_presigned_url(
            cache_result["asset"]
        )

        return {
            "status": "success",
            "cache_hit": True,
            "similarity": cache_result["similarity"],
            "matched_prompt": cache_result["matched_prompt"],
            "asset": cache_result["asset"],
            "asset_url": asset_url,
            "gpu_compute_bypassed": True,
            "impact": impact,
            "savings": {
                "energy_saved_joules": standard_impact[
                    "energy_joules"
                ],
                "energy_saved_kwh": standard_impact[
                    "energy_kwh"
                ],
                "water_saved_ml": standard_impact[
                    "water_ml"
                ],
                "co2_saved_grams": standard_impact[
                    "co2_grams"
                ],
            },
        }

    inference_time = estimate_inference_time()

    impact = calculate_impact(inference_time)

    save_to_cache(request.prompt)

    return {
        "status": "success",
        "cache_hit": False,
        "similarity": cache_result["similarity"],
        "matched_prompt": None,
        "asset": None,
        "gpu_compute_bypassed": False,
        "impact": impact,
        "savings": {
            "energy_saved_joules": 0.0,
            "water_saved_ml": 0.0,
        },
    }