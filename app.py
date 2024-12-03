from flask import *
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
from robo import *
import requests

app = Flask(__name__)
app.secret_key = "QuokkaQuiz"


@app.route('/')
def main_page():
    if session.get('quiz', False) == False:
        quiz_go = False
    else:
        quiz_go = True
    if session.get("auth", False) == False:
        auth_token = str(uuid.uuid4())
        hour = datetime.datetime.now().hour
        hello = say_hello_main(hour)
        return render_template('main.html', auth=0, token=auth_token, hello=hello, quiz_go=quiz_go)
    else:
        hour = datetime.datetime.now().hour
        hello = say_hello_main(hour)
        return render_template('main.html', auth=1, hello=hello, quiz_go=quiz_go)


@app.template_filter('shuffle')
def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq


@app.route('/constructor')
def main_menu_constructor():
    if session.get("auth", False) == False:
        return render_template('main.html', auth=0)
    else:
        if detect_bank_user(session['auth']) == True:
            user_bank = bank[session['auth']]
        else:
            bank[session['auth']] = []
            user_bank = bank[session['auth']]
        u = get_user_limits(session['auth'])
        return render_template('menu.html', auth=session['auth'], quiz=quiz, user=u, groups=groups, bank=user_bank)


@app.route('/constructor/<id>')
def constructor(id):
    q = find_quiz(id)
    u = get_user_limits(session['auth'])
    m = check_for_sale(id)
    return render_template('create.html', quiz=q, id=id, user=u, m=m)


@app.route('/teacher/login')
def teacher_login():
    if session.get('auth', False) == False:
        return render_template('enter.html')
    return redirect('/constructor')


@app.route('/constructor/create/<type>')
def create_constructor(type):
    id = str(random.randint(100000, 999999))
    quiz.append({
        'id': id,
        'type': type,
        'status': "Close",
        'plan': None,
        'author': session['auth'],
        'text': None,
        'title': None,
        'protect': False,
        'color': '#ffffff',
        'result': [],
        'test': [],
        'settings': {
            'special': None,
            'notify': None,
            'hide_res': None,
            'diploma': None
        }
    })
    add_used_quiz(session['auth'])
    save_data()
    return redirect(f'/constructor/{id}')


@app.route('/save/main/<id>', methods=['POST'])
def save_main_info(id):
    title = request.form.get('title')
    text = request.form.get('text')

    special = request.form.get('special')
    notify = request.form.get('notify')
    hide_res = request.form.get('hide_res')
    diploma = request.form.get('diploma')

    set_main_info(id, title, text)
    set_save(id, special, notify, hide_res, diploma)
    return redirect(f'/constructor/{id}')


@app.route('/create/<type>/<id>')
def create_new_quiz(type, id):
    task_id = str(random.randint(100000, 999999))
    add_new_task(id, type, task_id)
    return redirect(f'/constructor/{id}?focusquiz#test{task_id}')


@app.route('/delete/quiz/<id>/<quiz_id>')
def del_quiz(id, quiz_id):
    delete_quiz(id, quiz_id)
    return redirect(f'/constructor/{id}?focusquiz')


@app.route('/edit/quiz/<id>/<quiz_id>')
def edit_quiz(id, quiz_id):
    q = find_quiz(id)
    task = find_quiz_task(id, quiz_id)
    u = get_user_limits(session['auth'])
    return render_template('editor.html', quiz=q, id=id, user=u, test=task)


@app.route('/save/quiz/<id>/<type>/<test_id>', methods=['POST'])
def save_quiz_info(id, type, test_id):
    text = request.form.get('text')
    img_url = request.form.get('image')
    html_text = markdown.markdown(text)
    save_quiz(id, test_id, html_text, img_url)
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/add/answer/<id>/<type>/<quiz_id>')
def add_answer_quiz(id, type, quiz_id):
    add_answer(id, type, quiz_id)
    return redirect(f'/edit/quiz/{id}/{quiz_id}')


