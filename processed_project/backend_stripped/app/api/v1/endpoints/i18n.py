from typing import Annotated, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.i18n.translations import i18n_manager, get_locale
router = APIRouter()
@router.get('/messages/{locale}')
async def get_messages(locale: Annotated[str, Path(description='Locale code')]) -> Dict[str, Dict[str, str]]:
    if locale not in i18n_manager.available_locales:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Locale '{locale}' not found")
    sample_messages = {'common': {'save': 'Save', 'cancel': 'Cancel', 'delete': 'Delete', 'edit': 'Edit', 'back': 'Back', 'next': 'Next', 'search': 'Search', 'filter': 'Filter', 'sort': 'Sort', 'loading': 'Loading...', 'noResults': 'No results found', 'error': 'An error occurred'}, 'auth': {'login': 'Login', 'logout': 'Logout', 'register': 'Register', 'forgotPassword': 'Forgot password?', 'resetPassword': 'Reset password', 'username': 'Username', 'password': 'Password', 'confirmPassword': 'Confirm password', 'email': 'Email'}, 'products': {'product': 'Product', 'products': 'Products', 'partNumber': 'Part Number', 'description': 'Description', 'category': 'Category', 'price': 'Price', 'stock': 'Stock', 'addToCart': 'Add to cart', 'outOfStock': 'Out of stock', 'details': 'Details'}}
    return sample_messages
@router.get('/current-locale')
async def get_current_locale(locale: Annotated[str, Depends(get_locale)]) -> Dict[str, str]:
    return {'locale': locale}