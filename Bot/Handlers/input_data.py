from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram import Bot
import os
from dotenv import load_dotenv
from Parser import vin_data, categorys, details_data
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

token = os.getenv('API_KEY')

router = Router()


# Класс состояния
class Form(StatesGroup):
    vin = State()
    category = State()
    brand = State()
    ssd = State()
    brand_value = State()
    ManufacturerId = State()
    category_list = State()


# Объект бота
bot = Bot(token=token)


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Напишите вин-номер или фрейм(номер кузова) автомобиля: ')

    await state.set_state(Form.vin)


@router.message(F.text, Form.vin)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(vin=message.text)

    data = await state.get_data()

    try:
        Brand, Name, Date, Ssd, brand_value, ManufacturerId = vin_data.car_data(vin=data.get("vin"))

        Form.ssd = Ssd
        Form.brand_value = brand_value
        Form.ManufacturerId = ManufacturerId

        msg_text = f'Производитель - {Brand}\nНаименование - {Name}\nДата выпуска - {Date}'
        await message.answer(f'Данные по автомобилю с номером кузова {data.get("vin")}')
        await message.answer(msg_text)

        async with (ChatActionSender.typing(bot=bot, chat_id=message.chat.id)):

            builder = InlineKeyboardBuilder()

            category_list = categorys.categiry(brand_value, Ssd)

            Form.category_list = category_list

            for i in category_list:
                # InlineKeyboardButton(text="На главную", callback_data='back_home')
                builder.add(types.InlineKeyboardButton(
                    text=f'{list(category_list[i].keys())[0]}',
                    callback_data="category_id_" + str(list(category_list[i].values())[0]))
                )

            builder.adjust(2)

            await message.answer(f'Выбери категорию для ТО', reply_markup=builder.as_markup())

        await state.set_state(Form.category)

    except:

        builder = InlineKeyboardBuilder()

        builder.add(types.InlineKeyboardButton(text="Да", callback_data='category_id_'))
        # builder.add(types.InlineKeyboardButton(text="Нет", callback_data='category_id_'))
        builder.adjust(2)
        await message.answer('Данные по вин номеру или номеру кузова не найдены', reply_markup=builder.as_markup())




@router.callback_query(F.data.startswith('back_'), Form.category)
async def details(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback.from_user.id, f'Для повторного запроса нажми /start')
    await callback.message.delete()
    await callback.answer()
    await state.clear()


@router.callback_query(F.data.startswith('category_id_'), Form.category)
async def details(callback: types.CallbackQuery, state: FSMContext):
    code = callback.data.replace('category_id_', '')

    data = await state.get_data()

    Ssd = Form.ssd
    brand_value = Form.brand_value
    ManufacturerId = Form.ManufacturerId

    manufacturerName, partName, partNumber, minimalPrice, description = details_data.details(code, Ssd, brand_value,
                                                                                             ManufacturerId)

    msg_text = (f'Производитель - {manufacturerName}\nНазвание запчасти - {partName}\nНомер запчасти - {partNumber}\n'
                f'Минимальная цена - {minimalPrice}р\nОписание - {description}')

    await bot.send_message(callback.from_user.id, msg_text)

    await bot.send_message(callback.from_user.id, f'Для повторного запроса нажми /start')
    await callback.message.delete()
    await callback.answer()
    await state.clear()

# @router.message(F.text, Form.category)
# # @router.message(F.data = Form.category)
# async def capture_age(message: Message, state: FSMContext):
#     await state.update_data(category=message.text)
#
#     data = await state.get_data()
#
#     category_id = int(data.get("category"))
#
#     cat_id = {}
#
#     for i in Form.category_list:
#         if category_id == i:
#             cat_id = Form.category_list[i]
#
#     Ssd = Form.ssd
#     brand_value = Form.brand_value
#     ManufacturerId = Form.ManufacturerId
#
#     manufacturerName, partName, partNumber, minimalPrice, description = details_data.details(cat_id, Ssd, brand_value,
#                                                                                              ManufacturerId)
#
#     msg_text = (f'Производитель - {manufacturerName}\nНазвание запчасти - {partName}\nНомер запчасти - {partNumber}\n'
#                 f'Минимальная цена - {minimalPrice}\nОписание - {description}')
#
#     category = list(cat_id.keys())
#
#     await message.answer(f'Выбрана категория для ТО - {category[0]}')
#
#     await message.answer(msg_text)
#     await message.answer(f'Для повторного запроса нажми /start')
#     await state.clear()
