from fastapi import status
from src.models.charging_station import StationTypeEnum, ChargingStationType, ChargingStation, CurrentType
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

def test_retrieve_charging_station_type(authenticated_user, charging_station_type):
    response = authenticated_user.get(f"/charging_station_types/{charging_station_type.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == str(charging_station_type.id)
    assert data['name'] == charging_station_type.name.value


def test_update_charging_station_type(authenticated_user, charging_station_type):
    update_data = {
        "name": StationTypeEnum.TYPE_A.value,
        "plug_count": 5,
        "efficiency": 0.95,
        "current_type": CurrentType.DC.value
    }
    response = authenticated_user.patch(
        f"/charging_station_types/{charging_station_type.id}",
        json=update_data
    )
    print(response.json())
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == update_data["name"]
    assert data["plug_count"] == update_data["plug_count"]
    assert data["efficiency"] == update_data["efficiency"]
    assert data["current_type"] == update_data["current_type"]

def test_delete_charging_station_type(authenticated_user, charging_station_type):
    response = authenticated_user.delete(f"/charging_stations_types/{str(charging_station_type.id)}")
    assert response.status_code == 204


