from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import json
import re
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Headers per simulare un browser reale
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Configurazione globale della sessione
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0'
})

# Numero massimo di thread concorrenti
MAX_WORKERS = 10

def handle_security_redirect(response, url):
    max_redirects = 5  # Limite massimo di redirect da seguire
    redirects = 0
    
    while response.status_code == 202 and redirects < max_redirects:
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find('script')
        if script:
            # Estrai il cookie dal JavaScript
            cookie_match = re.search(r'document\.cookie="(SecurityAW-gl=[^;]+)', script.string)
            if cookie_match:
                cookie = cookie_match.group(1)
                # Imposta il cookie nella sessione
                cookie_name, cookie_value = cookie.split('=')
                session.cookies.set(cookie_name, cookie_value)
                # Estrai l'URL di redirect
                redirect_url = re.search(r'location\.href="([^"]+)"', script.string)
                if redirect_url:
                    # Assicurati che l'URL sia completo
                    next_url = redirect_url.group(1)
                    if not next_url.startswith('http'):
                        next_url = f"https://www.animeworld.so{next_url}"
                    
                    print(f"Seguendo redirect {redirects + 1} a: {next_url}")  # Debug
                    print(f"Cookie impostato: {cookie}")  # Debug
                    
                    # Aggiungi il cookie all'header della richiesta
                    headers = session.headers.copy()
                    headers['Cookie'] = f"{cookie_name}={cookie_value}"
                    
                    response = session.get(next_url, headers=headers, allow_redirects=True)
                    redirects += 1
                    continue
        break
    
    if redirects == max_redirects:
        print(f"Raggiunto limite massimo di {max_redirects} redirect")
    
    return response

def get_anime_info(anime_id):
    url = f"https://www.animeworld.so/api/tooltip/{anime_id}"
    try:
        print(f"Richiesta per anime {anime_id}")
        headers = {
            'Referer': 'https://www.animeworld.so/',
            'Origin': 'https://www.animeworld.so'
        }
        response = session.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"Risposta ricevuta per anime {anime_id}")
            return parse_anime_info(response.text)
        else:
            print(f"Errore {response.status_code} per anime {anime_id}")
            return None
    except Exception as e:
        print(f"Errore per anime {anime_id}: {str(e)}")
        return None

