from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
from view_data import ViewData
from flask_cors import CORS


app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)
CORS(app)
load_dotenv()

UPLOAD_FOLDER = 'flask_app/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['PORT'] = int(os.getenv('PORT', 5000))
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/table")
def table():
    return render_template("table.html")

@app.route("/api/data")
def api_data():
    view = ViewData()
    data_chunk = view.fetch_passenger_chunk(start, length, search, order_column, order_dir)
    total_count = view.get_passenger_count(search)

    # sample = {
    #     "item": "first rows",
    #     "number A": 123,
    #     "number B": 456,
    #     "info ": "statement"
    # }
    # return jsonify(sample)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)
        return f"File uploaded to {save_path}"


@app.route('/api/passenger-data')
def api_passenger_data():
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 50))
    search = request.args.get('search[value]', "").strip()

    order_column_index = int(request.args.get("order[0][column]", 0))
    order_dir = request.args.get("order[0][dir]", "asc")

    column_map = [
        "PassengerId", "Pclass", "Name", "Sex", "Age",
        "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked", "Survived"
    ]
    order_column = column_map[order_column_index]

    view = ViewData()
    data_chunk = view.fetch_passenger_chunk(start, length, search, order_column, order_dir)
    total_count = view.get_passenger_count(search)

    return jsonify({
        "draw": int(request.args.get("draw", 1)),
        "recordsTotal": total_count,
        "recordsFiltered": total_count,
        "data": data_chunk
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config['PORT'], debug=(app.config['FLASK_ENV'] == 'development'))
