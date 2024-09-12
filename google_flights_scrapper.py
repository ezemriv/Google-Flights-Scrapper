import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def navigate_to_google_flights(driver):
    driver.get("https://www.google.com/travel/flights")
    time.sleep(2)
    driver.find_elements(By.XPATH, "//button[@aria-label='Accept all']")[0].click()
    time.sleep(2)

def set_flight_details(driver, city_from, city_to):
    destinations = driver.find_elements(By.XPATH, "//input[@class='II2One j0Ppje zmMKJ LbIaRd']")
    destinations[0].clear()
    destinations[0].send_keys(city_from)
    time.sleep(2)
    driver.find_elements(By.XPATH, '//div[@class="zsRT0d"]')[0].click()
    destinations[2].send_keys(city_to)
    time.sleep(2)
    driver.find_elements(By.XPATH, '//div[@class="zsRT0d"]')[0].click()
    time.sleep(2)
    driver.find_elements(By.XPATH, '//button[@aria-label="Search"]')[0].click()
    time.sleep(5)

def get_best_dates(driver):
    best_departure_date = driver.find_elements(By.XPATH, '//input[@class="TP4Lpb eoY5cb j0Ppje"]')[0].get_attribute("value")
    best_return_date = driver.find_elements(By.XPATH, '//input[@class="TP4Lpb eoY5cb j0Ppje"]')[1].get_attribute("value")
    return best_departure_date, best_return_date

def get_flight_details(flight_element):
    has_luggage = 1 if len(flight_element.find_elements(By.XPATH, '*//div[@class="vmWDCc NMm5M"]')) == 0 else 0

    return (
        flight_element.find_elements(By.XPATH, '*//div[@class="sSHqwe tPgKwe ogfYpf"]')[0].text,
        flight_element.find_elements(By.XPATH, '*//span[contains(@aria-label,"Departure time")]')[0].text,
        flight_element.find_elements(By.XPATH, '*//span[contains(@aria-label,"Arrival time")]')[0].text,
        flight_element.find_elements(By.XPATH, '*//div[contains(@aria-label,"Total duration")]')[0].text,
        flight_element.find_elements(By.XPATH, '*//div[@class="EfT7Ae AdWm1c tPgKwe"]')[0].text,
        has_luggage,
        flight_element.find_elements(By.XPATH, '*//span[contains(@aria-label,"euros")]')[0].text.replace("€", "").strip()
    )

def scrape_flights(driver, city_from, city_to):
    flights_df = pd.DataFrame(columns=[
        "origin", "destination", "best_departure_date", "best_return_date",
        "outbound_airline", "outbound_departure_time", "outbound_arrival_time",
        "outbound_duration", "outbound_stops", "outbound_has_luggage",
        "return_airline", "return_departure_time", "return_arrival_time",
        "return_duration", "return_stops", "return_has_luggage", "price"
    ])

    best_departure_date, best_return_date = get_best_dates(driver)

    for i in range(2):
        outbound_flights = driver.find_elements(By.XPATH, "//div[@class='yR1fYc']")
        outbound_airline, outbound_departure_time, outbound_arrival_time, outbound_duration, outbound_stops, outbound_has_luggage, price = get_flight_details(outbound_flights[i])

        outbound_flights[i].click()
        time.sleep(2)
        return_flights = driver.find_elements(By.XPATH, "//div[@class='yR1fYc']")

        for return_flight in return_flights:
            return_airline, return_departure_time, return_arrival_time, return_duration, return_stops, return_has_luggage, return_price = get_flight_details(return_flight)

            flight_data = pd.DataFrame([{
                "origin": city_from,
                "destination": city_to,
                "best_departure_date": best_departure_date,
                "best_return_date": best_return_date,
                "outbound_airline": outbound_airline,
                "outbound_departure_time": outbound_departure_time,
                "outbound_arrival_time": outbound_arrival_time,
                "outbound_duration": outbound_duration,
                "outbound_stops": outbound_stops,
                "outbound_has_luggage": outbound_has_luggage,
                "return_airline": return_airline,
                "return_departure_time": return_departure_time,
                "return_arrival_time": return_arrival_time,
                "return_duration": return_duration,
                "return_stops": return_stops,
                "return_has_luggage": return_has_luggage,
                "price": return_price
            }])

            flights_df = pd.concat([flights_df, flight_data], ignore_index=True)

        driver.back()
        time.sleep(2)

    return flights_df

def get_flight_data(city_from, city_to):
    driver = initialize_driver()
    navigate_to_google_flights(driver)
    set_flight_details(driver, city_from, city_to)
    flights_df = scrape_flights(driver, city_from, city_to)
    driver.quit()
    return flights_df

if __name__ == "__main__":
    city_from = input("Enter the departure city: ")
    city_to = input("Enter the destination city: ")
    result = get_flight_data(city_from, city_to)
    print(result)