# Learn Fastapi_01

Usefell commands:

alembic init -t async alembic

alembic revision --autogenerate -m "Create products table" (create migrations)

alembic upgrade head  (install migrations)

alembic downgrade -1 (cancell migrations)