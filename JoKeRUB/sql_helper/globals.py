try:
    from . import BASE, SESSION
except ImportError as e:
    raise AttributeError from e

from sqlalchemy import Column, String, UnicodeText


class Globals(BASE):
    __tablename__ = "globals"
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, variable, value):
        self.variable = str(variable)
        self.value = value


# إصلاح: تمرير bind لإنشاء الجدول في قاعدة البيانات المرتبطة بالجلسة
Globals.__table__.create(bind=SESSION.bind, checkfirst=True)


def gvarstatus(variable):
    """
    ترجع قيمة المتغير من جدول globals.
    إذا لم يوجد، ترجع None.
    """
    try:
        result = SESSION.query(Globals).filter(
            Globals.variable == str(variable)
        ).first()
        return result.value if result else None
    except BaseException:
        return None
    finally:
        SESSION.close()


def addgvar(variable, value):
    """
    تضيف متغيرًا جديدًا أو تحدّث قيمة المتغير إذا كان موجودًا.
    """
    existing = SESSION.query(Globals).filter(
        Globals.variable == str(variable)
    ).one_or_none()

    if existing:
        delgvar(variable)

    adder = Globals(str(variable), value)
    SESSION.add(adder)
    SESSION.commit()


def delgvar(variable):
    """
    تحذف المتغير من الجدول إذا كان موجودًا.
    """
    rem = SESSION.query(Globals).filter(
        Globals.variable == str(variable)
    ).delete(synchronize_session="fetch")

    if rem:
        SESSION.commit()
