# Crown Nexus API Documentation

## Overview

The Crown Nexus API follows RESTful principles and is designed to be easy to use and integrate with various clients. All endpoints return JSON responses and accept JSON payloads where applicable.

## Base URL

All API endpoints are relative to the base URL:

```
/api/v1
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To authenticate, you need to:

1. Obtain an access token via the login endpoint
2. Include the token in the Authorization header of subsequent requests

Example:

```
Authorization: Bearer <your_access_token>
```

## Endpoints

The API includes the following main endpoints:

- **/auth**: Authentication-related endpoints
- **/users**: User management
- **/products**: Product catalog and management
- **/fitments**: Fitment data and associations
- **/media**: Media files management

## Interactive Documentation

When the API is running, you can access the interactive documentation at:

- Swagger UI: /api/v1/docs
- ReDoc: /api/v1/redoc

These provide a complete reference of all endpoints, request/response schemas, and the ability to try out API calls directly from the browser.

## Pagination

List endpoints support pagination with the following query parameters:

- **page**: Page number (starting from 1)
- **page_size**: Number of items per page

Example:

```
GET /api/v1/products?page=2&page_size=20
```

Response includes pagination metadata:

```json
{
  "items": [...],
  "total": 100,
  "page": 2,
  "page_size": 20,
  "pages": 5
}
```

## Filtering

Most list endpoints support filtering via query parameters. The specific filters are documented in the interactive documentation for each endpoint.

Example:

```
GET /api/v1/products?category_id=123&search=brake
```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests. In case of an error, the response body will include additional information:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common status codes:

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid input or request parameters
- **401 Unauthorized**: Authentication required or failed
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error
