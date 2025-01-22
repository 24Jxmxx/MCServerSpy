import sys
import json
from mcstatus.server import JavaServer
import time

# Базы данных для подсветки
friends = []
admins = []

# Загружаем данные из файла, если он существует
def load_data():
    global friends, admins
    try:
        with open("players.json", "r") as file:
            data = json.load(file)
            friends = [player.lower() for player in data.get("friends", [])]
            admins = [player.lower() for player in data.get("admins", [])]
    except FileNotFoundError:
        pass

# Сохраняем данные в файл
def save_data():
    data = {"friends": friends, "admins": admins}
    with open("players.json", "w") as file:
        json.dump(data, file)

def scan_server(ip):
    try:
        server = JavaServer.lookup(ip)

        # Начальная проверка статуса сервера
        status = server.status()
        current_players = status.players.online  # Начальное количество игроков

        if current_players > 35:
            print(f"На сервере {current_players} игроков. Сканирование будет долгим. Покажем только первые 12.")
            status = server.status()  # Получаем обновленный статус сервера
            visible_players = status.players.sample or []  # Получаем игроков

            found_players = [player.name for player in visible_players[:12]]  # Берем только первые 12 игроков
            print(f"Найдено игроков: {len(found_players)} / {current_players}")
            
            # Выводим первых 12 найденных игроков
            print("\n--- Все найденные игроки ---")
            for idx, player in enumerate(found_players, 1):
                marker = ""
                if player.lower() in friends:
                    marker += " [Friend]"
                if player.lower() in admins:
                    marker += " [Admin]"
                print(f"{idx}. {player}{marker}")

            print("\nСканирование завершено.")
            return

        all_players = set()  # Множество для хранения уникальных ников
        missing_players = current_players
        found_players = []

        while len(all_players) < missing_players:
            status = server.status()  # Обновляем статус сервера
            visible_players = status.players.sample or []  # Получаем игроков

            # Добавляем новых игроков в список
            for player in visible_players:
                if player.name.lower() not in all_players:
                    all_players.add(player.name.lower())
                    found_players.append(player.name)

            print(f"Найдено игроков: {len(all_players)} / {missing_players} (еще ищем...)")
            time.sleep(2)  # Подождём пару секунд перед следующим запросом

        # После того как все игроки найдены, выводим информацию о сервере
        print("\n--- Информация о сервере ---")
        print(f"Ядро сервера: {status.version.name}")
        print(f"Версия сервера: {status.version.protocol}")
        print(f"Макс. количество игроков: {status.players.max}")
        print(f"Всего игроков на сервере: {len(all_players)}")
        
        print("\n--- Все найденные игроки ---")
        for idx, player in enumerate(all_players, 1):
            marker = ""
            if player in friends:
                marker += " [Friend]"
            if player in admins:
                marker += " [Admin]"
            print(f"{idx}. {player}{marker}")

    except Exception as e:
        print(f"Ошибка: {e}")

def main():
    load_data()  # Загружаем данные из файла при запуске

    while True:
        print("\nМеню:")
        print("1 - Сканировать сервер")
        print("2 - Добавить игрока в список")
        print("3 - Удалить игрока из списка")
        print("4 - Выйти")
        
        choice = input("Выберите опцию: ").strip()

        if choice == "1":
            ip = input("Введите IP-адрес или доменное имя сервера: ").strip()
            if ip.lower() == "exit":
                print("Выход из программы.")
                sys.exit()
            print("Сканирую сервер...")
            scan_server(ip)
        elif choice == "2":
            player_name = input("Введите ник игрока для добавления: ").strip()
            team = input("В какую команду добавить (f - Friends, a - Admins): ").strip().lower()
            player_name = player_name.lower()  # Приводим ник к нижнему регистру
            if team == "f":
                if player_name not in friends:
                    friends.append(player_name)
            elif team == "a":
                if player_name not in admins:
                    admins.append(player_name)
            else:
                print("Неверная команда. Используйте 'f' для Friends или 'a' для Admins.")
                continue
            save_data()  # Сохраняем данные в файл
            print(f"Игрок {player_name} добавлен в команду {team}.")
        elif choice == "3":
            player_name = input("Введите ник игрока для удаления: ").strip().lower()
            if player_name in friends:
                friends.remove(player_name)
                print(f"Игрок {player_name} удалён из команды Friends.")
            elif player_name in admins:
                admins.remove(player_name)
                print(f"Игрок {player_name} удалён из команды Admins.")
            else:
                print(f"Игрок {player_name} не найден в списках.")
            save_data()  # Сохраняем изменения в файл
        elif choice == "4":
            print("Завершение работы программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите опцию снова.")

if __name__ == "__main__":
    main()
