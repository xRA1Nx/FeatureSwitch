from src.apps.main import application  # noqa
from logging import getLogger

import typer

from src.apps.user.managment_comands import user_management_app

logger = getLogger(__name__)

management_app = typer.Typer(help="Management commands")

management_app.add_typer(user_management_app, name="user")

if __name__ == "__main__":
    management_app()
