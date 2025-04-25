from fastapi import APIRouter
from .design import DesignBaseController

router = APIRouter(prefix='/api')
router.include_router(DesignBaseController.create_router())
