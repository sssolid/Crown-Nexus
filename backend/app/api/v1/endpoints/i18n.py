# backend/app/api/v1/endpoints/i18n.py
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.i18n.translations import i18n_manager, get_locale

router = APIRouter()


@router.get("/messages/{locale}")
async def get_messages(
    locale: Annotated[str, Path(description="Locale code")],
) -> Dict[str, Dict[str, str]]:
    """
    Get all translation messages for a specific locale.

    Args:
        locale: Locale code (e.g., 'en', 'es')

    Returns:
        Dict[str, Dict[str, str]]: Translation messages for the requested locale
    """
    if locale not in i18n_manager.available_locales:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Locale '{locale}' not found"
        )

    # In a real implementation, you would load messages from your translation files
    # For this example, we'll generate a simple response
    # This is where you would integrate with your actual translation system

    # Example structure - in reality, you would load this from your .mo files
    # or database
    sample_messages = {
        "common": {
            "save": "Save",
            "cancel": "Cancel",
            "delete": "Delete",
            "edit": "Edit",
            "back": "Back",
            "next": "Next",
            "search": "Search",
            "filter": "Filter",
            "sort": "Sort",
            "loading": "Loading...",
            "noResults": "No results found",
            "error": "An error occurred",
        },
        "auth": {
            "login": "Login",
            "logout": "Logout",
            "register": "Register",
            "forgotPassword": "Forgot password?",
            "resetPassword": "Reset password",
            "username": "Username",
            "password": "Password",
            "confirmPassword": "Confirm password",
            "email": "Email",
        },
        "products": {
            "product": "Product",
            "products": "Products",
            "partNumber": "Part Number",
            "description": "Description",
            "category": "Category",
            "price": "Price",
            "stock": "Stock",
            "addToCart": "Add to cart",
            "outOfStock": "Out of stock",
            "details": "Details",
        },
    }

    return sample_messages


@router.get("/current-locale")
async def get_current_locale(
    locale: Annotated[str, Depends(get_locale)],
) -> Dict[str, str]:
    """
    Get the current locale based on the request.

    Args:
        locale: Current locale from dependency

    Returns:
        Dict[str, str]: Current locale information
    """
    return {"locale": locale}
