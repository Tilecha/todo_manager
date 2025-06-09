from flask import Flask, request, jsonify
from datetime import date
from commands.load import load_tasks
from commands.save import save_tasks
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands.open_webapp import open_webapp
from commands.data import handle_webapp_data

BOT_TOKEN = "8036426582:AAEkGwTAkzfPKPUn0pCMFV4jAkZKzy6mH34"



app = Flask(__name__)

# Корневая страница (можно подключить index.html если нужно)
@app.route("/")
def index():
    return "✅ Миниап запущен и работает!"

# Получить все задачи
@app.route("/get_tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

# Добавить новую задачу
@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.get_json()
    task = {
        "text": data.get("text", "Без названия"),
        "tags": data.get("tags", []),
        "done": False,
        "created": date.today().isoformat()
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return jsonify({"success": True})

# Очистить все задачи
@app.route("/clean_tasks", methods=["POST"])
def clean_tasks():
    save_tasks([])
    return jsonify({"success": True})

# Удалить задачу по индексу
@app.route("/delete_task", methods=["POST"])
def delete_task():
    data = request.get_json()
    index = data.get("index")
    tasks = load_tasks()
    if index is not None and 0 <= index < len(tasks):
        deleted = tasks.pop(index)
        save_tasks(tasks)
        return jsonify({"success": True, "deleted": deleted})
    return jsonify({"success": False, "error": "Неверный индекс"}), 400

# Отметить задачу выполненной / невыполненной
@app.route("/toggle_done", methods=["POST"])
def toggle_done():
    data = request.get_json()
    index = data.get("index")
    tasks = load_tasks()
    if index is not None and 0 <= index < len(tasks):
        tasks[index]["done"] = not tasks[index]["done"]
        save_tasks(tasks)
        return jsonify({"success": True, "new_status": tasks[index]["done"]})
    return jsonify({"success": False, "error": "Неверный индекс"}), 400

# Поиск по тегу
@app.route("/filter", methods=["POST"])
def filter_by_tag():
    data = request.get_json()
    tag = data.get("tag", "").lower().strip()
    tasks = load_tasks()
    filtered = [
        task for task in tasks
        if any(t.lower() == tag for t in task.get("tags", []))
    ]
    return jsonify(filtered)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render задаёт PORT как переменную окружения
    app.run(host="0.0.0.0", port=port)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("open", open_webapp))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

app.run_polling()