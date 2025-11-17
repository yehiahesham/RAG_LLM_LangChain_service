from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_user_dep, get_pipeline, get_retry_policy, get_metrics
from app.schemas.extract import ExtractRequest, ExtractResult, AsyncTaskResponse, TaskStatusResponse
from app.workers.celery_app import run_extraction_task

router = APIRouter(tags=["extract"])


@router.post("/extract", response_model=ExtractResult)
async def extract(
    req: ExtractRequest,
    user = Depends(get_current_user_dep),
    pipeline = Depends(get_pipeline),
    retry = Depends(get_retry_policy),
):
    try:
        result = await pipeline.run(query=req.query, fields=req.fields, max_retries=retry.max_retries)
        return ExtractResult(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.post("/extract/async", response_model=AsyncTaskResponse)
async def extract_async(
    req: ExtractRequest,
    user = Depends(get_current_user_dep),
):
    task = run_extraction_task.delay(req.model_dump())
    return AsyncTaskResponse(task_id=str(task.id))


@router.get("/extract/status/{task_id}", response_model=TaskStatusResponse)
async def extract_status(task_id: str):
    from app.workers.celery_app import run_extraction_task
    async_result = run_extraction_task.AsyncResult(task_id)
    status_str = async_result.status
    result = async_result.result if async_result.ready() else None
    return TaskStatusResponse(task_id=task_id, status=status_str, result=result)