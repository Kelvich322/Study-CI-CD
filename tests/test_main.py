from fastapi import status

def test_get_all_recipes_empty(client):
    """Тест пустого списка рецептов"""
    response = client.get("/recipes/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_create_recipe(client, test_recipe_data):
    """Тест создания рецепта"""
    response = client.post("/recipes/", json=test_recipe_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["title"] == test_recipe_data["title"]
    assert data["ingredients"] == test_recipe_data["ingredients"]
    assert data["cook_time"] == test_recipe_data["cook_time"]
    assert data["description"] == test_recipe_data["description"]

def test_get_recipe(client, test_recipe_data):
    """Тест получения рецепта""" 
    response = client.post("/recipes/", json=test_recipe_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    response = client.get("/recipes/1")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["title"] == test_recipe_data["title"]
    assert data["ingredients"] == test_recipe_data["ingredients"]
    assert data["cook_time"] == test_recipe_data["cook_time"]
    assert data["description"] == test_recipe_data["description"] 

def test_recipe_not_found(client):
    """Тест несуществующего рецепта"""
    response = client.get("/recipes/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Рецепт не найден"

def test_negative_id(client):
    """Тест отрицательного ID"""
    response = client.get("/recipes/-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY