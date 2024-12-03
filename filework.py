import random
import uuid
import time
import markdown
from sender import send_email_message
from gpt import create_prompt
from system import run_code
import sys
from io import StringIO
from diploma import create_diploma
import qrcode
import datetime
from words import *
from documents import *
from excel import *
from filework import *
import json

quiz = []
user = []
social = []
shop = []
orders = []
bank = {}
groups = []
payment_history = []
market = []

try:
    with open('json/quiz.json', 'r') as file:
        quiz = json.loads(file.read())
    with open('json/user.json', 'r') as file:
        user = json.loads(file.read())
    with open('json/social.json', 'r') as file:
        social = json.loads(file.read())
    with open('json/shop.json', 'r') as file:
        shop = json.loads(file.read())
    with open('json/orders.json', 'r') as file:
        orders = json.loads(file.read())
    with open('json/bank.json', 'r') as file:
        bank = json.loads(file.read())
    with open('json/groups.json', 'r') as file:
        groups = json.loads(file.read())
    with open('json/payment.json', 'r') as file:
        payment_history = json.loads(file.read())
    with open('json/market.json', 'r') as file:
        market = json.loads(file.read())
except:
    pass


def save_data():
    with open('json/quiz.json', 'w') as file:
        file.write(json.dumps(quiz, ensure_ascii=False))
    with open('json/user.json', 'w') as file:
        file.write(json.dumps(user, ensure_ascii=False))
    with open('json/social.json', 'w') as file:
        file.write(json.dumps(social, ensure_ascii=False))
    with open('json/shop.json', 'w') as file:
        file.write(json.dumps(shop, ensure_ascii=False))
    with open('json/orders.json', 'w') as file:
        file.write(json.dumps(orders, ensure_ascii=False))
    with open('json/bank.json', 'w') as file:
        file.write(json.dumps(bank, ensure_ascii=False))
    with open('json/groups.json', 'w') as file:
        file.write(json.dumps(groups, ensure_ascii=False))
    with open('json/market.json', 'w') as file:
        file.write(json.dumps(market, ensure_ascii=False))


def delete_answers(id):
    for q in quiz:
        if q['id'] == id:
            q['result'] = []
            save_data()


def new_ask_ai_create(id, ask, answer, rand_id):
    for q in quiz:
        if q['id'] == id:
            q['test'].append(
                {
                    "answer": [
                        {
                            "answer": answer,
                            "id": f"{random.randint(100000, 999999)}"
                        }
                    ],
                    "id": f"{rand_id}",
                    "image": None,
                    "quality": None,
                    "system": None,
                    "text": ask,
                    "type": "text"
                }
            )
            save_data()


def update_audio_value(id, tid, audio_text):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == tid:
                    t['audio_text'] = audio_text
                    save_data()


def update_slider_values(id, tid, minval, maxval, step):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == tid:
                    t['slider']['minval'] = minval
                    t['slider']['maxval'] = maxval
                    t['slider']['step'] = step
                    save_data()


def change_quiz_color(id, color):
    for q in quiz:
        if q['id'] == id:
            q['color'] = color
            save_data()


def minus_limit_pro(mail):
    for u in user:
        if u['mail'] == mail:
            u['used_pro'] += 1
            save_data()


def apply_option(id):
    for q in quiz:
        if q['id'] == id:
            q['protect'] = True
            save_data()


def find_inv_id(id: int):
    for p in payment_history:
        if p == id:
            return True
    return False


def add_user_quiz(mail, kolvo: int, typi):
    for u in user:
        if u['mail'] == mail:
            if typi == "mini":
                u['limit'] += kolvo
            else:
                u['limit_pro'] += kolvo
            save_data()
            break


def change_social_send_status(user_id, quiz_id):
    for s in social:
        if s['id'] == user_id:
            for t in s['tasks']:
                if t['id'] == quiz_id:
                    t['send'] = True
                    save_data()




def send_info_to_teacher(group_id, quiz_id, u, result):
    for g in groups:
        if g['id'] == group_id:
            for w in g['works']:
                if w['id'] == quiz_id:
                    w['users'].append({
                        'id': u['id'],
                        'name': u['name'],
                        'mail': u['mail'],
                        'result': result,
                    })
                    change_social_send_status(u['id'], quiz_id)
                    save_data()


