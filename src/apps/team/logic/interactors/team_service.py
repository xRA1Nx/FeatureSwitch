from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.common.exceptions import BusinessLogicException
from src.apps.team.logic.selectors.team_service import team_service__find_by_name
from src.apps.team.models import TeamService


async def team_service__find_by_name_or_raise(
    *, name: str, session: AsyncSession | None = None
) -> TeamService:
    team_service = await team_service__find_by_name(name=name, session=session)
    if team_service is None:
        raise BusinessLogicException(f'Не существует объекта TeamService с названием = {name}')
    return team_service
