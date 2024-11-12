from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, PostForm, UpdateForm, DeletePostForm, LikeForm, UnlikeForm
from models import db, User, Post 
from sqlalchemy.orm import Session

app = Flask(__name__)
# Configuración de la base de datos y Flask-WTF
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///red_social.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='llave_secreta'

# Inicializar la base de datos (db) y Flask-Login
db.init_app(app)  # Vinculamos la base de datos con la app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige al login si no está autenticado

#Cargar el usuario actual(por flask-login)
@login_manager.user_loader
def load_user(user_id):
    with Session(db.engine) as session:  # Crear sesión con el motor
        return session.get(User, int(user_id))  # Obtener el usuario por ID

#Pagina de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        print(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('index'))  # Redirige al login después del registro
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    form = LoginForm()

    if form.validate_on_submit():
        # Buscar el usuario por nombre de usuario y correo electrónico
        user = User.query.filter(
            (User.username == form.username.data) | (User.email == form.username.data)
        ).first()

        # Verificar si existe el usuario y si la contraseña es correcta
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login exitoso', 'success')

            # Redirigir a la página deseada o al feed
            next_page = request.args.get('next')
            print(f"Redirigiendo a: {next_page}")  # Depuración
            return redirect(next_page) if next_page else redirect(url_for('feed'))
        else:
            flash('Nombre de usuario, correo o contraseña incorrectos', 'danger')

    return render_template('login.html', form=form)

# Cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('login'))

# Página principal (requiere inicio de sesión)
@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    form =  PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)

        db.session.add(post)
        db.session.commit()

        flash('Post creado con exito', 'success')

        return redirect(url_for('feed'))
    
    posts = Post.query.all()
    return render_template('feed.html', form=form, posts=posts)
    
@app.route('/feed/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        flash('No tienes permiso para editar esta publicación', 'danger')
        return redirect(url_for('feed'))
    
    form = UpdateForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('feed'))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('edit_post.html', title='Editar Publicación', form=form, post=post)

@app.route('/feed/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Verificamos que el post pertenece al usuario actual
    if post.user_id != current_user.id:
        flash('No tienes permiso para eliminar esta publicación', 'danger')
        return redirect(url_for('feed'))

    form = DeletePostForm()

    # Si el formulario de eliminación se envía (POST), eliminamos el post
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
        flash('La publicación ha sido eliminada', 'success')
        return redirect(url_for('feed'))

    return redirect(url_for('feed'))


@app.route('/')
def index():
    return redirect(url_for('feed')) if current_user.is_authenticated else redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas si no existen
    app.run(debug=True)