"""Views for create virtual rooms for conferences."""

from __future__ import absolute_import, print_function

import json
import os
import secrets

from bigbluebutton_api_python import BigBlueButton
from bigbluebutton_api_python.exception.bbbexception import BBBException
from dotenv import load_dotenv
from flask import Blueprint, abort, current_app, redirect, render_template, \
    request, url_for
from flask_babelex import gettext as _
from flask_login import login_required
from flask_menu import register_menu
from flask_security import current_user, roles_accepted

from .forms import RoomForm

# Loading dotenv
load_dotenv()

#: Big Blue Button server secret and url
BBB_SERVER_SECRET = os.getenv('BBB_SERVER_SECRET')
BBB_SERVER_URL = os.getenv('BBB_SERVER_URL')

# define a new Flask Blueprint that is register
# under the url path /conference
blueprint = Blueprint(
    'conference',
    __name__,
    url_prefix='/conference',
    template_folder='templates',
    static_folder='static',
)


@blueprint.route('/create_room', methods=('GET', 'POST'))
@register_menu(blueprint, 'settings.createroom',
               _('%(icon)s Crea videoconferenza',
                 icon='<i class="fa fa-video-camera fa-fw"></i>'
                 ),
               order=7,
               visible_when=lambda: bool(current_user.has_role('admin') or
                                         current_user.has_role('roomCreator')
                                         ) is not False
               )
def create_room():
    """View to let user create a virtual room."""
    if current_user.is_authenticated:
        if ('admin' in current_user.roles) or \
           ('roomCreator' in current_user.roles):
            form = RoomForm()

            # if the form is submitted and valid
            if form.validate_on_submit():
                roomId = form.roomId.data.strip()
                password = form.password.data
                username = form.username.data.strip().replace(" ", "_")
                modPassword = secrets.token_hex(16)

                b = BigBlueButton(BBB_SERVER_URL, BBB_SERVER_SECRET)

                # params
                dict = {
                    'name': username,
                    'attendeePW': password,
                    'moderatorPW': modPassword,
                    'record': True
                }

                if os.getenv('CURRENT_HOST'):
                    dict['logoutURL'] = os.getenv('CURRENT_HOST')

                try:
                    # use create meeting
                    b.create_meeting(roomId, params=dict)
                except BBBException:
                    return render_template(
                        'conference/create_conference.html',
                        form=form, existingId=True)

                # get room url
                room_url = b.get_join_meeting_url(username,
                                                  roomId,
                                                  modPassword)

                # redirect to the created room
                return redirect(room_url)

            return render_template('conference/create_conference.html',
                                   form=form)
        else:
            return render_template('conference/info_create.html')
    else:
        return render_template('conference/info_create.html')


@blueprint.route('/join_room', methods=('GET', 'POST'))
def join_room():
    """View to let user join a virtual room."""
    form = RoomForm()

    # if the form is submitted and valid
    if form.validate_on_submit():
        roomId = form.roomId.data.strip()
        password = form.password.data
        username = form.username.data.strip().replace(" ", "_")

        b = BigBlueButton(BBB_SERVER_URL, BBB_SERVER_SECRET)

        r = b.is_meeting_running(roomId)

        active_room = json.loads(r['xml']['running'].lower())

        # check if the meeting exists
        if not active_room:
            return render_template('conference/join_conference.html',
                                   form=form, existingId=True)
        else:
            # get room url
            room_url = b.get_join_meeting_url(username, roomId, password)

            # redirect to the room
            return redirect(room_url)

    return render_template('conference/join_conference.html', form=form)
