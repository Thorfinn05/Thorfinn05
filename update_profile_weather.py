#!/usr/bin/env python3
"""
Weather Auto-Update Script for GitHub Profile README
Updates the weather section in your profile README.md
"""

import json
import os
import re
from datetime import datetime
import urllib.request
import urllib.error

def get_weather():
    """Fetch weather data from Open-Meteo API (no auth required)"""
    try:
        # Default location: Kolkata, India (near your location)
        # Coordinates: 22.5726° N, 88.3639° E
        # Change these coordinates for your exact location
        latitude = 22.5726
        longitude = 88.3639
        location_name = "Kolkata, West Bengal, India"
        
        # Open-Meteo API - free, no authentication required
        url = (f"https://api.open-meteo.com/v1/forecast?"
               f"latitude={latitude}&longitude={longitude}"
               f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
               f"precipitation,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m"
               f"&timezone=auto")
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            data['location_name'] = location_name
            return data
    except urllib.error.URLError as e:
        print(f"Error fetching weather: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def format_weather_compact(data):
    """Format weather data in a compact format for profile README"""
    if not data:
        return "Weather data unavailable"
    
    try:
        current = data['current']
        location = data.get('location_name', 'Unknown Location')
        
        # Weather code descriptions with emojis
        weather_emojis = {
            0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
            45: "🌫️", 48: "🌫️",
            51: "🌦️", 53: "🌦️", 55: "🌧️",
            61: "🌧️", 63: "🌧️", 65: "⛈️",
            71: "🌨️", 73: "🌨️", 75: "❄️",
            77: "🌨️",
            80: "🌦️", 81: "⛈️", 82: "⛈️",
            85: "🌨️", 86: "❄️",
            95: "⛈️", 96: "⛈️", 99: "⛈️"
        }
        
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Foggy",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            77: "Snow grains",
            80: "Rain showers", 81: "Rain showers", 82: "Heavy rain showers",
            85: "Snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm"
        }
        
        weather_code = current.get('weather_code', 0)
        weather_emoji = weather_emojis.get(weather_code, "🌤️")
        weather_desc = weather_codes.get(weather_code, "Unknown")
        
        temp = current.get('temperature_2m', 'N/A')
        feels_like = current.get('apparent_temperature', 'N/A')
        humidity = current.get('relative_humidity_2m', 'N/A')
        wind = current.get('wind_speed_10m', 'N/A')
        
        # Compact format for profile
        weather_info = f"""### {weather_emoji} Current Weather in {location}

**{temp}°C** (feels like {feels_like}°C) • {weather_desc} • 💧 {humidity}% • 💨 {wind} km/h

*Updated: {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}*"""
        
        return weather_info
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        return "Weather data format error"

def update_profile_readme(weather_info):
    """Update the profile README.md with weather information"""
    
    readme_path = 'README.md'
    
    # Read existing README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("README.md not found!")
        return False
    
    # Define the markers for the weather section
    start_marker = "<!-- WEATHER:START -->"
    end_marker = "<!-- WEATHER:END -->"
    
    # Check if markers exist
    if start_marker in content and end_marker in content:
        # Replace content between markers
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        replacement = f"{start_marker}\n{weather_info}\n{end_marker}"
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        print("Weather markers not found in README.md")
        print("Please add the following markers to your README.md where you want the weather to appear:")
        print("\n<!-- WEATHER:START -->")
        print("<!-- WEATHER:END -->\n")
        return False
    
    # Write updated content
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("README.md updated successfully!")
    return True

def main():
    """Main function"""
    print("Fetching weather data...")
    weather_data = get_weather()
    
    print("Formatting weather information...")
    weather_info = format_weather_compact(weather_data)
    
    print("Updating profile README.md...")
    success = update_profile_readme(weather_info)
    
    if success:
        print("Done!")
    else:
        print("Failed to update README.md")

if __name__ == "__main__":
    main()
