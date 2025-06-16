from fastapi import FastAPI, Request, Form, RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import os
import telegram

app = FastAPI()
templates = Jinja2Templates(directory="dashboard/templates")

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)
DB_FILE = os.path.join(os.path.dirname(__file__), "../orders.db")

@app.get("/", response_class=HTMLResponse)
def read_orders(request: Request):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT rowid, user_id, name, service, time, attachment, order_id, status FROM orders ORDER BY time DESC")
        rows = cursor.fetchall()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": rows})

@app.post("/update-status")
async def update_status(
    order_id: str = Form(...),
    user_id: int = Form(...),
    status: str = Form(...),
):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))

    msg = f"📦 *طلبك رقم {order_id}* تم تحديث حالته إلى: *{status}*"
    await bot.send_message(chat_id=user_id, text=msg, parse_mode="Markdown")

    return RedirectResponse(url="/", status_code=303)
