import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@click.option(
    "--with-test-data/--no-test-data",
    is_flag=True,
    help="include some initial data for testing",
)
@with_appcontext
def init_db_command(with_test_data):
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

    if with_test_data:
        db = get_db()
        db.executemany(
            "INSERT INTO resource (name, effort) VALUES (?, ?)",
            [("horses", 0.3), ("iron", 0.4), ("wood", 0.2),],
        )
        db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (
                "andrew",
                "pbkdf2:sha256:150000$BmVNurOx$b8032d1c4f2f439173f75f861d634b5c88eaa992202d802ce84d5bf4aee8e986",
            ),
        )
        db.commit()
        click.echo("Inserted test data.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
