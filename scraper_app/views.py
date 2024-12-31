from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from django.conf import settings
import pandas as pd
import os
import time


def scrape_view(request):
    html_content = ""
    error_message = ""

    if request.method == "POST":
        url = request.POST.get("url")  # Get the input URL from the form

        try:
            # Setup Selenium WebDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)
            time.sleep(10)  # Wait for the page to fully load

            # Scrape and parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            html_content = soup.prettify()

            # Save the HTML content to a new file in the templates directory
            templates_dir = os.path.join(os.path.dirname(__file__), "templates", "scraper_app")
            os.makedirs(templates_dir, exist_ok=True)  # Create directory if it doesn't exist
            with open(os.path.join(templates_dir, "scraped_html.html"), "w", encoding="utf-8") as file:
                file.write(html_content)

            # Close the browser
            driver.quit()
        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render(request, 'index.html', {
        'html_content': html_content,
        'error_message': error_message,
    })





def extract_data_view(request):
    extracted_data = None
    error_message = None

    if request.method == "POST":
        file_path = "C:\\Users\\user\\Desktop\\scaby\\my_project\\scraper_app\\templates\\scraper_app\\scraped_html.html"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
        except FileNotFoundError:
            error_message = "Scraped HTML file not found!"
            return render(request, "extract_data.html", {"error_message": error_message})

        soup = BeautifulSoup(html_content, "html.parser")
        tags = request.POST.getlist("tag[]")
        class_names = request.POST.getlist("class_name[]")

        data_dict = {}

        for tag, class_name in zip(tags, class_names):
            elements = soup.find_all(tag, class_=class_name) if class_name else soup.find_all(tag)
            content = [element.get_text(strip=True) for element in elements]

            # Handle case when no data is found
            if not content:
                content = ['']  # Replace empty data with empty string

            if tag in data_dict:
                data_dict[class_name].extend(content)
            else:
                data_dict[class_name] = content

        # Ensure all columns have the same length
        max_length = max(len(values) for values in data_dict.values()) if data_dict else 0
        for key in data_dict:
            while len(data_dict[key]) < max_length:
                data_dict[key].append(None)  # Fill missing entries with None

        if data_dict:
            df = pd.DataFrame(data_dict)
            # Save the DataFrame to a CSV file
            csv_file_path = os.path.join(settings.BASE_DIR, "extracted_data.csv")
            df.to_csv(csv_file_path, index=False, encoding="utf-8")
            extracted_data = df.to_html(classes="dataframe", index=False, escape=False)
        else:
            error_message = "No data extracted. Please check your inputs."

    return render(request, "extract_data.html", {"extracted_data": extracted_data, "error_message": error_message})




def download_csv_file(request):
    csv_file_path = os.path.join(settings.BASE_DIR, "extracted_data.csv")
    try:
        with open(csv_file_path, 'rb') as csv_file:
            response = HttpResponse(csv_file, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="extracted_data.csv"'
            return response
    except FileNotFoundError:
        return render(request, "extract_data.html", {"error_message": "CSV file not found!"})


def download_scraped_html(request):
    file_path = os.path.join(os.path.dirname(__file__), "templates", "scraper_app", "scraped_html.html")
    try:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="scraped_html.html"'
        return response
    except Exception as e:
        return render(request, 'scraper_app/index.html', {'error_message': f"File not found: {str(e)}"})




