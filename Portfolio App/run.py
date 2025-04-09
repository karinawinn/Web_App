from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a147395982125e9268226cd2889bd10f'

@app.route("/", methods=['GET','POST'])
def home():
    return render_template('home.html')

def load_projects():
    file_path = os.path.join(os.path.dirname(__file__), "projects.json")
    with open(file_path) as f:
        return json.load(f)
    
def load_comments():
    file_path = os.path.join(os.path.dirname(__file__), "comments.json")
    with open(file_path) as f:
        return json.load(f)

def save_comments(comments):
    file_path = os.path.join(os.path.dirname(__file__), "comments.json")
    with open(file_path, "w") as f:
        json.dump(comments, f, indent=4)

@app.route("/<subject>")
def subject(subject):
    projects = load_projects()
    if subject in projects:
        return render_template("subject.html", subject=subject, projects=projects[subject])
    return "Subject not found", 404

@app.route("/<subject>/<project_title>", methods=["GET", "POST"])
def project(subject, project_title):
    projects = load_projects()
    comments = load_comments()

    for project in projects.get(subject, []):
        if project["title"] == project_title:
            if request.method == "POST":
                name = request.form.get("name")
                comment = request.form.get("comment")
                if not name or not comment:
                    error = "Both fields are required."
                    return render_template("project.html", project=project, subject=subject, comments=comments[subject][project_title], error=error)
                comments[subject][project_title].append({"name": name, "comment": comment})
                save_comments(comments)
                return redirect(url_for("project", subject=subject, project_title=project_title))
            return render_template("project.html", project=project, subject=subject, comments=comments[subject][project_title])
    return "Project not found", 404

if __name__ == '__main__':
    app.run(debug=True)