@app.route('/save/answer/<id>/<test_id>/<answer_id>', methods=['POST'])
def save_answer_to_quiz(id, test_id, answer_id):
    answer = request.form.get('answer')
    save_answer(id, test_id, answer_id, answer)
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/del/answer/<id>/<test_id>/<answer_id>')
def del_quiz_answer(id, test_id, answer_id):
    del_answer(id, test_id, answer_id)
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/set/answer/status/<id>/<test_id>/<a_id>/<status>')
def change_answer_status(id, test_id, a_id, status):
    if status == "True" or status == True:
        status = False
    else:
        status = True
    set_answer_status(id, test_id, a_id, status)
    # return redirect(f'/edit/quiz/{id}/{test_id}')
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/student/quiz/<id>')
def get_student_solve(id):
    q = find_quiz(id)
    ip_data = requests.get('https://api64.ipify.org?format=json').json()
    ip = ip_data['ip']
    location_data = requests.get(f'http://ip-api.com/json/{ip}?lang=ru').json()
    print(location_data)
    city = location_data['city']
    soc_user = ''
    if session.get('social', False) == False:
        pass
    else:
        soc_user = find_social(session['social'])
    pre_text = random_prequiz()
    sklon = true_word_form(len(q['test']))
    if session.get('quiz', False) == False:
        quiz_go = False
    else:
        quiz_go = True
    return render_template(
        'solve.html', start=True, id=id, quiz=q, sklon=sklon, soc=soc_user, pre_text=pre_text, quiz_go=quiz_go,
        location=location_data
    )


@app.route('/student/quiz/<id>', methods=['POST'])
def post_student_solve(id):
    q = find_quiz(id)
    name = request.form.get('name')
    unum = str(uuid.uuid4())
    session['student'] = unum
    session['num'] = 1
    session['quiz'] = id
    session['after'] = 0
    if session.get('social', False) == False:
        pass
    else:
        soc_user = find_social(session['social'])
        if soc_user['premium'] != False:
            session['premium'] = 1
    if q['type'] == 'bee':
        add_empty_bee_result(id, unum, name)
    else:
        add_empty_result(id, unum, name)
    add_start_time(id, unum, time.time())
    return redirect(f'/student/quiz')


@app.route('/student/quiz')
def student_quiz_num():
    id = session['quiz']
    num = int(session['num'])
    q = find_quiz(id)
    if int(num) > len(q['test']):
        result = find_quiz_result(id, session['student'])
        add_finish_time(id, session['student'], time.time())
        find_total_time(id, session['student'])
        q = find_quiz(session['quiz'])
        after_ask = session['after']
        stud = session['student']
        del session['student']
        del session['num']
        del session['quiz']
        del session['after']
        proc_result = round(int(result['score']) / len(q['test'] * 100))
        if q['settings']['notify'] == "on":
            send_email_message(session['auth'], f'Ученик №{stud} прошел ваш квиз! Подробности на сайте!',
                               'Ученик прошел квиз')

        soc_mail = ""
        socuser = ''
        if session.get('social', False) == False:
            pass
        else:
            soc_mail = session['social']
            find_and_done_social_task(session['social'], id, result['score'])

        points = int(result['score'])

        if session.get('premium', False) == False:
            pass
        else:
            points = points * 2
            add_limit_to_user(q['author'], 1)
            print("points", points)

        soc_add_points(soc_mail, result['score'], id, len(q['test']), q['title'])

        socuser = find_social(soc_mail)

        return render_template('solve.html', start="Final", id=id, result=result, len=len(q['test']), quiz=q,
                               after_ask=after_ask, proc_result=proc_result, stud=stud, soc_mail=soc_mail,
                               points=points, socuser=socuser)
    else:
        color = None
        if q['type'] == 'bee':
            color = find_user_bee_color(id, session['student'])
        premium = 0
        if session.get('premium', False) == False:
            pass
        else:
            premium = 1
        print(premium)
        return render_template('solve.html', quiz=q, num=num, start=False, id=id, color=color, premium=premium)


@app.route('/social/quiz', methods=['POST'])
def social_quiz():
    mail = request.form.get('mail')
    id = request.form.get('id')
    points = request.form.get('points')
    all_points = request.form.get('all_points')
    title = request.form.get('title')
    if check_social(mail) == True:
        soc_add_points(mail, points, id, all_points, title)
        return redirect(f'/student/quiz/{id}')
    else:
        return redirect(f'/student/quiz/{id}')


