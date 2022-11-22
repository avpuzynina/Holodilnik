import logging
import re
import tempfile

import pandas as pd
import PIL
import torch
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image

logging.basicConfig(level=logging.INFO, filename="logfile.log")
model = torch.hub.load(
    "ultralytics/yolov5",
    "custom",
    path="/home/anna/Holodilnik/models/best_yolo_large_460.pt",
)
df = pd.read_csv(
    "/home/anna/Holodilnik/recipes_text/recipes_zelen.csv", index_col="Unnamed: 0"
)
df_corr = pd.read_csv(
    "/home/anna/Holodilnik/recipes_text/all_receipts_correlation_updated_zelen.csv",
    index_col="Unnamed: 0",
)


# Initialize bot and dispatcher
bot = Bot(token="")
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    text = f"Привет, {user_name}! 🍕\nЯ бот, который выдаст тебе рецепты по фотографии твоего холодильника.".format(
        message
    )
    text_2 = "Просто отправь мне фотографию своего холодильника:"
    user_id = message.from_user.id
    logging.info(f"{user_name} {user_id} send message: {message.text}")
    await message.answer(text)
    await message.answer(text_2)


@dp.message_handler(content_types=["photo"])
async def get_photo(message: types.Message):
    with tempfile.NamedTemporaryFile() as tmpfile:
        await message.photo[-1].download(destination_file=tmpfile.name)
        img = PIL.Image.open(tmpfile.name)
    results = model(img)
    photo_products = set(results.pandas().xyxy[0]["name"])
    products = translate_products(photo_products)
    if len(products) != 0:
        recipes_indexes, warning = recomend_sistem(products)
        name_recipes = []
        for i in recipes_indexes:
            name_recipes.append((df.iloc[i]["name"], i))
        keybord = create_keybord_recipes(name_recipes)
        text1 = "Ваши рецепты:" + "\n" + warning
        await message.answer(text1, reply_markup=keybord)
    else:
        empty_warning = "Извините,я моргнул, сделайте ещё одну фотографию!"
        await message.answer(empty_warning)


def create_keybord_recipes(recipies):
    inline_kb = InlineKeyboardMarkup()
    for name, id_name in recipies:
        inline_btn = InlineKeyboardButton(name, callback_data=f"recipe_{id_name}")
        inline_kb.add(inline_btn)
    return inline_kb


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("recipe"))
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    index_out = int(callback_query.data.split("_")[1])
    recipe_out = (
        df.iloc[index_out]["name"]
        + "\n"
        + "\n"
        + df.iloc[index_out]["ingridients"]
        + "\n"
        + df.iloc[index_out]["instruction"]
        + "\n"
        + df.iloc[index_out]["url"]
    )
    keybord = InlineKeyboardMarkup()
    inline_btn = InlineKeyboardButton(
        "5 похожих рецептов", callback_data=f"similar_{index_out}"
    )
    keybord.add(inline_btn)
    await bot.send_message(
        callback_query.from_user.id, recipe_out, reply_markup=keybord
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("similar"))
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    index_rec = callback_query.data.split("_")[1]
    list_recommend = df_corr[index_rec].nlargest(n=6).index.tolist()[1:]
    name_recipes = []
    for i in list_recommend:
        name_recipes.append((df.iloc[i]["name"], i))
    keybord1 = create_keybord_recipes(name_recipes)
    await bot.send_message(
        callback_query.from_user.id, "5  похожих рецептов", reply_markup=keybord1
    )


