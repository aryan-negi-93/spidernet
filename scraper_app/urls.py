from django.urls import path
from .views import scrape_view
from scraper_app import views

urlpatterns = [

    path('', scrape_view, name='scrape'),  # Root URL for the app
    path('extract/', views.extract_data_view, name='extract_data'),  # Extract data page
    path('download_scraped_html/', views.download_scraped_html, name='download_scraped_html'),
    path('download-csv/', views.download_csv_file, name='download_csv_file'),

]





