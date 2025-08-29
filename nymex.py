#!/usr/bin/env python3

import argparse
import asyncio
import httpx
import sys
from termcolor import colored

# --- Banner for the Tool ---
BANNER = """
;;;;;;;;;;;;;;;;;&&&&&&&&&&&&&&&&&&&&&&&&&&&&;;;;;;;;;
;;;;;;;;;;;;;&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&;;;;;;;;;
;;;;;;;;;;;&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&;;;;;;;;;
;;;;;;;;;;;&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&;;;;;;;;;
;;;;;;;;;;&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&;;;;;;;  ███╗   ██╗██╗   ██╗███╗   ███╗███████╗ ██╗  ██╗
;;;;;;;;;;&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&;;;;;;;  ████╗  ██║╚██╗ ██╔╝████╗ ████║██╔════╝ ╚██╗██╔╝
;;;;;;;;&&&&&&&&&&&&.:.:.:.:&&&&&&&&&&&&&&&&&&&&;;;;;;  ██╔██╗ ██║ ╚████╔╝ ██╔████╔██║█████╗    ╚███╔╝ 
;;;;;;&&&&&&&&&&..:.:.:.:.:.:.::&&&&&&&&&&&&&&&&&&&;;;  ██║╚██╗██║  ╚██╔╝  ██║╚██╔╝██║██╔══╝    ██╔██╗ 
;;;;&&&&&&&&&&:.::.&&&&&&&&&&.:..:&&&&&&&&&&&&&&&&&&&;  ██║ ╚████║   ██║   ██║ ╚═╝ ██║███████╗ ██╔╝ ██╗
;&&&&&&&&&&&X.::.&&&&&&&&&&&&&&&:.:.&&&&&&&&&&Xx;;;;;;  ╚═╝  ╚═══╝   ╚═╝   ╚═╝     ╚═╝╚══════╝ ╚═╝  ╚═╝
;;;;;;;;;;;.::.xxxxxxx..Xxxxxxxxx.:.:xxxxxxxxx;;;;;;;; ==================================================
;;;;;;;;;;;:.:xx+x::xxxxxx;::xxxxx::.:xxxxxxx;;;;;;;;;              - Created by Galaxie -
;;;;;;;;;;:.:xxxx+xxxxx:.xxx++:.:xx::.xxxxxxxxx;;;;;;; ==================================================
;;;;;;;;;;:.:xxxxxx::xxxxx;::xxxxxx.::xxxxxxxxx;;;;;;;
;;;;;;;;;;:.:xx:.$xxxxx:.xxxxxx:.xx:.:xxxxxxxxx;;;;;;;
;;;;;;;;;;:.:xxxxxx.:+xxxx+;:.xxxxx::.+xxxxxxx;;;;;;;;
;;;;;;;;;;;:.:xx:xxxxxxx::xxxxxxxx.:.xxxxxxxx+;;;;;;;;
;;;;;;;;;;;;:.:xxxxX:.xxx+X::xxx+::.:xxxxxxx+;;;;;;;;;
;;;;;;;;;;;;;:.:.x++xxxxxxxxxx+::.:xxxxxxxxx;;;;;;;;;;
;;;;;;;;;;;;;;:.:.::XxxxxxxX.:.:.:+xxxxxxxx;;;;;;;;;;;
;;;;;;;;;;;;;;;;x:.::::.:.:.::.xxxxxxxxxxx;;;;;;;;;;;; 
;;;;;;;;;;$&&&&&&&&+x+;.:.xxxxxxxxxxxxxx&&&&&&;;;;;;;;
;;;;;;;;;&&&&&&&&&&&x.::.::.xxxxxxxxxxx&&&&&&&&&;;;;;;
;;;;;;;;;&&&&&&&&&&xxxxxxxxxxxx&&&&&&&&&&&&&&&&x;;;;;;

 
[+] Open-Source Intelligence Email Checker [+]
"""

# --- Website Modules ---
# Each function checks a single website.
# They are designed to be asynchronous to run checks concurrently.
# To add a new site, create a new async function following this template.

async def check_instagram(email, client):
    """
    Checks for an account on Instagram.
    It sends a POST request to the account recovery page.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'X-CSRFToken': 'missing',
        'X-Instagram-AJAX': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://www.instagram.com',
        'Referer': 'https://www.instagram.com/accounts/password/reset/',
    }
    data = {'email_or_username': email}
    try:
        response = await client.post('https://www.instagram.com/accounts/account_recovery_send_ajax/', headers=headers, data=data)
        if response.status_code == 200 and 'We sent an email to' in response.text:
            return True
    except httpx.RequestError as e:
        # This handles network-related errors
        print(colored(f"[!] Error checking Instagram: {e}", "red"))
    return False

async def check_spotify(email, client):
    """
    Checks for an account on Spotify.
    It queries an internal API used for password resets.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }
    params = {'email': email}
    try:
        response = await client.get('https://spclient.wg.spotify.com/password-reset/v1/send', headers=headers, params=params)
        # Spotify's API returns a specific JSON response if the email exists
        if response.status_code == 200 and "email_sent" in response.json():
            return True
    except httpx.RequestError as e:
        print(colored(f"[!] Error checking Spotify: {e}", "red"))
    return False

async def check_twitter(email, client):
    """
    Checks for an account on Twitter/X.
    This uses an internal API endpoint involved in the login flow.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    }
    params = {'email': email, 'flow_name': 'login'}
    try:
        response = await client.get('https://api.twitter.com/i/users/email_available.json', headers=headers, params=params)
        # The 'taken' field in the JSON response indicates if the email is registered
        if response.status_code == 200 and response.json().get('taken'):
            return True
    except httpx.RequestError as e:
        print(colored(f"[!] Error checking Twitter/X: {e}", "red"))
    return False


# --- Main Logic ---

async def main():
    """
    Main function to parse arguments and run the checks.
    """
    print(colored(BANNER, "cyan"))

    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(description="OSINT tool to check for accounts associated with an email address.")
    parser.add_argument("email", help="The email address to check.")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    email_to_check = args.email

    print(colored(f"[*] Starting scan for: {email_to_check}\n", "yellow"))

    # List of websites to check.
    # To add a new site, add its check function to this list.
    sites_to_check = [
        check_instagram,
        check_spotify,
        check_twitter,
    ]

    # Using httpx.AsyncClient for making asynchronous HTTP requests
    async with httpx.AsyncClient() as client:
        # Create a list of tasks to run concurrently
        tasks = [site(email_to_check, client) for site in sites_to_check]
        
        # asyncio.gather runs all tasks and waits for them to complete
        results = await asyncio.gather(*tasks)

    print(colored("--- Results ---", "magenta"))
    found_count = 0
    for site_func, result in zip(sites_to_check, results):
        site_name = site_func.__name__.replace('check_', '').capitalize()
        if result:
            print(colored(f"[+] {site_name}: Account Found!", "green"))
            found_count += 1
        else:
            print(colored(f"[-] {site_name}: Not Found", "red"))
    
    print(colored(f"\n[*] Scan complete. Found accounts on {found_count} of {len(sites_to_check)} sites.", "yellow"))


if __name__ == "__main__":
    # Ensure necessary libraries are installed
    try:
        import httpx
        from termcolor import colored
    except ImportError:
        print("Error: Required libraries not found.")
        print("Please install them using: pip install httpx termcolor")
        sys.exit(1)
        
    # Run the main asynchronous function
    asyncio.run(main())
