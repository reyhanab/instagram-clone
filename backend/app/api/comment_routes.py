from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Comment, db, Post, User, Follow
from app.forms import CommentForm
# from .post_routes import authorized_follower
from .auth_routes import validation_errors_to_error_messages


comment_routes = Blueprint("comments", __name__)


def authorized_follower2(cb):
    """
    Check's if:
        - Post belongs to a Public User or
        - Current user is a follower or
        - Post belongs to current user
    """
    def wrapper(post_id):

        post = Post.query.get(post_id)
        owner = User.query.get(post.user_id)
        is_owner = owner.id == current_user.id

        if not is_owner and owner.is_private and not post.is_story:
            follow = Follow.query.filter_by(
                follower_id=current_user.id, following_id=post.user_id, is_pending=False).first()
            print(follow)
            if not follow:
                return redirect(url_for("auth.unauthorized"))
        return cb(post_id)
    wrapper.__name__ = cb.__name__
    return wrapper


@comment_routes.route("/<int:comment_id>", methods=["PUT"])
@login_required
def edit_comment(comment_id):
    """
    Query for a comment by id and return it

    Use: edit a comment by comment owner
    """
    form = CommentForm()

    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():

        comment = Comment.query.get_or_404(comment_id)
        if comment.user_id == current_user.id:
            comment.comment = form.data["comment"]
            db.session.commit()
            return comment.to_dict()
        return redirect("../auth/unauthorized")


@comment_routes.route("/<int:comment_id>", methods=["DELETE"])
@login_required
def delete_comment(comment_id):
    """
    Query for a comment by id

    Use: delete the comment by comment owner or post owner
    """
    comment = Comment.query.get(comment_id)
    post = Post.query.get(comment.post_id)
    if comment.user_id == current_user.id or post.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        return "Successfully deleted"
    return redirect("../auth/unauthorized")



@comment_routes.route("/<int:post_id>/comments", methods=["GET"])
@login_required
@authorized_follower2
def get_comments(post_id):
    """
    Query for all comments of a post
    """
    print("Here**********************")
    post = Post.query.get_or_404(post_id)
    comments = post.comments
    return {"Comments": [comment.to_dict() for comment in comments]}


@comment_routes.route("/<int:post_id>/comments", methods=["POST"])
@login_required
@authorized_follower2
def add_comment(post_id):
    """
    Query for a post by id

    Creates a comment on the post
    """
    form = CommentForm()
    post = Post.query.get(post_id)

    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        comment = Comment(
            user_id = current_user.id,
            post_id = post.id,
            comment = form.data["comment"]
        )
        db.session.add(comment)
        db.session.commit()
        return comment.to_dict()
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401

