from __future__ import annotations
'\nCommand-line interface for AutoCare data management.\n\nThis module provides the main CLI for AutoCare data management,\nincluding import, export, and database operations.\n'
import sys
import typer
from typing import List, Optional
from app.domains.autocare.commands.import_autocare import import_autocare
app = typer.Typer(help='Manage AutoCare standard data (VCdb, PCdb, PAdb, Qdb)')
app.command(name='import')(import_autocare)
@app.callback()
def callback(verbose: bool=typer.Option(False, '--verbose', '-v', help='Print verbose output'), version: bool=typer.Option(False, '--version', help='Print version and exit')) -> None:
    if version:
        typer.echo('AutoCare CLI v0.1.0')
        raise typer.Exit()
def main() -> None:
    try:
        print('=' * 80)
        print(' AUTOCARE DATA MANAGEMENT TOOL ')
        print('=' * 80)
        app()
    except Exception as e:
        print(f'ERROR: {str(e)}')
        sys.exit(1)
if __name__ == '__main__':
    main()