"""
This script invokes app instance.

This is the file that is invoked to start up a development server.
It gets a copy of the app from app package and runs it.
"""

from app import create_app, db
from app.models import Face

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Shell content variables.

    This functions return db and Face variable for using in flask shell.
    Returns:
        db: database instance.
        Face: Face model class.
    """
    return {'db': db, 'Face': Face}
