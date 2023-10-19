from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user
from .sendmail import send_verify_mail

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        verification = request.form.get("verification")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                if verification == user.verification_code:
                    user.is_verified = "True"
                    db.session.commit()
                if user.is_verified == "False":
                    flash("Please verify your account.", category="success")
                    return render_template(
                        "login.html", verification_needed="True", user=current_user
                    )
                flash("Logged in succesfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))

            else:
                flash("Incorrect password", category="error")
        else:
            flash(
                "User does not exist. Try again or create a new account.",
                category="error",
            )

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        is_verified = "False"

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email zaten kayitli.", category="error")

        elif len(email) < 4:
            flash("Email 8 karakterden uzun olmalidir.", category="error")
        elif len(first_name) < 2:
            flash("İsim 2 karakterden uzun olmalidir.", category="error")
        elif password1 != password2:
            flash("Şifreler eşleşmiyor.", category="error")

        elif len(password1) < 7:
            flash("Şifreniz en az 8 karakter olmalidir.", category="error")
        else:
            verification_code = send_verify_mail(email)
            is_verified = "False"
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method="sha256"),
                is_verified=is_verified,
                verification_code=verification_code,
            )

            flash(
                "Dogrulama kodu gonderildi! Mail adresinizi dogruladiktan sonra giris yapabilirsiniz.",
                category="success",
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(
                url_for(
                    "auth.login",
                )
            )

    return render_template("sign_up.html", user=current_user)
