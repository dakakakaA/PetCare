# PetCare — система учёта домашних животных

Учебный проект для дисциплины «Проектирование информационных систем».

## Стек
Python 3.11, FastAPI, SQLAlchemy, Pydantic, JWT HS256, bcrypt, PostgreSQL 15, SPA на HTML/CSS/JavaScript, Nginx Alpine, Docker Compose.

## Запуск
Требуются Docker Engine и Docker Compose v2.

```bash
cp .env.example .env
# Для production обязательно смените SECRET_KEY и пароль БД.
docker compose up --build -d
```
Откройте http://localhost:3000. Проверка API: http://localhost:3000/api/health. Swagger доступен на backend по `/docs`; для доступа с хоста временно опубликуйте порт `8000:8000` в сервисе backend.

## Тестовые учётные записи
- Client: `client` / `client123`
- Admin: `admin` / `admin123`

Таблицы, учётные записи и каталог создаются автоматически при первом запуске. Регистрация создаёт только роль `Client`.

## Возможности
- JWT-регистрация и вход; bcrypt-хеширование паролей.
- Каталог животных: чтение клиентом, полный CRUD администратором.
- Личные карточки питомцев: CRUD только владельцем.
- Дневник ухода: кормление, прогулки, здоровье, уход, вакцинация и заметки.
- Панель администратора с журналом аудита.
- Поиск, фильтрация, адаптивная тёмная тема и быстрый демо-вход.

## GitHub Issues: 60 пользовательских историй
1. Загрузите проект в репозиторий GitHub.
2. Создайте fine-grained Personal Access Token с правом Issues: Read and write для этого репозитория.
3. Задайте переменные `GITHUB_TOKEN` и `GITHUB_REPOSITORY=owner/repository`.
4. Запустите `python docs/upload_issues.py`. Скрипт проверяет, что в файле ровно 60 историй и 20 тегов MVP, затем создаёт Issues и пропускает уже импортированные `use-case-XX`.

## Остановка
`docker compose down`. Для удаления данных тестовой БД: `docker compose down -v`.

## Безопасность и ограничения
Учебный прототип: перед production нужны HTTPS, сильные секреты, rate limiting, миграции Alembic, резервное копирование и автоматические тесты. Вес хранится в поле `weight_grams` целым числом (например, 1300 означает 1,3 кг).