@app.route('/student/quiz/answer', methods=['POST'])
def student_quiz_num_answer():
    id = session['quiz']
    num = session['num']
    answer = request.form.get('ans')
    q = find_quiz(id)
    if q['status'] == "Close":
        result = find_quiz_result(id, session['student'])
        add_finish_time(id, session['student'], time.time())
        find_total_time(id, session['student'])
        del session['student']
        del session['num']
        del session['quiz']
        del session['after']
        return render_template('solve.html', start="QuizClose", result=result, len=len(q['test']), id=id)
    print(answer)
    n = int(num) + 1
    session['num'] = n
    if find_answer_type(id, num) == "after_check":
        session['after'] += 1
        add_after_result(id, session['student'], answer)
        return redirect(f'/student/quiz')
    elif find_answer_type(id, num) == "python_code":
        i_data, o_data, length = get_python_io_data(id, num)
        print(i_data, o_data, length)
        counter = 0
        i_data, o_data, length = get_python_io_data(id, num)
        for i in range(0, length):
            input_data = i_data[i]
            output_data = o_data[i]
            sys.stdin = StringIO(input_data)
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            try:
                exec(answer)
            except Exception as e:
                print(e)
            sys.stdout = old_stdout
            result = redirected_output.getvalue()
            print(str(result.strip()), str(output_data.strip()))
            if str(result.strip()) == str(output_data.strip()):
                counter += 1
        if counter == length:
            add_true_result(id, session['student'], "Правильный код")
        elif counter > 0 and counter < length:
            add_mixed_result(id, session['student'], f'Python: {counter} / {length}')
        else:
            add_false_result(id, session['student'], "Неправильный код")
        return redirect(f'/student/quiz')
    elif find_answer_type(id, num) == "cross":
        result = check_answer_cross(id, num, answer)
        if result == 'Correct answer':
            add_true_result(id, session['student'], answer)
        else:
            add_false_result(id, session['student'], answer)
        return redirect(f'/student/quiz')
    else:
        if session.get('premium', False) == False:
            pass
        else:
            if session['premium'] == 1:
                if answer == 'ПОДСКАЗКА':
                    add_true_result(id, session['student'], answer)
                    session['premium'] = 0
                    return redirect(f'/student/quiz')
                else:
                    pass
            else:
                pass
        result = check_answer(id, num, answer)
        if result == 'Correct answer':
            add_true_result(id, session['student'], answer)
        else:
            add_false_result(id, session['student'], answer)
        return redirect(f'/student/quiz')


@app.route('/find/quiz', methods=['POST'])
def find_quiz_post():
    id = request.form.get('num')
    if bool_find_quiz(id) == True:
        return redirect(f'/student/quiz/{id}')
    else:
        return render_template('main.html', error="Такой квиз не найден")


@app.route('/login/check', methods=['POST'])
def login_check_post():
    mail = request.form.get('email')
    password = request.form.get('password')
    u = find_user(mail, password)
    if u == "OK":
        session['auth'] = mail
        return redirect('/constructor')
    elif u == "Incorrect password":
        return render_template('main.html', error="Пароль неверный, повторите попытку")
    elif u == "User not found":
        create_user(mail, password)
        session['auth'] = mail
        return redirect('/constructor')


@app.route('/whoid/login')
def whoid_login():
    result = request.args.get('status')
    mail = request.args.get('mail')
    if result == "Success":
        u = find_user_mail(mail)
        if u == True:
            session['auth'] = mail
            return redirect('/constructor')
        elif u == False:
            create_user(mail, 'password')
            session['auth'] = mail
            return redirect('/constructor')
    else:
        return redirect('/')


@app.route('/constructor/delete/<id>')
def del_quiz_app(id):
    del_quiz_def(id)
    del_used_quiz(session['auth'])
    return redirect('/constructor?focusquiz')


@app.route('/value/user/answer/<id>/<ans>/<val>')
def value_user_answer(id, ans, val):
    change_user_answer(id, ans, val)
    mail = find_remember_user_mail(id, ans)
    if mail != "None" or mail is not None:
        send_email_message(mail, f'Учитель проверил ваш ответ, у вас {val} правильных заданий!', 'Задание проверено')
    return redirect(f'/dashboard/answers/{id}')


@app.route('/remember/mail/<id>/<stud>', methods=['POST'])
def send_after_mail(id, stud):
    mail = request.form.get('mail')
    remember_user_mail(id, stud, mail)
    return render_template('solve.html', id=id, start="SuccessMail")


@app.route('/add/gpt/answer/<id>/<task_id>')
def add_gpt_answer(id, task_id):
    add_system_answer(id, task_id)
    return redirect(f'/constructor/{id}?focusquiz#test{task_id}')


@app.route('/add/gpt/plan/<id>')
def add_gpt_plan(id):
    create_gpt_plan(id)
    return redirect(f'/constructor/{id}')


@app.route('/dashboard/answers/<id>')
def quiz_show_answers(id):
    q = find_quiz(id)
    return render_template('answers.html', quiz=q, id=id)


@app.route('/show/board/mode/<id>/<num>')
def show_board_mode(id, num):
    q = find_quiz(id)
    all_info = show_list_test(id)[int(num) - 1]
    return render_template('board.html', test=all_info, num=int(num), id=id, quiz=q, mode='classic')


