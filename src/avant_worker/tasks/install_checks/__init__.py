"""Tarefas da verificação de instalação."""

from avant_worker.tasks.install_checks.install_check_tasks import (
    check_install,
    check_site_installs,
    daily_install_checks,
)

__all__ = ["check_install", "check_site_installs", "daily_install_checks"]