def find_and_done_social_task(mail, qid, res):
    for s in social:
        if s['mail'] == mail:
            for t in s['tasks']:
                if t['id'] == qid:
                    t['done'] = res
                    save_data()


def find_uniq_social_key(key):
    for s in social:
        if s['uni_key'] == key:
            return s['mail']
    return False


def change_social_uniq(mail):
    for s in social:
        if s['mail'] == mail:
            s['uni_key'] = str(random.randint(10000000, 99999999))
            save_data()


def send_stud_new_task(id, title, tid):
    for g in groups:
        if g['id'] == id:
            for s in g['students']:
                text = f'Ваш учитель в группе <b>{g["title"]}</b> задал задание - пройти квиз "{title}" с ID <b>{tid}</b><p>Команда КвоккаКвиза желает вам успеха!)</p>'
                send_email_message(s['mail'], text, f"Новое задание в группе {g['title']}")
                for u in social:
                    if u['mail'] == s['mail']:
                        u['tasks'].append({
                            "id": tid,
                            "gid": g['id'],
                            "title": title,
                            "from": g['title'],
                            "done": False,
                            "send": False
                        })
                        save_data()
                        break


def add_new_group_task(gid, q):
    for g in groups:
        if g['id'] == gid:
            g['works'].append({
                'id': q['id'],
                'title': q['title'],
                'users': []
            })
            save_data()


def find_if_quiz(id):
    for q in quiz:
        if q['id'] == id:
            return True
    return False


def add_new_group_user(gid, u):
    for g in groups:
        if g['id'] == gid:
            g['students'].append({
                'id': u['id'],
                'mail': u['mail'],
                'name': u['name']
            })
            save_data()


def find_social_id(id):
    for s in social:
        if s['id'] == id:
            return True
    return False


def find_social_id_full(id):
    for s in social:
        if s['id'] == id:
            return s


def find_social_user(id):
    for s in social:
        if s['id'] == id:
            return s


def find_group(id):
    for g in groups:
        if g['id'] == id:
            return g


def delete_task_from_bank(id, s):
    b = bank[s]
    for q in b:
        if q['id'] == id:
            bank[s].remove(q)
            save_data()


def calculate_payment_price(typi, kolvo: int):
    if typi == 'classic':
        if 1 <= kolvo < 10:
            return kolvo * 14.5
        elif 10 <= kolvo < 25:
            return kolvo * 12.5
        elif 25 <= kolvo < 50:
            return kolvo * 10.5
        elif kolvo >= 50:
            return kolvo * 8.5
    elif typi == 'premier':
        if 1 <= kolvo < 10:
            return kolvo * 13.5
        elif 10 <= kolvo < 25:
            return kolvo * 11.5
        elif 25 <= kolvo < 50:
            return kolvo * 9.5
        elif kolvo >= 50:
            return kolvo * 7.5


def for_api_find_text_answer(id):
    texts = []
    answers = []
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                texts.append(t['text'])
                answers.append(t['answer'])
            break
    return texts, answers


