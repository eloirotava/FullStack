from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

# caminhos base/instance absolutos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

app = Flask(__name__)

# config básica
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')

# agora usando caminho absoluto pro app.db dentro de instance
db_path = os.path.join(INSTANCE_DIR, 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# MODELOS --------------------------------------------------------------------


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='todo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# HELPERS --------------------------------------------------------------------


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


# ROTAS WEB ------------------------------------------------------------------


@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    tasks = (
        Task.query
        .filter_by(user_id=user_id)
        .order_by(Task.created_at.desc())
        .all()
    )
    return render_template('index.html', tasks=tasks)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        if not email or not password:
            flash('Preencha e-mail e senha.')
            return redirect(url_for('register'))

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('Esse e-mail já está cadastrado.')
            return redirect(url_for('register'))

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Conta criada! Faça login.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Credenciais inválidas.')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['user_email'] = user.email

        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/tasks', methods=['POST'])
@login_required
def create_task():
    title = request.form['title'].strip()
    description = request.form.get('description', '').strip()
    status = request.form.get('status', 'todo')

    if not title:
        flash('Título é obrigatório.')
        return redirect(url_for('index'))

    task = Task(
        title=title,
        description=description,
        status=status,
        user_id=session['user_id'],
    )
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/tasks/<int:task_id>/update', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()

    task.title = request.form.get('title', task.title).strip()
    task.description = request.form.get('description', task.description or '').strip()
    task.status = request.form.get('status', task.status)

    db.session.commit()
    return redirect(url_for('index'))


@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


# API ------------------------------------------------------------------------


@app.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    user_id = session['user_id']
    tasks = (
        Task.query
        .filter_by(user_id=user_id)
        .order_by(Task.created_at.desc())
        .all()
    )
    data = [
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'created_at': t.created_at.isoformat(),
        }
        for t in tasks
    ]
    return jsonify(data)


@app.route('/api/tasks', methods=['POST'])
@login_required
def api_create_task():
    payload = request.get_json() or {}

    title = (payload.get('title') or '').strip()
    description = (payload.get('description') or '').strip()
    status = payload.get('status') or 'todo'

    if not title:
        return jsonify({'error': 'title é obrigatório'}), 400

    task = Task(
        title=title,
        description=description,
        status=status,
        user_id=session['user_id'],
    )
    db.session.add(task)
    db.session.commit()

    return jsonify({'message': 'ok', 'id': task.id}), 201


# MAIN -----------------------------------------------------------------------


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)

