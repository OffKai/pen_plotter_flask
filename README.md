# Dev container (recommended)

`docker compose -f docker-compose-dev.yaml up`

App will open on `http://localhost`, admin auth is:

`username: oke_admin`

`password: admin`

# Local server (Windows, Mac instruction TODO)

To start server locally:

`$Env.SECRET_ADMIN_AUTH = "oke_admin: admin"`
`$Env.SECRET_ADMIN_TOKEN = "admin123"`


`python -m venv ppenv`

`.\ppenv\Scripts\activate`

`pip install -r requirements.txt`


`python main.py --config config.yaml`


App will open on `http://localhost:5000`, admin auth is:

`username: oke_admin`

`password: admin`
