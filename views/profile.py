# views/profile.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.profile import Profile
from forms.profile_form import ProfileForm
from utils.uploads import save_image, remove_file_safe

@login_required
def profile_view():
    # só exibe; cria o Profile se ainda não existir (evita None no template)
    prof = current_user.profile
    if prof is None:
        prof = Profile(user=current_user)
        db.session.add(prof)
        db.session.flush()
    return render_template("profile.html", profile=prof)

@login_required
def profile_edit():
    prof = current_user.profile
    if prof is None:
        prof = Profile(user=current_user)
        db.session.add(prof)
        db.session.flush()

    form = ProfileForm()

    if request.method == "POST" and form.validate_on_submit():
        prof.telefone    = form.telefone.data or None
        prof.instituicao = form.instituicao.data or None
        prof.cargo       = form.cargo.data or None
        prof.bio         = form.bio.data or None

        file = form.foto.data
        if file:
            remove_file_safe(prof.foto)
            remove_file_safe(prof.foto_thumb)
            filename, thumb = save_image(file_storage=file, user_name=current_user.nome)
            prof.foto = filename
            prof.foto_thumb = thumb
        elif not prof.foto and not prof.foto_thumb:
            _, thumb = save_image(file_storage=None, user_name=current_user.nome)
            prof.foto_thumb = thumb

        db.session.commit()
        flash("Perfil atualizado com sucesso.", "success")
        return redirect(url_for("users.profile"))

    return render_template("profile_edit.html", form=form, profile=prof)