@app.route('/show/bee/mode/<id>')
def show_board_bee_mode(id):
    q = find_quiz(id)
    return render_template('board.html', id=id, quiz=q, mode="bee")


@app.route('/bee/board/update/<id>')
def bee_borad_update(id):
    q = find_quiz(id)
    update_bee_status(id)
    return redirect(f'/show/bee/mode/{id}')


@app.route('/add/checkpoint/<id>/<test_id>')
def add_checkpoint(id, test_id):
    add_new_check_point(id, test_id)
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/save/checkpoint/<id>/<test_id>/<check_id>', methods=['POST'])
def save_checkpoint(id, test_id, check_id):
    code_input = request.form.get("input")
    code_output = request.form.get("output")
    saving_checkpoint_info(id, test_id, check_id, code_input, code_output)
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/del/checkpoint/<id>/<test_id>/<check_id>')
def del_checkpoint(id, test_id, check_id):
    delete_quiz_checkpoint(id, test_id, check_id)
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/quiz/open/<id>')
def open_quiz(id):
    func_open_quiz(id)
    return redirect(f'/constructor/{id}')


@app.route('/quiz/close/<id>')
def close_quiz(id):
    func_close_quiz(id)
    return redirect(f'/constructor/{id}')


@app.route('/set/cross/answer/<id>/<test_id>', methods=['POST'])
def set_cross_answer(id, test_id):
    answer = request.form.get('answer')
    set_cross_quiz_answer(id, test_id, answer)
    return redirect(f'/edit/quiz/{id}/{test_id}')


@app.route('/sale/quiz/<id>', methods=['POST'])
def sale_quiz(id):
    q = find_quiz(id)
    q['result'] = []
    author = q['author']
    price = int(request.form.get('price'))
    market.append({
        "id": f'{random.randint(10000000, 99999999)}',
        'author': author,
        "price": price,
        "kolvo": 0,
        "benefit": 0,
        "status": True,
        "quiz": q,
    })
    save_data()
    return redirect(f'/constructor/{id}?focussettings')


@app.route('/sale/out/<id>')
def sale_out(id):
    change_market_status(id, False)
    return redirect(f'/constructor/{id}?focussettings')


@app.route('/sale/new/<id>')
def sale_new(id):
    change_market_status(id, True)
    return redirect(f'/constructor/{id}?focussettings')


@app.route('/api/find/quiz/<id>')
def api_find_quiz(id):
    return jsonify(find_quiz(id))


@app.route('/api/quiz/text/<id>')
def api_quiz_text(id):
    texts, answers = for_api_find_text_answer(id)
    print(texts)
    return jsonify(texts)


@app.route('/api/quiz/answer/<id>')
def api_quiz_answer(id):
    texts, answers = for_api_find_text_answer(id)
    print(answers)
    return jsonify(answers)


@app.route('/api/answer/quiz/<id>/<score>/<name>')
def api_answer_quiz(id, score, name):
    add_telegram_result(id, score, name)
    return jsonify({"status": "OK"})


@app.route('/pay/noti/<kolvo>', methods=['POST', 'GET'])
def payment_notify(kolvo):
    mail = request.args.get('customerEmail')
    kolvo = int(kolvo)
    add_limit_to_user(mail, kolvo)
    return jsonify({"status": "Pay"})


@app.route('/pay/protect', methods=['POST', 'GET'])
def payment_notify_protect():
    print(request.data)
    return jsonify({"status": "OK"})


@app.route('/pay/after')
def payment_after():
    return render_template('pay.html')


@app.route('/payment/combo/<id>')
def payment_combo(id):
    id = int(id)
    SHOP_LOGIN = 'quokkaquizpro'
    SHOP_PASSWORD = 'ycZtq70Jx5znu0Spx6zw'
    shopping_id = random.randint(10000, 99999)
    if id == 1:
        link = generate_payment_link(
            SHOP_LOGIN,
            SHOP_PASSWORD,
            '3.24',
            shopping_id,
            'МиниКомбо',
            session['auth']
        )
        session['shop'] = {"id": shopping_id, 'info': 'МиниКомбо'}
        return redirect(link)
    elif id == 2:
        link = generate_payment_link(
            SHOP_LOGIN,
            SHOP_PASSWORD,
            '4.80',
            shopping_id,
            'МидиКомбо',
            session['auth']
        )
        session['shop'] = {"id": shopping_id, 'info': 'МидиКомбо'}
        return redirect(link)
    elif id == 3:
        link = generate_payment_link(
            SHOP_LOGIN,
            SHOP_PASSWORD,
            '6.72',
            shopping_id,
            'МаксиКомбо',
            session['auth']
        )
        session['shop'] = {"id": shopping_id, 'info': 'МаксиКомбо'}
        return redirect(link)


