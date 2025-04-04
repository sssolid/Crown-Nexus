from __future__ import annotations
import gettext
import os
from typing import Any, Dict, Optional
from fastapi import Depends, Header, Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
class I18nManager:
    def __init__(self) -> None:
        self.translations: Dict[str, gettext.GNUTranslations] = {}
        self.default_locale = settings.DEFAULT_LOCALE
        self.available_locales = settings.AVAILABLE_LOCALES
        self._load_translations()
    def _load_translations(self) -> None:
        locale_dir = os.path.join(settings.BASE_DIR, 'app', 'i18n', 'locales')
        default_domain = gettext.translation('messages', locale_dir, languages=[self.default_locale], fallback=True)
        self.translations[self.default_locale] = default_domain
        for locale in self.available_locales:
            if locale == self.default_locale:
                continue
            try:
                domain = gettext.translation('messages', locale_dir, languages=[locale], fallback=False)
                self.translations[locale] = domain
            except FileNotFoundError:
                self.translations[locale] = default_domain
    def gettext(self, message: str, locale: Optional[str]=None) -> str:
        if not locale:
            locale = self.default_locale
        if locale not in self.translations:
            locale = self.default_locale
        return self.translations[locale].gettext(message)
    def ngettext(self, singular: str, plural: str, n: int, locale: Optional[str]=None) -> str:
        if not locale:
            locale = self.default_locale
        if locale not in self.translations:
            locale = self.default_locale
        return self.translations[locale].ngettext(singular, plural, n)
i18n_manager = I18nManager()
def get_locale(request: Request, accept_language: Optional[str]=Header(None)) -> str:
    query_locale = request.query_params.get('lang')
    if query_locale and query_locale in i18n_manager.available_locales:
        return query_locale
    if accept_language:
        for locale_entry in accept_language.split(','):
            locale = locale_entry.split(';')[0].strip()
            if locale in i18n_manager.available_locales:
                return locale
    return i18n_manager.default_locale
class TranslatorDependency:
    def __init__(self, locale: Optional[str]=None):
        self.locale_override = locale
    async def __call__(self, locale: str=Depends(get_locale)) -> Dict[str, Any]:
        final_locale = self.locale_override or locale
        return {'_': lambda text: i18n_manager.gettext(text, final_locale), '_n': lambda singular, plural, n: i18n_manager.ngettext(singular, plural, n, final_locale), 'locale': final_locale}
get_translator = TranslatorDependency()
class I18nMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        locale = get_locale(request)
        request.state.locale = locale
        response = await call_next(request)
        return response