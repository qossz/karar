import os
from pathlib import Path
import imp
from ..Config import Config
from ..utils import load_module, remove_plugin
from . import CMD_HELP, CMD_LIST, SUDO_LIST, l313l, edit_delete, edit_or_reply, reply_id

plugin_category = "tools"

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")

@l313l.ar_cmd(
    pattern="جد بكج (.*)",
    command=("جد بكج", plugin_category),
    info={
        "header": "البحث عن بكج.",
        "description": "لمعرفة هل ان البكج موجود ام لا.",
    },
)
async def findpkg(event):
    pkgname = event.pattern_match.group(1)
    try:
         imp.find_module(pkgname)
         await edit_or_reply(event, f"᯽︙ الباكج موجود ✓\n{pkgname}")
    except ImportError:
         await edit_or_reply(event, f"᯽︙ الباكج غير موجود X \n{pkgname}")

@l313l.ar_cmd(
    pattern="تنصيب$",
    command=("تنصيب", plugin_category),
    info={
        "header": "لتنصيب ملف خارجي.",
        "description": "رد على ملف إضافة خارجي لتثبيته في البوت.",
    },
)
async def install(event):
    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        try:
            # تحميل الملف
            downloaded_file_name = await event.client.download_media(reply_msg, "JoKeRUB/plugins/")
            path = Path(downloaded_file_name)

            # تحقق من عدم وجود أحرف غير صالحة في اسم الملف
            if "(" in downloaded_file_name:
                raise ValueError("الملف يحتوي على () ويبدو أنه مكرر.")

            # استعلام المستخدم لاختيار اسم للبكج
            await edit_or_reply(event, "᯽︙ من فضلك اختر اسمًا للبكج (أو اتركه كما هو):")
            response = await event.client.wait_for_message(from_user=event.sender_id, timeout=30)
            custom_name = response.text.strip()

            # استخدام الاسم المخصص أو الاسم الافتراضي
            if custom_name:
                new_name = f"{custom_name}.py"
            else:
                new_name = f"{path.stem}.py"

            # إعادة تسمية الملف
            new_path = Path(f"JoKeRUB/plugins/{new_name}")
            os.rename(path, new_path)

            # تحميل الموديل الجديد
            load_module(new_name.replace(".py", ""))

            await edit_delete(event, f"᯽︙ تـم تثبيـت المـلف `{new_name}` بنجاح", 10)
        except Exception as e:
            await edit_delete(event, f"**خـطأ:**\n`{str(e)}`", 10)
        finally:
            # تأكد من حذف الملف الأصلي في حال حدوث خطأ
            if path.exists() and path != new_path:
                os.remove(path)

@l313l.ar_cmd(
    pattern="الغاء التنصيب (.*)",
    command=("الغاء التنصيب", plugin_category),
    info={
        "header": "To uninstall a plugin temporarily.",
        "description": "To stop functioning of that plugin and remove that plugin from bot.",
        "note": "To unload a plugin permanently from bot set NO_LOAD var in heroku with that plugin name, give space between plugin names if more than 1.",
        "usage": "{tr}uninstall <plugin name>",
        "examples": "{tr}uninstall markdown",
    },
)
async def unload(event):
    shortname = event.pattern_match.group(1)
    path = Path(f"JoKeRUB/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(event, f"᯽︙ لا يوجد هكذا ملف مع المسار {path} لحذفه")
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"᯽︙ {shortname} تم الغاء تثبيت الملف بنجاح")
    except Exception as e:
        await edit_or_reply(event, f"᯽︙ تم الغاء التثبيت بنجاح {shortname}\n{str(e)}")
