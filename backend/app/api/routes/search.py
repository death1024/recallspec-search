from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional
import shutil
import os
from ..services.identity_spec import IdentitySpecEngine
from ..services.retrieval import RetrievalEngine
from ..services.match_judge import MatchJudge
from ..services.resolution_spec import ResolutionSpecEngine
from ..services.ocr import OCREngine
from ..models.specs import ProductIdentitySpec, RecallResolutionSpec

router = APIRouter(prefix="/api/v1", tags=["search"])

class SearchRequest(BaseModel):
    query: Optional[str] = None
    fields: Optional[dict] = None

class SearchResponse(BaseModel):
    identity_spec: ProductIdentitySpec
    resolution_spec: RecallResolutionSpec

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Main search endpoint: query -> identity spec -> recall match -> resolution"""

    # Step 1: Parse input into identity spec
    identity_engine = IdentitySpecEngine()
    identity_spec = identity_engine.parse_text(request.query or "", request.fields)

    # Step 2: Search for recalls
    retrieval_engine = RetrievalEngine()
    candidates = await retrieval_engine.search(identity_spec)

    # Step 3: Score and judge matches
    match_judge = MatchJudge()
    scored_matches = match_judge.judge_matches(identity_spec, candidates)

    # Step 4: Generate resolution spec with action card
    resolution_engine = ResolutionSpecEngine()
    resolution_spec = resolution_engine.generate_resolution(identity_spec, scored_matches)

    return SearchResponse(
        identity_spec=identity_spec,
        resolution_spec=resolution_spec
    )

@router.post("/search/image", response_model=SearchResponse)
async def search_by_image(image: UploadFile = File(...), query: Optional[str] = Form(None)):
    """Search with image upload - extracts fields via OCR"""

    # Save uploaded image temporarily
    temp_path = f"/tmp/{image.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Extract fields from image
    ocr_engine = OCREngine()
    ocr_fields = ocr_engine.extract_from_image(temp_path)

    # Clean up temp file
    os.remove(temp_path)

    # Combine OCR fields with query text
    identity_engine = IdentitySpecEngine()
    identity_spec = identity_engine.parse_text(query or ocr_fields.get("raw_text", ""), ocr_fields)

    # Continue with normal search flow
    retrieval_engine = RetrievalEngine()
    candidates = await retrieval_engine.search(identity_spec)

    match_judge = MatchJudge()
    scored_matches = match_judge.judge_matches(identity_spec, candidates)

    resolution_engine = ResolutionSpecEngine()
    resolution_spec = resolution_engine.generate_resolution(identity_spec, scored_matches)

    return SearchResponse(
        identity_spec=identity_spec,
        resolution_spec=resolution_spec
    )
