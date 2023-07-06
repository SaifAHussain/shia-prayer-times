package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"time"

	"github.com/go-resty/resty/v2"
)

// Enable CORS middleware
func enableCORS(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}

		next.ServeHTTP(w, r)
	})
}

type PrayerTime struct {
	Location string `json:"Location"`
	Date     string `json:"Date"`
	Month    string `json:"Month"`
	Year     string `json:"Year"`
	Imsaak   string `json:"Imsaak"`
	Dawn     string `json:"Dawn"`
	Sunrise  string `json:"Sunrise"`
	Noon     string `json:"Noon"`
	Sunset   string `json:"Sunset"`
	Maghrib  string `json:"Maghrib"`
	Midnight string `json:"Midnight"`
}

// Handler function for getting prayer times
func prayerTimesHandler(w http.ResponseWriter, r *http.Request) {
	// Load the JSON file containing prayer times
	file, err := ioutil.ReadFile("prayer_times.json")
	if err != nil {
		http.Error(w, "Failed to read prayer times data", http.StatusInternalServerError)
		return
	}

	// Unmarshal the JSON data into a slice of PrayerTime objects
	var prayerTimes []PrayerTime
	err = json.Unmarshal(file, &prayerTimes)
	if err != nil {
		http.Error(w, "Failed to parse prayer times data", http.StatusInternalServerError)
		return
	}

	// Determine the user's location based on their IP address
	client := resty.New()
	resp, err := client.R().
		SetQueryParam("fields", "city").
		Get("https://ipapi.co/json/")
	if err != nil {
		http.Error(w, "Failed to determine user location", http.StatusInternalServerError)
		return
	}

	type IPResponse struct {
		City string `json:"city"`
	}

	var ipResp IPResponse
	err = json.Unmarshal(resp.Body(), &ipResp)
	if err != nil {
		http.Error(w, "Failed to parse user location data", http.StatusInternalServerError)
		return
	}

	userLocation := ipResp.City

	// Find the matching prayer time for the user's location and today's date
	var matchingPrayerTime PrayerTime
	today := time.Now()
	currentDate := today.Format("2-1-2006") // Format: Day-Month-Year

	for _, pt := range prayerTimes {
		if pt.Location == userLocation && pt.Date+"-"+pt.Month+"-"+pt.Year == currentDate {
			matchingPrayerTime = pt
			break
		}
	}

	// Check if a matching prayer time was found
	if matchingPrayerTime.Location == "" {
		http.Error(w, "No prayer time found for today in your location", http.StatusNotFound)
		return
	}

	// Return the prayer time data to the client
	prayerTimeJSON, err := json.Marshal(matchingPrayerTime)
	if err != nil {
		http.Error(w, "Failed to encode prayer time data", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(prayerTimeJSON)
}

func main() {
	http.HandleFunc("/prayer-time", prayerTimesHandler)
	log.Fatal(http.ListenAndServe("0.0.0.0:8080", enableCORS(http.DefaultServeMux)))
}
