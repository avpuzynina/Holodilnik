# Holodilnik
<p align="justify"><b>Holodilnik (Холодильник)</b> -  это умный телеграм бот, который подберет рецепты по фотографии продуктов в холодильнике. Всё что нужно - отправить фотографию холодильника в бот, и он выдаст подходящие рецепты.
Проект разработан и реализован в команде <a href="https://t.me/annapuzynina">@annapuzynina</a> и <a href="https://t.me/estoy_hablando_contigo">@nikitaakhmetov</a> с помощью телеграм бота, написанного с использованием библиотеки <a href="https://docs.aiogram.dev/en/latest/">Aiogram</a>.</p>

<img src="https://github.com/avpuzynina/Holodilnik/blob/main/image_save/project_idea.png" alt="альтернативный текст" />

#### Шаги реализации проекта:
- Парсинг датасата рецептов с помощью библиотеки BeatifulSoup с сайта [eda.ru](https://eda.ru/) и сохранение его в файл с расширением .csv
- Предобработка датасета рецептов с помощью библиотеки [Pandas](https://pandas.pydata.org/)
- Сбор фотографий с продуктами и разметка их с помощью [Roboflow](https://app.roboflow.com/holod/holodilnik_products_new/4) для модели [Yolov5](https://github.com/ultralytics/yolov5)
![image](https://github.com/avpuzynina/Holodilnik/blob/main/image_save/train_valid_dataset.png)
- Обучение модели [Yolov5](https://github.com/ultralytics/yolov5) с помощью библиотеки [PyTorch](https://pytorch.org/) c использованием мощности [Google Colab](https://colab.research.google.com/)
- Разработка рекомендательной системы выдачи продуктов
- Разработка рекомендательной системы похожих продуктов

##### **Функции телеграм бота:**
- Получение 5-ти рецептов по фотографии холодильника или продукта:
![image](https://github.com/avpuzynina/Holodilnik/blob/main/image_save/interface_1.jpg)
- Получение 5-ти похожих рецептов при выборе какого-либо рецепта:
![image](https://github.com/avpuzynina/Holodilnik/blob/main/image_save/interface_2.jpg)

##### Стэк:
<img src="https://raw.githubusercontent.com/devicons/devicon/2ae2a900d2f041da66e950e4d48052658d850630/icons/pandas/pandas-original.svg" alt="pandas" width="40" height="40"/>
<img src="https://www.vectorlogo.zone/logos/pytorch/pytorch-icon.svg" alt="pytorch" width="40" height="40"/> </a> 
<img src="https://upload.wikimedia.org/wikipedia/commons/d/d0/Google_Colaboratory_SVG_Logo.svg" alt="colab" width="40" height="40"/>
<img src="https://avatars.githubusercontent.com/u/33784865?s=200&v=4" alt="colab" width="40" height="40"/>
<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSbfHP132oL2LKGsA_kV5VSekHToyfRZmd1mXXmuBmbA&s" alt="colab" width="40" height="40"/>

### Интерфейс бота:
![Alt Text](https://github.com/avpuzynina/Holodilnik/blob/main/image_save/interface_telegrambot.gif)\
Видеодемонстрация лежит [тут](https://youtube.com/shorts/6m-21gWsE0Q?feature=share).

**Участники проекта:**
- [Анна Пузынина](https://github.com/avpuzynina) 
- [Никита Ахметов](https://github.com/SenhorMaestro)

## Инструкция по запуску
1. Запустить терминал и прописать команду\
`pip install -r 'requirements.txt'`
2. Открыть файл bot.py, в терминале прописать команду\
```python home/anna/Holodilnik/TelegramBot/bot.py```

### Ideas For New Features
1. Добавление кнопки докупить продукты


2. Улучшение качества модели


3. Запрос на определение вида мяса