@app.route('/payment/kolvo/<id>', methods=['POST'])
def payment_kolvo(id):
    SHOP_LOGIN = 'quokkaquizpro'
    SHOP_PASSWORD = 'ycZtq70Jx5znu0Spx6zw'
    shopping_id = random.randint(10000, 99999)
    kolvo = int(request.form.get('kolvo'))
    if kolvo <= 0:
        return abort(500)
    price = calculate_payment_price(id, kolvo)
    if id == 'classic':
        ds = f'КвоккаКвиз Шаблон - {kolvo} шт.'
        link = generate_payment_link(
            SHOP_LOGIN,
            SHOP_PASSWORD,
            price,
            shopping_id,
            ds,
            session['auth']
        )
        session['shop'] = {"id": shopping_id, 'info': 'Классик', 'kolvo': kolvo}
        return render_template('payment.html', status='PREPARE', price=price, ds=ds, link=link)
    elif id == 'premier':
        ds = f'КвоккаКвиз Премьер - {kolvo} шт.'
        link = generate_payment_link(
            SHOP_LOGIN,
            SHOP_PASSWORD,
            price,
            shopping_id,
            ds,
            session['auth']
        )
        session['shop'] = {"id": shopping_id, 'info': 'Премьер', 'kolvo': kolvo}
        return render_template('payment.html', status='PREPARE', price=price, ds=ds, link=link)


@app.route('/success/sell')
def sell_success():
    summa = str(request.args.get("OutSum"))
    invid = int(request.args.get("InvId"))
    if session['shop']['id'] == invid:
        if session['shop']['info'] == 'МиниКомбо':
            add_user_quiz(session['auth'], 15, 'mini')
            add_user_quiz(session['auth'], 15, 'maxi')
            return render_template('payment.html', status=True)
        elif session['shop']['info'] == 'МиниКомбо':
            add_user_quiz(session['auth'], 30, 'mini')
            add_user_quiz(session['auth'], 30, 'maxi')
            return render_template('payment.html', status=True)
        elif session['shop']['info'] == 'МаксиКомбо':
            add_user_quiz(session['auth'], 60, 'mini')
            add_user_quiz(session['auth'], 60, 'maxi')
            return render_template('payment.html', status=True)
        elif session['shop']['info'] == 'Классик':
            add_user_quiz(session['auth'], session['shop']['kolvo'], 'mini')
            return render_template('payment.html', status=True)
        elif session['shop']['info'] == 'Премьер':
            add_user_quiz(session['auth'], session['shop']['kolvo'], 'maxi')
            return render_template('payment.html', status=True)
    else:
        return render_template('payment.html', status=False)


@app.route(f'/success/fail')
def sell_fail():
    return render_template('payment.html', status=False)


@app.route('/save/settings/<id>', methods=['POST'])
def post_settings(id):
    return redirect(f'/constructor/{id}')


@app.route('/diploma/create', methods=['POST'])
def diploma_create():
    user_name = request.form.get('user_name')
    quiz_name = request.form.get('quiz_name')
    create_diploma(user_name, quiz_name)
    return send_file('static/user_diploma.png')


@app.route('/qr/create/<id>')
def qr_create(id):
    with open('static/qr.png', 'w') as file:
        file = qrcode.make(f'https://pro.quokkaquiz.ru/student/quiz/{id}')
        file.save('./static/qr.png')
        return send_file('static/qr.png')


@app.route('/logout')
def logout():
    del session['auth']
    return redirect('/')


@app.route('/social/connect')
def soc_connect():
    return render_template('social.html', start=True)


@app.route('/social/reg', methods=['POST'])
def soc_reg():
    name = request.form.get('name')
    mail = request.form.get('mail')
    if check_social(mail) == False:
        id = str(random.randint(100000, 999999))
        social.append({
            'mail': mail,
            'balance': 0,
            'name': name,
            'id': id,
            'solved': 0,
            'premium': False,
            'history': [],
            'quizes': [],
            'tasks': [],
            'uni_key': str(random.randint(10000000, 99999999))
        })
        save_data()
        session['social'] = mail
        send_email_message(
            mail,
            f'Добро пожаловать в QuokkaConnect! Вы сможете получать призы, просто решая квизы. Чтобы все результаты засчитывались - не забывайте после прохождения вводить индивидуальный номер - <h1>{id}</h1>',
            'Добро пожаловать!'
        )
        return redirect('/social/my')
    else:
        return redirect('/social/my')


