from fastapi import APIRouter, BackgroundTasks, Depends, Response, File, UploadFile
from pydantic import BaseModel
from typing import List
from quiz_bot_service import travelbot_service
from auth.auth_models import AuthenticatedUser
from auth.auth_middleware import auth_middleware
from models.quiz_models import QuizSubmission
from utils.commons import to_json_response

travelbot_router = APIRouter(prefix="/api/v1/travelbot", tags=["travelbot"])


class GenerateQuizRequest(BaseModel):
    quiz_subject: str
    no_of_questions: int


@travelbot_router.post("/quiz-bank")
async def create_quiz_bank(
    file: UploadFile = File(...),
    current_user: AuthenticatedUser = Depends(auth_middleware.require_admin()),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Upload a PDF file to create a quiz bank.
    The PDF will be saved in the inbound folder and processed asynchronously.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        from models.api_responses import ErrorResponse
        from models.status_code import sc
        return to_json_response(ErrorResponse(
            error="Invalid file type. Only PDF files are allowed.",
            status_code=sc.VALIDATION_ERROR
        ))
    
    # Read file content
    pdf_content = await file.read()
    
    # Upload PDF and initiate quiz bank creation
    result = await travelbot_service.upload_pdf(current_user.email,file.filename, pdf_content, background_tasks)
    return to_json_response(result)


@travelbot_router.get("/quiz-bank/status/{job_id}")
async def get_quiz_bank_status(job_id: str):
    result = await travelbot_service.get_job_status(job_id)
    return to_json_response(result)


@travelbot_router.get("/subjects")
async def get_subjects():
    result = await travelbot_service.get_subjects()
    return to_json_response(result)


@travelbot_router.post("/generate")
async def generate_quiz(request: GenerateQuizRequest,current_user: AuthenticatedUser = Depends(auth_middleware.get_current_user)):
    result = await travelbot_service.generate_quiz(
        request.quiz_subject,
        request.no_of_questions,
    )
    return to_json_response(result)


@travelbot_router.post("/submit")
async def submit_quiz(submission: List[QuizSubmission],current_user: AuthenticatedUser = Depends(auth_middleware.get_current_user)):
    result = await travelbot_service.submit_quiz(submission)
    return to_json_response(result)


@travelbot_router.get("/quiz-bank/download")
async def download_question_bank(
    subject: str,
    current_user: AuthenticatedUser = Depends(auth_middleware.require_admin()),
):
    csv_bytes = await travelbot_service.download_question_bank(subject)
    filename = f"{subject}_question_bank.csv" if subject else "question_bank.csv"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return Response(content=csv_bytes, media_type="text/csv", headers=headers)

@travelbot_router.get("/quiz-bank/jobs")
async def get_all_jobs(current_user: AuthenticatedUser = Depends(auth_middleware.require_admin())):
  result = await travelbot_service.get_all_jobs()
  return to_json_response(result)