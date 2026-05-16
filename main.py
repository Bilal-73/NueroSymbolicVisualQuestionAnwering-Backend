from flask import Flask
from Routes.nlproutes import nlp_routes
from Routes.ContactPics import contact_routes
from Routes.Blind_Assistant import blind_assistant_bp
from Routes.BlindHistory import blind_routes
from Routes.objectroutes import object_routes
from Routes.answer_routes import answer_routes
from Routes.DirectoryRoutes import direct_routes
from flask_cors import CORS
from Routes.emotionroute import emotion_routes
from Routes.AudioRoutes import audioRoutes

app = Flask(__name__)
CORS(app)

app.register_blueprint(nlp_routes, url_prefix="/nlp")
app.register_blueprint(contact_routes, url_prefix="/contacts")
app.register_blueprint(blind_assistant_bp, url_prefix="/users")
app.register_blueprint(blind_routes, url_prefix="/history")
app.register_blueprint(object_routes, url_prefix="/images")
app.register_blueprint(answer_routes, url_prefix="/answers")
app.register_blueprint(direct_routes,url_prefix="/static")
app.register_blueprint(emotion_routes, url_prefix="/emotion")
app.register_blueprint(audioRoutes, url_prefix="/audio")

@app.route('/')
def home():
    return "API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
