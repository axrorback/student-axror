from django.shortcuts import render , redirect , get_object_or_404
from accounts.decorators import student_required
from codepaste.models import CodePaste
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from accounts.models import StudentProfile


def get_current_student(request):
    profile_id = request.session.get("student_profile_id")

    if not profile_id:
        return None

    return StudentProfile.objects.filter(id=profile_id).first()

@student_required
def create_paste(request):

    student = StudentProfile.objects.get(
        id=request.session["student_profile_id"]
    )

    if request.method == "POST":

        language = request.POST.get("language")
        code = request.POST.get("code")

        paste = CodePaste.objects.create(
            user=student,
            language=language,
            code=code,
            expire_at=timezone.now() + timedelta(hours=2)
        )

        return redirect(
            "share_paste",
            username=student.auid,
            language=language,
            id=paste.id
        )

    return render(request, "codepaste/create.html")



def share_paste(request, username, language, id):

    paste = get_object_or_404(
        CodePaste,
        id=id,
        user__auid=username,
        language=language
    )

    expired = False

    if paste.is_expired():
        expired = True

        if paste.is_active:
            paste.is_active = False
            paste.save(update_fields=["is_active"])

    return render(
        request,
        "codepaste/detail.html",
        {
            "paste": paste,
            "expired": expired
        }
    )