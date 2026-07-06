#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import requests
import random
import string
import time
import json
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs

# ============================================================================
# КОНФИГУРАЦИЯ ПРОГРАММЫ
# ============================================================================
CONFIG = {
    "title": "Vostro - Engagement Service",
    "version": "3.0.0",
    "window_size": "800x650",
    "theme_bg": "#1a1a2e",
    "theme_fg": "#e0e0e0",
    "theme_accent": "#e94560",
    "theme_button": "#0f3460",
    "theme_button_hover": "#16213e",
    "theme_entry_bg": "#16213e",
    "theme_entry_fg": "#ffffff",
    "max_threads": 50,
    "api_timeout": 15,
    "retry_attempts": 3,
    "retry_delay": 1.5,
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.169 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    ]
}

# ============================================================================
# ГЕНЕРАТОР УЧЁТНЫХ ЗАПИСЕЙ БОТОВ
# ============================================================================
class BotAccountGenerator:
    """Генерирует уникальные учётные данные для каждого бота."""
    
    FIRST_NAMES_MALE = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas",
        "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven",
        "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian", "George", "Timothy", "Ronald",
        "Edward", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan",
        "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Raymond",
        "Gregory", "Frank", "Alexander", "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron",
        "Jose", "Adam", "Nathan", "Henry", "Douglas", "Zachary", "Peter", "Kyle", "Ethan",
        "Walter", "Noah", "Jeremy", "Christian", "Keith", "Roger", "Terry", "Gerald", "Harold",
        "Sean", "Austin", "Carl", "Arthur", "Lawrence", "Dylan", "Jesse", "Jordan", "Bryan",
        "Billy", "Joe", "Bruce", "Gabriel", "Logan", "Albert", "Willie", "Alan", "Juan",
        "Wayne", "Elijah", "Randy", "Roy", "Vincent", "Ralph", "Eugene", "Russell", "Bobby",
        "Mason", "Philip", "Louis"
    ]
    
    FIRST_NAMES_FEMALE = [
        "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica",
        "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra", "Ashley", "Dorothy",
        "Kimberly", "Emily", "Donna", "Michelle", "Carol", "Amanda", "Melissa", "Deborah",
        "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen", "Amy", "Angela",
        "Shirley", "Anna", "Brenda", "Pamela", "Emma", "Nicole", "Helen", "Samantha",
        "Katherine", "Christine", "Debra", "Rachel", "Carolyn", "Janet", "Catherine", "Maria",
        "Heather", "Diane", "Ruth", "Julie", "Olivia", "Joyce", "Virginia", "Victoria",
        "Kelly", "Lauren", "Christina", "Joan", "Madison", "Martha", "Judith", "Cheryl",
        "Megan", "Andrea", "Hannah", "Jacqueline", "Ann", "Jean", "Alice", "Teresa", "Gloria",
        "Doris", "Sara", "Janice", "Kathryn", "Abigail", "Sophia", "Isabella", "Grace",
        "Marie", "Denise", "Amber", "Danielle", "Beverly", "Marilyn", "Brittany", "Natalie",
        "Diana", "Rose", "Julia", "Theresa", "Kayla", "Alexis", "Lori"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
        "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
        "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
        "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson",
        "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
        "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster"
    ]
    
    DOMAINS = [
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com",
        "protonmail.com", "mail.com", "aol.com", "zoho.com", "yandex.com"
    ]
    
    def __init__(self):
        self.used_usernames = set()
        self.used_emails = set()
        self.lock = threading.Lock()
    
    def _random_string(self, length=8, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choices(chars, k=length))
    
    def _generate_username(self):
        prefixes = ["user", "the", "real", "its", "official", "mr", "ms", "dr", "king", "queen",
                    "lil", "big", "super", "mega", "ultra", "pro", "elite", "vip", "cool", "hot"]
        patterns = [
            lambda: f"{random.choice(prefixes)}_{self._random_string(5)}",
            lambda: f"{random.choice(self.FIRST_NAMES_MALE + self.FIRST_NAMES_FEMALE).lower()}_{self._random_string(4)}",
            lambda: f"{random.choice(self.LAST_NAMES).lower()}.{self._random_string(3)}",
            lambda: f"{self._random_string(6)}_{random.randint(10, 9999)}",
            lambda: f"{random.choice(prefixes)}{random.choice(self.LAST_NAMES).lower()}{random.randint(1, 999)}",
            lambda: f"{self._random_string(4)}_{self._random_string(4)}_{random.randint(100, 999)}",
        ]
        while True:
            username = random.choice(patterns)()
            if len(username) <= 30 and username not in self.used_usernames:
                with self.lock:
                    self.used_usernames.add(username)
                return username
    
    def _generate_email(self, username):
        patterns = [
            lambda: f"{username}{random.randint(1, 9999)}@{random.choice(self.DOMAINS)}",
            lambda: f"{username}_{random.randint(10, 9999)}@{random.choice(self.DOMAINS)}",
            lambda: f"{username}.{random.randint(100, 9999)}@{random.choice(self.DOMAINS)}",
            lambda: f"{username}{self._random_string(3)}@{random.choice(self.DOMAINS)}",
            lambda: f"{random.choice(self.FIRST_NAMES_MALE + self.FIRST_NAMES_FEMALE).lower()}{random.randint(100, 99999)}@{random.choice(self.DOMAINS)}",
        ]
        while True:
            email = random.choice(patterns)()
            if email not in self.used_emails and len(email) <= 50:
                with self.lock:
                    self.used_emails.add(email)
                return email
    
    def generate_bot_account(self):
        """Создаёт полный профиль бота."""
        gender = random.choice(["male", "female"])
        if gender == "male":
            first_name = random.choice(self.FIRST_NAMES_MALE)
        else:
            first_name = random.choice(self.FIRST_NAMES_FEMALE)
        last_name = random.choice(self.LAST_NAMES)
        
        username = self._generate_username()
        email = self._generate_email(username)
        
        bio_options = [
            f"Just living life ✌️ | {first_name}",
            f"{random.choice(['Music', 'Art', 'Travel', 'Food', 'Fitness'])} lover 🎵",
            f"Dream big ✨ | {random.choice(['Dog', 'Cat'])} person",
            f"Be yourself; everyone else is already taken.",
            f"{random.choice(['Coffee', 'Tea', 'Sunsets', 'Photography'])} addict ☕",
            f"Making memories | {first_name} {last_name[0]}.",
            f"Stay positive, work hard, make it happen 💪",
            f"Just a {random.choice(['simple', 'cool', 'chill'])} person 🌟",
            f"Life is what happens when you're busy making other plans.",
            f"Living my best life 🚀",
        ]
        
        return {
            "username": username,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "bio": random.choice(bio_options),
            "gender": gender,
            "age": random.randint(18, 45),
            "profile_pic_seed": random.randint(1, 99999),
            "device_id": f"android_{self._random_string(16)}",
            "device_model": random.choice([
                "SM-G998B", "iPhone12,1", "Pixel 6 Pro", "SM-A525F", "iPhone13,2",
                "Redmi Note 10", "OnePlus 9", "iPhone14,3", "SM-G991B", "Pixel 7"
            ]),
            "os_version": random.choice([
                "Android 13", "Android 12", "iOS 16.5", "iOS 17.1", "Android 14",
                "iOS 16.7", "Android 11", "iOS 15.7"
            ]),
            "app_version": random.choice([
                "28.3.1", "28.4.0", "28.2.3", "28.5.0", "28.3.2", "28.6.1"
            ]),
        }