def translate_products(photo_products):
    dict_products_translate = {
        "arbuz": "Арбуз",
        "avokado": "Авокадо",
        "ananas": "Ананас",
        "apelsin": "Апельсины",
        "banan": "Бананы",
        "vinograd": "Виноград",
        "vishnya": "Вишня",
        "grusha": "Груши",
        "yabloko": "Яблоко",
        "klubnika": "Клубника",
        "laim": "Лайм",
        "limon": "Лимон",
        "mandarin": "Мандарины",
        "mango": "Манго",
        "malina": "Малина",
        "persiki": "Персики",
        "sliva": "Сливы",
        "baklazhan": "Баклажаны",
        "kapusta": "Капуста",
        "goroshek": "Горошек",
        "imbir": "Имбирь",
        "kitayskaya pekinskaya kapusta": "Китайская пекинская капуста",
        "kabachok": "Кабачки",
        "olivki": "Оливки",
        "luk repchatiy": "Лук репчатый",
        "krasnokochannaya kapusta": "Краснокочанная капуста",
        "kartofel": "Картофель",
        "brokkoli": "Брокколи",
        "luk krasniy": "Лук красный",
        "luk-porey": "Лук-порей",
        "maslini": "Маслины",
        "ogurtsi": "Огурцы",
        "marinovannie ogurtsi": "Маринованные огурцы",
        "morkov": "Морковь",
        "perets chili": "Перец чили",
        "pomidori cherri": "Помидоры черри",
        "pomidori": "Помидоры",
        "redis": "Редис",
        "bolgarskiy perets": "Болгарский перец",
        "selderey": "Сельдерей",
        "kukuruza": "Кукуруза",
        "svekla": "Свекла",
        "tykva": "Тыква",
        "tsvetnaya kapusta": "Цветная капуста",
        "chesnok": "Чеснок",
        "gribi": "Грибы",
        "shampinyoni": "Шампиньоны",
        "yogurt": "Йогурт",
        "kurinoye yaytso": "Куриное яйцо",
        "kefir": "Кефир",
        "moloko": "Молоко",
        "slivki": "Сливки",
        "slivochnoye maslo": "Сливочное масло",
        "sgushennoye moloko": "Сгущенное молоко",
        "tvorog": "Творог",
        "slivochniy sir": "Сливочный сыр маскарпоне",
        "mozzarella": "Сыр моцарелла",
        "brynza": "Сыр брынза",
        "tverdiy sir": "Твердый сыр",
        "bekon": "Бекон",
        "vetchina": "Ветчина",
        "myaso": "Мясо",
        "sosiski": "Сосиски",
        "farsh": "Фарш",
        "kuritsa": "Курица",
        "krevetki": "Креветки",
        "riba": "Рыба",
        "tomatnaya pasta": "Томатная паста",
        "hleb": "Хлеб",
        "gorchitsa": "Горчица",
        "smetana": "Сметана",
        "ketchup": "Кетчуп",
        "mayonez": "Майонез",
        "med": "Мед",
        "bazilik": "Базилик",
        "zelen": "Зелень",
        "zelyoniy luk": "Зеленый лук",
        "zelyoniy salat": "Зеленый салат",
        "petrushka": "Петрушка",
        "rukola": "Рукола",
        "ukrop": "Укроп",
        "kolbasa": "Колбаса",
    }
    products_search = []
    for i in dict_products_translate.keys():
        if i in photo_products:
            products_search.append(dict_products_translate[i])

    products_search = set(products_search)
    return products_search


def recomend_sistem(products):
    resept_count = 0
    recipes_indexes = set()
    warning = ""
    for i in range(len(df["ingridients_superclean"])):
        ingr = set(re.split(r"\s+(?=[А-Я])", df["ingridients_superclean"][i]))
        if ingr == products:
            resept_count += 1
            recipes_indexes.add(i)
        if len(recipes_indexes) == 5:
            break

    if len(recipes_indexes) < 5:
        for i in range(len(df["ingridients_superclean"])):
            ingr = set(re.split(r"\s+(?=[А-Я])", df["ingridients_superclean"][i]))
            if products.issubset(ingr):
                count_less_products = len(ingr) - len(products)
                if count_less_products == 1:
                    resept_count += 1
                    recipes_indexes.add(i)
            if len(recipes_indexes) == 5:
                break

    if len(recipes_indexes) < 5:
        for i in range(len(df["ingridients_superclean"])):
            ingr = set(re.split(r"\s+(?=[А-Я])", df["ingridients_superclean"][i]))
            if products.issubset(ingr):
                count_less_products = len(ingr) - len(products)
                if count_less_products == 2:
                    resept_count += 1
                    recipes_indexes.add(i)
            if len(recipes_indexes) == 5:
                break

    if len(recipes_indexes) < 5:
        for i in range(len(df["ingridients_superclean"])):
            ingr = set(re.split(r"\s+(?=[А-Я])", df["ingridients_superclean"][i]))
            if products.issubset(ingr):
                count_less_products = len(ingr) - len(products)
                if count_less_products == 3:
                    resept_count += 1
                    recipes_indexes.add(i)
            if len(recipes_indexes) == 5:
                break

    if len(recipes_indexes) < 5:
        for i in range(len(df["ingridients_superclean"])):
            ingr = set(re.split(r"\s+(?=[А-Я])", df["ingridients_superclean"][i]))
            counter_products = len(products.intersection(ingr))
            count_less_products = len(ingr) - counter_products
            if counter_products != 0:
                if count_less_products == 1:
                    resept_count += 1
                    recipes_indexes.add(i)
            if len(recipes_indexes) == 5:
                break

    if len(recipes_indexes) < 5:
        for i in range(len(df["ingridients_superclean"])):
            ingr = set(re.split(r"\s+(?=[А-Я])", df["ingridients_superclean"][i]))
            counter_products = len(products.intersection(ingr))
            count_less_products = len(ingr) - counter_products
            if counter_products != 0:
                if count_less_products == 2:
                    resept_count += 1
                    recipes_indexes.add(i)
            if len(recipes_indexes) == 5:
                break

    if len(recipes_indexes) < 5:
        for i in range(len(df["ingridients_superclean"])):
            ingr = set(re.split(r"\s+(?=[А-Я])", df["ingridients_superclean"][i]))
            counter_products = len(products.intersection(ingr))
            count_less_products = len(ingr) - counter_products
            if counter_products != 0:
                if count_less_products == 3:
                    resept_count += 1
                    recipes_indexes.add(i)
                else:
                    warning = "Внимание! Слишком много продуктов докупать!"
                    for k in products:
                        if k in ingr:
                            resept_count += 1
                            recipes_indexes.add(i)
            if len(recipes_indexes) == 5:
                break

    return recipes_indexes, warning


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
