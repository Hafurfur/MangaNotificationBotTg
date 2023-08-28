# Телеграм бот

Телеграм бот для уведомлений о выходе новых глав манги с "Mangalib"

## Инструкция использования:

### Docker:

- Убедитесь, что установлен docker, docker-compose, git
- Запустите `git https://github.com/Hafurfur/MangaNotificationBotTg.git`
- Переименуйте `.env.example` в `.env` и заполните его
- В `docker-compose.yml` заполните нужные значения
- Создайте и запустите докер контейнер `docker-compose up --build -d`
- Теперь бот работает в контейнере и может быть использован

### Запуск в терминале

- Убедитесь, что установлен git, python 11
- Запустите `git https://github.com/Hafurfur/MangaNotificationBotTg.git`
- Создайте виртуальное окружение `python -m venv venv`
- Активируйте виртуальное окружение (см. таблицу ниже)

| Platform | Shell      | Command to activate virtual environment |
|----------|------------|-----------------------------------------|
| POSIX    | bash/zsh   | 	$ source <venv>/bin/activate           |
| POSIX    | fish       | $ source <venv>/bin/activate.fish       |
| POSIX    | csh/tcsh   | $ source <venv>/bin/activate.csh        |
| POSIX    | PowerShell | $ <venv>/bin/Activate.ps1               |
| Windows  | cmd.exe    | C:\> <venv>\Scripts\activate.bat        |
| Windows  | PowerShell | PS C:\> <venv>\Scripts\Activate.ps1     |

- Установите зависимости нужные для бота `pip install -r requirements.txt`
- Запасите бота `start.py`
