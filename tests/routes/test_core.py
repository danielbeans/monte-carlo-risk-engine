import pytest
from fastapi import status
from fastapi import testclient


def test_health_check_success(client: testclient.TestClient) -> None:
    response = client.get("/health")
    
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert isinstance(result, dict)
    assert "status" in result
    assert result["status"] == "healthy"
