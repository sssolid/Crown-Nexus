# Project Structure Tree View

Project: backend

```
backend/
├── alembic/
│   ├── versions/
│   │   └── __init__.py
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── chat.py
│   │   │   │   ├── currency.py
│   │   │   │   ├── fitments.py
│   │   │   │   ├── i18n.py
│   │   │   │   ├── media.py
│   │   │   │   ├── products.py
│   │   │   │   ├── search.py
│   │   │   │   └── users.py
│   │   │   ├── __init__.py
│   │   │   └── router.py
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── responses.py
│   ├── commands/
│   │   ├── __init__.py
│   │   └── init_currencies.py
│   ├── core/
│   │   ├── cache/
│   │   │   ├── backends/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── memory.py
│   │   │   │   ├── null.py
│   │   │   │   └── redis.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── decorators.py
│   │   │   ├── exceptions.py
│   │   │   ├── keys.py
│   │   │   ├── manager.py
│   │   │   └── service.py
│   │   ├── config/
│   │   │   ├── integrations/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── as400.py
│   │   │   │   └── elasticsearch.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── celery.py
│   │   │   ├── currency.py
│   │   │   ├── database.py
│   │   │   ├── fitment.py
│   │   │   ├── media.py
│   │   │   ├── security.py
│   │   │   └── settings.py
│   │   ├── error/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   ├── manager.py
│   │   │   ├── reporters.py
│   │   │   └── service.py
│   │   ├── events/
│   │   │   ├── __init__.py
│   │   │   ├── backend.py
│   │   │   └── init.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── domain.py
│   │   │   ├── handlers.py
│   │   │   └── system.py
│   │   ├── metrics/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── collectors.py
│   │   │   ├── decorators.py
│   │   │   ├── exceptions.py
│   │   │   ├── manager.py
│   │   │   ├── prometheus.py
│   │   │   ├── service.py
│   │   │   └── trackers.py
│   │   ├── pagination/
│   │   │   ├── providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── cursor.py
│   │   │   │   └── offset.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── exceptions.py
│   │   │   ├── factory.py
│   │   │   ├── manager.py
│   │   │   └── service.py
│   │   ├── permissions/
│   │   │   ├── __init__.py
│   │   │   ├── checker.py
│   │   │   ├── decorators.py
│   │   │   ├── models.py
│   │   │   ├── permissions.py
│   │   │   └── utils.py
│   │   ├── rate_limiting/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── limiter.py
│   │   │   ├── models.py
│   │   │   ├── rate_limiter.py
│   │   │   ├── service.py
│   │   │   └── utils.py
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── api_keys.py
│   │   │   ├── csrf.py
│   │   │   ├── dependencies.py
│   │   │   ├── encryption.py
│   │   │   ├── models.py
│   │   │   ├── passwords.py
│   │   │   ├── tokens.py
│   │   │   └── validation.py
│   │   ├── startup/
│   │   │   ├── __init__.py
│   │   │   └── as400_sync.py
│   │   ├── validation/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── db.py
│   │   │   ├── factory.py
│   │   │   ├── manager.py
│   │   │   ├── service.py
│   │   │   └── validators.py
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── celeryconfig.py
│   │   ├── dependency_manager.py
│   │   └── dependency_manager.pyi
│   ├── data_import/
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── import_products.py
│   │   │   └── sync_as400.py
│   │   ├── connectors/
│   │   │   ├── __init__.py
│   │   │   ├── as400_connector.py
│   │   │   ├── base.py
│   │   │   ├── file_connector.py
│   │   │   └── filemaker_connector.py
│   │   ├── importers/
│   │   │   ├── __init__.py
│   │   │   ├── as400_importers.py
│   │   │   ├── base.py
│   │   │   └── product_importer.py
│   │   ├── pipeline/
│   │   │   ├── __init__.py
│   │   │   ├── as400_pipeline.py
│   │   │   ├── base.py
│   │   │   └── product_pipeline.py
│   │   ├── processors/
│   │   │   ├── __init__.py
│   │   │   ├── as400_processor.py
│   │   │   ├── base.py
│   │   │   └── product_processor.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── session.py
│   │   └── utils.py
│   ├── domains/
│   │   ├── api_key/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── audit/
│   │   │   ├── service/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── factory.py
│   │   │   │   ├── loggers.py
│   │   │   │   ├── query.py
│   │   │   │   └── service.py
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── autocare/
│   │   │   ├── fitment/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── padb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── pcdb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── qdb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── vcdb/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── service.py
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── chat/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── service_DUPLICATEMAYBE.py
│   │   │   ├── tasks.py
│   │   │   └── websocket.py
│   │   ├── company/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── compliance/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── currency/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── tasks.py
│   │   ├── fitment/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── inventory/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── location/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── media/
│   │   │   ├── service/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   ├── factory.py
│   │   │   │   ├── local.py
│   │   │   │   ├── s3.py
│   │   │   │   ├── service.py
│   │   │   │   └── thumbnails.py
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── model_mapping/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── products/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   ├── reference/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── schemas.py
│   │   ├── security/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── models.py
│   │   │   ├── passwords.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   └── tokens.py
│   │   ├── sync_history/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── repository.py
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   ├── exceptions.py
│   │   │   ├── handlers.py
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   └── __init__.py
│   ├── fitment/
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── mapper.py
│   │   ├── models.py
│   │   ├── parser.py
│   │   └── validator.py
│   ├── i18n/
│   │   └── translations.py
│   ├── logging/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── context.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── error_handler.py
│   │   ├── logging.py
│   │   ├── metrics.py
│   │   ├── rate_limiting.py
│   │   ├── request_context.py
│   │   ├── response_formatter.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── associations.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── services/
│   │   ├── base_service/
│   │   │   ├── operations/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── create_update.py
│   │   │   │   └── read_delete.py
│   │   │   ├── __init__.py
│   │   │   ├── contracts.py
│   │   │   ├── permissions.py
│   │   │   └── service.py
│   │   ├── search/
│   │   │   ├── providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── database.py
│   │   │   │   └── elasticsearch.py
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   └── service.py
│   │   ├── __init__.py
│   │   ├── as400_sync_service.py
│   │   ├── interfaces.py
│   │   ├── test_service.py
│   │   └── vehicle.py
│   ├── tasks/
│   │   └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── circuit_breaker.py
│   │   ├── crypto.py
│   │   ├── file.py
│   │   ├── redis_manager.py
│   │   └── retry.py
│   ├── __init__.py
│   ├── as400_integration.md
│   └── main.py
├── autocare/
│   ├── ACES.xsd
│   ├── PAdb_schema.sql
│   ├── PCAdb_schema.sql
│   ├── PCdb_schema.sql
│   ├── PIES.xsd
│   ├── Qdb_schema.sql
│   └── VCdb_light_power_schema.sql
├── scripts/
│   ├── auto_translate.py
│   ├── bootstrap_countries.py
│   ├── database_bootstrap.py
│   ├── extract_messages.py
│   ├── init_db.py
│   └── reset_db.py
├── tests/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── test_auth.py
│   │   │   ├── test_products.py
│   │   │   └── test_users.py
│   │   └── __init__.py
│   ├── integration/
│   │   ├── test_api/
│   │   │   ├── test_auth.py
│   │   │   └── test_products.py
│   │   └── test_as400_sync.py
│   ├── unit/
│   │   ├── test_config.py
│   │   └── test_db.py
│   ├── utils/
│   │   └── factories.py
│   ├── __init__.py
│   ├── conftest.py
│   └── utils.py
├── DEVELOPERS_GUIDE.md
├── README.md
├── alembic.ini
├── backend.iml
├── pyproject.toml
├── pytest.ini
├── requirements.in
└── requirements.txt
```

[Back to Project Index](index.md)