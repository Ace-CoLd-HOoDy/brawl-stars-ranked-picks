import time

# Функция для плавного вывода текста
def print_slowly(text, delay=0.005, color="default"):
    color_codes = {
        "default": "\033[0m",  # Стандартный цвет
        "blue": "\033[34m",     # Синий
        "red": "\033[31m",      # Красный
        "green": "\033[32m",    # Зеленый
    }
    color_code = color_codes.get(color, "\033[0m")  # Если цвет не найден, использовать стандартный
    for char in text:
        print(f"{color_code}{char}", end="", flush=True)
        time.sleep(delay)
    print("\033[0m")  # Сброс цвета

# Словарь с лучшими персонажами для каждого режима
best_characters = {
    "pinball dreams": ["Moe", "Barley", "Twins", "Rico", "Chester", "Berry", "Lily", "Mortis", "Primo", "Mike", "Squeack", "Frank", "Darryl"],
    "center Stage": ["Moe", "Gale", "Clancy", "Rico", "Chester", "Buster", "Lily", "Mortis", "Primo", "Grom", "Squeack", "Frank"],
    "retina": ["Draco", "Nita", "Melody", "Sandy", "Shelly", "Cord", "Amber", "Melody", "Mike", "Barly", "Lou", "Sam"],
    "нокаут": ["Гас", "Белль", "Рико"],
    "осад": ["Пэм", "Биби", "8-Бит"],
}

# Словарь с персонажами и против кого они хороши
counters = {
    "Shelly": ["Otis", "Gale", "Surge", "Bea", "Stu", "Barley", "Mike"],
    "Nita": ["Darryl", "Rosa", "Frank", "Mortis", "Sam", "Buster"],
    "Colt": ["Bull", "Primo", "Rosa", "Jacky", "Frank", "Biby", "Ash", "Buster", "Sam"],
    "Bull": ["Frank", "Rosa", "Primo", "Mortis", "Sam", "Hank", "Doug"],
    "Brock": ["Barley", "Mike", "Sprout", "Willow", "Grom", "Penny"],
    "Кроу": ["Булл", "Шелли", "Дэррил"],
    "Сту": ["Шелли", "Тик", "Гром"],
    "Биби": ["Сту", "Шелли", "Кроу"],
    "Мортис": ["Дино", "Тик", "Биби"],  # Мортис боится этих персонажей
    "Дино": ["Мортис", "Тик", "Биби"],  # Дино хорош против Мортиса
}

# Словарь с персонажами, которых боятся
afraid_of = {
    "Shelly": ["Bull", "Primo", "Rosa", "Jacky", "Darryl", "Frank", "Edgar", "Mortis", "Doug"],
    "Nita": ["Amber", "Griff", "Colt", "Max", "Otis"],
    "Colt": ["Brock", "Piper", "Bea", "Belle", "Nani", "Stu"],
    "Bull": ["Shelly", "Crow", "Stu", "Spike", "Otis", "Amber", "Max"],  # Шелли боится Сту
    "Фрэнк": ["Сту", "Белль"],
    "Булл": ["Санди", "Кроу"],
    "Мортис": ["Дино", "Тик", "Биби"],  # Мортис боится этих персонажей
    "Дино": ["Мортис", "Тик", "Биби"],  # Дино боится этих персонажей
}

def suggest_characters(mode, picked_characters, all_picked_characters):
    # Получаем лучших персонажей для режима, исключая уже выбранных
    mode_characters = [
        char for char in best_characters.get(mode, []) if char not in all_picked_characters
    ]

    # Ищем пересечение для каждого врага
    counter_recommendations = {}
    for enemy in picked_characters:
        if enemy in counters:
            countered_by = set(
                char for char in counters[enemy] if char not in all_picked_characters
            )
            counter_recommendations[enemy] = countered_by  # Сохраняем рекомендации по контрпикам

    # Поиск общих персонажей, которые подходят и для режима, и для контрпиков
    common_characters = set(mode_characters)  # Начнем с персонажей для режима
    for countered_by in counter_recommendations.values():
        common_characters &= countered_by  # Пересечение персонажей для режима и контрпиков

    # Если хотя бы один персонаж подходит и для режима, и для контрпиков, то включаем его в общие
    if common_characters:
        return common_characters, mode_characters, counter_recommendations
    else:
        return set(), mode_characters, counter_recommendations

