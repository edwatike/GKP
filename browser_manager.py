import os
import random
import subprocess
import time
from pathlib import Path

class BrowserManager:
    def __init__(self, base_profile_dir="/home/edwa/Project/grokbot/ChromeProfile"):
        self.base_profile_dir = base_profile_dir
        self.current_profile = None
        
    def _kill_browser_processes(self):
        """Завершает все процессы браузера"""
        try:
            subprocess.run(['pkill', 'chromium'], check=False)
            subprocess.run(['pkill', 'chrome'], check=False)
            time.sleep(1)  # Даем время на завершение процессов
        except Exception as e:
            print(f"Ошибка при завершении процессов браузера: {e}")

    def _remove_singleton_lock(self, profile_dir):
        """Удаляет файл блокировки профиля"""
        lock_file = os.path.join(profile_dir, "SingletonLock")
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
                time.sleep(0.5)  # Даем время на освобождение файловой системы
        except Exception as e:
            print(f"Ошибка при удалении файла блокировки: {e}")

    def get_profile_dir(self, use_random=False):
        """Возвращает путь к профилю браузера"""
        if use_random:
            profile_suffix = f"_{random.randint(1000, 9999)}"
            self.current_profile = f"{self.base_profile_dir}{profile_suffix}"
        else:
            self.current_profile = self.base_profile_dir

        # Создаем директорию профиля, если она не существует
        os.makedirs(self.current_profile, exist_ok=True)
        return self.current_profile

    def prepare_profile(self, use_random=False):
        """Подготавливает профиль браузера к использованию"""
        self._kill_browser_processes()
        profile_dir = self.get_profile_dir(use_random)
        self._remove_singleton_lock(profile_dir)
        return profile_dir

    @staticmethod
    def get_stealth_args():
        """Возвращает аргументы запуска для обхода антибот-защиты"""
        return [
            '--disable-blink-features=AutomationControlled',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-site-isolation-trials',
            '--disable-features=BlockInsecurePrivateNetworkRequests',
            '--disable-web-security',
            '--no-sandbox',
            '--disable-process-singleton',
            f'--window-size={random.randint(1050, 1200)},{random.randint(800, 900)}',
            '--start-maximized',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--ignore-certificate-errors',
            '--no-default-browser-check',
            '--no-first-run',
            '--disable-infobars',
            '--disable-gpu'
        ] 