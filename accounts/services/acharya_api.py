import requests

BASE = "https://acharyajava.uz/AcharyaInstituteUZB/api"

class AcharyaAuthError(Exception):
    pass

def acharya_authenticate(username: str, password: str) -> dict:
    r = requests.post(
        f"{BASE}/authenticate",
        json={"username": username, "password": password},
        timeout=15,
    )
    data = r.json()

    if r.status_code != 200 or not data.get("success"):
        raise AcharyaAuthError("Login yoki parol noto‘g‘ri (yoki API xato).")

    d = data["data"]
    return {
        "auid": d["userName"],          # ABT24CCS008
        "user_id": d.get("userId"),     # 745
        "token": d["token"],            # JWT
        "role": d.get("role"),          # Student
    }


def acharya_get_student_details(auid: str, token: str) -> dict:

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    r = requests.get(
        f"{BASE}/student/getStudentDetailsByAuid/{auid}",
        headers=headers,
        timeout=15,
    )
    data = r.json()

    if r.status_code != 200 or not data.get("success"):
        raise AcharyaAuthError("Student details olinmadi (token yoki API xato).")

    d = data["data"]

    return {
        "student_id": d.get("student_id"),  # 689
        "full_name": d.get("student_name") or d.get("candidate_name") or "",
        "acharya_email": d.get("acharya_email") or None,
        "mobile": str(d.get("mobile") or ""),
        "program_name": d.get("program_name") or "",
        "specialization": d.get("program_specialization_name") or "",
        "ac_year": d.get("ac_year") or "",
        "current_city": d.get("current_city_name") or "",
    }
