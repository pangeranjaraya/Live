from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
YOUTUBE_API_KEY = 'AIzaSyCdYeZaAsw0jb7Zy5LjUKlICohSS-x75JI'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live')
def live_page():
    return render_template('live.html')

@app.route('/jadwal')
def jadwal_page():
    return render_template('jadwal.html')

@app.route('/info')
def info():
    return render_template('info.html')

# API Search City (Untuk pindah halaman)
@app.route('/api/search_city')
def search_city():
    city_name = request.args.get('q', '')
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}"
    headers = {'User-Agent': 'CaaXAdzanApp/1.0'}
    try:
        response = requests.get(url, headers=headers).json()
        if response:
            return jsonify({'status': 'success', 'lat': response[0]['lat'], 'lon': response[0]['lon'], 'name': response[0]['display_name']})
        return jsonify({'status': 'error'})
    except: return jsonify({'status': 'error'})

# API Jadwal Sholat
@app.route('/api/schedule_by_coord')
def get_schedule_coord():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon: return jsonify({})
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=2"
    try:
        return jsonify(requests.get(url).json()['data']['timings'])
    except: return jsonify({})

# API Cari Live YouTube (Untuk Halaman Search Result)
@app.route('/api/search_live_results')
def search_live_results():
    city = request.args.get('city', 'Makkah')
    query = f"Adzan Live {city} Mosque"
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&eventType=live&q={query}&key={YOUTUBE_API_KEY}'
    try:
        response = requests.get(url).json()
        results = []
        if 'items' in response:
            for item in response['items']:
                results.append({
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'thumbnail': item['snippet']['thumbnails']['high']['url']
                })
        return jsonify(results)
    except: return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
