from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import time
import requests
import json
from concurrent import futures

GO_SERVICE_URL = "http://127.0.0.1:8090/api/internal/frax/result"
AUTH_TOKEN = "secret12" # Псевдо-токен

executor = futures.ThreadPoolExecutor(max_workers=1)

def calculate_logic(data):
    """
    Симуляция долгого вычисления и отправка результата обратно.
    """
    print(f"Start processing Frax ID: {data.get('id')}")
    
    time.sleep(7)

    age = float(data.get('age', 0))
    gender_val = 1.5 if data.get('gender') else 1.0
    
    weight = float(data.get('weight', 0))
    height = float(data.get('height', 0))

    height_m = height / 100.0
    bmi = 0.0
    if height_m > 0:
        bmi = weight / (height_m * height_m)


    factor_sum = float(data.get('factor_sum', 0))


    pof = 0.1*age + 0.2*gender_val + 0.05*bmi + 0.3*factor_sum + 0.5
    phf = 0.05*age + 0.15*gender_val + 0.03*bmi + 0.2*factor_sum + 0.2


    pof = max(0, min(100, pof))
    phf = max(0, min(100, phf))

    result_payload = {
        "id": data.get('id'),
        "POF": pof,
        "PHF": phf
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": AUTH_TOKEN 
    }

    try:
        print(f"Sending result for Frax ID: {data.get('id')} to {GO_SERVICE_URL}")
        requests.put(GO_SERVICE_URL, json=result_payload, headers=headers, timeout=5)
    except Exception as e:
        print(f"Error callback to Go service: {e}")


@api_view(['POST'])
def perform_calculation(request):
    """
    Принимает запрос на расчет, запускает его в фоне и сразу отвечает 200.
    """
    try:
        data = request.data
        if "id" not in data:
             return Response({"error": "No ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        executor.submit(calculate_logic, data)

        return Response({"message": "Calculation started"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)