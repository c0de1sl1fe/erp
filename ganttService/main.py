# main.py
import os
from flask import Flask, request, Response

from gantt_renderer import render_gantt, render_stats

app = Flask(__name__)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "gantt_template.html")


def load_template() -> str:
    """Читает HTML-шаблон из файла."""
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


@app.route("/gantt", methods=["POST"])
def gantt_endpoint() -> Response:
    """
    Получает JSON, генерирует HTML фрагмент диаграммы,
    оборачивает его в шаблон, сохраняет gantt.html и
    возвращает фрагмент (для Jmix).
    """
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return Response("Invalid JSON", status=400, mimetype="text/plain; charset=utf-8")

    html_fragment = render_gantt(payload)
    template = load_template()

    title = payload.get("name", "Gantt Diagram")
    full_html = (
        template
        .replace("{{title}}", title)
        .replace("{{content}}", html_fragment)
    )

    output_path = os.path.join(os.path.dirname(__file__), "gantt.html")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"[INFO] Gantt HTML сохранён: {output_path}")
    except Exception as e:
        print(f"[ERROR] Не удалось сохранить Gantt HTML: {e}")

    return Response(html_fragment, mimetype="text/html; charset=utf-8")


@app.route("/stats", methods=["POST"])
def stats_endpoint() -> Response:
    """
    Получает тот же JSON, генерирует HTML статистики,
    сохраняет stats.html и возвращает только фрагмент.
    """
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return Response("Invalid JSON", status=400, mimetype="text/plain; charset=utf-8")

    html_fragment = render_stats(payload)
    template = load_template()

    title = f"Статистика: {payload.get('name', 'Проект')}"
    full_html = (
        template
        .replace("{{title}}", title)
        .replace("{{content}}", html_fragment)
    )

    output_path = os.path.join(os.path.dirname(__file__), "stats.html")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"[INFO] Stats HTML сохранён: {output_path}")
    except Exception as e:
        print(f"[ERROR] Не удалось сохранить Stats HTML: {e}")

    return Response(html_fragment, mimetype="text/html; charset=utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
