import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, author_id, message_id, question):
    answer = "Осталось секунд: "
    timeout = parse(question)
    persents = render_progressbar(timeout, (timeout-secs_left))
    bot.update_message(author_id, message_id, f"{answer} {secs_left}\n {persents}")


def wait(chat_id, question):
    message_id = bot.send_message(chat_id, "Думаем")
    timeout = parse(question)
    bot.create_countdown(timeout, notify_progress, question=question, message_id=message_id, author_id=chat_id)
    bot.create_timer(parse(question), choose, author_id=chat_id)


def choose(author_id):
    answer = "Время вышло"
    bot.send_message(author_id, answer)


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv("TOKEN")
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(wait)
    bot.run_bot()