def parse_anime_info(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        info = {}
        
        # Estrazione dati più robusta
        for meta in soup.find_all('div', class_='meta'):
            label = meta.find('label')
            span = meta.find('span')
            if label and span:
                key = label.text.strip().replace(':', '')
                value = span.text.strip()
                info[key] = value
        
        desc = soup.find('p', class_='desc')
        if desc:
            info['descrizione'] = desc.text.strip()
            
        return info
    except Exception as e:
        print(f"Errore nel parsing: {str(e)}")
        return None

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/api/popolari')
def get_popolari():
    print("\n=== Inizio recupero anime popolari ===")
    url = "https://www.animeworld.so/filter?sort=6"
    try:
        response = session.get(url)
        response = handle_security_redirect(response, url)
        soup = BeautifulSoup(response.text, 'html.parser')
        anime_list = []
        
        film_list = soup.find('div', class_='film-list')
        if not film_list:
            print("Nessuna lista anime trovata")
            return jsonify([])
            
        items = film_list.find_all('div', class_='item')
        print(f"Trovati {len(items)} anime popolari")
        
        anime_tasks = []
        for item in items:
            inner = item.find('div', class_='inner')
            if inner:
                title_link = inner.find('a', class_='name')
                poster_link = inner.find('a', class_='poster')
                img = inner.find('img')
                
                if title_link and poster_link and img:
                    anime_id = re.search(r'api/tooltip/(\d+)', poster_link.get('data-tip', '')).group(1)
                    anime_tasks.append({
                        'id': anime_id,
                        'titolo': title_link.text,
                        'href': title_link['href'],
                        'poster': img['src']
                    })
        
        print(f"Inizio processamento {len(anime_tasks)} anime")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_anime = {executor.submit(get_anime_info, task['id']): task for task in anime_tasks}
            
            for future in concurrent.futures.as_completed(future_to_anime):
                task = future_to_anime[future]
                try:
                    info = future.result()
                    anime_list.append({
                        'titolo': task['titolo'],
                        'href': task['href'],
                        'poster': task['poster'],
                        'info': info
                    })
                except Exception as e:
                    print(f"Errore nel processare un anime: {str(e)[:100]}")
        
        print(f"Completato. Processati {len(anime_list)} anime")
        return jsonify(anime_list)
    except Exception as e:
        print(f"Errore generale in get_popolari: {str(e)[:100]}")
        return jsonify([])

@app.route('/api/ultime-uscite')
def get_ultime_uscite():
    url = "https://www.animeworld.so/newest"
    try:
        response = session.get(url)
        response = handle_security_redirect(response, url)
        soup = BeautifulSoup(response.text, 'html.parser')
        anime_list = []
        
        film_list = soup.find('div', class_='film-list')
        if not film_list:
            return jsonify([])
            
        items = film_list.find_all('div', class_='item')
        
        anime_tasks = []
        for item in items:
            inner = item.find('div', class_='inner')
            if inner:
                title_link = inner.find('a', class_='name')
                poster_link = inner.find('a', class_='poster')
                img = inner.find('img')
                
                if title_link and poster_link and img:
                    anime_id = re.search(r'api/tooltip/(\d+)', poster_link.get('data-tip', '')).group(1)
                    anime_tasks.append({
                        'id': anime_id,
                        'titolo': title_link.text,
                        'href': title_link['href'],
                        'poster': img['src']
                    })
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_anime = {
                executor.submit(get_anime_info, task['id']): task 
                for task in anime_tasks
            }
            
            for future in concurrent.futures.as_completed(future_to_anime):
                task = future_to_anime[future]
                try:
                    info = future.result()
                    anime_list.append({
                        'titolo': task['titolo'],
                        'href': task['href'],
                        'poster': task['poster'],
                        'info': info
                    })
                except Exception as e:
                    print(f"Errore nel processare anime {task['id']}: {e}")
        
        return jsonify(anime_list)
    except Exception as e:
        print(f"Errore generale: {e}")
        return jsonify([])

@app.route('/api/calendario')
def get_calendario():
    url = "https://www.livechart.me/schedule"
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        anime_list = []
        data_oggi = "Oggi"  # Valore predefinito
        
        today_section = soup.find('div', class_='lc-timetable-day lc-today')
        if today_section:
            heading = today_section.find('div', class_='lc-timetable-day__heading')
            if heading:
                data_oggi = heading.text.strip()
            
            for timeslot in today_section.find_all('div', class_='lc-timetable-timeslot__content'):
                time = timeslot.find('span', {'data-timeslot-target': 'time'})
                anime_block = timeslot.find('div', class_='lc-timetable-anime-block')
                
                if anime_block:
                    poster = anime_block.find('img', class_='lc-tt-poster')
                    title = anime_block.find('a', class_='lc-tt-anime-title')
                    episode = anime_block.find('a', class_='lc-tt-release-label')
                    
                    if title and poster and episode:
                        poster_url = poster.get('src')
                        
                        anime = {
                            "ora": time.text.strip() if time else "N/A",
                            "titolo": title.text.strip(),
                            "poster": poster_url,
                            "episodio": episode.text.strip()
                        }
                        anime_list.append(anime)
        
        return jsonify({
            "data": data_oggi,
            "anime": anime_list
        })
    except Exception as e:
        print(f"Errore nel calendario: {e}")
        return jsonify({"data": "Oggi", "anime": []})

@app.route('/api/ultimi-episodi')
def get_ultimi_episodi():
    url = "https://www.animeworld.so/updated"
    try:
        response = session.get(url)
        response = handle_security_redirect(response, url)
        soup = BeautifulSoup(response.text, 'html.parser')
        episodi_list = []
        
        items = soup.find_all('div', class_='item')
        
        anime_tasks = []
        for item in items:
            inner = item.find('div', class_='inner')
            if inner:
                title_link = inner.find('a', class_='name')
                poster_link = inner.find('a', class_='poster')
                img = inner.find('img')
                ep_div = inner.find('div', class_='ep')
                
                if title_link and poster_link and img and ep_div:
                    anime_id = re.search(r'api/tooltip/(\d+)', poster_link.get('data-tip', '')).group(1)
                    anime_tasks.append({
                        'id': anime_id,
                        'titolo': title_link.text,
                        'href': title_link['href'],
                        'poster': img['src'],
                        'episodio': ep_div.text.strip()
                    })
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_anime = {
                executor.submit(get_anime_info, task['id']): task 
                for task in anime_tasks
            }
            
            for future in concurrent.futures.as_completed(future_to_anime):
                task = future_to_anime[future]
                try:
                    info = future.result()
                    episodi_list.append({
                        'titolo': task['titolo'],
                        'href': task['href'],
                        'poster': task['poster'],
                        'episodio': task['episodio'],
                        'info': info
                    })
                except Exception as e:
                    print(f"Errore nel processare anime {task['id']}: {e}")
        
        return jsonify(episodi_list)
    except Exception as e:
        print(f"Errore generale: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
