from flask import Flask, render_template, request, jsonify, Response, send_file
import sqlite3
from datetime import datetime
from pydub import AudioSegment
from io import BytesIO, StringIO
import tempfile
import os
import base64
import io
from flask_cors import CORS
from PaswordGen import pwdGenerator # импорт функции генерации пароли;

# Функция запуска сайта
app = Flask(__name__)
CORS(app)
def create_app():
    return app

#===============================================================#
#                    Глобальные переменные                      #
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV#

path_bd_1 = 'fairy_tales.db'
path_bd_2 = 'users.db'
subscription_price = 1500 # Стоимость подписки;

#===============================================================#
#                Работа_с_базой_данных_SQLite3                  #
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV#

#============СОЗДАНИЕ_БАЗЫ_ДАННЫХ_ДЛЯ_СКАЗОК============#
conn = sqlite3.connect(path_bd_1) # Подключение к базе данных (если она не существует, будет создана новая);
cursor = conn.cursor() # Создание объекта курсора для выполнения SQL-запросов;
# Создание таблицы;
cursor.execute('''
    CREATE TABLE IF NOT EXISTS fairy_tales (
        id INTEGER PRIMARY KEY,
        audio BLOB,
        img_audio BLOB,
        name TEXT,
        name_sakha TEXT,
        description TEXT,
        description_sakha TEXT,
        upload_date TEXT,
        duration TEXT,
        genre_ru TEXT,
        genre TEXT,
        volume TEXT,
        age TEXT 
    )
''')
cursor.close()
conn.close()

