
"""
1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;	--pygal--

2. Implementati o solutie care sa va avertizeze automat cand stocul unui produs este mai mic decat o
limita minima, predefinita per produs. Limita sa poata fi variabila (per produs). Preferabil sa
transmita automat un email de avertizare;

3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului) ; 	--SMTP--
"""

from datetime import datetime
import pygal
import smtplib
import tempfile


class Stoc:
    """Tine stocul unui depozit"""

    def __init__(self, prod, categ, um='Buc', sold=0):
        self.prod = prod			# parametri cu valori default ii lasam la sfarsitul listei
        self.categ = categ  		# fiecare instanta va fi creata obligatoriu cu primii trei param.
        self.sold = sold			# al patrulea e optional, soldul va fi zero
        self.um = um
        self.i = {}					# fiecare instanta va avea trei dictionare intrari, iesiri, data
        self.e = {}					# pentru mentinerea corelatiilor cheia operatiunii va fi unica
        self.d = {}
        self.temp_lista_d = []
        self.limita_avertisment = int(input('Introduceti limita de la care doriti sa fiti avertizat in caz ca stocul este mai mic:\n'))

    def intr(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        self.data = data
        self.cant = cant
        self.sold += cant          # recalculam soldul dupa fiecare tranzactie
        if self.d.keys():               # dictionarul data are toate cheile (fiecare tranzactie are data)
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.i[cheie] = cant       # introducem valorile in dictionarele de intrari si data
        self.d[cheie] = self.data

    def iesi(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        #   datetime.strftime(datetime.now(), '%Y%m%d') in Python 3.5
        self.data = data
        self.cant = cant
        if (self.sold - self.cant) <= self.limita_avertisment:
            input('Atentie! Stocul produsului va fi sub limita de {0}. '
                  'Apasati <Enter> pentru continua'.format(self.limita_avertisment))

        answer = input('Doriti sa trimiteti un e-mail de avertizare? (Y/N)')

        self.sold -= self.cant

        if answer.upper() == 'Y':
            sender = input('introduceti adresa dvs de gmail:\n')
            passw = input('introduceti parola dvs de gmail:\n')
            receiver = input('introduceti adresa la care doriti sa trimiteti mailul de avertizare:\n')
            subiect_ma = 'Limita de {0} a fost atinsa pentru soldul produsului: {1}'.format(self.limita_avertisment,
                                                                                            self.prod)
            text_ma = 'Soldul produsului {0} este acum: {1}'.format(self.prod, self.sold)
            mesaj_avertizare='Subject: {0}\n\n{1}'.format(subiect_ma,text_ma)
            conexiune = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            conexiune.login(user=sender, password=passw)
            conexiune.sendmail(from_addr=sender, to_addrs=receiver, msg=mesaj_avertizare)
        else:
            pass

        if self.d.keys():
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.e[cheie] = self.cant       # similar, introducem datele in dictionarele iesiri si data
        self.d[cheie] = self.data

    def fisap(self):
        self.f1 = tempfile.mktemp('f1.txt')
        self.f2 = open(self.f1, 'w+')
        print('Fisa produsului ' + self.prod + ': ' + self.um)
        self.f2.write('Fisa produsului ' + self.prod + ': ' + self.um)
        print(40 * '-')
        self.f2.write('\n'+40 * '-')
        print(' Nrc ', '  Data ', 'Intrari', 'Iesiri')
        self.f2.write('\n'+' Nrc '+'  Data '+'Intrari '+' Iesiri')
        print(40 * '-')
        self.f2.write('\n'+40 * '-')

        for v in self.d.keys():
            if v in self.i.keys():
                print(str(v).rjust(5), self.d[v], str(self.i[v]).rjust(6), str(0).rjust(6))
                a = str(v).rjust(2) + ' '+ str(self.d[v])+str(self.i[v]).rjust(6)+str(0).rjust(6)
                self.f2.write('\n'+a)
            else:
                print(str(v).rjust(5), str(self.d[v]).rjust(5), str(0).rjust(6), str(self.e[v]).rjust(6))
                a = str(v).rjust(2)+' '+str(self.d[v]).rjust(5)+str(0).rjust(6)+str(self.e[v]).rjust(6)
                self.f2.write('\n'+a)

        print(40 * '-')

        self.f2.write('\n'+40 * '-')

        print('Stoc actual:      ' + str(self.sold).rjust(10))
        self.f2.write('\n'+'Stoc actual:      ' + str(self.sold).rjust(10))

        print(40 * '-')
        self.f2.write('\n'+40 * '-')
        self.f2.close()

        self.f3 = open(self.f1, 'r')

    def grafic(self):
        # 1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
        # anumita perioada, pentru un anumit produs;	--pygal--
        data_start = int(input('Introduceti data start (format AAAALLZZ): '))
        data_sfarsit = int(input('Introduceti data sfarsit (format AAAALLZZ): '))
        self.dictionar_intrari = {}
        self.dictionar_iesiri = {}
        lista_chei_data=[]
        lista_temp_i=[]
        lista_temp_e = []
        for q in self.d.items():
            if data_start <= int(q[1]) <= data_sfarsit:
                self.temp_lista_d.append(q[1])
        lista_date_unice = sorted(set(self.temp_lista_d))
        for data in lista_date_unice:
            for i in self.d.keys():
                if self.d[i] == data:
                    lista_chei_data.append(i)
            for cheie in lista_chei_data:
                if cheie in self.i.keys():
                    lista_temp_i.append(self.i[cheie])
                elif cheie in self.e.keys():
                    lista_temp_e.append(self.e[cheie])
                self.dictionar_iesiri.update({data: lista_temp_e})
                self.dictionar_intrari.update({data: lista_temp_i})
            lista_chei_data = []
            lista_temp_i = []
            lista_temp_e = []
        chart = pygal.StackedBar()
        chart.x_labels = lista_date_unice
        lista1 = []
        lista2 = []
        suma = 0
        for element in chart.x_labels:
            if len(self.dictionar_intrari[element]) == 1:
                for item in self.dictionar_intrari[element]:
                    lista1.append(item)
            elif not len(self.dictionar_intrari[element]):
                lista1.append(0)
            else:
                for item in self.dictionar_intrari[element]:
                     suma += item
                lista1.append(suma)
        suma = 0
        for element in chart.x_labels:
            if len(self.dictionar_iesiri[element]) == 1:
                for item in self.dictionar_iesiri[element]:
                    lista2.append(item)
            elif not len(self.dictionar_iesiri[element]):
                lista2.append(0)
            else:
                for item in self.dictionar_iesiri[element]:
                     suma += item
                lista2.append(suma)
        chart.add('Intrari',lista1)
        chart.add('Iesiri',lista2)
        chart.render_to_file('Grafic intrari si iesiri '+ str(data_start) + ' ' + str(data_sfarsit) + '.svg')

    def email(self):
        sender = input('Va rog introduceti adresa dvs de gmail:\n')
        passw = input('Va rog introduceti parola dvs de gmail:\n')
        receiver = input('Introduceti adresa de e-mail a destinatarului:\n')
        subject =  'Fisa produsului ' + self.prod + ': ' + self.um
        self.fisap()
        message = 'Subject: {0}\n\n{1}'.format(subject, self.f3.read())

        smtp_ob = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_ob.login(user=sender, password=passw)
        smtp_ob.sendmail(from_addr=sender, to_addrs=receiver, msg=message)

# Introducerea de elemente in stoc

fragute = Stoc('fragute', 'fructe', 'kg') # cream instantele clasei
fragute.intr(100, data='20191001')
fragute.intr(60, data='20191007')
fragute.iesi(111, data='20191105')
fragute.intr(100)
fragute.iesi(73)
fragute.iesi(85)

"""1. Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;	--pygal--"""

fragute.grafic()

"""Exercitiul 2 poate fi testat prin instantiere"""

"""3. Creati o metoda cu ajutorul careia sa puteti transmite prin email diferite informatii(
de exemplu fisa produsului) ; 	--SMTP--"""

fragute.email()

