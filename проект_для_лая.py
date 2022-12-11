import sys
import sqlite3
import csv

from PyQt5 import uic
from csv import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel


class Podrobnee(QMainWindow): # окно подробнее, в котором рассказывается о темпераментах
    def __init__(self, temp, k):
        super().__init__()
        uic.loadUi("ui6.ui", self)
        self.k = k
        self.k += 1
        self.name_temp = temp
        if self.name_temp == "тест не пройден" or self.name_temp == "":
            self.label.setText(
                """
К сожалению, вы не прошли тест до конца
и мы не можем определить ваш темперамент"""
            )
            self.label_2.setText(
                """
                Всего существует четыре типа темперамента.
                Холерики - горячие, несдержанные, смелые, задорные.
                Сангвинники - уравновешенные, оптимистичные, жизнерадостные.
                Фегматики - спокойные, сдержанные.
                Меланхолики - чувствительные, неэнергичные, склонные к унынию."""
            )
            self.name_temp == "тест не пройден"
        elif self.name_temp == "холерик":
            self.label.setText("Описание холерика")
            self.label_2.setText(
                """
                Холерик — горячий, несдержанный, смелый, задорный. 
                Такие люди инициативны, с азартом берутся за любую работу (кроме рутинной) 
                и с легкостью преодолевают трудности.
                Они способны схватывать информацию на лету, обладают лидерскими качествами, 
                однако нетерпеливы, вспыльчивы и подвержены эмоциональным срывам."""
            )
        elif self.name_temp == "сангвинник":
            self.label.setText("Описание сангвинника")
            self.label_2.setText(
                """
                Сангвиник — уравновешенный, оптимистичный, жизнерадостный.
                Сангвинический темперамент характеризует человека веселого,
                эмоционального, общительного, живущего настроением.
                Он легко переживает неудачи, создает приятный микроклимат в любом коллективе,
                но не всегда выполняет свои обещания, порой слишком поспешен в делах 
                и суждениях и излишне самоуверен."""
            )
        elif self.name_temp == "флегматик":
            self.label.setText("Описание флегматика")
            self.label_2.setText(
                """
                Флегматик — спокойный, сдержанный.
                Он плохо приспосабливается к новой обстановке и в неблагоприятных
                условиях может стать пассивным и вялым,
                при этом отличается самообладанием, терпеливостью, предприимчивостью.
                В обществе флегматик в меру общителен,
                не любит пустословия и не подвержен панике в стрессовых ситуациях."""
            )
        elif self.name_temp == "меланхолик":
            self.label.setText("Описание меланхолика")
            self.label_2.setText(
                """
                Меланхолик — чувствительный, неэнергичный, болезненно реагирующий
                на неприятности, склонный к унынию.
                Люди с меланхолическим темпераментом подвержены пессимизму,
                излишне подозрительны и ревнивы,
                но обладают аналитическим мышлением, творчески подходят к работе,
                тонко чувствуют и доводят дело до завершения."""
            )
        self.pushButton.clicked.connect(self.back)

    def back(self): # возврат к окну Eend
        self.close()
        self.kon = Eend(self.name_temp, self.k)
        self.kon.show()


