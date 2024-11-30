import requests
from behave import given

# HTTP Return Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204

@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    
    # List all of the products and delete them one by one
    rest_endpoint = f"{context.base_url}/products"
    
    # Get the list of existing products
    context.resp = requests.get(rest_endpoint)
    assert(context.resp.status_code == HTTP_200_OK)
    
    # Delete all existing products
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        assert(context.resp.status_code == HTTP_204_NO_CONTENT)

    # Load the database with new products from context.table
    for row in context.table:
        # Prepare the payload with product details from the feature file table
        payload = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'].lower() in ['true', '1'],  # Convert 'true'/'false' to boolean
            "category": row['category']
        }
        
        # Send a POST request to create the new product
        context.resp = requests.post(rest_endpoint, json=payload)
        
        # Assert that the product was successfully created
        assert context.resp.status_code == HTTP_201_CREATED
