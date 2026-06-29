from django.utils import timezone


def new_lesson_message(lesson):

    start = timezone.localtime(lesson.starts_at)
    end = timezone.localtime(lesson.ends_at)

    return f"""
📚 <b>New Lesson Scheduled</b>

━━━━━━━━━━━━━━━━━━

📖 <b>Lesson</b>
{lesson.title}

👥 <b>Group</b>
{lesson.group.name}

👨‍🏫 <b>Teacher</b>
{lesson.teacher.get_full_name() or lesson.teacher.username}

📅 <b>Date</b>
{start:%d %B %Y}

🕒 <b>Time</b>
{start:%H:%M} - {end:%H:%M}

📍 <b>Location</b>
{lesson.location or "-"}

━━━━━━━━━━━━━━━━━━

📝 <b>Description</b>

{lesson.content or "No description"}

━━━━━━━━━━━━━━━━━━

🚀 See you in class!
"""