@app.route('/social/my')
def social_my():
    if session.get('social', False) == False:
        return render_template('social.html', start=False, auth=0)
    else:
        u = find_social(session['social'])
        now_time = time.time()
        if u['premium'] == False:
            pass
        else:
            if u['premium'] <= now_time:
                u['premium'] = False
                save_data()
        alert = request.args.get('alert')
        return render_template('social.html', start=False, auth=1, user=u, shop=shop, orders=orders, alert=alert)


@app.route('/social/logout')
def social_logout():
    del session['social']
    return redirect('/')


@app.route('/social/log', methods=['POST'])
def social_log():
    mail = request.form.get('mail')
    if '@' in mail:
        code = str(random.randint(100000, 999999))
        session['code'] = code
        session['mail'] = mail
        if check_social(mail) == True:
            send_email_message(
                mail,
                f'Вход в аккаунт QuokkaConnect. Для входа введите ваш код, он будет действовать в течении нескольких минут - <h1>{code}</h1>',
                'Подтверждение входа QuokkaConnect'
            )
            return render_template('social.html', start=False, auth=0, code=mail)
        else:
            return redirect('/social/my')
    else:
        res = find_uniq_social_key(mail)
        if res != False:
            session['social'] = res
            worker = random_name_choice()
            msg_text = f'В ваш аккаунт КвоккаConnect только что вошли с помощью секретного кода.<p>Если это были вы - проигнорируйте данное сообщение. А если нет - срочно смените секретный код в личном кабинете.</p>С уважением, сотрудник службы безопасности КвоккаКвиз - {worker}'
            send_email_message(res, msg_text, 'Вход в КвоккаConnect')
            return redirect('/social/my')
        else:
            return redirect('/social/my?error=Код неверный')


@app.route('/social/code', methods=['POST'])
def social_code():
    code = request.form.get('code')
    print(code, session['code'])
    if str(code) == str(session['code']):
        session['social'] = session['mail']
        del session['mail']
        del session['code']
        return redirect('/social/my')
    else:
        return render_template('social.html', start=False, auth=0, code=session['mail'])


@app.route('/social/new/uniq', methods=['GET'])
def social_new_uniq():
    change_social_uniq(session['social'])
    alert = 'Код быстрого доступа успешно изменен'
    return redirect(f'/social/my?alert={alert}')


@app.route('/shop/buy/<id>', methods=['POST'])
def shop_buy(id):
    item = find_item(id)
    soc_user = find_social(session['social'])
    if soc_user['balance'] >= item['price']:
        soc_user['balance'] -= item['price']
        save_data()
        name = request.form.get('name')
        phone = request.form.get('phone')
        clas = request.form.get('class')
        delivery = request.form.get('delivery')
        order_id = str(random.randint(1000000, 9999999))
        data = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        new_order = {
            'id': order_id,
            'mail': soc_user['mail'],
            'phone': phone,
            'item_id': item['id'],
            'item_title': item['title'],
            'price': item['price'],
            'status': 'Принят',
            'title': item['title'],
            'date': data,
            'class': clas,
            'delivery': delivery,
            'name': name
        }
        orders.append(new_order)
        save_data()
        send_email_message(
            session['social'],
            f'Ваш заказ №{new_order["id"]} на сумму {new_order["price"]} QC успешно <b>оформлен</b><p>Вы получите уведомление, когда заказ будет готов к выдаче</p><i>По всем вопросам обращайтесь на почту help@quokkaquiz.ru</i>',
            'Заказ оформлен'
        )
        return render_template('social.html', start=False, auth=2, order=new_order)
    else:
        return redirect('/social/my')


@app.route('/shop/console')
def shop_console():
    return render_template('admin.html', orders=orders)


@app.route('/shop/order/<id>/<stat>')
def shop_set_stat(id, stat):
    new_st = get_new_status(stat)
    o = find_order(id)
    set_new_order_status(id, new_st)
    return redirect('/shop/console')


@app.route('/one')
def show_one():
    soc_u = find_social(session['social'])
    return render_template('one.html', soc_u=soc_u)


@app.route('/one/new', methods=['POST'])
def one_create_sign():
    mail = request.form.get('mail')
    create_new_premium(mail)
    return render_template('one.html', soc_u=soc_u)


