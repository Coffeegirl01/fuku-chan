    @classmethod
    def from_weather_data(cls, name: str, country: str, surface: str, weather: Dict[str, Any]) -> "Track":
        """Create a Track from weather or Forecast data later."""
        return cls(
            name=name,
            country=country,
            altitude=int(weather.get("altitude", 0)),
            surface=surface,
            specialty_distance=str(weather.get("specialty_distance", "middle")),
            track_layout=str(weather.get("track_layout", "oval")),
            temperature_c=float(weather.get("temperature_c", 20.0)),
            humidity_pct=float(weather.get("humidity_pct", 50.0)),
            wind_speed_kph=float(weather.get("wind_speed_kph", 0.0)),
            precipitation_mm=float(weather.get("precipitation_mm", 0.0)),
            soil_moisture=float(weather.get("soil_moisture", 0.0)),
            track_rating=float(weather.get("track_rating", 0.5)),
            metadata=dict(weather.get("metadata", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "country": self.country,
            "altitude": self.altitude,
            "surface": self.surface,
            "specialty_distance": self.specialty_distance,
            "track_layout": self.track_layout,
            "temperature_c": self.temperature_c,
            "humidity_pct": self.humidity_pct,
            "wind_speed_kph": self.wind_speed_kph,
            "precipitation_mm": self.precipitation_mm,
            "soil_moisture": self.soil_moisture,
            "track_rating": self.track_rating,
        }

    def __repr__(self) -> str:
        return f"Track(name={self.name!r}, country={self.country!r}, surface={self.surface!r})"


__all__ = ["Track"]
