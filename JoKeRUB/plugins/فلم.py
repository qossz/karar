#JoKeRUB ©
#By Reda telegram: @rd0r0

from telethon.tl.custom import Button
from cryptography.fernet import Fernet
import requests
from html_telegraph_poster.upload_images import upload_image
import random
from JoKeRUB import l313l
import asyncio
from ..core.managers import edit_delete, edit_or_reply

valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]

ek = "ayD8OiHzrmRxNWUlhbgXY__xzObPjLxd87kj2ipE9wk="
ea = "gAAAAABkkpU1sfechRmGwMJB3XPOylswN2TwCioE9-EBmNudPKr537aSI9Tf_tVyB39nv1p_5Oro1ZGIG2cNduPbF-fhk4onPBmDOJSP3fwaSznl1Mu8FFsEzKPh4qXeWT8TgUF4nma2"

from telethon.tl.custom import Button
from cryptography.fernet import Fernet
import requests
from html_telegraph_poster.upload_images import upload_image
import random
from JoKeRUB import l313l
import asyncio
from ..core.managers import edit_delete, edit_or_reply

valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]

ek = "ayD8OiHzrmRxNWUlhbgXY__xzObPjLxd87kj2ipE9wk="
ea = "gAAAAABkkpU1sfechRmGwMJB3XPOylswN2TwCioE9-EBmNudPKr537aSI9Tf_tVyB39nv1p_5Oro1ZGIG2cNduPbF-fhk4onPBmDOJSP3fwaSznl1Mu8FFsEzKPh4qXeWT8TgUF4nma2"

@l313l.ar_cmd(pattern="(فلم|مسلسل)")
async def get_movie_or_series(event):
    # قراءة النص بعد الأمر
    content_type = event.pattern_match.group(1).strip()

    await event.edit(f"يرجى الانتظار، جاري البحث عن {content_type}... يمكنك اختيار نوع البحث:\n\n"
                     "• أكثر شهرة\n"
                     "• أكثر مشاهدة\n"
                     "• أعلى تقييمًا")

    # تشفير API key
    dk = ek.encode()
    nk = ea.encode()
    cipher_suite = Fernet(dk)
    api_key = cipher_suite.decrypt(nk).decode()

    # تحديد نوع المحتوى (فلم أو مسلسل)
    if content_type == "فلم":
        url_base = "https://api.themoviedb.org/3/movie"
        type_name = "فيلم"
    else:  # مسلسل
        url_base = "https://api.themoviedb.org/3/tv"
        type_name = "مسلسل"

    # استعلام جلب البيانات بناءً على الفئة المحددة
    if "أكثر شهرة" in event.text:
        url_category = "popular"
    elif "أكثر مشاهدة" in event.text:
        url_category = "now_playing" if content_type == "فلم" else "on_the_air"
    else:  # أعلى تقييمًا
        url_category = "top_rated"

    url = f"{url_base}/{url_category}?api_key={api_key}&language=ar&page=1"
    response = requests.get(url)
    results = response.json()["results"]

    # اختيار عشوائي
    random_content = random.choice(results)
    content_id = random_content["id"]
    url_content_details = f"{url_base}/{content_id}?api_key={api_key}&language=ar"
    response_content_details = requests.get(url_content_details)
    content = response_content_details.json()

    # استخراج البيانات بناءً على النوع
    content_title = random_content["title"] if content_type == "فلم" else random_content["name"]
    rating = content["vote_average"]
    overview = content["overview"] or "-"
    release_date = content["release_date"] if content_type == "فلم" else content["first_air_date"]
    poster_path = content["poster_path"]
    content_poster = f"https://image.tmdb.org/t/p/w500{poster_path}"

    # تحميل الصورة إذا كانت بتنسيق مناسب
    if any(content_poster.endswith(ext) for ext in valid_extensions):
        try:
            content_poster = upload_image(content_poster)
        except BaseException:
            content_poster = None
    else:
        content_poster = "https://telegra.ph/file/15480332b663adae49205.jpg"

    # تنسيق الرسالة
    content_text = f"الاسم: {content_title}\nالسنة: {release_date}\nالتقييم: {rating}\nالقصة:\n{overview}"

    await event.delete()

    try:
        await l313l.tgbot.send_message(
            event.chat_id,
            f"{type_name} من فئة: {url_category}\n{content_text}",
            file=content_poster,
            force_document=False,
            link_preview=False,
        )
    except ValueError:
        await l313l.send_message(
            event.chat_id,
            f"{type_name} من فئة: {url_category}\n{content_text}",
            file=content_poster,
            force_document=False,
            link_preview=False,
        )
