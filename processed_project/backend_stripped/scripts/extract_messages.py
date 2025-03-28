import os
import subprocess
from app.core.config import settings
def extract_python_messages() -> None:
    base_dir = settings.BASE_DIR
    locale_dir = os.path.join(base_dir, 'app', 'i18n', 'locales')
    pot_file = os.path.join(locale_dir, 'messages.pot')
    os.makedirs(locale_dir, exist_ok=True)
    cmd = ['pybabel', 'extract', '--charset=utf-8', f'--output={pot_file}', '--keywords=_:1,2', '--keywords=_n:1,2', '--no-location', '--project=Crown-Nexus', '--copyright-holder=Your Company', '--msgid-bugs-address=translations@example.com', 'app']
    print('Extracting messages from Python files...')
    subprocess.run(cmd, cwd=base_dir, check=True)
    print(f'Messages extracted to {pot_file}')
def update_translation_files() -> None:
    base_dir = settings.BASE_DIR
    locale_dir = os.path.join(base_dir, 'app', 'i18n', 'locales')
    pot_file = os.path.join(locale_dir, 'messages.pot')
    for locale in settings.AVAILABLE_LOCALES:
        locale_path = os.path.join(locale_dir, locale, 'LC_MESSAGES')
        po_file = os.path.join(locale_path, 'messages.po')
        os.makedirs(locale_path, exist_ok=True)
        if os.path.exists(po_file):
            print(f"Updating translation file for locale '{locale}'...")
            cmd = ['pybabel', 'update', f'--input-file={pot_file}', f'--output-file={po_file}', f'--locale={locale}']
            subprocess.run(cmd, cwd=base_dir, check=True)
        else:
            print(f"Creating new translation file for locale '{locale}'...")
            cmd = ['pybabel', 'init', f'--input-file={pot_file}', f'--output-file={po_file}', f'--locale={locale}']
            subprocess.run(cmd, cwd=base_dir, check=True)
def compile_translation_files() -> None:
    base_dir = settings.BASE_DIR
    locale_dir = os.path.join(base_dir, 'app', 'i18n', 'locales')
    for locale in settings.AVAILABLE_LOCALES:
        locale_path = os.path.join(locale_dir, locale, 'LC_MESSAGES')
        po_file = os.path.join(locale_path, 'messages.po')
        if os.path.exists(po_file):
            print(f"Compiling translation file for locale '{locale}'...")
            cmd = ['pybabel', 'compile', f'--directory={locale_dir}', f'--locale={locale}']
            subprocess.run(cmd, cwd=base_dir, check=True)
if __name__ == '__main__':
    extract_python_messages()
    update_translation_files()
    compile_translation_files()