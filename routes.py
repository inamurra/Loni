from flask import render_template, url_for, flash, redirect
from network import app, db
from network.forms import PostForm
from network.models import Post
from flask_login import login_user, current_user, logout_user, login_required


    def __repr__(self):
        return f"User('{self.username}')"



    #def __repr__(self):
        return f"Vlan('{self.name}', '{self.date_created}')"


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/vlan")
def vlan():
    return render_template('vlan.html', title='vlan config')

@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    form = NewuserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password='hashed_password')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('newuser.html', title='newuser', form=form)

@app.route("/newuser")
def newuser():
  form = NewuserForm()
  return render_template('newuser.html', title='newuser', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user and check_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/account")
@login_required
def account():
   return render_template('account.html', title='Account')


@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(ID=form.ID.data, title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('vlan has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post1.html', title='New Vlan',
                           form=form, legend='New Vlan')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('vlan has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('vlan has been deleted!', 'success')
    return redirect(url_for('home'))
