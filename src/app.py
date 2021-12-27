import api
import memes
import functools
import flask
from flask import Flask, request, send_file

app = Flask(__name__)
app.register_blueprint(api.api)
app.register_blueprint(memes.blueprint)

navbar_elements = {
    "left": {
        #"About Me": "about",
        #"Projects": "projects",
        #"Resume": "resume",
        #"Meme Generator": "memes"
    },
    "right": {
        #"Contact": "contact"
    }
}

def navbar(route="", name=None, position="left"):

    print(route, name, position)
    navbar_elements[position][name if name is not None else func.__name__] = route

    return app.route(route)

@app.context_processor
def inject_navbar():
    return dict(navbar=navbar_elements)

@app.route("/")
def starting_url():
    return flask.redirect(flask.url_for("about"))

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@navbar(route="/about", name="About")
def about():
    print(navbar_elements)
    return flask.render_template('about.html')

@navbar(route="/projects", name="Projects")
def projects():
    return flask.render_template('projects.html')


@navbar(route="/resume", name="Resume")
def resume():
    return flask.render_template('resume.html')


@navbar(route="/contact", name="Contact", position="right")
def contact():
    return flask.render_template('contact.html')


            