@app.route('/one/noti', methods=['POST', 'GET'])
def one_payment_notify():
    mail = request.args.get('customerEmail')
    # summa = int(request.args.get('productPrice'))
    create_new_premium(mail)
    return jsonify({"status": "Pay"})


@app.route('/list')
def quiz_list_show():
    return render_template('list.html', quiz=quiz)


@app.route('/bank')
def open_bank():
    if detect_bank_user(session['auth']) == True:
        user_bank = bank[session['auth']]
        return render_template('bank.html', bank=user_bank)
    else:
        bank[session['auth']] = []
        return redirect('/bank')


@app.route('/bank/add/<id>/<tid>')
def bank_add(id, tid):
    if detect_bank_user(session['auth']) == True:
        new_test = find_need_test(id, tid)
        bank[session['auth']].append(new_test)
        save_data()
        return redirect(f'/constructor/{id}?focusquiz#test{tid}')
    else:
        bank[session['auth']] = []
        return redirect(f'/bank/add/{id}/{tid}')


@app.route('/bank/import/<id>', methods=['POST'])
def post_bank_import(id):
    num = request.form.get('number')
    task = get_task_from_bank(num)
    if task == False:
        return redirect(f'/constructor/{id}')
    else:
        if from_bank_quiz_id_find(id, num) == False:
            add_task_to_quiz_bank(id, task)
            return redirect(f'/constructor/{id}?focusquiz#test{task["id"]}')
        else:
            return redirect(f'/constructor/{id}?focusquiz#test{num}')


@app.route('/bank/del/<id>')
def bank_del(id):
    delete_task_from_bank(id, session['auth'])
    return redirect('/constructor?focusbox')


@app.route('/quality/check/<id>/<tid>')
def check_quality(id, tid):
    gpt_check_test(id, tid)
    return redirect(f'/constructor/{id}?focusquiz#test{tid}')


@app.route('/group')
def group():
    return render_template('group.html', groups=groups, author=session['auth'], open=0)


@app.route('/group/<id>')
def group_open(id):
    g = find_group(id)
    return render_template('group.html', group=g, open=1)


@app.route('/group/create', methods=['POST'])
def group_create():
    title = request.form.get('title')
    groups.append({
        "id": str(random.randint(100000, 999999)),
        "title": title,
        "author": session['auth'],
        "students": [],
        "works": [],
        "messages": []
    })
    save_data()
    return redirect('/group')


@app.route('/group/<id>/new/student', methods=['POST'])
def group_add_user(id):
    number = request.form.get('number')
    if find_social_id(number) == True:
        u = find_social_user(number)
        add_new_group_user(id, u)
        return redirect(f'/group/{id}')
    else:
        return redirect(f'/group/{id}')


@app.route('/group/<id>/new/work', methods=['POST'])
def group_add_task(id):
    number = request.form.get('number')
    if find_if_quiz(number) == True:
        q = find_quiz(number)
        title = q['title']
        add_new_group_task(id, q)
        send_stud_new_task(id, title, number)
        return redirect(f'/group/{id}')
    else:
        return redirect(f'/group/{id}')


@app.route('/group/<group_id>/send/<quiz_id>/<user_id>/<result>')
def group_send_info(group_id, quiz_id, user_id, result):
    u = find_social_id_full(user_id)
    send_info_to_teacher(group_id, quiz_id, u, result)
    return redirect('/social/my')


@app.route('/support/send', methods=['POST'])
def support_send():
    text = request.form.get('text')
    worker = random_name_choice()
    send_email_message(session['auth'],
                       f'Спасибо за обращение в службу поддержки, специалист все проверит и отправит вам ответ в течении одного рабочего дня!<p>С уважением, менеджер службы поддержки учителей {worker}!</p>',
                       "Служба поддержки учителей КвоккаКвиз")
    send_email_message("hi@quokkaquiz.ru", f'Вопрос от учителя {session["auth"]}: <p>{text}</p>',
                       'Новый запрос в поддержку')
    return redirect('/constructor')


@app.route('/sales/send', methods=['POST'])
def sales_send():
    typi = request.form.get('type')
    kolvo = request.form.get('kolvo')
    text = request.form.get('text')
    worker = random_name_choice()
    send_email_message(session['auth'],
                       f'Ваш запрос в отдел продаж успешно отправлен! В течении одного рабочего дня с вами свяжется специалист.<p>С уважением, сотрудник отдела продаж {worker}!</p>',
                       "Отдел продаж КвоккаКвиз")
    send_email_message("hi@quokkaquiz.ru",
                       f'Учитель {session["auth"]} отправил запрос:<br><br>- {typi}<br>- {kolvo}<br>- {text}',
                       'Запрос в отдел продаж')
    return redirect('/constructor')