class Statics(QMainWindow): # статистика, окно с csv таблицей
    def __init__(self, temp, k):
        super().__init__()
        uic.loadUi("ui5.ui", self)
        self.name_temp = temp
        self.k = k
        self.k += 1
        self.con = sqlite3.connect("new1.db")
        cur = self.con.cursor()
        self.kol = list(cur.execute(f"""select COUNT(*) from user"""))[0][0]
        self.fleg = list(
            cur.execute(
                f"""select COUNT(*) as fleg from results where temperament == "флегматик" """
            )
        )[0][0]
        self.xol = list(
            cur.execute(
                f"""select COUNT(*) as xol from results where temperament == "холерик" """
            )
        )[0][0]
        self.sang = list(
            cur.execute(
                f"""select COUNT(*) as sang from results where temperament == "сангвинник" """
            )
        )[0][0]
        self.melan = list(
            cur.execute(
                f"""select COUNT(*) as melan from results where temperament == "меланхолик" """
            )
        )[0][0]
        self.id = list(cur.execute(f"""select id from user where id == {self.kol}"""))[
            0
        ][0]
        self.label.setText(
            f"""
                Всего холериков: {self.xol}
                Всего сангвинников: {self.sang}
                Всего флегматиков: {self.fleg}
                Всего меланхоликов: {self.melan}"""
        )
        self.loadTable("resuts.csv")
        if self.name_temp == "тест не пройден" or self.name_temp == "":
            self.label_2.setText(
                f"Вы не прошли тест полностью, но можете увидеть все результаты. Ваш id {self.id}"
            )
            self.name_temp == "тест не пройден"
        elif self.name_temp == "холерик":
            self.label_2.setText(
                f"Вы холерик, можете увидеть другие результаты. Ваш id {self.id}"
            )
        elif self.name_temp == "сангвинник":
            self.label_2.setText(
                f"Вы сангвинник, можете увидеть другие результаты. Ваш id {self.id}"
            )
        elif self.name_temp == "флегматик":
            self.label_2.setText(
                f"Вы флегматик, можете увидеть другие результаты. Ваш id {self.id}"
            )
        elif self.name_temp == "меланхолик":
            self.label_2.setText("Вы меланхолик, можете увидеть другие результаты")
        self.pushButton.clicked.connect(self.back)

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setHorizontalHeaderLabels(
                ["id", "name", "gender", "age", "temperament"]
            )
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()

    def back(self):
        self.close()
        self.kon = Eend(self.name_temp, self.k)
        self.kon.show()


class Eend(QMainWindow): # конечное окно
    def __init__(self, sp, k=0):
        super().__init__()
        uic.loadUi("ui4.ui", self)
        self.k = k
        self.temp = 0
        self.name_temp = ""
        self.pushButton_3.clicked.connect(self.mn_wn) # переход на главное окно(перовое)
        self.sp = sp
        if (
            self.sp != "холерик"
            and self.sp != "сангвинник"
            and self.sp != "флегматик"
            and self.sp != "меланхолик"
            and self.sp != "тест не пройден"
            and self.k == 0
        ):
            if sum(self.sp) != 12:
                self.label_2.setText(
                    """
        Вы не прошли наш тест полнотстью,
        поэтому мы не можем вам предоставить
        достоверные резльтаты."""
                )
                self.name_temp = "тест не пройден"
            elif max(self.sp) == self.sp[0]:
                self.label_2.setText(
                    """
                Вы холерик"""
                )
                self.name_temp = "холерик"
            elif max(self.sp) == self.sp[1]:
                self.label_2.setText(
                    """
                Вы сангвинник"""
                )
                self.name_temp = "сангвинник"
            elif max(self.sp) == self.sp[2]:
                self.label_2.setText(
                    """
                Вы флегматик"""
                )
                self.name_temp = "флегматик"
            elif max(self.sp) == self.sp[3]:
                self.label_2.setText(
                    """
                Вы меланхолик"""
                )
                self.name_temp = "меланхолик"
            con = sqlite3.connect("new1.db")
            cur = con.cursor()
            cur.execute(
                f"""INSERT INTO results (temperament) VALUES('{self.name_temp}');"""
            )
            self.kol = list(cur.execute(f"""select COUNT(*) from user"""))[0][0]
            self.id = list(
                cur.execute(f"""select id from user where id == {self.kol}""")
            )[0][0]
            self.name = list(
                cur.execute(f"""select user_name from user where id == {self.id}""")
            )[0][0]
            self.gender = list(
                cur.execute(f"""select gender from user where id == {self.id}""")
            )[0][0]
            self.age = list(
                cur.execute(f"""select age from user where id == {self.id}""")
            )[0][0]
            self.lst = [self.id, self.name, self.gender, self.age, self.name_temp]
            with open("resuts.csv", "a", newline="\n", encoding="utf8") as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
                )
                writer.writerow(self.lst)
            con.commit()
            con.close()
        else:
            if self.sp == "тест не пройден" or self.sp == "":
                self.label_2.setText(
                    """
        Вы не прошли наш тест полнотстью,
        поэтому мы не можем вам предоставить 
        достоверные резльтаты."""
                )
                self.name_temp == "тест не пройден"
            elif self.sp == "холерик":
                self.label_2.setText(
                    """
                Вы холерик"""
                )
                self.name_temp = "холерик"
            elif self.sp == "сангвинник":
                self.label_2.setText(
                    """
                Вы сангвинник"""
                )
                self.name_temp = "сангвинник"
            elif self.sp == "флегматик":
                self.label_2.setText(
                    """
                Вы флегматик"""
                )
                self.name_temp = "флегматик"
            elif self.sp == "меланхолик":
                self.label_2.setText(
                    """
                Вы меланхолик"""
                )
                self.name_temp = "меланхолик"
        self.pushButton.clicked.connect(self.podr)
        self.pushButton_2.clicked.connect(self.stat)

    def mn_wn(self): # переход к главному окну
        self.close()
        self.mn_wind = MyWidget()
        self.mn_wind.show()

    def podr(self):  # переход к новому окну(кнопка подробнее)
        self.close()
        self.podr = Podrobnee(self.name_temp, self.k)
        self.podr.show()

    def stat(self):  # переход к новому окну (кнопка статистика)
        self.close()
        self.statis = Statics(self.name_temp, self.k)
        self.statis.show()