# Запись на базу данных сказки;
@app.route('/downloading_a_fairy_tale_f', methods=['POST'])
def downloading_a_fairy_tale_f():
    # открытие базы данных;
    conn = sqlite3.connect('fairy_tales.db')
    cursor = conn.cursor()

    # опредление последнего значения индекса строк в БД для дальнейшей работы со значением;
    cursor.execute("SELECT id FROM fairy_tales")
    dataid_file = list(cursor.fetchall())[-1][0]
    
    # вывод с html-form аудио файла;
    audio_n = request.files['audio_n']
    # загрузка аудио файл сказки на папку aud;
    audio_n.save(os.path.join('static/aud', f'aud_id_{dataid_file + 1}.mp3'))
    audio_n = audio_n.read()
    # вывод с html-form файла изображения;
    img_audio_n = request.files['img_audio_n']
    # загрузка иконки сказки на папку img;
    img_audio_n.save(os.path.join('static/img', f'img_id_{dataid_file + 1}.jpg'))
    img_audio_n = img_audio_n.read()

    # вывод с html-form прочее данных;
    name_n = request.values['name_n'] # наименование сказки на Русском языке;
    name_sakha_n = request.values['name_sakha_n'] # наименование сказки на Якутском языке;
    description_n = request.values['description_n'] # описание сказки на Русском языке;
    description_sakha_n = request.values['description_sakha_n'] # описание сказки на Якутском языке;
    genre_ru_n = request.values['genre_ru_n']  # жанр сказки на Русском;
    genre_n = request.values['genre_n'] # жанр сказки на Якутском;
    age_n = request.values['age_n'] # возрастной рейтинг;

    # вывод текущей даты;
    current_datetime = datetime.now() # Получение текущей даты;
    upload_date = current_datetime.strftime("%Y.%m.%d") # Форматирование для вывода в строку;
    # вывод продолжительности аудио файла;
    duration = request.values['duration_n']
    # вывод размера аудио файла;
    volume = request.values['volume_n']

    # СОХРАНЕНИЕ В БАЗЕ ДАННЫХ;
    cursor.execute("INSERT INTO fairy_tales (audio, img_audio, name, name_sakha, description, description_sakha, upload_date, duration, genre_ru, genre, volume, age) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (audio_n, img_audio_n, name_n, name_sakha_n, description_n, description_sakha_n, upload_date, duration, genre_ru_n, genre_n, volume, age_n))
    conn.commit()
    conn.close()

    return render_template("audio_catalog.html")

# Функция передачи данных сказок;
@app.route('/api_fairy_tales', methods=['GET'])
def api_fairy_tales_f():
    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        return jsonify({'error': 'Invalid API key'}), 401  # Unauthorized
    conn = sqlite3.connect('fairy_tales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, name_sakha, description, description_sakha, upload_date, duration, genre_ru, genre, volume, age FROM fairy_tales")
    data = list(cursor.fetchall())
    conn.commit()
    conn.close()
    return jsonify(data)

# Запрос "GET" для вывода с БД данные о сказказ;
@app.route('/request_for_fairy_tales', methods=['GET'])
def request_for_fairy_tales_f():
    conn = sqlite3.connect('fairy_tales.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, name_sakha, description, description_sakha, upload_date, duration, genre_ru, genre, volume, age FROM fairy_tales")
    data = list(cursor.fetchall())
    conn.commit()
    conn.close()
    return jsonify(data)

# Запрос "POST" для удаление сказки из БД;
@app.route('/deleting_data', methods=['POST'])
def deleting_data_fairy_tales_f():
    post_request = request.get_json(force=True)
    post_request = int(post_request['data'])
    conn = sqlite3.connect('fairy_tales.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fairy_tales WHERE id = ?", (post_request,))
    conn.commit()
    conn.close()
    try:
        os.remove(f'static/aud/aud_id_{post_request}.mp3') # удаление аудио файла;
    except Exception as e:
        print(f"Произошла ошибка при удалении файла: {e}")
    try:
        os.remove(f'static/img/img_id_{post_request}.jpg') # удаление иконки изображения;
    except Exception as e:
        print(f"Произошла ошибка при удалении файла: {e}")

    return post_request

#============СОЗДАНИЕ_БАЗЫ_ДАННЫХ_ПОЛЬЗОВАТЕЛЕЙ============#
conn = sqlite3.connect(path_bd_2) # Подключение к базе данных (если она не существует, будет создана новая);
cursor = conn.cursor() # Создание объекта курсора для выполнения SQL-запросов;
# Создание таблицы;
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        login TEXT,
        pasword TEXT,
        name TEXT,
        surname TEXT,
        mail TEXT,
        phone TEXT,
        subscription TEXT,
        like TEXT,
        subscribe_fairy_tale TEXT,
        listening TEXT
    )
''')
cursor.close()
conn.close()

# Запрос "GET" для вывода с БД список пользователей;
@app.route('/request_for_users', methods=['GET'])
def request_for_users_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, login, pasword, name, surname, mail, phone, subscription, like, subscribe_fairy_tale, listening FROM users")
    data = list(cursor.fetchall())
    conn.commit()
    conn.close()
    return jsonify(data)

# Функция записи пользователя в БД;
@app.route('/api_user_record', methods=['GET'])
def api_users_f():
    # открытие базы данных;
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        return jsonify({'error': 'Invalid API key'}), 401  # ощибка в идентификации API;
    api_login = request.args.get('api_login')
    # вывод списка логинов пользователей для проверки занятости логина;
    cursor.execute("SELECT login FROM users")
    login_data = [record[0] for record in cursor.fetchall()]
    # проверка на отсутствие логина;
    if api_login in login_data:
        conn.close()
        return jsonify('Логин уже существует')  # логин уже существует;
    # запись логина и его данных в базу данных 'USERS';
    api_password = request.args.get('api_password')
    pasword = pwdGenerator(api_password, api_login, 30) # генерация пароли;
    name = request.args.get('api_name') # имя пользователя;
    surname = request.args.get('api_surname') # фамилия пользователя;
    mail = request.args.get('api_mail') # эл.почта пользователя;
    phone = request.args.get('api_phone') # номер телефона пользователя;
    subscription = 'нет' # имя пользователя;
    like = '' # за лайканные сказки;
    subscribe_fairy_tale = '' # слушаю;
    listening = '' # слушаю офлайн;
    cursor.execute("INSERT INTO users (login, pasword, name, surname, mail, phone, subscription, like, subscribe_fairy_tale, listening) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (api_login, pasword, name, surname, mail, phone, subscription, like, subscribe_fairy_tale, listening))
    conn.commit()
    conn.close()
    return jsonify('запись пользователя удалась')

# Функция входа в аккаунт;
@app.route('/api_log_in_to_your_account', methods=['GET'])
def secondary_input_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify({'error': 'Invalid API key'}), 401  # ощибка в идентификации API;
    
    # Проверка логина;
    api_login = request.args.get('api_login') # логин;
    cursor.execute("SELECT login FROM users")
    login_data = [record[0] for record in cursor.fetchall()]
    if api_login not in login_data:
        conn.close()
        return jsonify('Логина НЕ существует')  # логин уже существует;
    
    # Проверка пароли;
    api_password = request.args.get('api_password') # пароль;
    api_password = pwdGenerator(api_password, api_login,30) 
    cursor.execute("SELECT pasword FROM users")
    password_data = [record[0] for record in cursor.fetchall()]
    if api_password not in password_data:
        conn.close()
        return jsonify('Пароль НЕ правильный')  # логин уже существует;
    conn.close()
    return jsonify('вход в аккаунт')

#============Вывод_с_БД_данных_пользователей============#
@app.route('/WithdrawalOfAccountData', methods=['GET'])
def WithdrawalOfAccountData_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify({'error': 'Invalid API key'}), 401  # ощибка в идентификации API;

    api_login = request.args.get('api_login')

    work_text = f"SELECT id, login, pasword, name, surname, mail, phone, subscription, like, subscribe_fairy_tale, listening FROM users WHERE login = ?"
    cursor.execute(work_text, (api_login,))
    data = [record for record in cursor.fetchall()]
    conn.close()

    return jsonify(data)

#============Перезапись_данных_акккаунта============#
@app.route('/saving_account_data', methods=['GET'])
def saving_account_data_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('не верный')  # ощибка в идентификации API;
    
    api_login = request.args.get('api_login')
    api_name = request.args.get('api_name')
    api_surname = request.args.get('api_surname')
    api_mail = request.args.get('api_mail')
    api_phone = request.args.get('api_phone')

    work_text = "UPDATE users SET name = ?, surname = ?, mail = ?, phone = ? WHERE login = ?"
    cursor.execute(work_text, (api_name, api_surname, api_mail, api_phone, api_login))
    conn.commit()
    conn.close()
    return jsonify('данные изменены')

#============Запись_и_удаление_лайка============#
@app.route('/installing_a_like_f', methods=['GET'])
def installing_a_like_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('неверный api')  # ощибка в идентификации API;
    
    api_like = request.args.get('api_like')
    api_user = request.args.get('api_user')

    work_text = f"SELECT like FROM users WHERE login = ?"
    cursor.execute(work_text, (api_user,))
    data = [record[0] for record in cursor.fetchall()]
    data = str(data[0]).split(',')

    if str(api_like) not in data:
        # добавление лайка;
        work_data = []
        if data[0] == '':
            work_data.append(str(api_like))
        else:
            work_data.extend((d for d in data))
            work_data.append(api_like)
        data = ','.join(work_data)
        work_data = "UPDATE users SET like = ? WHERE login = ?"
        cursor.execute(work_data, (data, api_user))
        conn.commit()
        conn.close()
        print('лайк засчитан')
        return jsonify('лайк засчитан')
    else:
        # удаление лайка;
        work_data = []
        if data[0] == api_like and len(data) == 1:
            work_data = ''
        else:
            work_data.extend((d for d in data))
            work_data.remove(api_like)
        data = ','.join(work_data)
        work_data = "UPDATE users SET like = ? WHERE login = ?"
        cursor.execute(work_data, (data, api_user))
        conn.commit()
        conn.close()
        print('лайк удален')
        return jsonify('лайк удален')

#============запрос_на_данные_лайков============#
@app.route('/info_like', methods=['GET'])
def info_like_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('неверный api')  # ощибка в идентификации API;

    api_user = request.args.get('api_user')

    work_text = f"SELECT like FROM users WHERE login = ?"
    cursor.execute(work_text, (api_user,))
    data = [record[0] for record in cursor.fetchall()]
    conn.close()
    return jsonify(data[0])

#============запрос_на_избранные_видео============#
@app.route('/api_favourites', methods=['GET'])
def api_favourites_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('неверный api')  # ощибка в идентификации API;
    api_user = request.args.get('api_user')
    work_text = f"SELECT like FROM users WHERE login = ?"
    cursor.execute(work_text, (api_user,))
    data = [record[0] for record in cursor.fetchall()]
    conn.close()
    data = str(data[0]).split(',')
    conn = sqlite3.connect('fairy_tales.db')
    cursor = conn.cursor()
    new_data = []
    for id in data:
        work_text = f"SELECT id, name, name_sakha, description, description_sakha, upload_date, duration, genre_ru, genre, volume, age FROM fairy_tales WHERE id = ?"
        cursor.execute(work_text, (id,))
        new_data.append(cursor.fetchall()[0])
    conn.close()
    print(new_data)
    return jsonify(new_data)

#============Запись_и_удаление_подписки============#
@app.route('/installing_a_subscription_f', methods=['GET'])
def installing_a_subscription_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('неверный api')  # ощибка в идентификации API;
    
    api_subscription = request.args.get('api_subscription')
    api_user = request.args.get('api_user')

    work_text = f"SELECT subscribe_fairy_tale FROM users WHERE login = ?"
    cursor.execute(work_text, (api_user,))
    data = [record[0] for record in cursor.fetchall()]
    data = str(data[0]).split(',')

    if str(api_subscription) not in data:
        # добавление подписки;
        work_data = []
        if data[0] == '':
            work_data.append(str(api_subscription))
        else:
            work_data.extend((d for d in data))
            work_data.append(api_subscription)
        data = ','.join(work_data)
        work_data = "UPDATE users SET subscribe_fairy_tale = ? WHERE login = ?"
        cursor.execute(work_data, (data, api_user))
        conn.commit()
        conn.close()
        print('подписка засчитана')
        return jsonify('подписка засчитана')
    else:
        # удаление подписки;
        work_data = []
        if data[0] == api_subscription and len(data) == 1:
            work_data = ''
        else:
            work_data.extend((d for d in data))
            work_data.remove(api_subscription)
        data = ','.join(work_data)
        work_data = "UPDATE users SET subscribe_fairy_tale = ? WHERE login = ?"
        cursor.execute(work_data, (data, api_user))
        conn.commit()
        conn.close()
        print('подписка удалена')
        return jsonify('подписка удалена')
    
#============запрос_на_данные_подписок============#
@app.route('/info_subscription', methods=['GET'])
def info_subscription_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('неверный api')  # ощибка в идентификации API;

    api_user = request.args.get('api_user')

    work_text = f"SELECT subscribe_fairy_tale FROM users WHERE login = ?"
    cursor.execute(work_text, (api_user,))
    data = [record[0] for record in cursor.fetchall()]
    conn.close()
    return jsonify(data[0])

#============запрос_на_подписанное_видео============#
@app.route('/api_subscription_fun', methods=['GET'])
def api_subscription_fun_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('неверный api')  # ощибка в идентификации API;
    api_user = request.args.get('api_user')
    work_text = f"SELECT subscribe_fairy_tale FROM users WHERE login = ?"
    cursor.execute(work_text, (api_user,))
    data = [record[0] for record in cursor.fetchall()]
    conn.close()
    data = str(data[0]).split(',')
    conn = sqlite3.connect('fairy_tales.db')
    cursor = conn.cursor()
    new_data = []
    for id in data:
        work_text = f"SELECT id, name, name_sakha, description, description_sakha, upload_date, duration, genre_ru, genre, volume, age FROM fairy_tales WHERE id = ?"
        cursor.execute(work_text, (int(id),))
        new_data.append(cursor.fetchall()[0])
    conn.close()
    print(new_data)
    return jsonify(new_data)

#============запрос_на_ПОДПИСКУ_и_цену_за_подписку============#
subscription_price = 1500
@app.route('/checking_subscription_data', methods=['GET'])
def checking_subscription_data_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение ключа API из URL-параметров;
    api_key = request.args.get('api_key')
    # Проверка ключа API;
    if api_key != '123456789':
        conn.close()
        return jsonify('неверный api')  # ощибка в идентификации API;
    
    api_user = request.args.get('api_user')
    work_text = f"SELECT subscription FROM users WHERE login = ?"
    cursor.execute(work_text, (api_user,))
    data = [record[0] for record in cursor.fetchall()]
    global subscription_price
    data = [data, subscription_price]
    print(data)
    conn.close()

    return jsonify(data)

#============ПОДПИСКА============#
@app.route('/paying_subscription', methods=['GET'])
def paying_for_a_subsc_f():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получение ключа API из URL-параметров
    api_key = request.args.get('api_key')
    # Проверка ключа API
    if api_key != '123456789':
        conn.close()
        return jsonify('не верный')  # ощибка в идентификации API;
    
    api_user = request.args.get('api_user')
    api_text_inp_1 = request.args.get('api_text1')
    api_text_inp_2 = request.args.get('api_text2')
    api_text_inp_3 = request.args.get('api_text3')
    api_text_inp_4 = request.args.get('api_text4')
    api_text_inp_5 = request.args.get('api_text5')
    global subscription_price

    

    work_text = "UPDATE users SET subscription = ? WHERE login = ?"
    signed = 'подписан'
    cursor.execute(work_text, (signed, api_user))
    conn.commit()
    conn.close()
    return jsonify('Оплата прошла')

#===============================================================#
#                     Работа с запросами                        #
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV#

# # Запрос "POST";
# @app.route('/post_request_1', methods=['POST'])
# def post_request_1_f():
#     post_request = request.get_json(force=True)
#     post_request = [post_request['name_basket']]
#     if request.method == 'GET':
#         return None
#     return post_request

# # Запрос "GET";
# @app.route('/get_request_1', methods=['GET'])
# def get_request_1_f():
#     data = 1
#     search_object = ''
#     if request.method == 'POST':
#         return Response(search_object, content_type='application/octet-stream')
    
#     return jsonify(data)


#===============================================================#
#                      Функции и классы                         #
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV#


#===============================================================#
#                    Работа со страницами                       #
#VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV#

# Рендер тела сайта (запуск сайта);
@app.route('/')
@app.route('/main')
def main_f():
    render_template('main.html')
    return render_template('audio_catalog.html')
# Рендер страницы "ГЛАВНАЯ";
@app.route("/1_main")
def _1_main_f():
    return render_template("1_main.html")

# Рендер страницы "audio_catalog";
@app.route("/audio_catalog")
def _audio_catalog_f():
    return render_template("audio_catalog.html")

# Рендер страницы "users_catalog";
@app.route("/users_catalog")
def _users_catalog_f():
    return render_template("users_catalog.html")
