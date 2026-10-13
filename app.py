from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-for-real-deployments"

# In-memory storage: records reset whenever the application process restarts.
students = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html", total_students=len(students))


@app.route("/add", methods=["GET", "POST"])
def add_student():
    global next_id
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll_number = request.form.get("roll_number", "").strip()
        branch = request.form.get("branch", "").strip()
        marks_text = request.form.get("marks", "").strip()

        if not all([name, roll_number, branch, marks_text]):
            flash("Please fill in every field.", "error")
            return redirect(url_for("add_student"))

        if any(s["roll_number"].lower() == roll_number.lower() for s in students):
            flash("That roll number already exists.", "error")
            return redirect(url_for("add_student"))

        try:
            marks = float(marks_text)
            if not 0 <= marks <= 100:
                raise ValueError
        except ValueError:
            flash("Marks must be a number between 0 and 100.", "error")
            return redirect(url_for("add_student"))

        students.append({
            "id": next_id,
            "name": name,
            "roll_number": roll_number,
            "branch": branch,
            "marks": marks,
        })
        next_id += 1
        flash(f"Student {name} added successfully.", "success")
        return redirect(url_for("view_students"))

    return render_template("add_student.html")


@app.route("/students")
def view_students():
    return render_template("students.html", students=students)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    flash("Student record deleted.", "success")
    return redirect(url_for("view_students"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", "5050")))