class Qst12(QMainWindow):
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui7.ui", self)
        self.k = 0
        self.sp = sp
        self.pixmap = QPixmap('temp.jpg')
        self.label.setPixmap(self.pixmap)
        self.pushButton.clicked.connect(self.end1)

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[2] += 1
        elif self.radioButton_3.isChecked():
            self.sp[3] += 1
        elif self.radioButton_4.isChecked():
            self.sp[1] += 1
        self.close()
        self.kon = Eend(self.sp, self.k)
        self.kon.show()

class Qst11(QMainWindow):  # последний (одиннадцатый) вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.k = 0
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("стремитесь к новому")
        self.radioButton_2.setText("у вас всегда бодрое настроение")
        self.radioButton_3.setText("любите аккуратность")
        self.radioButton_4.setText("робки, малоактивны")
        if self.radioButton.isChecked(): 
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.pushButton_2.clicked.connect(self.end1)
        self.pushButton.clicked.connect(self.cont2)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst12(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp, self.k)
        self.kon.show()


class Qst10(QMainWindow):  # десятый вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("инициативны и решительны")
        self.radioButton_2.setText("быстро схватываете новое")
        self.radioButton_3.setText("не любите попусту болтать, молчаливы")
        self.radioButton_4.setText("одиночество переносите легко")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst11(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst9(QMainWindow):  # девятый вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("быстро решаете и действуете")
        self.radioButton_2.setText("в сложной обстановке сохраняете самообладание")
        self.radioButton_3.setText("ровные отношения со всеми")
        self.radioButton_4.setText("необщительны")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst10(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst8(QMainWindow):  # восьмой вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("вам присуща несобранность")
        self.radioButton_2.setText("настойчивы в достижении цели")
        self.radioButton_3.setText("вялы, малоподвижны")
        self.radioButton_4.setText("ищите сочувствия других")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst9(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst7(QMainWindow):  # седьмой вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("работаете рывками")
        self.radioButton_2.setText("за любое новое дело беретесь с увлечением")
        self.radioButton_3.setText("попусту сил не растрачиваете")
        self.radioButton_4.setText("у вас тихая, слабая речь")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst8(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst6(QMainWindow):  # шестой вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("у вас быстрая, страстная речь")
        self.radioButton_2.setText("в новую работу включаетесь быстро")
        self.radioButton_3.setText("порыв сдерживаете легко")
        self.radioButton_4.setText("очень впечатлительны")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst7(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst5(QMainWindow):  # пятый вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("у вас выразительная мимика")
        self.radioButton_2.setText("быстрая, громкая речь с живыми жестами")
        self.radioButton_3.setText("медленно включаетесь в работу")
        self.radioButton_4.setText("очень обидчивы")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst6(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst4(QMainWindow):  # четвертый вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("к недостаткам нетерпимы")
        self.radioButton_2.setText("работоспособны, выносливы")
        self.radioButton_3.setText("в своих интересы постоянны")
        self.radioButton_4.setText("легко ранимы, чувствительны")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst5(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst3(QMainWindow):  # третий вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.radioButton.setText("вы обладатель порывистых, резких движений")
        self.radioButton_2.setText("быстро засыпаете")
        self.radioButton_3.setText("вам тяжело приспособиться к новой обстановке")
        self.radioButton_4.setText("покорны")
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst4(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst2(QMainWindow):  # второй вопрос
    def __init__(self, sp):
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.sp = sp
        self.radioButton.setChecked(False)
        self.radioButton_2.setChecked(False)
        self.radioButton_3.setChecked(False)
        self.radioButton_4.setChecked(False)
        self.sp2 = self.sp
        self.radioButton.setText("если что-то перестает интересовать, быстро остываете")
        self.radioButton_2.setText("незлопамятны")
        self.radioButton_3.setText(
            "строго придерживаетесь системы в работе и распорядка дня"
        )
        self.radioButton_4.setText(
            "приспосабливаетесь невольно к характеру собеседника"
        )  # с 621 по данную строку - добавление новых вариантов ответа
        self.pushButton.clicked.connect(self.cont2)
        self.pushButton_2.clicked.connect(self.end1)

    def cont2(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText("Ответьте на вопрос или завершите тест.")
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst = Qst3(self.sp)
            self.qst.show()

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Qst1(QMainWindow):  # п��рвый вопрос
    def __init__(self):
        self.sp = [0, 0, 0, 0]  # счетчик ответов, который позже считается и даст ответ
        super().__init__()
        uic.loadUi("ui3.ui", self)
        self.pushButton.clicked.connect(self.cont1)  # кнопка продолжения теста
        self.pushButton_2.clicked.connect(self.end1)  # кнопка окончания теста

    def cont1(self):
        if (
            self.radioButton.isChecked()
            == self.radioButton_2.isChecked()
            == self.radioButton_3.isChecked()
            == self.radioButton_4.isChecked()
            == False
        ):
            self.label_2.setText(
                "Ответьте на вопрос или завершите тест."
            )  # если пользователь ничего не нажал
        else:
            if self.radioButton.isChecked():
                self.sp[0] += 1
            elif self.radioButton_2.isChecked():
                self.sp[1] += 1
            elif self.radioButton_3.isChecked():
                self.sp[2] += 1
            elif self.radioButton_4.isChecked():
                self.sp[3] += 1
            self.close()
            self.qst2 = Qst2(self.sp)
            self.qst2.show()
            # далее аналогично до класса Qst11

    def end1(self):
        if self.radioButton.isChecked():
            self.sp[0] += 1
        elif self.radioButton_2.isChecked():
            self.sp[1] += 1
        elif self.radioButton_3.isChecked():
            self.sp[2] += 1
        elif self.radioButton_4.isChecked():
            self.sp[3] += 1
        self.close()
        self.kon = Eend(self.sp)
        self.kon.show()


class Test(QMainWindow):  # окно с информацией о тесте
    def __init__(self):
        super().__init__()
        uic.loadUi("ui2.ui", self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.close()
        self.qst = Qst1()  # переход к первому вопросу
        self.qst.show()


class MyWidget(QMainWindow):  # создание начального окна
    def __init__(self):
        super().__init__()
        uic.loadUi("ui1.ui", self)  # подключение ui - файла
        self.pushButton_4.clicked.connect(self.res)

    def res(self):
        self.a = self.lineEdit.text()
        self.b = str(self.comboBox.currentText())
        self.c = self.spinBox.text()
        if self.a == "" or self.c == 0 or self.a[0].isdigit() or self.c[0] == "0":
            self.label_5.setText(
                "Пожалуйста, введите ваши данные правильно"
            )  # показ ошибки, если пользовател неправильно ввел данные
        else:
            con = sqlite3.connect("new1.db")
            cur = con.cursor()
            cur.execute(
                f"""INSERT INTO user (user_name, gender, age) VALUES('{self.a.capitalize()}', '{self.b}', {self.c});"""
            )  # добавление пользователя в базу данных
            con.commit()
            con.close()
            self.close()
            self.test = Test()
            self.test.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":  # начало работы с pyqt
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
