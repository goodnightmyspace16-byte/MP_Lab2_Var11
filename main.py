import requests
import json
import xml.etree.ElementTree as ET

API_KEY = "7e2d1b308df8df24749494f88cb4615d"

CITIES = ["Moscow", "London", "Dubai"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_data():
    weather_results = []
    print("Запрос данных из API")
    for city in CITIES:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            weather_results.append({
                "city": city,
                "temp": data['main']['temp'],
                "wind_speed": data['wind']['speed'],
                "description": data['weather'][0]['description']
            })
            print(f"Данные по городу {city} получены.")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {city}: {e}")
    return weather_results


def analyze_weather(data):

    warmest = max(data, key=lambda x: x['temp'])
    coldest = min(data, key=lambda x: x['temp'])
    windiest = max(data, key=lambda x: x['wind_speed'])

    return {
        "all_data": data,
        "summary": {
            "warmest_city": warmest['city'],
            "coldest_city": coldest['city'],
            "windiest_city": windiest['city']
        }
    }


def save_json(report):

    with open("weather_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
    print("Отчет JSON сохранен.")


def save_xml(report):

    root = ET.Element("WeatherReport")

    summary = ET.SubElement(root, "Summary")
    for key, val in report['summary'].items():
        ET.SubElement(summary, key).text = str(val)

    cities_node = ET.SubElement(root, "Cities")
    for city_data in report['all_data']:
        city_node = ET.SubElement(cities_node, "City")
        for k, v in city_data.items():
            ET.SubElement(city_node, k).text = str(v)

    tree = ET.ElementTree(root)
    tree.write("weather_report.xml", encoding="utf-8", xml_declaration=True)
    print("Отчет XML сохранен.")


if __name__ == "__main__":
    weather_list = get_weather_data()
    if weather_list:
        final_report = analyze_weather(weather_list)
        save_json(final_report)
        save_xml(final_report)
