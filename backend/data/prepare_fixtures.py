import json

# Сей скрипт берёт данные из поставляемого файла ingredients.json
# и переводит их в поддерживаемый формат для установки фикстур
# через loaddata и сохраняет его в data/fixtures.json

with open('data/ingredients.json', encoding='utf-8') as file:
    with open('data/fixtures.json', 'w', encoding='utf-8') as fix:

        data = json.load(file)

        def transform_ingredients(ingredients):
            transformed = []

            for index, ingredient in enumerate(ingredients, start=1):
                transformed.append({
                    "model": "recipes.ingredient",
                    "pk": index,
                    "fields": {
                        "name": ingredient['name'],
                        "measurement_unit": ingredient['measurement_unit']
                    }
                })

            return transformed

        transformed_data = transform_ingredients(data)
        json.dump(transformed_data, fix, ensure_ascii=False, indent=4)
