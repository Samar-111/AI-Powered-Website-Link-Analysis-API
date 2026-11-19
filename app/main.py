from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.config import settings
from app.schemas import LinkAnalysisRequest, LinkAnalysisResponse, ErrorResponse
from app.services.analysis_service import analysis_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="AI-Powered Website Link Analysis API",
    description="Enterprise API that analyzes website URLs using LLMs to extract competitor insights, target search queries, SEO strategies, core services, and target audiences.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            success=False,
            error="Validation or Processing Error",
            detail=str(exc)
        ).model_dump()
    )

@app.get("/", tags=["General"])
async def root():
    return {
        "service": "AI-Powered Website Link Analysis API",
        "version": "1.0.0",
        "status": "operational",
        "docs_url": "/docs",
        "endpoints": {
            "link_analysis": "POST /link-analysis",
            "health": "GET /health"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "model": settings.GEMINI_MODEL,
        "api_configured": bool(settings.GEMINI_API_KEY)
    }

@app.post(
    "/link-analysis",
    response_model=LinkAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid URL or SSRF block"},
        500: {"model": ErrorResponse, "description": "LLM or scraping internal error"},
    },
    tags=["Analysis"]
)
async def analyze_link(payload: LinkAnalysisRequest):
    try:
        result = await analysis_service.run_analysis(payload.url)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during link analysis: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
