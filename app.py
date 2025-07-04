from flask import Flask
from flask import render_template
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(dashboard_bp)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
