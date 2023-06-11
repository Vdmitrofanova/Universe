import socket

def start_my_server():
    try: #Обработчик исключений
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 2000)) #Назвначаем адресс для серверного соккета

        server.listen(4) #Кол-во входящих запросов
        while True: #Бесконечный цикл обработки запросов
            print('Working...')
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8') #Представляем информацию в читабильном виде
            #print(data)
            content = load_page_from_get_request(data) #Ответ клиенту
            client_socket.send(content) #Енкодируем заголовки
            client_socket.shutdown(socket.SHUT_WR) #Закрывает соединение с клиентом
    except KeyboardInterrupt:
        server.close()
        print('Shutdown this shit...')

def load_page_from_get_request(request_data): # Передаем запрос клиента
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n' #Тип ответа, статус, код статуса, кодировка
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    path = request_data.split(' ')[1] #Распарсим функцией split
    response = ''
    try:
        with open('views' + path, 'rb') as file: #Вычитываем его содержимое сразу в байтовом представлении
            response = file.read()
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Sorry, but there is no page..').encode('utf-8') #Не может открыть файл, потому что его нет

if __name__ == '__main__':
    start_my_server()

