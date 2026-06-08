from django.shortcuts import render
from accounts.decorators import student_required
from accounts.models import StudentProfile
from .livekit import create_room_token


@student_required
def join_meeting(request, room_name):

    profile = StudentProfile.objects.get(auid=request.session["student_auid"])

    token = create_room_token(room_name=room_name,identity=profile.auid)

    return render(
        request,
        "meet/room.html",
        {
            "room_name": room_name,
            "token": token,
            "ws_url": "wss://meet.axror.tech",
            "profile": profile,
        }
    )