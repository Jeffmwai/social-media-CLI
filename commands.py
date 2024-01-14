# commands.py
import click
from sqlalchemy import func
from models import User, Post, Comment, Like, Follow, ContextObject

def init_db(context_obj):
    from models import Base
    Base.metadata.create_all(context_obj.engine)
    click.echo("Database initialized successfully!")

def create_user(context_obj, username, email):
    new_user = User(username=username, email=email)
    context_obj.session.add(new_user)
    context_obj.session.commit()
    click.echo(f"User {username} created successfully!")

def create_post(context_obj, title, content, author):
    user = context_obj.session.query(User).filter_by(username=author).first()
    if user:
        new_post = Post(title=title, content=content, author=user)
        context_obj.session.add(new_post)
        context_obj.session.commit()
        click.echo(f"Post {title} created successfully by {author}!")
    else:
        click.echo(f"Author {author} not found!")

def follow_user(context_obj, follower, followee):
    follower = context_obj.session.query(User).filter_by(username=follower).first()
    followee = context_obj.session.query(User).filter_by(username=followee).first()
    if follower and followee:
        follower.following.append(followee)
        context_obj.session.commit()
        click.echo(f"{follower.username} is now following {followee.username}!")
    else:
        click.echo(f"Invalid follower or followee! Please check your inputs.")

def like_post(context_obj, user, post):
    user = context_obj.session.query(User).filter_by(username=user).first()
    post = context_obj.session.query(Post).filter_by(title=post).first()

    if user and post:
        user.liked_posts.append(post)
        context_obj.session.commit()
        click.echo(f"{user.username} liked the post {post.title}!")
    else:
        click.echo(f"Invalid user or post! Please check your inputs.")

def create_comment(context_obj, post, author, content):
    post = post.strip()
    post_obj = context_obj.session.query(Post).filter(func.lower(Post.title) == func.lower(post)).first()
    user_obj = context_obj.session.query(User).filter_by(username=author).first()
    if post_obj and user_obj:
        new_comment = Comment(content=content, post=post_obj, author=user_obj)
        context_obj.session.add(new_comment)
        context_obj.session.commit()
        click.echo(f"Comment created successfully by {author} on post {post_obj.title}!")
    else:
        click.echo(f"Invalid post or author! Please check your inputs.")
