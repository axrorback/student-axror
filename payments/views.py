from django.shortcuts import render , get_object_or_404 ,redirect ,reverse
from django.views.decorators.csrf import csrf_exempt
from config import settings
from accounts.decorators import student_required
from .models import Course , Order
from accounts.models import StudentProfile
import requests
import json
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
@student_required
def courses(request):

    course = Course.objects.filter(is_active=True)

    context = {
        "courses":course
    }

    return render(request,"payments/courses.html",context)


@student_required
def pay_course(request, uuid):

    profile = StudentProfile.objects.get(
        auid=request.session["student_auid"])

    course = get_object_or_404(Course,id=uuid,is_active=True,)

    order = Order.objects.create(student=profile,course=course,amount=course.price,)

    response = requests.post(
        settings.CLICK_BASE_URL,
        json={
            "id": str(order.id),
            "amount": int(course.price),
            "payment_method": "click",
            "return_url": request.build_absolute_uri(reverse("payment_success", args=[str(order.id)])),
            "callback_url": request.build_absolute_uri(reverse("payment_callback")),
        },
        timeout=15,
    )

    response.raise_for_status()

    payment = response.json()

    return redirect(payment["payment_link"])

@csrf_exempt
def payment_callback(request):
    try:
        logger.info("BODY: %s", request.body)

        data = json.loads(request.body)

        logger.info("DATA: %s", data)

        order = Order.objects.get(pk=data["order_id"])

        if data["status"] == "paid":
            order.status = Order.Status.PAID
        elif data["status"] == "cancelled":
            order.status = Order.Status.CANCELLED

        order.save(update_fields=["status"])

        return JsonResponse({"success": True})

    except Exception:
        logger.exception("Payment callback error")
        return JsonResponse(
            {"success": False},
            status=500,
        )

@student_required
def payment_success(request, uuid):

    profile = get_object_or_404(
        StudentProfile,
        auid=request.session["student_auid"],
    )

    order = get_object_or_404(
        Order.objects.select_related("course"),
        id=uuid,
        student=profile,
    )

    return render(
        request,
        "payments/success.html",
        {
            "order": order,
        },
    )