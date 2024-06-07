from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
app = Flask(__name__)#создаёт экземпляр
application = app#— присваивает переменной application значение экземпляра
app.config.from_pyfile("config.py")#подгружает секретный ключ для шифрования данных между клиентом и сервером
login_manager = LoginManager()
login_manager.login_view = 'enter'# установка страницы вхова #что делает функция
login_manager.login_message = 'Пожалуйста, авторизуйтесь.'
login_manager.login_message_category = 'warning'#категория сообщения
login_manager.init_app(app)
"""импортирует необходимые модули и функции из библиотеки Flask для создания веб-приложения.
"""

#для чего нужен сеекретный ключ


class User(UserMixin):#класс для работы с фласк логин
    def __init__(self, login, user_id):
        self.login = login
        self.id = user_id

@login_manager.user_loader#загрузка пользователя по его ID
def load_user(user_id):#что делает функция
    for user_data in users_list():
        if user_data["user_id"] == user_id:
            return User(user_data['login'], user_data['user_id'])
    return None
def users_list():
    return [{"user_id": "3", "login": "login", "password": "password"}, {"user_id": "4", "login": "user", "password":"qwerty"}]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/counter')
def counter():
    if not("counter" in session):
        session["counter"] = 1
    else:
        session["counter"] += 1
    return render_template('counter.html')

@app.route('/enter', methods=['post', 'get'])
def enter():
    massage=''
    if request.method == 'POST':
        user_login = request.form['login']
        user_password = request.form['password']
        check_remember = True if request.form.get('user_remember') else False
        for user in users_list():
            if user_login == user['login'] and user_password == user['password']:
                login_user(User(user['login'], user['user_id']), remember=check_remember )#что делает функция #что делает функция remember
                flash("Вход выполнен успешно", "success")
                return redirect(request.args.get('next', url_for('index')))
        massage = 'Введены неверные данные'
        flash(massage, "danger")
    return render_template('enter.html')

@app.route('/logout')
def logout():
    logout_user()#что делает функция
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True)