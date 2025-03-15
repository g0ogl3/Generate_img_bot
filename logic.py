import json #для работы с json
import time #для работы с временем
from config import * #импорт переменных из файла config.py
import requests #импорт библиотеки для работы с запросами
from PIL import Image #импорт библиотеки для работы с изображениями
import base64 #для работы с base64
from io import BytesIO #для работы с байтами

class Text2ImageAPI: #класс для работы с API

    def __init__(self, url, api_key, secret_key): #инициализация класса
        self.URL = url #ссылка на
        self.AUTH_HEADERS = { #заголовки для авторизации
            'X-Key': f'Key {api_key}', #ключ для апи
            'X-Secret': f'Secret {secret_key}', #секретный ключ для апи
        } #заголовки для авторизации

    def get_model(self): #функция для получения модели
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS) #запрос на получение моделей
        data = response.json() #получение данных
        return data[0]['id'] #возвращение id первой модели

    def generate(self, prompt, model, images=1, width=1024, height=1024): #функция для генерации изображения
        params = { #параметры для генерации
            "type": "GENERATE", #тип запроса
            "numImages": images, #количество изображений
            "width": width, #ширина изображения
            "height": height, #высота изображения
            "generateParams": { #параметры генерации
                "query": f"{prompt}" #текст запроса
            } #параметры генерации
        } #параметры для генерации

        data = { #данные для запроса
            'model_id': (None, model), #id модели
            'params': (None, json.dumps(params), 'application/json') #параметры запроса
        } #данные для запроса
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data) #запрос на генерацию изображения
        data = response.json() #получение данных
        return data['uuid'] #возвращение uuid

    def check_generation(self, request_id, attempts=10, delay=10): #функция для проверки генерации
        while attempts > 0: #цикл пока попытки не закончились
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS) #запрос на проверку генерации
            data = response.json() #получение данных
            if data['status'] == 'DONE': #если генерация завершена
                return data['images'] #возвращение изображений

            attempts -= 1 #уменьшение попыток
            time.sleep(delay) #задержка

def generate_img_from_text(prompt, url, api_key=api_key, secret_key=secret_key): #функция для генерации изображения по тексту
    api = Text2ImageAPI(url, api_key, secret_key) #создание объекта класса Text2ImageAPI
    model_id = api.get_model() #получение id модели
    uuid = api.generate(prompt, model_id) #генерация изображения
    images = api.check_generation(uuid) #проверка генерации изображения
    
    
    image_data = base64.b64decode(images[0]) #декодирование изображения
    image = Image.open(BytesIO(image_data)) #открытие изображения
    image.save('generated_image.png') #сохранение изображения
    
    return 'generated_image.png' #возвращение пути к изображению


if __name__ == '__main__': #проверка на то, что файл был запущен напрямую
    image_path = generate_img_from_text('Рыжий кот, реалистичный', url) #генерация изображения
    print(f'Изображение сохранено по пути: {image_path}') #вывод пути к изображению 
