from fastapi import status
from src.models.charging_station import StationTypeEnum, ChargingStationType, ChargingStation
def test_create_charging_station_type(authenticated_user):
    response = authenticated_user.post(
        "/charging_station_types/",
        json={"name": StationTypeEnum.TYPE_A.value, "plug_count": 4, "efficiency": 0.9, "current_type": "AC"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == StationTypeEnum.TYPE_A.value

def test_list_charging_station_types(authenticated_user):
    response = authenticated_user.get("/charging_station_types/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
