"""
Some little utility functions to help get set up. These will likely be replaced
by calls to the existing backend.
"""

from eui.db import get_db

def get_resources():
    """Get the set of resources"""

    db = get_db()
    return db.execute("SELECT id, name, effort FROM resource").fetchall()