from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from eui.auth import login_required
from eui.db import get_db
from eui.util import get_resources

bp = Blueprint('builder', __name__)

@bp.route('/')
def index():
    db = get_db()
    inventory = db.execute(
        'SELECT u.username, r.name, r.effort, i.obtained'
        ' FROM inventory i JOIN user u ON i.owner_id = u.id'
        ' JOIN resource r ON i.resource_id = r.id'
        ' ORDER BY obtained DESC'
    ).fetchall()
    return render_template('builder/index.html', inventory=inventory)


@bp.route('/obtain', methods=('GET', 'POST'))
@login_required
def obtain():
    if request.method == 'POST':
        resource_id = request.form['resource_id']
        error = None

        if not resource_id:
            error = 'No resource selected.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO inventory (resource_id, owner_id)'
                ' VALUES (?, ?)',
                (resource_id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('builder.index'))

    return render_template('builder/obtain.html', resources=get_resources())