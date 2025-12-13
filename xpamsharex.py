# -*- coding: utf-8 -*-
import os
import re
import json
import threading
import sys
import uuid
import hashlib
import requests
import random
import string
from datetime import datetime, timezone, timedelta
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess  # For direct TTS using espeak-ng

# ===============================
# CONFIG
# ===============================
APPROVAL_URL = "https://raw.githubusercontent.com/blep111/APPROVAL/main/approval.txt"
PREFIX = "404-dev-"

# ===============================
# DEVICE KEY (PERMANENT)
# ===============================
def generate_device_key():
    base = str(uuid.getnode())
    h = hashlib.md5(base.encode()).hexdigest()
    return (
        ''.join(random.choices(string.ascii_letters, k=4)) +
        h[:10] +
        ''.join(random.choices(string.digits, k=6))
    )

def get_device_key():
    if os.path.exists("device_key.txt"):
        with open("device_key.txt", "r") as f:
            return f.read().strip()

    key = generate_device_key()
    with open("device_key.txt", "w") as f:
        f.write(key)
    return key

# ===============================
# FETCH APPROVAL LIST (NO CACHE)
# ===============================
def fetch_approved_keys():
    try:
        headers = {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
        r = requests.get(APPROVAL_URL, headers=headers, timeout=10)
        if r.status_code == 200:
            return [line.strip() for line in r.text.splitlines() if line.strip()]
    except Exception as e:
        print("[NETWORK ERROR]", e)
    return []

# ===============================
# APPROVAL CHECK (RESET BASED)
# ===============================
def approval_check():
    device_key = get_device_key()
    approve_key = PREFIX + device_key

    approved_keys = fetch_approved_keys()

    if approve_key in approved_keys:
        print("\n[SUCCESS] ✔ DEVICE APPROVED\n")
        return

    print("\n[KEY NOT APPROVED YET!]")
    print("Send this key to admin:\n")
    print(approve_key)
    print("\nIf the admin approve your key")
    print("EXIT & RUN THE TOOL AGAIN AFTER A MINUTES.\n")
    sys.exit()

# ===============================
# START PROGRAM
# ===============================
if __name__ == "__main__":
    approval_check()

    # ===============================
    # TOOL STARTS AFTER APPROVAL
    # ===============================

    # PLACE YOUR TOOL CODE BELOW
    print("Tool is running...\n")

    # Session object
ses = requests.Session()

# Random user agents
ua_list = [
    "Mozilla/5.0 (Linux; Android 10; Wildfire E Lite Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.136 Mobile Safari/537.36[FBAN/EMA;FBLC/en_US;FBAV/298.0.0.10.115;]",
    "Mozilla/5.0 (Linux; Android 11; KINGKONG 5 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36[FBAN/EMA;FBLC/fr_FR;FBAV/320.0.0.12.108;]",
    "Mozilla/5.0 (Linux; Android 11; G91 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/106.0.5249.126 Mobile Safari/537.36[FBAN/EMA;FBLC/fr_FR;FBAV/325.0.1.4.108;]"
]
ua = random.choice(ua_list)

# Function to get current Philippine time
def get_ph_time():
    ph_tz = timezone(timedelta(hours=8))  # UTC+8
    return datetime.now(ph_tz)

# Function to get time-based greeting
def get_greeting(name):
    now = get_ph_time()
    hour = now.hour
    if 5 <= hour < 12:
        return f"Good morning {name}"
    elif 12 <= hour < 17:
        return f"Good afternoon {name}"
    elif 17 <= hour < 21:
        return f"Good evening {name}"
    else:
        return f"Good night {name}"

# Function to speak text using espeak-ng directly
def speak(text):
    try:
        subprocess.run(["espeak-ng", text], check=True)
    except subprocess.CalledProcessError:
        print(color("Voice not available. Ensure espeak-ng is installed.", '91'))
    except FileNotFoundError:
        print(color("espeak-ng not found. Install with 'pkg install espeak-ng'.", '91'))

# Function to get user input with optional voice
def voice_input(prompt, speak_input=True):
    user_input = input(color(prompt, '96'))
    if speak_input:
        speak(user_input)  # Speak what the user typed, unless disabled
    return user_input

# Loading animation function
def loading_animation(duration, message="Loading"):
    chars = "/—\\|"
    for i in range(duration * 10):  # 10 iterations per second
        sys.stdout.write(color(f'\r{message} {chars[i % len(chars)]}', '93'))
        sys.stdout.flush()
        sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')  # Clear line

# Function to speak and print greeting cleanly (only once)
def greet_user(name):
    greeting = get_greeting(name)
    welcome_msg = f"{greeting}, welcome to Facebook Xpam by dev 404! Enjoy using my tools!"
    print(color(f"\n{welcome_msg}", '96'))
    speak(welcome_msg)
    print(color(f"{greeting}! Let's start sharing and make some magic happen!", '92'))

# Colored print helper with bold
def color(text, color_code, bold=False):
    bold_code = "\033[1m" if bold else ""
    return f"{bold_code}\033[{color_code}m{text}\033[0m"

def banner():
    os.system("clear")
    print(color("""
\033[91m██╗  ██╗\033[92m██████╗ \033[93m █████╗ \033[94m███╗   ███╗\033[0m
\033[91m╚██╗██╔╝\033[92m██╔══██╗\033[93m██╔══██╗\033[94m████╗ ████║\033[0m
\033[91m ╚███╔╝ \033[92m██████╔╝\033[93m███████║\033[94m██╔████╔██║\033[0m
\033[91m ██╔██╗ \033[92m██╔═══╝ \033[93m██╔══██║\033[94m██║╚██╔╝██║\033[0m
\033[91m██╔╝ ██╗\033[92m██║     \033[93m██║  ██║\033[94m██║ ╚═╝ ██║\033[0m
\033[91m╚═╝  ╚═╝\033[92m╚═╝     \033[93m╚═╝  ╚═╝\033[94m╚═╝     ╚═╝\033[0m
""", '94'))  # Vibrant multi-colored logo with proper color assignments

    print(color("Owner : Net", '96', bold=True))  # Cyan bold
    print(color("Facebook: https://facebook.com/net", '96', bold=True))  # Cyan bold
    print(color("GitHub  : https://github.com/xxxtools404", '96', bold=True))
print (color("Status : Paid", '96', bold=True)) # Cyan bold
    print(color("-" * 50, '90'))  # Grey line

# Function to add cookies to database manually
def add_cookies_to_db():
    banner()
    print(color("Add Cookies to Database (Manual Input)", '93', bold=True))
    try:
        num_cookies = int(voice_input("How many cookies will you add? "))
    except ValueError:
        print(color("Oops, that must be a number. Try again!", '91'))
        return add_cookies_to_db()

    tokens = []
    cookies_list = []

    # Load existing if any
    try:
        with open("tokens.txt", "r") as f:
            existing_tokens = json.load(f)
        with open("cookies.txt", "r") as f:
            existing_cookies = json.load(f)
    except FileNotFoundError:
        existing_tokens = []
        existing_cookies = []

    for i in range(num_cookies):
        loading_animation(2, f"Getting ready for cookie {i+1}")
        cookie_input = voice_input(f"Cookie {i+1}: ", speak_input=False)
        cookies = {j.split("=")[0]: j.split("=")[1] for j in cookie_input.split("; ") if "=" in j}

        try:
            data = ses.get("https://business.facebook.com/business_locations", headers={
                "user-agent": ua,
                "referer": "https://www.facebook.com/",
                "host": "business.facebook.com",
                "origin": "https://business.facebook.com",
                "upgrade-insecure-requests": "1",
                "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "max-age=0",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "content-type": "text/html; charset=utf-8"
            }, cookies=cookies, timeout=10)

            find_token = re.search(r"(EAAG\w+)", data.text)
            if not find_token:
                print(color(f"\n❌ Token extraction failed for cookie {i+1}. Skipping.", '91'))
                continue

            token = find_token.group(1)
            tokens.append(token)
            cookies_list.append(cookies)
            print(color(f"\n✅ Token found for cookie {i+1}: {token}", '92'))

        except Exception as e:
            print(color(f"Error with cookie {i+1}: {e}", '91'))

    # Append to existing
    existing_tokens.extend(tokens)
    existing_cookies.extend(cookies_list)

    # Save back
    with open("tokens.txt", "w") as f:
        json.dump(existing_tokens, f)
    with open("cookies.txt", "w") as f:
        json.dump(existing_cookies, f)

    print(color(f"Added {len(tokens)} cookies to database. Total now: {len(existing_tokens)}", '92'))
    time.sleep(2)

# Function to manage suspended cookies
def manage_suspended_cookies():
    banner()
    print(color("Manage Suspended Cookies", '93', bold=True))
    try:
        with open("suspended_cookies.txt", "r") as f:
            suspended = json.load(f)
    except FileNotFoundError:
        suspended = {}
    
    num_suspended = len(suspended)
    print(color(f"Number of Suspended Cookies: {num_suspended}", '96', bold=True))
    if num_suspended == 0:
        print(color("No suspended cookies to manage.", '92'))
        input(color("Press Enter to return to main menu...", '96'))
        return main_menu()
    
    print(color("\nSuspended Cookies List:", '94', bold=True))
    for idx, (name, cookie) in enumerate(suspended.items(), 1):
        print(color(f"  {idx}. Name: {name} - Cookie: {str(cookie)[:50]}...", '91', bold=True))  # Red for suspended
    
    print(color("\nOptions:", '96', bold=True))
    print(color("1. Remove a suspended cookie by number", '92'))
    print(color("2. Remove all suspended cookies", '92'))
    print(color("3. Back to Main Menu", '91'))
    
    choice = voice_input("Choose an option (1/2/3): ").strip()
    if choice == '1':
        try:
            num = int(voice_input("Enter the number of the cookie to remove: "))
            if 1 <= num <= num_suspended:
                name_to_remove = list(suspended.keys())[num-1]
                del suspended[name_to_remove]
                with open("suspended_cookies.txt", "w") as f:
                    json.dump(suspended, f)
                print(color(f"Removed suspended cookie: {name_to_remove}", '92'))
            else:
                print(color("Invalid number.", '91'))
        except ValueError:
            print(color("Invalid input.", '91'))
        manage_suspended_cookies()
    elif choice == '2':
        suspended.clear()
        with open("suspended_cookies.txt", "w") as f:
            json.dump(suspended, f)
        print(color("All suspended cookies removed.", '92'))
        manage_suspended_cookies()
    elif choice == '3':
        main_menu()
    else:
        print(color("Invalid choice.", '91'))
        manage_suspended_cookies()

# Main menu
def main_menu():
    banner()
    print(color("Main Menu", '96', bold=True))
    print(" " * 5 + color("1. Add Cookies to Database (Manual Input)", '92', bold=True))
    print(" " * 5 + color("2. Start Sharing (Load from Database or Manual)", '92', bold=True))
    print(" " * 5 + color("3. Manage Suspended Cookies", '93', bold=True))
    print(" " * 5 + color("4. Exit", '91', bold=True))
    choice = voice_input("Choose an option (1/2/3/4): ").strip()
    if choice == '1':
        add_cookies_to_db()
        main_menu()
    elif choice == '2':
        login()
    elif choice == '3':
        manage_suspended_cookies()
    elif choice == '4':
        print(color("Goodbye!", '92'))
        sys.exit()
    else:
        print(color("Invalid choice. Try again.", '91'))
        main_menu()

def login():
    banner()
    name = voice_input("Enter your name: ")
    greet_user(name)
    choice = voice_input("Do you want to load cookies from database or enter new ones? (load/manual): ").strip().lower()
    tokens = []
    cookies_list = []
    if choice == 'load':
        try:
            with open("tokens.txt", "r") as f:
                saved_tokens = json.load(f)
            with open("cookies.txt", "r") as f:
                saved_cookies = json.load(f)
            # Exclude suspended cookies
            try:
                with open("suspended_cookies.txt", "r") as f:
                    suspended = json.load(f)
                suspended_names = set(suspended.keys())
                filtered_tokens = []
                filtered_cookies = []
                for i, cookie in enumerate(saved_cookies):
                    name = cookie.get('c_user', f'Cookie_{i+1}')
                    if name not in suspended_names:
                        filtered_tokens.append(saved_tokens[i])
                        filtered_cookies.append(cookie)
                saved_tokens = filtered_tokens
                saved_cookies = filtered_cookies
            except FileNotFoundError:
                pass
            num_saved = len(saved_cookies)
            print(color(f"There are {num_saved} cookies live in the database.", '92'))
            if num_saved == 0:
                print(color("No saved cookies. Switching to manual input.", '91'))
                choice = 'manual'
            else:
                try:
                    num_use = int(voice_input(f"How many cookies from database do you want to use? (max: {num_saved}): "))
                    if num_use > num_saved:
                        num_use = num_saved
                    elif num_use < 1:
                        num_use = 1
                    tokens = saved_tokens[:num_use]
                    cookies_list = saved_cookies[:num_use]
                    print(color(f"Loaded {num_use} cookies from database.", '92'))
                except ValueError:
                    print(color("Invalid number. Using all saved cookies.", '91'))
                    tokens = saved_tokens
                    cookies_list = saved_cookies
        except FileNotFoundError:
            print(color("No database found. Switching to manual input.", '91'))
            choice = 'manual'
    if choice == 'manual' or choice != 'load':
        print(color("Enter your Facebook cookies here (multiple allowed)", '93'))
        try:
            num_cookies = int(voice_input("How many cookies will you enter? "))
        except ValueError:
            print(color("Oops, that must be a number, not nonsense. Let's try again!", '91'))
            return login()

        for i in range(num_cookies):
            loading_animation(2, f"Getting ready for cookie {i+1}")
            cookie_input = voice_input(f"Cookie {i+1}: ", speak_input=False)
            cookies = {j.split("=")[0]: j.split("=")[1] for j in cookie_input.split("; ") if "=" in j}

            try:
                data = ses.get("https://business.facebook.com/business_locations", headers={
                    "user-agent": ua,
                    "referer": "https://www.facebook.com/",
                    "host": "business.facebook.com",
                    "origin": "https://business.facebook.com",
                    "upgrade-insecure-requests": "1",
                    "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                    "cache-control": "max-age=0",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "content-type": "text/html; charset=utf-8"
                }, cookies=cookies, timeout=10)

                find_token = re.search(r"(EAAG\w+)", data.text)
                if not find_token:
                    print(color(f"\n❌ Token extraction failed for cookie {i+1}. Please check your cookie.", '91'))
                    continue

                token = find_token.group(1)
                tokens.append(token)
                cookies_list.append(cookies)
                print(color(f"\n✅ Token found for cookie {i+1}: {token}", '92'))

            except Exception as e:
                print(color(f"Error with cookie {i+1}: {e}", '91'))

        if tokens:
            with open("tokens.txt", "w") as f:
                json.dump(tokens, f)
            with open("cookies.txt", "w") as f:
                json.dump(cookies_list, f)

    if not tokens:
        print(color("No valid cookies found. Let's try again!", '91'))
        return login()

    print(color("Great! Setup complete. Start sharing now!...", '92'))
    time.sleep(3)
    bot()

def share_post(token, cookie, link, n, start_time, suspended_cookies):
    try:
        post = ses.post(
            f"https://graph.facebook.com/v13.0/me/feed?link={link}&published=0&access_token={token}",
            headers={
                "authority": "graph.facebook.com",
                "cache-control": "max-age=0",
                "sec-ch-ua-mobile": "?0",
                "user-agent": ua
            }, cookies=cookie, timeout=10
        ).text

        data = json.loads(post)
        if "id" in data:
            elapsed = str(datetime.now() - start_time).split('.')[0]
            print(color(f"*--> {n}. Sharing in progress, just wait until it's finished! ({elapsed})", '92'))
            return True
        else:
            error_msg = data.get('error', {}).get('message', 'Unknown error')
            if 'suspended' in error_msg.lower() or 'blocked' in error_msg.lower() or 'rate limit' in error_msg.lower():
                name = cookie.get('c_user', f'Cookie_{n}')
                print(color(f"*--> {n}. {name} suspended. Removing from list.", '91', bold=True))  # Red bold
                suspended_cookies[name] = cookie
                return False
            else:
                print(color(f"*--> {n}. Failed: {error_msg}", '91'))
                return False
    except json.JSONDecodeError:
        print(color(f"*--> {n}. Invalid response from server.", '91'))
        return False
    except requests.exceptions.Timeout:
        print(color(f"*--> {n}. Request timed out.", '91'))
        return False
    except requests.exceptions.ConnectionError:
        print(color(f"*--> {n}. Connection error.", '91'))
        return False
    except Exception as e:
        print(color(f"*--> {n}. Unexpected error: {e}", '91'))
        return False

def bot():
    os.system("clear")
    banner()
    try:
        with open("tokens.txt", "r") as f:
            tokens = json.load(f)
        with open("cookies.txt", "r") as f:
            cookies_list = json.load(f)
    except:
        if os.path.exists("tokens.txt"): os.remove("tokens.txt")
        if os.path.exists("cookies.txt"): os.remove("cookies.txt")
        print(color("Your cookies have expired. Let's log in again!", '91'))
        return login()

    while True:
        link = voice_input("Enter post link: ", speak_input=False)  # Disabled speaking for long link
        try:
            limitasyon = int(voice_input("Enter Amount: "))
        except ValueError:
            print(color("That must be a number. Try again!", '91'))
            continue

        print(color("Starting sharing process...", '93'))
        start_time = datetime.now()

        chunk_size = 40
        cooldown = 10
        suspended_cookies = {}

        with ThreadPoolExecutor(max_workers=50) as executor:
            n = 1
            while n <= limitasyon:
                futures = []
                for _ in range(min(chunk_size, limitasyon - n + 1)):
                    available = [
                        (tokens[i], cookies_list[i])
                        for i in range(len(tokens))
                        if cookies_list[i].get('c_user', f'Cookie_{i+1}') not in suspended_cookies
                    ]

                    if not available:
                        print(color("All cookies suspended. Stopping shares.", '91'))
                        break

                    token, cookie = random.choice(available)
                    futures.append(
                        executor.submit(
                            share_post,
                            token,
                            cookie,
                            link,
                            n,
                            start_time,
                            suspended_cookies
                        )
                    )
                    n += 1

                for future in as_completed(futures):
                    pass

                # Remove suspended cookies from active lists
                if suspended_cookies:
                    new_tokens = []
                    new_cookies = []

                    for i, cookie in enumerate(cookies_list):
                        name = cookie.get('c_user', f'Cookie_{i+1}')
                        if name not in suspended_cookies:
                            new_tokens.append(tokens[i])
                            new_cookies.append(cookie)

                    tokens = new_tokens
                    cookies_list = new_cookies

                    # Save suspended cookies
                    try:
                        with open("suspended_cookies.txt", "r") as f:
                            saved_suspended = json.load(f)
                    except FileNotFoundError:
                        saved_suspended = {}

                    saved_suspended.update(suspended_cookies)
                    with open("suspended_cookies.txt", "w") as f:
                        json.dump(saved_suspended, f)

                    with open("tokens.txt", "w") as f:
                        json.dump(tokens, f)
                    with open("cookies.txt", "w") as f:
                        json.dump(cookies_list, f)

                    suspended_cookies.clear()

                if n <= limitasyon and tokens:
                    loading_animation(
                        cooldown,
                        f"Cooldown {cooldown}s after {n-1} shares"
                    )

        print(color("All shares completed successfully!", '92', bold=True))
        choice = voice_input("Do you want to share another post? (y/n): ").strip().lower()
        if choice == 'y':
            continue
        else:
            print(color("Returning to main menu...", '93'))
            time.sleep(2)
            main_menu()
            break


# Program entry point
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(color("\nProgram interrupted by user. Goodbye!", '91'))
        sys.exit()