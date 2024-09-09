from fastapi import APIRouter

router = APIRouter(tags=["root"])


@router.get('/')
def index():
    return 'Hello!'
