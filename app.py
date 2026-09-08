from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = 'AIzaSyCdYeZaAsw0jb7Zy5LjUKlICohSS-x75JI'

@app.route('/')
def home():
    return render_template('index.html')

# 1. API untuk Mencari Koordinat Kota (Geocoding)
@app.route('/api/search_city')
def search_city():
    city_name = request.args.get('q', '')
    # Menggunakan OpenStreetMap Nominatim (Gratis, tanpa API Key)
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}"
    headers = {'User-Agent': 'CaaXAdzanApp/1.0'} # Wajib ada header user-agent
    
    try:
        response = requests.get(url, headers=headers).json()
        if response:
            lat = response[0]['lat']
            lon = response[0]['lon']
            display_name = response[0]['display_name']
            return jsonify({'status': 'success', 'lat': lat, 'lon': lon, 'name': display_name})
        else:
            return jsonify({'status': 'error', 'message': 'Kota tidak ditemukan'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# 2. API Jadwal Sholat Berdasarkan Koordinat
@app.route('/api/schedule_by_coord')
def get_schedule_coord():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon: return jsonify({})
    
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2" # Method 2 = ISNA (Standar Internasional)
    try:
        data = requests.get(url).json()['data']['timings']
        return jsonify(data)
    except:
        return jsonify({})

# 3. API Cari Live Stream YouTube Berdasarkan Nama Kota
@app.route('/api/search_live')
def search_live():
    city = request.args.get('city', 'Makkah')
    query = f"Adzan Live {city} Mosque" # Kata kunci pencarian otomatis
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=live&q={query}&key={YOUTUBE_API_KEY}'
    
    try:
        response = requests.get(url).json()
        if 'items' in response and len(response['items']) > 0:
            video_id = response['items'][0]['id']['videoId']
            title = response['items'][0]['snippet']['title']
            return jsonify({'status': 'success', 'video_id': video_id, 'title': title})
        else:
            # Fallback jika tidak ada live, cari video adzan terbaru
            return jsonify({'status': 'error', 'message': 'Tidak ada live stream aktif saat ini'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
