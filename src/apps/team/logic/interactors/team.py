from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.common.exceptions import BusinessLogicException
from src.apps.team.logic.selectors.team import team__find_by_name
from src.apps.team.models import Team


async def team__find_by_name_or_raise(
    *, name: str, session: AsyncSession | None = None
) -> Team:
    team = await team__find_by_name(name=name, session=session)
    if team is None:
        raise BusinessLogicException(f'Не существует объекта Team с названием = {name}')
    return team