def gpt_check_test(id, task_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == task_id:
                    title = q['title']
                    text = t['text']
                    answer = create_prompt(
                        f'Проверь вопрос из квиза с названием "{title}" на качество составления и дай рекомендации. Вот текст вопроса: "{text}"'
                    )
                    answer = markdown.markdown(answer)
                    t['quality'] = answer
                    save_data()


def from_bank_quiz_id_find(id, num):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == num:
                    return True
            break
    return False


def add_task_to_quiz_bank(id, task):
    for q in quiz:
        if q['id'] == id:
            q['test'].append(task)
            save_data()


def get_task_from_bank(num):
    b = bank[session['auth']]
    for q in b:
        if q['id'] == num:
            return q
    return False


def find_need_test(id, quiz_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == quiz_id:
                    return t


def detect_bank_user(mail):
    for key, value in bank.items():
        if key == mail:
            return True
    return False


def create_new_premium(mail):
    for s in social:
        if s['mail'] == mail:
            now_time = time.time()
            sub_stop = now_time + 2592000
            s['premium'] = sub_stop
            save_data()


def set_new_order_status(id, stat):
    for o in orders:
        if o['id'] == id:
            if stat == "В сборке":
                o['status'] = stat
                send_email_message(
                    o['mail'],
                    f'Сейчас мы начали бережно собирать ваш заказ №{o["id"]} - в нем товар {o["item_title"]}.<p>Следующим этапом заказ передадут курьеру для передачи в пункт выдачи</p><i>По всем вопросам обращайтесь на почту help@quokkaquiz.ru</i>',
                    'Ваш заказ собирается'
                )
                save_data()
            elif stat == 'В пути':
                o['status'] = stat
                send_email_message(
                    o['mail'],
                    f'Курьер получил заказ №{o["id"]} и спешит к пункту выдачи по адресу {o["delivery"]}<p>Когда заказ будет доставлен - вам придет уведомление. Также вы можете просматривать информацию о заказах в QuokkaQuiz</p><i>По всем вопросам обращайтесь на почту help@quokkaquiz.ru</i>',
                    'Заказ передан курьеру'
                )
                save_data()
            elif stat == 'Готов':
                o['status'] = stat
                send_email_message(
                    o['mail'],
                    f'Вы можете получить заказ №{o["id"]} по адресу - {o["delivery"]}<p>При необходимости с вами свяжутся по телефону и уточнят детали получения. Также для получения назоваите код <b>{random.randint(1000, 9999)}</b></p><i>По всем вопросам обращайтесь на почту help@quokkaquiz.ru</i>',
                    'Заказ готов к выдаче'
                )
                save_data()
            elif stat == 'Выдан':
                o['status'] = stat
                send_email_message(
                    o['mail'],
                    f'Спасибо, что оформили заказ в QuokkaConncet!<p><i>По всем вопросам обращайтесь на почту help@quokkaquiz.ru</i></p>',
                    'Заказ выдан'
                )
                save_data()


def find_order(id):
    for o in orders:
        if o['id'] == id:
            return o


def get_new_status(stat):
    stat = int(stat)
    if stat == 1:
        return "Принят"
    elif stat == 2:
        return "В сборке"
    elif stat == 3:
        return "В пути"
    elif stat == 4:
        return "Готов"
    elif stat == 5:
        return "Выдан"


def find_item(id):
    for i in shop:
        if i['id'] == id:
            return i


def soc_add_points(mail, points, id, all_points, title):
    for s in social:
        if s['mail'] == mail:
            s['balance'] += int(points)
            s['solved'] += 1
            s['quizes'].append({
                'id': id,
                'points': points,
                'all_points': all_points,
                'title': title
            })
            save_data()


def find_social(mail):
    for s in social:
        if s['mail'] == mail:
            return s
    return ''


def check_social(mail):
    for s in social:
        if s['mail'] == mail:
            return True
    return False


def set_save(id, special, notify, hide_res, diploma):
    for q in quiz:
        if q['id'] == id:
            set = q['settings']
            set['special'] = special
            set['notify'] = notify
            set['hide_res'] = hide_res
            set['diploma'] = diploma
            save_data()


def add_used_quiz(mail):
    for q in user:
        if q['mail'] == mail:
            q['used'] += 1
            save_data()


def del_used_quiz(mail):
    for q in user:
        if q['mail'] == mail:
            q['used'] -= 1
            save_data()


def add_limit_to_user(mail, summa):
    for u in user:
        if u['mail'] == mail:
            u['limit'] += summa
            save_data()


def set_cross_quiz_answer(id, test_id, answer):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == test_id:
                    t['answer'] = answer
                    save_data()


def func_open_quiz(id):
    for q in quiz:
        if q['id'] == id:
            q['status'] = "Open"
            save_data()


def func_close_quiz(id):
    for q in quiz:
        if q['id'] == id:
            q['status'] = "Close"
            save_data()


def get_python_io_data(id, num):
    input_data = []
    output_data = []
    for q in quiz:
        if q['id'] == id:
            for t in range(len(q['test'])):
                if (t + 1) == num:
                    for c in range(len(q['test'][t]['checkpoints'])):
                        input_data.append(q['test'][t]['checkpoints'][c]['input'])
                        output_data.append(q['test'][t]['checkpoints'][c]['output'])
                    length = len(q['test'][t]['checkpoints'])
                    return input_data, output_data, length


def add_new_check_point(id, test_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == test_id:
                    if 'checkpoints' in t:
                        pass
                    else:
                        t['checkpoints'] = []
                        save_data()
                    t['checkpoints'].append({
                        "id": str(uuid.uuid4()),
                        'input': "",
                        'output': ""
                    })
                    save_data()


def saving_checkpoint_info(id, test_id, point_id, code_input, output):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == test_id:
                    for c in t['checkpoints']:
                        if c['id'] == point_id:
                            c['input'] = code_input
                            c['output'] = output
                            save_data()


def show_list_test(id):
    test_list = []
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                test_list.append(t)
    return test_list


def add_system_answer(id, task_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == task_id:
                    answer = create_prompt(
                        f'Напиши свой ответ на тему: {t["text"]}. Используй разметку Markdown, но не упоминай это в тексте')
                    answer = markdown.markdown(answer)
                    t['system'] = answer
                    save_data()


def create_gpt_plan(id):
    for q in quiz:
        if q['id'] == id:
            answer = create_prompt(
                f'Создай примерный план квиза по названию "{q["title"]} и описанию "{q["text"]}". Используй разметку Markdown, но не упоминай это в тексте')
            answer = markdown.markdown(answer)
            q['plan'] = answer
            save_data()


def remember_user_mail(id, ans_id, mail):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == ans_id:
                    r['mail'] = mail
                    save_data()


def find_remember_user_mail(id, ans_id):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == ans_id:
                    return r['mail']


def change_user_answer(id, ans_id, val):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == ans_id:
                    r['score'] += int(val)
                for a in r['answers']:
                    if a['is_true'] == "Wait":
                        a['is_true'] = "Checked"
                save_data()


def del_quiz_def(id):
    for q in quiz:
        if q['id'] == id:
            quiz.remove(q)
            save_data()


def delete_quiz_checkpoint(id, t_id, c_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == t_id:
                    for c in t['checkpoints']:
                        if c['id'] == c_id:
                            t['checkpoints'].remove(c)
                            save_data()


def create_user(mail, password):
    user.append({
        'mail': mail,
        'password': password,
        'used': 0,
        'limit': 3,
        'limit_pro': 0,
        'used_pro': 0,
        "coins": 0,
    })
    save_data()


def get_user_limits(mail):
    for u in user:
        if u['mail'] == mail:
            return u


def find_user(mail, password):
    for u in user:
        if u['mail'] == mail:
            if u['password'] == password:
                return "OK"
            else:
                return "Incorrect password"
    return "User not found"


def find_user_mail(mail):
    for u in user:
        if u['mail'] == mail:
            return True
    return False


def bool_find_quiz(id):
    for q in quiz:
        if q['id'] == id:
            return True
    return False


def find_quiz_task(id, tid):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == tid:
                    return t


def bool_find_status(id):
    for q in quiz:
        if q['id'] == id:
            if q['status'] == "Close":
                return False
            else:
                return True


def find_quiz_result(id, uid):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == uid:
                    return r


def add_empty_result(id, uid, name):
    for q in quiz:
        if q['id'] == id:
            q['result'].append({
                "id": uid,
                "score": 0,
                "name": name,
                "answers": [],
                "start": None,
                "finish": None,
                "mail": None,
                "total": "Еще не пройдено"
            })
            save_data()


def add_empty_bee_result(id, uid, name):
    for q in quiz:
        if q['id'] == id:
            q['result'].append({
                "id": uid,
                'color': random.choice(colors),
                "score": 0,
                'active': True,
                "name": name,
                "answers": [],
                "start": None,
                "finish": None,
                "mail": None,
                "total": "Еще не пройдено"
            })
            save_data()


def find_user_bee_color(id, uid):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == uid:
                    return r['color']


def update_bee_status(id):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                r['active'] = False
                save_data()


def add_telegram_result(id, score, name):
    for q in quiz:
        if q['id'] == id:
            q['result'].append({
                "id": str(uuid.uuid4()),
                "score": score,
                "name": name,
                "answers": [
                    {
                        "answer": "Пройдено в Telegram",
                        "is_true": "Checked"
                    }
                ],
                "start": None,
                "finish": None,
                "mail": None,
                "total": "Пройдено"
            })
            save_data()


def find_total_time(id, res_id):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == res_id:
                    total_sec = r['finish'] - r['start']
                    minutes = round(total_sec / 60)
                    seconds = round(total_sec % 60)
                    r['total'] = f'{minutes}:{seconds}'
                    save_data()


def add_start_time(id, res_id, time):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == res_id:
                    r['start'] = time
                    save_data()


def add_finish_time(id, res_id, time):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == res_id:
                    r['finish'] = time
                    save_data()


def add_false_result(id, res_id, answer):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == res_id:
                    r['answers'].append({
                        "answer": answer,
                        "is_true": False
                    })
                    save_data()


def add_after_result(id, res_id, answer):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == res_id:
                    r['answers'].append({
                        "answer": answer,
                        "is_true": "Wait"
                    })
                    save_data()


def add_true_result(id, res_id, answer):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == res_id:
                    r['score'] += 1
                    r['answers'].append({
                        "answer": answer,
                        "is_true": True
                    })
                    save_data()


def add_mixed_result(id, res_id, answer):
    for q in quiz:
        if q['id'] == id:
            for r in q['result']:
                if r['id'] == res_id:
                    r['answers'].append({
                        "answer": answer,
                        "is_true": "Mixed"
                    })
                    save_data()


def check_answer(id, num, answer):
    for q in quiz:
        if q['id'] == id:
            for t in range(len(q['test'])):
                if (t + 1) == int(num):
                    for a in q['test'][t]['answer']:
                        print(a['answer'], answer)
                        if q['test'][t]['type'] == 'choice':
                            if a['answer'] == answer and a['true'] == True:
                                return "Correct answer"
                        else:
                            if a['answer'] == answer:
                                return "Correct answer"
    return "Answer not found"


def check_answer_cross(id, num, answer):
    for q in quiz:
        if q['id'] == id:
            for t in range(len(q['test'])):
                if (t + 1) == int(num):
                    if q['test'][t]['answer'] == answer:
                        return "Correct answer"
    return "Answer not found"


def find_answer_type(id, num):
    for q in quiz:
        if q['id'] == id:
            for t in range(len(q['test'])):
                if (t + 1) == int(num):
                    return q['test'][t]['type']


def find_quiz(id):
    for q in quiz:
        if q['id'] == id:
            return q

def change_market_status(id, status: bool):
    for m in market:
        if m['quiz']['id'] == id:
            m['status'] = status
            save_data()

def check_for_sale(id):
    for m in market:
        if m['quiz']['id'] == id:
            return m
    return False

def find_shop_item_id(id):
    for m in market:
        if m['id'] == id:
            return m

def new_user_benefit(email, coins: int):
    for u in user:
        if u['mail'] == email:
            final_coins = round(coins - (coins / 100 * 10))
            u['coins'] += final_coins
            save_data()

def new_quiz_benefit(id, coins: int):
    for m in market:
        if m['id'] == id:
            m['benefit'] += coins
            m['kolvo'] += 1
            save_data()

def get_teacher_balance(email):
    for u in user:
        if u['mail'] == email:
            return u['coins']

def teacher_minus_shop(email, coins: int):
    for u in user:
        if u['mail'] == email:
            u['coins'] -= coins
            save_data()

def set_main_info(id, title, text):
    for q in quiz:
        if q['id'] == id:
            q['title'] = title
            q['text'] = text
            save_data()


def add_new_task(id, type, task_id):
    for q in quiz:
        if q['id'] == id:
            if type == "cross":
                q['test'].append({
                    'id': task_id,
                    'image': None,
                    'quality': None,
                    'text': None,
                    'answer': "",
                    'type': type,
                    'system': None
                })
                save_data()
            elif type == "slider":
                q['test'].append({
                    'id': task_id,
                    'image': None,
                    'text': None,
                    'slider': {"minval": 1, "maxval": 10, "step": 1},
                    'quality': None,
                    'answer': [],
                    'type': type,
                    'system': None
                })
                save_data()
            elif type == "audio":
                q['test'].append({
                    'id': task_id,
                    'image': None,
                    'text': None,
                    'audio_text': "Here is audio text",
                    'quality': None,
                    'answer': [],
                    'type': type,
                    'system': None
                })
                save_data()
            elif type == "param":
                randid = random.randint(10000, 99999)
                q['test'].append({
                    'id': task_id,
                    'image': None,
                    'text': None,
                    'param': [
                        {"id": f"{randid}", "min": 1, "max": 10, "name": "x"}
                    ],
                    'formula': "100 - x",
                    'quality': None,
                    'answer': [],
                    'type': type,
                    'system': None
                })
                save_data()
            else:
                q['test'].append({
                    'id': task_id,
                    'image': None,
                    'text': None,
                    'quality': None,
                    'answer': [],
                    'type': type,
                    'system': None
                })
                save_data()


def delete_quiz(id, quiz_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == quiz_id:
                    q['test'].remove(t)
                    save_data()


def save_quiz(id, quiz_id, text, img_url):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == quiz_id:
                    t['text'] = text
                    t['image'] = img_url
                    save_data()


def add_answer(id, type, quiz_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == quiz_id:
                    if type == 'choice':
                        t['answer'].append({
                            'id': str(random.randint(100000, 999999)),
                            'true': False,
                            'answer': None
                        })
                    else:
                        t['answer'].append({
                            'id': str(random.randint(100000, 999999)),
                            'answer': None
                        })
                    save_data()


def save_answer(id, test_id, answer_id, answer):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == test_id:
                    for a in t['answer']:
                        if a['id'] == answer_id:
                            a['answer'] = answer
                            save_data()


def set_answer_status(id, test_id, answer_id, status):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == test_id:
                    for a in t['answer']:
                        if a['id'] == answer_id:
                            a['true'] = status
                            save_data()


def del_answer(id, test_id, answer_id):
    for q in quiz:
        if q['id'] == id:
            for t in q['test']:
                if t['id'] == test_id:
                    for a in t['answer']:
                        if a['id'] == answer_id:
                            t['answer'].remove(a)
                            save_data()


def true_word_form(s):
    n1 = " вопросов"
    n2 = " вопрос"
    n3 = " вопроса"
    if s == 0:
        return str(s) + n1
    elif s % 100 >= 10 and s % 100 <= 20:
        return str(s) + n1
    elif s % 10 == 1:
        return str(s) + n2
    elif s % 10 >= 2 and s % 10 <= 4:
        return str(s) + n3
    else:
        return str(s) + n1


def say_hello_main(hour):
    if hour >= 6 and hour < 12:
        return 'Доброе утро! 🌝'
    elif hour >= 12 and hour < 18:
        return 'Добрый день! ☀️'
    elif hour >= 18 and hour < 22:
        return 'Добрый вечер! 🌚'
    elif hour >= 22 or hour < 6:
        return 'Доброй ночи! ✨'


colors = [
    '#CD5C5C',
    '#FFA07A',
    '#8B0000',
    '#FFC0CB',
    '#FF1493',
    '#DB7093',
    '#FF7F50',
    '#FF4500',
    '#FFA500',
    '#FFD700',
    '#EEE8AA',
    '#BDB76B',
    '#D8BFD8',
    '#EE82EE',
    '#BA55D3',
    '#8A2BE2',
    '#8B008B',
    '#4B0082',
    '#483D8B',
    '#7B68EE',
    '#ADFF2F',
    '#32CD32',
    '#00FF7F',
    '#2E8B57',
    '#9ACD32',
    '#808000',
    '#66CDAA',
    '#008B8B',
    '#AFEEEE',
    '#40E0D0',
    '#5F9EA0',
    '#B0C4DE',
    '#87CEEB',
    '#1E90FF',
    '#4169E1',
    '#000080',
    '#D2B48C',
    '#BC8F8F',
    '#FFDEAD',
    '##8B4513',
    '#800000'
]
