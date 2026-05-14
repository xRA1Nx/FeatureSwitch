from __future__ import annotations

import asyncio

import typer

from src.apps.user.logic.facades.user import admin_user__create
from src.utils.strings import ensure_valid_email


user_management_app = typer.Typer(help="User management commands")


@user_management_app.command(name="create-admin")
def create_admin(
    email: str = typer.Option(None, "--email", "-e"),
    password: str = typer.Option(None, "--password", "-p", hide_input=True),
) -> None:
    """Create a new admin user"""
    if email is None:
        email = typer.prompt("Email")
    is_valid_email = ensure_valid_email(email=email, should_raise_exception=False)
    if not is_valid_email:
        typer.secho("❌ Email is not valid!", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if password is None:
        password = typer.prompt("Password", hide_input=True)
        confirm = typer.prompt("Confirm password", hide_input=True)
        if password != confirm:
            typer.secho("❌ Passwords do not match!", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    typer.secho(f"Creating admin user: {email}...", fg=typer.colors.CYAN)
    asyncio.run(admin_user__create(email=email, password=password))
    typer.secho(f"✅ Admin user '{email}' created successfully!", fg=typer.colors.GREEN)
