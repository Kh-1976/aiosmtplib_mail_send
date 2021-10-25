import asyncio
from email.message import EmailMessage
import aiosmtplib
import aiosqlite

db = '/..../contacts.db'

# sudo docker run -p 8025:8025 -p 1025:1025 mailhog/mailhog
# sudo docker run mailhog/mailhog


async def async_data_upload(loop):
    async with aiosqlite.connect(db, loop=loop) as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT first_name, last_name, email FROM contacts")
            result = await cur.fetchall()
            return result

loop = asyncio.get_event_loop()
result = loop.run_until_complete(async_data_upload(loop))


async def send_mail():
    for i in result:
        message = EmailMessage()
        message["From"] = "root@localhost"
        message["To"] = list(i)[2]
        message["Subject"] = f"Уважаемый {list(i)[0]} {list(i)[1]}!"
        message.set_content("Спасибо, что пользуетесь нашим сервисом объявлений.")
        await aiosmtplib.send(message, hostname="127.0.0.1", port=1025)

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(send_mail())