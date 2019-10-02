"""Data related commands to use on the command-line."""

import os

import click
from flask import current_app
from flask.cli import with_appcontext
from invenio_db import db
from invenio_files_rest.models import Location


def load_locations(force=False):
    """
    Load default file store and archive location.
    Lifted from https://github.com/zenodo/zenodo
    """
    # NOTE: os.path.join returns its 2nd argument if that argument is an
    #       absolute path which is what we want
    files_location = os.path.join(
        current_app.instance_path,
        current_app.config['FIXTURES_FILES_LOCATION']
    )
    archive_location = os.path.join(
        current_app.instance_path,
        current_app.config['FIXTURES_ARCHIVE_LOCATION']
    )

    try:
        locations = []
        uris = [
            ('default', True, files_location),
            ('archive', False, archive_location)
        ]
        for name, default, uri in uris:
            if uri.startswith('/') and not os.path.exists(uri):
                os.makedirs(uri)
            if not Location.query.filter_by(name=name).first():
                loc = Location(name=name, uri=uri, default=default)
                db.session.add(loc)
                locations.append(loc)

        db.session.commit()
        return locations
    except Exception:
        db.session.rollback()
        raise


@click.group()
def locations():
    """Deposit location commands.
    Usage on the command line becomes:
        menrva locations <command>
    """
    pass


@locations.command('setup_storage')
@with_appcontext
def load_locations_cli():
    """
    Sets up where files are stored or archived.
    Lifted from https://github.com/zenodo/zenodo
    """
    locations = load_locations()
    click.secho(
        'Created location(s): {0}'.format([loc.uri for loc in locations]),
        fg='green'
    )
