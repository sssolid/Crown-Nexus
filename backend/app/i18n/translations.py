# backend/app/i18n/translations.py
from __future__ import annotations

import gettext
import os
from typing import Any, Dict, Optional

from fastapi import Depends, Header, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


class I18nManager:
    """
    Manages internationalization (i18n) for the application.
    
    Provides functions to translate text based on the current locale.
    Translations are loaded from gettext .mo files.
    """
    
    def __init__(self) -> None:
        """Initialize the I18nManager."""
        self.translations: Dict[str, gettext.GNUTranslations] = {}
        self.default_locale = settings.DEFAULT_LOCALE
        self.available_locales = settings.AVAILABLE_LOCALES
        self._load_translations()
    
    def _load_translations(self) -> None:
        """Load all available translations."""
        locale_dir = os.path.join(settings.BASE_DIR, "app", "i18n", "locales")
        
        # Load default locale first
        default_domain = gettext.translation(
            "messages", 
            locale_dir, 
            languages=[self.default_locale],
            fallback=True
        )
        self.translations[self.default_locale] = default_domain
        
        # Load other available locales
        for locale in self.available_locales:
            if locale == self.default_locale:
                continue
                
            try:
                domain = gettext.translation(
                    "messages", 
                    locale_dir, 
                    languages=[locale],
                    fallback=False
                )
                self.translations[locale] = domain
            except FileNotFoundError:
                # If translation file doesn't exist, fall back to default
                self.translations[locale] = default_domain
    
    def gettext(self, message: str, locale: Optional[str] = None) -> str:
        """
        Translate a message to the specified locale.
        
        Args:
            message: The message to translate
            locale: The locale to translate to, or None for default
            
        Returns:
            str: The translated message
        """
        if not locale:
            locale = self.default_locale
            
        if locale not in self.translations:
            locale = self.default_locale
            
        return self.translations[locale].gettext(message)
    
    def ngettext(self, singular: str, plural: str, n: int, locale: Optional[str] = None) -> str:
        """
        Translate singular/plural form based on number.
        
        Args:
            singular: Singular form
            plural: Plural form
            n: The count determining which form to use
            locale: The locale to translate to, or None for default
            
        Returns:
            str: The translated message
        """
        if not locale:
            locale = self.default_locale
            
        if locale not in self.translations:
            locale = self.default_locale
            
        return self.translations[locale].ngettext(singular, plural, n)


# Create a global instance
i18n_manager = I18nManager()


def get_locale(request: Request, accept_language: Optional[str] = Header(None)) -> str:
    """
    Determine the best locale based on the request.
    
    Priority:
    1. Query parameter 'lang'
    2. Accept-Language header
    3. User preferences (if authenticated)
    4. Default locale
    
    Args:
        request: FastAPI request object
        accept_language: Accept-Language header
        
    Returns:
        str: Best matching locale
    """
    # Check query parameter
    query_locale = request.query_params.get("lang")
    if query_locale and query_locale in i18n_manager.available_locales:
        return query_locale
    
    # Check Accept-Language header
    if accept_language:
        # Parse the Accept-Language header (simplistic implementation)
        for locale_entry in accept_language.split(","):
            locale = locale_entry.split(";")[0].strip()
            if locale in i18n_manager.available_locales:
                return locale
    
    # Check user preferences if authenticated
    # This would require accessing the current user from the request state
    # if hasattr(request.state, "user") and request.state.user.preferred_language:
    #     preferred_language = request.state.user.preferred_language
    #     if preferred_language in i18n_manager.available_locales:
    #         return preferred_language
    
    # Fall back to default locale
    return i18n_manager.default_locale


class TranslatorDependency:
    """
    Dependency that provides a translator function for the current request.
    """
    
    def __init__(self, locale: Optional[str] = None):
        """
        Initialize the TranslatorDependency.
        
        Args:
            locale: Optional locale override
        """
        self.locale_override = locale
    
    async def __call__(
        self, locale: str = Depends(get_locale)
    ) -> Dict[str, Any]:
        """
        Get translation functions for the current locale.
        
        Args:
            locale: The locale from get_locale dependency
            
        Returns:
            Dict[str, Any]: Translation functions
        """
        final_locale = self.locale_override or locale
        
        return {
            "_": lambda text: i18n_manager.gettext(text, final_locale),
            "_n": lambda singular, plural, n: i18n_manager.ngettext(singular, plural, n, final_locale),
            "locale": final_locale
        }


# Convenient shorthand for dependency injection
get_translator = TranslatorDependency()


class I18nMiddleware(BaseHTTPMiddleware):
    """
    Middleware to set locale in request state.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process a request and set locale in request state.
        
        Args:
            request: FastAPI request
            call_next: Next middleware handler
            
        Returns:
            Response from next middleware
        """
        locale = get_locale(request)
        request.state.locale = locale
        
        response = await call_next(request)
        return response
