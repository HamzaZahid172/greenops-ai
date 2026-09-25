import { useEffect, useState } from "react";

import {
  getCarbonForecast,
  getCurrentCarbon,
} from "../services/carbon";

import type {
  CarbonCurrentResponse,
  CarbonForecastResponse,
} from "../types/carbon";


async function fetchCarbonData() {
  return Promise.all([
    getCurrentCarbon(),
    getCarbonForecast(),
  ]);
}


function CarbonIntelligence() {
  const [current, setCurrent] =
    useState<CarbonCurrentResponse | null>(
      null,
    );

  const [forecast, setForecast] =
    useState<CarbonForecastResponse | null>(
      null,
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    let cancelled = false;


    async function loadInitialData() {
      try {
        const [
          currentResult,
          forecastResult,
        ] = await fetchCarbonData();


        if (cancelled) {
          return;
        }


        setCurrent(currentResult);
        setForecast(forecastResult);

      } catch {
        if (!cancelled) {
          setError(
            "Carbon data is currently unavailable.",
          );
        }

      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }


    void loadInitialData();


    return () => {
      cancelled = true;
    };
  }, []);


  async function handleRefresh() {
    setLoading(true);
    setError(null);

    try {
      const [
        currentResult,
        forecastResult,
      ] = await fetchCarbonData();

      setCurrent(currentResult);
      setForecast(forecastResult);

    } catch {
      setError(
        "Carbon data is currently unavailable.",
      );

    } finally {
      setLoading(false);
    }
  }


  if (loading) {
    return (
      <main>
        <h1>Carbon Intelligence</h1>

        <p>Loading carbon data...</p>
      </main>
    );
  }


  if (error) {
    return (
      <main>
        <h1>Carbon Intelligence</h1>

        <p>{error}</p>

        <button onClick={handleRefresh}>
          Retry
        </button>
      </main>
    );
  }


  return (
    <main>
      <h1>Carbon Intelligence</h1>

      <p>
        Real-time electricity carbon
        intensity information.
      </p>


      {current && (
        <section className="carbon-current">

          <h2>
            Current Carbon Intensity
          </h2>

          <p>
            Region:{" "}
            <strong>
              {current.region}
            </strong>
          </p>

          <div className="carbon-value">
            {
              current.intensity.actual ??
              current.intensity.forecast
            }

            <span>
              {" "}
              {current.unit}
            </span>
          </div>

          <p>
            Level:{" "}
            <strong>
              {current.intensity.index}
            </strong>
          </p>

          <p>
            Provider:{" "}
            {current.provider}
          </p>

        </section>
      )}


      {forecast && (
        <section className="carbon-forecast">

          <h2>
            Carbon Forecast
          </h2>

          <div className="forecast-grid">

            {forecast.points
              .slice(0, 8)
              .map((point) => (

                <div
                  className="forecast-card"
                  key={point.from_time}
                >

                  <strong>
                    {new Date(
                      point.from_time,
                    ).toLocaleTimeString(
                      [],
                      {
                        hour: "2-digit",
                        minute: "2-digit",
                      },
                    )}
                  </strong>

                  <p>
                    {point.forecast}{" "}
                    {forecast.unit}
                  </p>

                  <small>
                    {point.index}
                  </small>

                </div>
              ))}

          </div>

        </section>
      )}


      <button onClick={handleRefresh}>
        Refresh Carbon Data
      </button>

    </main>
  );
}


export default CarbonIntelligence;