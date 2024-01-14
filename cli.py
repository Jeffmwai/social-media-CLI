# cli.py
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Post, Comment, Like, Follow
from sqlalchemy import func

DATABASE_URI = "sqlite:///social_media.db"

class ContextObject:
    def __init__(self, engine, session):
        self.engine = engine
        self.session = session

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = ContextObject(engine, Session())

@cli.command()
@click.pass_context
def init_db(ctx):
    from models import Base
    Base.metadata.create_all(ctx.obj.engine)
    click.echo("Database initialized successfully!")

@cli.command()
@click.pass_context
@click.option('--username', prompt='Enter username', help='Username of the user')
@click.option('--email', prompt='Enter email', help='Email of the user')
def create_user(ctx, username, email):
    new_user = User(username=username, email=email)
    ctx.obj.session.add(new_user)
    ctx.obj.session.commit()
    click.echo(f"User {username} created successfully!")

@cli.command()
@click.pass_context
@click.option('--title', prompt='Enter title', help='Title of the post')
@click.option('--content', prompt='Enter content', help='Content of the post')
@click.option('--author', prompt='Enter author username', help='Username of the author')
def create_post(ctx, title, content, author):
    user = ctx.obj.session.query(User).filter_by(username=author).first()
    if user:
        new_post = Post(title=title, content=content, author=user)
        ctx.obj.session.add(new_post)
        ctx.obj.session.commit()
        click.echo(f"Post {title} created successfully by {author}!")
    else:
        click.echo(f"Author {author} not found!")

@cli.command()
@click.pass_context
@click.option('--follower', prompt='Enter username of the follower', help='Username of the follower')
@click.option('--followee', prompt='Enter username of the user to be followed', help='Username of the user to be followed')
def follow_user(ctx, follower, followee):
    follower = ctx.obj.session.query(User).filter_by(username=follower).first()
    followee = ctx.obj.session.query(User).filter_by(username=followee).first()
    if follower and followee:
        follower.following.append(followee)
        ctx.obj.session.commit()
        click.echo(f"{follower.username} is now following {followee.username}!")
    else:
        click.echo(f"Invalid follower or followee! Please check your inputs.")

@cli.command()
@click.pass_context
@click.option('--user', prompt='Enter username of the user who liked', help='Username of the user who liked')
@click.option('--post', prompt='Enter post title to be liked', help='Title of the post to be liked')
def like_post(ctx, user, post):
    user = ctx.obj.session.query(User).filter_by(username=user).first()
    post = ctx.obj.session.query(Post).filter_by(title=post).first()
    if user and post:
        user.liked_posts.append(post)
        ctx.obj.session.commit()
        click.echo(f"{user.username} liked the post {post.title}!")
    else:
        click.echo(f"Invalid user or post! Please check your inputs.")

@cli.command()
@click.pass_context
@click.option('--post', prompt='Enter post title for the comment', help='Title of the post for the comment')
@click.option('--author', prompt='Enter author username', help='Username of the comment author')
@click.option('--content', prompt='Enter comment content', help='Content of the comment')
def create_comment(ctx, post, author, content):
    post = post.strip()
    post_obj = ctx.obj.session.query(Post).filter(func.lower(Post.title) == func.lower(post)).first()
    user_obj = ctx.obj.session.query(User).filter_by(username=author).first()
    if post_obj and user_obj:
        new_comment = Comment(content=content, post=post_obj, author=user_obj)
        ctx.obj.session.add(new_comment)
        ctx.obj.session.commit()
        click.echo(f"Comment created successfully by {author} on post {post_obj.title}!")
    else:
        click.echo(f"Invalid post or author! Please check your inputs.")

@cli.command()
@click.pass_context
@click.option('--username', prompt='Enter username', help='Username of the user')
def show_relationships(ctx, username):
    user = ctx.obj.session.query(User).filter_by(username=username).first()
    if user:
        click.echo(f"Relationships of user {username}:")

        # Display followers
        followers = [follower.username for follower in user.followers]
        click.echo(f"Followers: {', '.join(followers)}")

        # Display following
        following = [followee.username for followee in user.following]
        click.echo(f"Following: {', '.join(following)}")

        # Display liked posts
        liked_posts = [post.title for post in user.liked_posts]
        click.echo(f"Liked Posts: {', '.join(liked_posts)}")
    else:
        click.echo(f"User {username} not found!")        

if __name__ == "__main__":
    cli(obj=ContextObject(engine, Session()))
