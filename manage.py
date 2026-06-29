#!/usr/bin/env python
import os
import sys

def create_admin_if_not_exists():
    """Автоматически создает суперзера, если его нет в базе"""
    try:
        import django
        django.setup()
        from legoshop.accounts.models import User  # Импортируем из правильного пути приложения

        username = 'admin1'
        email = ''
        password = 'qwerty77!'

        if not User.objects.filter(username=username).exists():
            print("=== Создаем суперпользователя... ===")
            User.objects.create_superuser(username=username, email=email, password=password)
            print("=== Суперпользователь успешно создан! ===")
        else:
            print("=== Суперпользователь уже существует. ===")
    except Exception as e:
        # Если таблицы еще не созданы (до миграций), просто пропускаем, чтобы не крашить билд
        print(f"=== Пропуск создания суперзера: БД еще не готова ({e}) ===")

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legoshop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and available on your PYTHONPATH."
        ) from exc
    
    # Запускаем оригинальную команду Django
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # Перехватываем момент ПОСЛЕ выполнения команды. 
    # Но так как execute_from_command_line завершает процесс сам, 
    # для Render надежнее вызвать проверку прямо ПЕРЕД запуском основного процесса, 
    # если выполняется команда, не ломающая базу.
    
    # Но самый надежный способ для Render — запустить это отдельным шагом в Build Command!
    main()