# ============================================================================
# СЕТЕВОЙ ДВИЖОК
# ============================================================================
class NetworkEngine:
    """Управляет HTTP-запросами с ротацией заголовков и сессий."""
    
    def __init__(self):
        self.session_pool = []
        self.lock = threading.Lock()
        self._init_session_pool()
    
    def _init_session_pool(self, pool_size=30):
        for _ in range(pool_size):
            session = requests.Session()
            session.headers.update({
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": random.choice([
                    "en-US,en;q=0.9", "en-GB,en;q=0.8", "en-CA,en;q=0.7",
                    "es-ES,es;q=0.9", "fr-FR,fr;q=0.8", "de-DE,de;q=0.7"
                ]),
                "Accept-Encoding": "gzip, deflate, br",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.tiktok.com",
                "Referer": "https://www.tiktok.com/",
            })
            self.session_pool.append(session)
    
    def get_session(self):
        with self.lock:
            if not self.session_pool:
                self._init_session_pool(10)
            return self.session_pool.pop()
    
    def return_session(self, session):
        with self.lock:
            if len(self.session_pool) < 50:
                self.session_pool.append(session)
    
    def get_random_headers(self, bot_account):
        return {
            "User-Agent": random.choice(CONFIG["user_agents"]),
            "X-Tt-Device-Id": bot_account["device_id"],
            "X-Tt-Device-Model": bot_account["device_model"],
            "X-Tt-Os-Version": bot_account["os_version"],
            "X-Tt-App-Version": bot_account["app_version"],
            "Cookie": f"sessionid={self._gen_session_token()}; tt_webid={self._gen_webid()}; "
                      f"tt_webid_v2={self._gen_webid()}; odin_tt={self._gen_odin_tt()}; "
                      f"csrftoken={self._gen_csrf_token()};"
        }
    
    def _gen_session_token(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
    
    def _gen_webid(self):
        return ''.join(random.choices(string.digits, k=19))
    
    def _gen_odin_tt(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
    
    def _gen_csrf_token(self):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
    
    def make_request(self, url, method="GET", data=None, bot_account=None, proxy=None):
        session = self.get_session()
        try:
            headers = self.get_random_headers(bot_account) if bot_account else {}
            session.headers.update(headers)
            
            proxies = None
            if proxy:
                proxies = {"http": proxy, "https": proxy}
            
            for attempt in range(CONFIG["retry_attempts"]):
                try:
                    if method.upper() == "GET":
                        resp = session.get(url, timeout=CONFIG["api_timeout"], proxies=proxies)
                    else:
                        resp = session.post(url, json=data, timeout=CONFIG["api_timeout"], proxies=proxies)
                    
                    if resp.status_code == 200:
                        return resp
                    elif resp.status_code == 429:
                        time.sleep(CONFIG["retry_delay"] * (attempt + 1))
                        continue
                    else:
                        return resp
                except requests.exceptions.RequestException:
                    if attempt < CONFIG["retry_attempts"] - 1:
                        time.sleep(CONFIG["retry_delay"])
                    else:
                        return None
            return None
        finally:
            self.return_session(session)

# ============================================================================
# СИМУЛЯТОР API TIKTOK (В РЕАЛЬНОСТИ - ВЗАИМОДЕЙСТВИЕ С ЭМУЛИРУЕМЫМИ ЭНДПОИНТАМИ)
# ============================================================================
class TikTokAPI:
    """Обрабатывает запросы к TikTok (симулированные эндпоинты)."""
    
    FOLLOW_ENDPOINTS = [
        "https://www.tiktok.com/api/v1/commit/follow/user/",
        "https://m.tiktok.com/api/v1/commit/follow/user/",
        "https://api2.musical.ly/aweme/v1/commit/follow/user/",
        "https://api2-16.tiktokv.com/aweme/v1/commit/follow/user/",
    ]
    
    LIKE_ENDPOINTS = [
        "https://www.tiktok.com/api/v1/commit/item/like/",
        "https://m.tiktok.com/api/v1/commit/item/like/",
        "https://api2.musical.ly/aweme/v1/commit/item/like/",
        "https://api2-16.tiktokv.com/aweme/v1/commit/item/like/",
    ]
    
    COMMENT_LIKE_ENDPOINTS = [
        "https://www.tiktok.com/api/v1/commit/comment/like/",
        "https://m.tiktok.com/api/v1/commit/comment/like/",
        "https://api2.musical.ly/aweme/v1/commit/comment/like/",
    ]
    
    VIEW_ENDPOINTS = [
        "https://www.tiktok.com/api/v1/commit/item/view/",
        "https://m.tiktok.com/api/v1/commit/item/view/",
        "https://api2-16.tiktokv.com/aweme/v1/commit/item/view/",
    ]
    
    SHARE_ENDPOINTS = [
        "https://www.tiktok.com/api/v1/commit/item/share/",
        "https://m.tiktok.com/api/v1/commit/item/share/",
        "https://api2.musical.ly/aweme/v1/commit/item/share/",
    ]
    
    SAVE_ENDPOINTS = [
        "https://www.tiktok.com/api/v1/commit/item/favorite/",
        "https://m.tiktok.com/api/v1/commit/item/favorite/",
        "https://api2.musical.ly/aweme/v1/commit/item/favorite/",
    ]
    
    @staticmethod
    def extract_user_id(target_url):
        """Извлекает ID пользователя из URL."""
        try:
            # Обработка различных форматов URL
            parsed = urlparse(target_url)
            path_parts = parsed.path.strip("/").split("/")
            
            # Формат: tiktok.com/@username
            if "@" in parsed.path:
                for part in path_parts:
                    if part.startswith("@"):
                        return f"@{part[1:]}"  # возвращаем username как идентификатор
            
            # Формат: tiktok.com/user/username
            if "user" in path_parts:
                idx = path_parts.index("user")
                if idx + 1 < len(path_parts):
                    return f"@{path_parts[idx + 1]}"
            
            return parsed.path.split("@")[-1].split("/")[0] if "@" in parsed.path else parsed.path.split("/")[-1]
        except Exception:
            return target_url.split("@")[-1].split("/")[0] if "@" in target_url else target_url
    
    @staticmethod
    def extract_video_id(video_url):
        """Извлекает ID видео из URL."""
        try:
            # Формат: tiktok.com/@user/video/123456789
            parsed = urlparse(video_url)
            path_parts = parsed.path.strip("/").split("/")
            if "video" in path_parts:
                idx = path_parts.index("video")
                if idx + 1 < len(path_parts):
                    return path_parts[idx + 1]
            # Формат: vm.tiktok.com/XXXXX или tiktok.com/v/12345
            return path_parts[-1] if path_parts else None
        except Exception:
            return video_url.split("/video/")[-1].split("?")[0] if "/video/" in video_url else video_url.split("/")[-1]
    
    @staticmethod
    def extract_comment_id(comment_url):
        """Извлекает ID комментария из URL."""
        try:
            if "comment" in comment_url.lower():
                parsed = urlparse(comment_url)
                query_params = parse_qs(parsed.query)
                if "cid" in query_params:
                    return query_params["cid"][0]
                path_parts = parsed.path.strip("/").split("/")
                for part in path_parts:
                    if part.isdigit() and len(part) > 10:
                        return part
            return comment_url.split("/")[-1]
        except Exception:
            return comment_url

# ============================================================================
# ЛОГИКА ВЫПОЛНЕНИЯ ДЕЙСТВИЙ
# ============================================================================
class EngagementExecutor:
    """Выполняет накрутку с использованием ботов."""
    
    def __init__(self, network_engine, logger_callback=None):
        self.network = network_engine
        self.bot_generator = BotAccountGenerator()
        self.logger = logger_callback or print
        self.stats = {"success": 0, "failed": 0, "total": 0}
        self.running = False
        self.lock = threading.Lock()
    
    def _log(self, message):
        if self.logger:
            self.logger(message)
    
    def _simulate_action(self, bot, target_id, action_type, endpoint_list):
        """
        Симулирует действие бота. В реальном сценарии здесь было бы обращение
        к API TikTok с правильными токенами и подписями.
        """
        endpoint = random.choice(endpoint_list)
        
        # Симуляция данных запроса
        payload = {
            "user_id": bot["username"],
            "target_id": target_id,
            "device_id": bot["device_id"],
            "session_token": ''.join(random.choices(string.ascii_letters + string.digits, k=128)),
            "timestamp": int(time.time() * 1000),
            "nonce": ''.join(random.choices(string.hexdigits, k=32)),
            "app_version": bot["app_version"],
            "os_version": bot["os_version"],
            "device_model": bot["device_model"],
            "action_type": action_type,
            "client": "mobile",
            "region": random.choice(["US", "GB", "CA", "AU", "DE", "FR", "BR", "MX", "JP", "KR"]),
            "lang": random.choice(["en", "es", "pt", "fr", "de", "ja", "ko"]),
        }
        
        # Симулируем сетевую задержку
        delay = random.uniform(0.3, 2.5)
        time.sleep(delay)
        
        # Симулируем ответ (в реальности - HTTP-запрос)
        success = random.random() < 0.92  # 92% вероятность успеха для симуляции
        
        return {
            "success": success,
            "bot_username": bot["username"],
            "target_id": target_id,
            "action": action_type,
            "timestamp": datetime.now().isoformat(),
            "delay": delay,
            "endpoint_used": endpoint,
        }
    
    def execute_follow(self, target_url, count):
        """Выполняет подписки."""
        self._log(f"[FOLLOW] Starting {count} follows for {target_url}")
        target_id = TikTokAPI.extract_user_id(target_url)
        return self._run_batch("follow", target_id, count, TikTokAPI.FOLLOW_ENDPOINTS)
    
    def execute_like(self, video_url, count):
        """Выполняет лайки на видео."""
        self._log(f"[LIKE] Starting {count} likes for {video_url}")
        target_id = TikTokAPI.extract_video_id(video_url)
        return self._run_batch("like", target_id, count, TikTokAPI.LIKE_ENDPOINTS)
    
    def execute_comment_like(self, comment_url, count):
        """Выполняет лайки на комментариях."""
        self._log(f"[COMMENT_LIKE] Starting {count} comment likes for {comment_url}")
        target_id = TikTokAPI.extract_comment_id(comment_url)
        return self._run_batch("comment_like", target_id, count, TikTokAPI.COMMENT_LIKE_ENDPOINTS)
    
    def execute_views(self, video_url, count):
        """Выполняет просмотры."""
        self._log(f"[VIEW] Starting {count} views for {video_url}")
        target_id = TikTokAPI.extract_video_id(video_url)
        return self._run_batch("view", target_id, count, TikTokAPI.VIEW_ENDPOINTS)
    
    def execute_shares(self, video_url, count):
        """Выполняет репосты."""
        self._log(f"[SHARE] Starting {count} shares for {video_url}")
        target_id = TikTokAPI.extract_video_id(video_url)
        return self._run_batch("share", target_id, count, TikTokAPI.SHARE_ENDPOINTS)
    
    def execute_saves(self, video_url, count):
        """Выполняет сохранения."""
        self._log(f"[SAVE] Starting {count} saves for {video_url}")
        target_id = TikTokAPI.extract_video_id(video_url)
        return self._run_batch("save", target_id, count, TikTokAPI.SAVE_ENDPOINTS)
    
    def _run_batch(self, action_type, target_id, count, endpoints):
        """Запускает пакетное выполнение действий."""
        results = []
        self.running = True
        
        with ThreadPoolExecutor(max_workers=CONFIG["max_threads"]) as executor:
            futures = []
            for i in range(count):
                bot = self.bot_generator.generate_bot_account()
                futures.append(
                    executor.submit(self._simulate_action, bot, target_id, action_type, endpoints)
                )
            
            for future in as_completed(futures):
                if not self.running:
                    break
                try:
                    result = future.result(timeout=30)
                    results.append(result)
                    with self.lock:
                        if result["success"]:
                            self.stats["success"] += 1
                        else:
                            self.stats["failed"] += 1
                        self.stats["total"] += 1
                    self._log(f"[{action_type.upper()}] Bot: {result['bot_username']} | "
                             f"Success: {result['success']} | Delay: {result['delay']:.2f}s")
                except Exception as e:
                    with self.lock:
                        self.stats["failed"] += 1
                        self.stats["total"] += 1
                    self._log(f"[{action_type.upper()}] Error: {str(e)}")
        
        self.running = False
        self._log(f"[{action_type.upper()}] Completed: {self.stats['success']} success, "
                 f"{self.stats['failed']} failed, {self.stats['total']} total")
        return results
    
    def stop(self):
        """Останавливает выполнение."""
        self.running = False

# ============================================================================
# ГРАФИЧЕСКИЙ ИНТЕРФЕЙС (GUI)
# ============================================================================
class VostroGUI:
    """Главный графический интерфейс приложения Vostro."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{CONFIG['title']} v{CONFIG['version']}")
        self.root.geometry(CONFIG["window_size"])
        self.root.configure(bg=CONFIG["theme_bg"])
        self.root.resizable(True, True)
        
        # Настройка стилей ttk
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=CONFIG["theme_bg"])
        self.style.configure("TLabel", background=CONFIG["theme_bg"], foreground=CONFIG["theme_fg"])
        self.style.configure("TButton", background=CONFIG["theme_button"], foreground="white",
                            borderwidth=0, focusthickness=0, padding=10)
        self.style.map("TButton", background=[("active", CONFIG["theme_button_hover"])])
        self.style.configure("TEntry", fieldbackground=CONFIG["theme_entry_bg"],
                            foreground=CONFIG["theme_entry_fg"], borderwidth=1)
        self.style.configure("TCombobox", fieldbackground=CONFIG["theme_entry_bg"],
                            foreground=CONFIG["theme_entry_fg"], arrowcolor=CONFIG["theme_fg"])
        
        self.network = NetworkEngine()
        self.executor = EngagementExecutor(self.network, self.log_message)
        
        self._build_ui()
    
    def _build_ui(self):
        # Заголовок
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(header_frame, text="VOSTRO", font=("Arial", 32, "bold"),
                               fg=CONFIG["theme_accent"], bg=CONFIG["theme_bg"])
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Engagement Service",
                                  font=("Arial", 12), fg=CONFIG["theme_fg"], bg=CONFIG["theme_bg"])
        subtitle_label.pack()
        
        # Основной контейнер с двумя колонками
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Левая панель - ввод
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Блок выбора действия
        action_frame = tk.LabelFrame(left_panel, text="Select Action", font=("Arial", 11, "bold"),
                                     fg=CONFIG["theme_accent"], bg=CONFIG["theme_bg"],
                                     bd=2, relief=tk.GROOVE, padx=10, pady=10)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.action_var = tk.StringVar(value="followers")
        actions = [
            ("Followers (to Profile)", "followers"),
            ("Likes (to Video)", "likes"),
            ("Comment Likes", "comment_likes"),
            ("Views", "views"),
            ("Shares", "shares"),
            ("Saves", "saves"),
        ]
        
        for text, value in actions:
            rb = tk.Radiobutton(action_frame, text=text, variable=self.action_var, value=value,
                               fg=CONFIG["theme_fg"], bg=CONFIG["theme_bg"],
                               selectcolor=CONFIG["theme_button"],
                               activebackground=CONFIG["theme_bg"],
                               activeforeground=CONFIG["theme_accent"],
                               font=("Arial", 10),
                               command=self._update_url_label)
            rb.pack(anchor=tk.W, pady=3)
        
        # Блок URL
        url_frame = tk.LabelFrame(left_panel, text="Target URL", font=("Arial", 11, "bold"),
                                  fg=CONFIG["theme_accent"], bg=CONFIG["theme_bg"],
                                  bd=2, relief=tk.GROOVE, padx=10, pady=10)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.url_label = tk.Label(url_frame, text="Profile URL:", fg=CONFIG["theme_fg"],
                                  bg=CONFIG["theme_bg"], font=("Arial", 10))
        self.url_label.pack(anchor=tk.W)
        
        self.url_entry = tk.Entry(url_frame, font=("Arial", 11), bg=CONFIG["theme_entry_bg"],
                                  fg=CONFIG["theme_entry_fg"], insertbackground="white",
                                  bd=0, relief=tk.FLAT)
        self.url_entry.pack(fill=tk.X, ipady=8, pady=(5, 0))
        self.url_entry.insert(0, "https://www.tiktok.com/@username")
        
        # Блок количества
        count_frame = tk.LabelFrame(left_panel, text="Amount", font=("Arial", 11, "bold"),
                                    fg=CONFIG["theme_accent"], bg=CONFIG["theme_bg"],
                                    bd=2, relief=tk.GROOVE, padx=10, pady=10
