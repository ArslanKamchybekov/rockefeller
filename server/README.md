# Rockefeller Server

FastAPI backend with Shopify OAuth and Admin API helpers.

## Setup

1) Create and activate a virtual environment
```bash
cd server
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2) Install dependencies
```bash
pip install -r requirements.txt
```

3) Environment variables (.env in server/)
```ini
APP_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
SHOPIFY_API_KEY=your_public_api_key
SHOPIFY_API_SECRET=your_private_api_secret
SHOPIFY_SCOPES=read_products,write_products,read_themes,write_themes,read_customers,read_orders
```

4) Run the server
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server at `http://localhost:8000`.

## Routes

- `GET /auth?shop={shop_domain}` → begin OAuth
- `GET /auth/callback?shop=...&code=...&hmac=...` → exchange code → token stored in-memory
- `GET /api/products?shop=...` → list products
- `POST /api/products?shop=...` → create product `{ title, body_html?, vendor? }`
- `GET /api/themes?shop=...` → list themes
- `PUT /api/themes/assets?shop=...` → upsert theme asset `{ theme_id, key, value }`
- `POST /api/webhooks` → receives Shopify webhooks (HMAC validated)

Note: token is kept in memory for this demo. Replace with a database for persistence.

## Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
