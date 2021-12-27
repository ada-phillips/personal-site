import flask
from flask import Blueprint, request, send_file
import api

blueprint = Blueprint('memes', __name__, url_prefix='/projects/memes')


@blueprint.context_processor
def inject_memes():
    return dict(memes=api.meme_data)

@blueprint.route("")
def memes():
    if request.method == "POST":
        pass
        # generate meme, reload page with meme on screen 
    return flask.render_template('memes.html')
    
@blueprint.route("/<meme_format>", methods=('GET', 'POST'))
def meme_form(meme_format):
    if meme_format not in api.meme_data:
        return flask.redirect(flask.url_for("memes.memes"))
    
    meme_url = flask.url_for('api.meme_gen', meme_format=meme_format)
    if request.method == "POST":
        meme_url += f"?{'&'.join([field+'='+value for field,value in request.form.items()])}"
    else:
        meme_url += f"?{'&'.join([field+'='+data.get('placeholder', 'Field '+field) for field,data in api.meme_data[meme_format]['fields'].items()])}"
    return flask.render_template(
        'memeform.html', 
        meme_format=meme_format, 
        meme_data=api.meme_data[meme_format],
        meme_url=meme_url
    )