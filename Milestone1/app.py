from flask import Flask, render_template, request, flash, redirect, url_for
from database import get_connection

app = Flask(__name__)
app.secret_key = "milestone-1-development-key"


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_project():
    project_name = request.form.get("project_name", "").strip()
    project_description = request.form.get("project_description", "").strip()
    target_market = request.form.get("target_market", "").strip()
    budget = request.form.get("budget", "").strip()
    competition = request.form.get("competition", "").strip()
    resources = request.form.get("resources", "").strip()
    objectives = request.form.get("objectives", "").strip()

    if not all([
        project_name,
        project_description,
        target_market,
        budget,
        competition,
        resources,
        objectives,
    ]):
        flash("Please complete all project fields.", "error")
        return redirect(url_for("home"))

    try:
        budget_value = float(budget)
    except ValueError:
        flash("Budget must be a valid number.", "error")
        return redirect(url_for("home"))

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO projects (
                project_name,
                project_description,
                target_market,
                budget,
                competition,
                resources,
                objectives
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                project_name,
                project_description,
                target_market,
                budget_value,
                competition,
                resources,
                objectives,
            ),
        )

        connection.commit()
        flash("Project submitted successfully!", "success")

    except Exception as error:
        if connection:
            connection.rollback()
        app.logger.exception("Project submission failed")
        flash("Unable to save the project. Please check your database connection.", "error")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