# Основная логика программы
def main():
    print("Добро пожаловать в помощник по выбору персонажей для Brawl Stars!")
    mode = input("Введите режим игры: ").strip().lower()
    if mode not in best_characters:
        print_slowly("Извините, для этого режима у нас пока нет рекомендаций.")
        return

    print(f"Лучшие персонажи для режима '{mode}': {', '.join(best_characters[mode])}")
    enemy_count = int(input("Сколько персонажей выбрали противники (0-3)? "))
    picked_characters = []
    all_picked_characters = []  # Список всех уже выбранных персонажей

    for i in range(enemy_count):
        enemy = input(f"Введите имя выбранного противником персонажа ({i + 1}/{enemy_count}): ").strip().capitalize()
        picked_characters.append(enemy)
        all_picked_characters.append(enemy)

    if enemy_count == 0:
        print_slowly(f"Лучшие персонажи для режима '{mode}': {', '.join(best_characters[mode])}")
    else:
        common_characters, mode_suggestions, counter_recommendations = suggest_characters(
            mode, picked_characters, all_picked_characters
        )

        # Вывод рекомендаций по контрпикам с красным цветом
        print_slowly(f"Лучшие персонажи для режима '{mode}': {', '.join(mode_suggestions)}", color="blue")
        print_slowly("Рекомендации против каждого персонажа противника:", color="blue")
        for enemy in picked_characters:
            if enemy in counter_recommendations and counter_recommendations[enemy]:
                print_slowly(f"Против {enemy} возьмите: {', '.join(counter_recommendations[enemy])}", color="blue")
            else:
                print_slowly(f"Для {enemy} контрпиков не найдено.", color="blue")

        # Выводим общие персонажи, если они есть, с красным цветом
        if common_characters:
            print_slowly(f"Общие персонажи для режима и контрпиков: {', '.join(common_characters)}", color="blue")
        
        # Поиск общих контрпиков (с учетом хотя бы одного совпадения)
        common_in_counters = set()

        # Сначала ищем пересечения между контрпиками для врагов и лучшими персонажами для режима
        for enemy in picked_characters:
            if enemy in counters:
                countered_by = set(counters[enemy])
                common_in_counters.update(countered_by & set(best_characters.get(mode, [])))

        # Также добавляем пересечения контрпиков между самими противниками
        for i, enemy1 in enumerate(picked_characters):
            for enemy2 in picked_characters[i+1:]:
                if enemy1 in counters and enemy2 in counters:
                    common_in_counters.update(set(counters[enemy1]) & set(counters[enemy2]))

        # Вывод общего списка контрпиков с красным цветом
        if common_in_counters:
            print_slowly(f"Общие контрпики для противников или режима: {', '.join(common_in_counters)}", color="green")
        else:
            print_slowly("Нет общих контрпиков для противников или режима.", color="red")
        
        # Рекомендации о том, кого не стоит брать (кто боится выбранных противников) - выводим зелёным
        not_recommended = set()
        for enemy in picked_characters:
            if enemy in afraid_of:
                not_recommended.update(afraid_of[enemy])

        if not_recommended:
            print_slowly(f"Не рекомендуемые персонажи (боятся выбранных противников): {', '.join(not_recommended)}", color="red")
        else:
            print_slowly("Нет персонажей, которых стоит избегать.", color="green")

        # Финальный выбор: если есть пересечение между общими контрпиками и не рекомендуемыми персонажами
        final_choice = common_in_counters & not_recommended
        if final_choice:
            print_slowly(f"Финальный выбор (общие контрпики и не рекомендуемые персонажи): {', '.join(final_choice)}", color="green")
        
        # Дополнительно выводим фильтрованные общие контрпики (без не рекомендуемых)
        filtered_common_in_counters = common_in_counters - not_recommended
        if filtered_common_in_counters:
            print_slowly(f"Фильтрованные общие контрпики, финальные (без не рекомендуемых персонажей): {', '.join(filtered_common_in_counters)}", color="blue")
        else:
            print_slowly("Нет общих контрпиков без не рекомендуемых персонажей.", color="red")

# Запуск программы
if __name__ == "__main__":
    main()