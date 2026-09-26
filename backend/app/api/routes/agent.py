from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.db.session import get_db

from app.schemas.agent import (
    AgentQueryRequest,
    AgentQueryResponse,
)

from app.services.agent.agent import (
    run_agent,
)

from app.services.ai.base import (
    AIProviderError,
)

from app.services.carbon.base import (
    CarbonProviderError,
)


router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"],
)


@router.post(
    "/query",
    response_model=AgentQueryResponse,
)
async def agent_query(
    request: AgentQueryRequest,
    db: AsyncSession = Depends(get_db),
):

    try:
        return await run_agent(
            request,
            db,
        )

    except AIProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "AI provider is currently "
                "unavailable."
            ),
        ) from exc

    except CarbonProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Carbon provider is currently "
                "unavailable."
            ),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc