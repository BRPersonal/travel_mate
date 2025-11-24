from fastapi import APIRouter, BackgroundTasks, Depends, Response, File, UploadFile
from pydantic import BaseModel
from typing import List
from datetime import date
from models.travel_models import TravelRequest
from travel_bot_service import travelbot_service
from auth.auth_models import AuthenticatedUser
from auth.auth_middleware import auth_middleware
from utils.commons import to_json_response

travelbot_router = APIRouter(prefix="/api/v1/travelbot", tags=["travelbot"])

@travelbot_router.post("/plan")
async def generate_travel_plan(
    request: TravelRequest,
    current_user: AuthenticatedUser = Depends(auth_middleware.get_current_user)):

    result = await travelbot_service.generate_travel_plan(current_user.email,request)
    return to_json_response(result)

@travelbot_router.get("/plan/download")
async def download_travel_plan(
    start_date: date,
    current_user: AuthenticatedUser = Depends(auth_middleware.get_current_user),
):
    pdf_bytes = await travelbot_service.download_travel_plan(current_user.email, start_date)
    filename = f"{current_user.firstName}-travelPlan.pdf"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)

@travelbot_router.get("/plan/all")
async def get_all_travel_plans(current_user: AuthenticatedUser = Depends(auth_middleware.require_admin())):
  result = await travelbot_service.get_all_travel_plans()
  return to_json_response(result)