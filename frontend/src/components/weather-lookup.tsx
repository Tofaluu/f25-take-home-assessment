"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";

function WeatherLookup() {
  const [id, setId] = useState("");
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");

  const handleLookup = async () => {
    setError("");
    setData(null);
    if (!id.trim()) {
      setError("Please enter an ID.");
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/weather/${id}`);
      if (!res.ok) {
        throw new Error("Weather data not found for this ID.");
      }
      const json = await res.json();
      setData(json);
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Weather Data Lookup</CardTitle>
        <CardDescription>
          Enter an ID to view stored weather info.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="Enter Weather ID"
            value={id}
            onChange={(e) => setId(e.target.value)}
          />
          <Button onClick={handleLookup}>Lookup</Button>
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        {data && (
          <div className="space-y-1 text-sm mt-2">
            <p>
              <strong>Date:</strong> {data.date}
            </p>
            <p>
              <strong>Location:</strong> {data.location}
            </p>
            <p>
              <strong>Notes:</strong> {data.notes || "—"}
            </p>
            <hr />
            <p>
              <strong>Temperature:</strong> {data.weather.temperature}°C
            </p>
            <p>
              <strong>Description:</strong>{" "}
              {data.weather.weather_descriptions?.[0]}
            </p>
            <p>
              <strong>Humidity:</strong> {data.weather.humidity}%
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default WeatherLookup;
