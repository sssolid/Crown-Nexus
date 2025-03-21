# AS400 Integration

This documentation covers the AS400 integration system, which securely synchronizes data between your AS400 (iSeries) database and the application.

## Overview

The AS400 integration provides a secure, read-only synchronization of critical data from your AS400 database to the application database. It includes:

- Secure connections with multiple security layers
- Scheduled automatic synchronization
- Manual synchronization through CLI commands
- Robust error handling and retry mechanisms
- Detailed synchronization auditing and logging

## Architecture

The integration follows a secure, layered architecture:

1. **Connector Layer**: Establishes secure connections to AS400 using read-only accounts
2. **Processor Layer**: Transforms AS400 data into application models
3. **Importer Layer**: Safely creates or updates records in the application database
4. **Service Layer**: Orchestrates and schedules synchronization operations
5. **Monitoring Layer**: Tracks synchronization status and performance

## Security Features

Security is a top priority in this implementation:

- **Read-Only Access**: The integration uses read-only accounts for AS400 access
- **Table Whitelisting**: Only explicitly allowed tables can be accessed
- **Query Validation**: All SQL is validated before execution to prevent SQL injection
- **SSL Encryption**: Communications are encrypted when available
- **Credential Protection**: Passwords are handled as secure strings and not logged
- **Audit Logging**: All synchronization operations are audited for security review

## Configuration

### Environment Variables

The following environment variables must be set:

```
AS400_DSN=your_dsn
AS400_USERNAME=your_username
AS400_PASSWORD=your_password
AS400_DATABASE=your_database
AS400_SERVER=optional_server_name
AS400_PORT=optional_port
AS400_SSL=true
AS400_ALLOWED_TABLES=TABLE1,TABLE2,TABLE3
AS400_SYNC_ENABLED=true
AS400_SYNC_INTERVAL=86400
```

### Configuration File

For more detailed configuration, modify `app/core/config/as400.py`.

## Data Mappings

The following data is synchronized from AS400:

| AS400 Table | Application Model | Sync Frequency | Description |
|-------------|-------------------|----------------|-------------|
| PRODUCTLIB.PRODUCTS | Product | Daily | Product master data |
| PRODUCTLIB.MEASUREMENTS | ProductMeasurement | Daily | Product dimensions and weights |
| INVENTORYLIB.INVENTORY | ProductStock | Hourly | Inventory levels |
| PRODUCTLIB.PRICING | ProductPricing | Daily | Product pricing information |

## Usage

### Automatic Synchronization

By default, synchronization runs automatically at the intervals specified in configuration.
No action is required for this.

### Manual Synchronization

For manual synchronization, use the CLI commands:

```bash
# Run product synchronization
python -m app.commands.sync_as400 sync --entity product

# Run stock synchronization
python -m app.commands.sync_as400 sync --entity stock

# Check synchronization status
python -m app.commands.sync_as400 status

# Test AS400 connection
python -m app.commands.sync_as400 test-connection
```

### Monitoring

Synchronization status can be monitored through:

1. Application logs (`logs/as400_sync.log`)
2. Database records in the `sync_history` and `sync_event` tables
3. CLI status command: `python -m app.commands.sync_as400 status`

## Troubleshooting

### Connection Issues

If experiencing connection problems:

1. Verify environment variables are correctly set
2. Ensure firewall rules allow connections to AS400
3. Check network connectivity with `ping`
4. Validate DSN configuration
5. Run the connection test: `python -m app.commands.sync_as400 test-connection`

### Synchronization Failures

If synchronization fails:

1. Check logs for detailed error messages
2. Verify table permissions on AS400
3. Confirm field mappings in processor configuration
4. Try running with smaller batch sizes

## Adding New Sync Entities

To add synchronization for additional AS400 data:

1. Define the data model in `app/models/`
2. Create a Pydantic schema in `app/schemas/`
3. Add a processor in `app/data_import/processors/as400_processor.py`
4. Add an importer in `app/data_import/importers/as400_importers.py`
5. Add a sync method in `app/services/as400_sync_service.py`
6. Update the `SyncEntityType` enum to include the new entity

## Performance Considerations

For optimal performance:

- Use appropriate sync intervals for each data type
- Configure batch sizes based on record size
- Schedule sync operations during low-traffic periods
- Monitor database load during synchronization
- Consider adding indexes to frequently accessed fields

## Technical Details

The integration uses several technologies:

- **pyodbc**: For AS400 database connectivity via ODBC
- **SQLAlchemy**: For ORM operations
- **Pydantic**: For data validation
- **asyncio**: For asynchronous processing
- **typer**: For CLI commands

## Support

For issues or questions related to the AS400 integration, contact the development team.
