from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    print('Не удалось загрузить .env')
else:
    load_dotenv()
