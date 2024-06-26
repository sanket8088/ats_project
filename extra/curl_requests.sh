Create candidate
curl --location 'http://127.0.0.1:8000/api/candidates' \
--header 'Cookie: csrftoken=o5GRWYJ9FEQUslYCXQGgTbdrwH6edJsduc1AXozQObYDMZShI9skprowlOHt3lov' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Mohit kumar yadav",
    "age": 32,
    "gender": "Male",
    "years_of_exp": 5,
    "phone_number": "+917830346904",
    "email": "sanket.nihal2@example.com",
    "current_salary": 50000,
    "expected_salary": 60000
}'

Filter candidates 

1. Filter by name
curl --location 'http://127.0.0.1:8000/api/candidates?name=anil' \
--header 'Content-Type: application/json'

2. Filter by salary range
curl --location 'http://localhost:8000/api/candidates?min_expected_salary=100000&max_expected_salary=150000' \
--header 'Accept: application/json'

3. Filter by experience and age
curl --location 'http://localhost:8000/api/candidates?min_age=21&max_age=30&min_years_of_exp=3' \
--header 'Accept: application/json'

4. Filter by email
curl --location 'http://127.0.0.1:8000/api/candidates?email=sanket.nihal%40gmail.com' \
--header 'Content-Type: application/json'

5. Filter by phone number
curl --location 'http://127.0.0.1:8000/api/candidates?phone_number=7830346973' \
--header 'Content-Type: application/json'

Modify Candidates status // valid operations are shortlist and reject
curl --location --request PATCH 'http://localhost:8000/api/candidates/6' \
--header 'Content-Type: application/json' \
--data '{
  "operation": "reject"
}'

