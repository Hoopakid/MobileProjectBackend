from celery import shared_task
import os


@shared_task
def clear_temporary_files():
    temporary_directory = '/home/hoopakid/PythonMain/DRF_JWT/MobileProjectBackend/MobileProject/media/temporarily'
    for filename in os.listdir(temporary_directory):
        file_path = os.path.join(temporary_directory, filename)
        os.remove(file_path)
