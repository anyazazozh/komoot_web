from flask import Flask, render_template, request, jsonify, send_file
import tempfile
import os
from parser_def import html_to_gpx_bytes

app = Flask(__name__)


# Главная страница
@app.route("/")
def home():
    return render_template("index.html", title="HTML to GPX Parser")


# API для парсинга HTML файла
@app.route("/api/parse", methods=["POST"])
def api_parse():
    # Проверяем, что файл был отправлен
    if 'html_file' not in request.files:
        return jsonify({"error": "HTML файл не передан"}), 400

    file = request.files['html_file']

    # Проверяем, что файл имеет имя
    if file.filename == '':
        return jsonify({"error": "Файл не выбран"}), 400

    # Проверяем, что это HTML файл
    if not file.filename.lower().endswith(('.html', '.htm')):
        return jsonify({"error": "Файл должен быть в формате HTML"}), 400

    try:
        # Читаем содержимое HTML файла
        html_content = file.read().decode('utf-8')

        # Парсим HTML и получаем GPX
        gpx_bytes = html_to_gpx_bytes(html_content)

        # Создаем временный файл для GPX
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gpx') as temp_file:
            temp_file.write(gpx_bytes)
            temp_file_path = temp_file.name

        # Возвращаем файл для скачивания
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name=f"{os.path.splitext(file.filename)[0]}.gpx",
            mimetype='application/gpx+xml'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
