from fastapi import APIRouter, Depends
from app.api.deps import get_metrics

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def view_metrics(metrics = Depends(get_metrics)):
    return metrics.report()