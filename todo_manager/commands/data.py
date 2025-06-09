import json
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ContextTypes
from datetime import date
from commands.load import load_tasks
from commands.save import save_tasks
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

async def open_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Открыть трекер", web_app=WebAppInfo(url="https://todo-manager-n3vu.onrender.com"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Нажми кнопку ниже, чтобы открыть трекер:", reply_markup=reply_markup)


app = Flask(__name__)

@app.route("/get_tasks")
def get_tasks():
    return jsonify(load_tasks())

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



async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.web_app_data:
        return
    try:
        data = json.loads(update.message.web_app_data.data)
        if data.get("action") == "add":
            task = {
                "text": data.get("text", "Без названия"),
                "tags": data.get("tags", []),
                "done": False,
                "created": date.today().isoformat()
            }
            tasks = load_tasks()
            tasks.append(task)
            save_tasks(tasks)
            await update.message.reply_text(f"✅ Задача добавлена:\n{task['text']}\n🏷️ {', '.join(task['tags']) if task['tags'] else 'без тегов'}")
        elif data.get("action") == "delete":
            index = data.get("index")
            tasks = load_tasks()
            if 0 <= index < len(tasks):
                deleted = tasks.pop(index)
                save_tasks(tasks)
                await update.message.reply_text(f"🗑️ Удалена задача: {deleted['text']}")
            return
        elif data.get("action") == "edit":
            index = data.get("index")
            new_text = data.get("text")

            if index is None or not isinstance(index, int):
                await update.message.reply_text("❌ Неверный индекс задачи.")
                return

            if not new_text:
                await update.message.reply_text("❌ Новый текст задачи пустой.")
                return

            tasks = load_tasks()

            if 0 <= index < len(tasks):
                old_text = tasks[index]["text"]
                tasks[index]["text"] = new_text
                save_tasks(tasks)
                await update.message.reply_text(f"✏️ Задача изменена:\n\nДо: {old_text}\nПосле: {new_text}")
            else:
                await update.message.reply_text("❌ Индекс вне диапазона.")

        elif data.get("action") == "clean":
            save_tasks([])
            await update.message.reply_text("Список очищен.")

        elif data.get("action") == "done":
            tasks = load_tasks()
            index = data.get("index")
            tasks[index]["done"]=not tasks[index]["done"]
            status = "✅ Выполнено" if tasks[index]["done"] else "❌ Не выполнено"
            await update.message.reply_text(f"Статус задачи изменён: {status} — {tasks[index]['text']}")

        elif data.get("action") == "filter":
            tasks = load_tasks()
            tag = data.get("tag").lower().strip()
            matched_tasks = []
            for i, task in enumerate(tasks, 1):
                for t in task.get("tags", []):
                    if t.lower() == tag:
                        matched_tasks.append((i,task))
                        break
            if not matched_tasks:
                await update.message.reply_text(f"Задач с тегом '{tag}' не найдено.")
            else:
                response = f"Задачи с тегом '{tag}':\n"
                for i, task in matched_tasks:
                    status = "✅" if task["done"] else "❌"
                    tags = ", ".join(task["tags"]) if task["tags"] else "Без тегов"
                    response += f"{i}. {status} {task['text']}, теги: {tags}\n"
                await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("❌ Ошибка при обработке задачи.")
        print("Ошибка:", e)