@app.route('/support/student', methods=['POST'])
def support_student_send():
    text = request.form.get('text')
    mail = request.form.get('mail')
    worker = random_name_choice()
    send_email_message(mail,
                       f'Спасибо за внимательность и обращение в службу поддержки, наш специалист все проверит и свяжется с вами в течении одного рабочего дня!<p>С уважением, специалист службы поддержки учеников {worker}!</p>',
                       "Служба поддержки учеников КвоккаКвиз")
    send_email_message("hi@quokkaquiz.ru", f'Вопрос от ученика {mail}: <p>{text}</p>', 'Новый запрос в поддержку')
    return redirect('/')


@app.route('/cheating/detect')
def detect_devtools():
    del session['student']
    del session['num']
    del session['quiz']
    del session['after']
    return render_template('cheating.html')


@app.route(f'/result/test/<type>/sell')
def result_test_sell(type):
    invid = int(request.args.get("InvId"))
    if find_inv_id(invid) == False:
        payment_history.append(invid)
        save_data()
        if type == "maxi":
            add_user_quiz(session['auth'], 20, 'mini')
        else:
            add_user_quiz(session['auth'], 40, 'maxi')
        return render_template('payment.html', status=True)
    else:
        return render_template('payment.html', status=False)


@app.route(f'/result/test/<type>/sell/fail')
def result_test_sell_fail():
    return render_template('payment.html', status=False)


@app.route('/option/apply/<id>')
def option_apply_quiz(id):
    apply_option(id)
    minus_limit_pro(session['auth'])
    return redirect(f'/constructor/{id}?focussettings')


@app.route('/option/update/<id>', methods=['POST'])
def option_update(id):
    color = request.form.get('color')
    change_quiz_color(id, color)
    return redirect(f'/constructor/{id}?focussettings')


@app.route('/quiz/<id>/<tid>/slider/save', methods=['POST'])
def quiz_slider_save(id, tid):
    minval = int(request.form.get('minval'))
    maxval = int(request.form.get('maxval'))
    step = int(request.form.get('step'))
    update_slider_values(id, tid, minval, maxval, step)
    return redirect(f'/constructor/{id}?focusquiz#test{tid}')


@app.route('/quiz/<id>/<tid>/audio/save', methods=['POST'])
def quiz_audio_save(id, tid):
    audio_text = request.form.get('audio_text')
    update_audio_value(id, tid, audio_text)
    return redirect(f'/constructor/{id}?focusquiz#test{tid}')


@app.route('/ai/create/<id>', methods=['POST'])
def ai_create_ask(id):
    theme = request.form.get('text')
    ask_test = create_prompt(
        f"Как учитель - создай РОВНО ОДИН вопрос для квиза по теме '{theme}', ОТВЕТ НЕ УКАЗЫВАЙ. Напиши его БЕЗ ВСТУПИТЕЛЬНОГО И КОНЕЧНОГО ТЕКСТА - ТОЛЬКО ВОПРОС. БЕЗ ТЕКСТА 'Вот один из ...")
    ask_answer = create_prompt(
        "Для предыдущего вопроса напиши ответ В ОДНО-ДВА слова, БЕЗ ВСТУПИТЕЛЬНОГО И КОНЕЧНОГО ТЕКСТА - ТОЛЬКО ОТВЕТ. БЕЗ ТЕКСТА 'Вот одно из ...'")
    rand_id = random.randint(100000, 999999)
    new_ask_ai_create(id, ask_test, ask_answer, rand_id)
    return redirect(f'/constructor/{id}?focusquiz#test{rand_id}')


@app.route('/document/create/<id>')
def document_create(id):
    create_pdf(find_quiz(id))
    return send_file('static/tasks.docx')


@app.route('/document/export/<id>')
def document_export(id):
    create_excel(find_quiz(id))
    return send_file('static/result.xlsx')


@app.route('/clear/answers/<id>')
def clear_answers(id):
    delete_answers(id)
    return redirect(f'/constructor/{id}?focusresult')


@app.errorhandler(500)
def error_500(e):
    return render_template('errorhandler.html'), 500


@app.errorhandler(502)
def error_502(e):
    return render_template('errorhandler.html'), 502


@app.errorhandler(400)
def error_400(e):
    return render_template('errorhandler.html'), 400


@app.errorhandler(404)
def error_404(e):
    return render_template('errorhandler.html'), 404


app.run(port=5066)