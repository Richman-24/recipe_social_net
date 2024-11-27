# на количество символов
USER_LENGTH_LIMIT = 150
EMAIL_LENGTH_LIMIT = 254

PER_PAGE_LIMIT = 6

TAG_LENGTH_LIMIT = 32
RECIPE_LENGTH_LIMIT = 256

INGREDIENT_LENGTH_LIMIT = 128
UNIT_LENGTH_LIMIT = 64

# на количество единиц
INGREDIENT_AMOUNT_MIN = 1
COOKING_TIME_MIN = 1

ERROR_MESSAGE = {
    'amount_error': (
        f'Количество не может быть меньше {INGREDIENT_AMOUNT_MIN}'
    ),
    'time_error': (
        f'Время не может быть меньше {INGREDIENT_AMOUNT_MIN}'
    ),
    'reserved_name_error': (
        'Данное имя пользователя занято. Выберите другое.'
    ),
}
