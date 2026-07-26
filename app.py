"""Duddy's Crash Coarse in Rocketry local application."""

from flask import Flask, abort, jsonify, render_template, request

from rocket_curriculum import (
    all_modules,
    module_by_slug,
    search_curriculum,
    seminar_by_number,
    validate_curriculum,
)
from rocket_sources import ACCESSED, SOURCES


APP_NAME = "Duddy's Crash Coarse in Rocketry"
REPOSITORY_URL = "https://github.com/JohnDuddy/Duddys-Crash-Coarse-in-Rocketry"

app = Flask(__name__)


@app.context_processor
def inject_shared_context():
    modules = all_modules()
    return {
        "app_name": APP_NAME,
        "nav_modules": modules,
        "repository_url": REPOSITORY_URL,
        "total_modules": len(modules),
        "total_seminars": sum(len(item["seminars"]) for item in modules),
        "total_words": sum(
            seminar["word_count"]
            for item in modules
            for seminar in item["seminars"]
        ),
    }


@app.get("/")
def index():
    modules = all_modules()
    return render_template(
        "index.html",
        modules=modules,
        total_minutes=sum(
            seminar["minutes"]
            for item in modules
            for seminar in item["seminars"]
        ),
    )


@app.get("/module/<slug>")
def course_module(slug):
    selected = module_by_slug(slug)
    if not selected:
        abort(404)
    modules = all_modules()
    index = modules.index(selected)
    return render_template(
        "module.html",
        module=selected,
        previous_module=modules[index - 1] if index > 0 else None,
        next_module=modules[index + 1] if index + 1 < len(modules) else None,
    )


@app.get("/module/<slug>/seminar/<int:number>")
def research_seminar(slug, number):
    selected = module_by_slug(slug)
    selected_seminar = seminar_by_number(selected, number)
    if not selected or not selected_seminar:
        abort(404)
    return render_template(
        "seminar.html",
        module=selected,
        seminar=selected_seminar,
        previous_seminar=seminar_by_number(selected, number - 1),
        next_seminar=seminar_by_number(selected, number + 1),
    )


@app.get("/review")
def review():
    return render_template("review.html")


@app.get("/funding")
def funding():
    return render_template("funding.html")


@app.get("/sources")
def sources():
    return render_template(
        "sources.html",
        sources=[{"id": key, **value} for key, value in SOURCES.items()],
        accessed=ACCESSED,
    )


@app.get("/search")
def search():
    query = request.args.get("q", "").strip()
    return render_template(
        "search.html",
        query=query,
        results=search_curriculum(query),
    )


@app.get("/health")
def health():
    errors = validate_curriculum()
    modules = all_modules()
    return jsonify(
        {
            "status": "ok" if not errors else "invalid",
            "modules": len(modules),
            "seminars": sum(len(item["seminars"]) for item in modules),
            "seminar_words": sum(
                seminar["word_count"]
                for item in modules
                for seminar in item["seminars"]
            ),
            "primary_sources": len(SOURCES),
            "curriculum_errors": errors,
            "repository": REPOSITORY_URL,
        }
    )


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html"), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5080, debug=False)

