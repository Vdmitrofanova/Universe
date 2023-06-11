import socket

import requests

from transformers import pipeline, set_seed
def generate_text(text):
    set_seed(42) #фиксируем генерацию текста для повторяемости результатов
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B') #используем GPT модель с помощью Hugging Face
    result = generator(text, max_length=256, do_sample=True, temperature=0.7) #генерируем текст с помощью модели
    return result[0]['generated_text']

def process_response(response):
    return "The main idea of the text is: " + response


def start_my_server():
    try: #Обработчик исключений
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 2000)) #Назвначаем адресс для серверного соккета

        server.listen(4) #Кол-во входящих запросов
        while True: #Бесконечный цикл обработки запросов
            print('Working...')
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8') #Представляем информацию в читабильном виде

            url = data.split()[1].split("?")[1].split("=")[1] # Извлекаем ссылку из GET запроса
            text = requests.get(url).text   # Получаем текст по ссылке
            response = generate_text(text) # Получаем основную идею текста из GPT модели с помощью Hugging Face
            #print(data)
            content = process_response(response) # Преобразовываем ответ в строку и отправляем клиенту
            client_socket.sendall(content) #Енкодируем заголовки
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

