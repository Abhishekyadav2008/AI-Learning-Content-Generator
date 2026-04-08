import uuid
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET","POST"])
def create():
    myid = uuid.uuid1()

    if request.method == "POST":
        rec_id = str(uuid.uuid4())
        desc = request.form.get("text")
        input_files = []

        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(folder_path, exist_ok=True)

        for key, value in request.files.items():
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(folder_path, filename))
                input_files.append(filename)

        with open(os.path.join(folder_path, "desc.txt"), "w", encoding="utf-8") as f:
            f.write(desc)

        with open(os.path.join(folder_path, "input.txt"), "w") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\n")
                f.write("duration 1\n")

    return render_template("create.html", myid=myid)


# ✅ MUST ADD THIS
if __name__ == "__main__":
    app.run(debug=True)