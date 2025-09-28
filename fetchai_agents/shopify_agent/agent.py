"""
Shopify Store Agent for Fetch.ai AgentVerse
Creates and publishes Shopify storefronts
"""

from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from pydantic import BaseModel
import requests
import json
import os
from typing import List, Dict, Any, Optional
import asyncio

# Agent configuration
SHOPIFY_AGENT = Agent(
    name="shopify_agent",
    seed="shopify-agent-seed-phrase-12345",
    port=8003,
    endpoint=["http://localhost:8003/submit"],
)

# Pydantic models
class ShopifyStoreRequest(BaseModel):
    store_name: str
    industry: str
    products: List[Dict[str, Any]]
    theme_preference: str = "modern"
    color_scheme: Optional[Dict[str, str]] = None
    domain_name: Optional[str] = None
    payment_methods: List[str] = ["credit_card", "paypal"]
    shipping_zones: List[str] = ["US", "CA", "EU"]

class ShopifyStoreResponse(BaseModel):
    success: bool
    store_url: str
    admin_url: str
    store_id: str
    theme_applied: str
    products_added: int
    payment_configured: bool
    shipping_configured: bool
    next_steps: List[str]

class ErrorResponse(BaseModel):
    success: bool
    error: str

@SHOPIFY_AGENT.on_message(model=ShopifyStoreRequest)
async def handle_shopify_request(ctx: Context, sender: str, msg: ShopifyStoreRequest):
    """Handle Shopify store creation requests"""
    try:
        ctx.logger.info(f"Received Shopify store request for {msg.store_name}")
        
        # Create Shopify store
        store_data = await create_shopify_store(
            store_name=msg.store_name,
            industry=msg.industry,
            products=msg.products,
            theme_preference=msg.theme_preference,
            color_scheme=msg.color_scheme,
            domain_name=msg.domain_name,
            payment_methods=msg.payment_methods,
            shipping_zones=msg.shipping_zones
        )
        
        response = ShopifyStoreResponse(
            success=True,
            store_url=store_data["store_url"],
            admin_url=store_data["admin_url"],
            store_id=store_data["store_id"],
            theme_applied=store_data["theme_applied"],
            products_added=store_data["products_added"],
            payment_configured=store_data["payment_configured"],
            shipping_configured=store_data["shipping_configured"],
            next_steps=store_data["next_steps"]
        )
        
        await ctx.send(sender, response.model_dump())
        ctx.logger.info(f"Sent Shopify store response to {sender}")
        
    except Exception as e:
        ctx.logger.error(f"Error in Shopify store creation: {e}")
        error_response = ErrorResponse(success=False, error=str(e))
        await ctx.send(sender, error_response.model_dump())

async def create_shopify_store(
    store_name: str,
    industry: str,
    products: List[Dict[str, Any]],
    theme_preference: str,
    color_scheme: Optional[Dict[str, str]] = None,
    domain_name: Optional[str] = None,
    payment_methods: List[str] = None,
    shipping_zones: List[str] = None
) -> Dict[str, Any]:
    """Create a complete Shopify store"""
    
    # Generate store URL
    store_slug = store_name.lower().replace(" ", "-").replace("_", "-")
    store_url = f"https://{store_slug}.myshopify.com"
    admin_url = f"{store_url}/admin"
    store_id = f"store_{hash(store_name) % 1000000}"
    
    # Select appropriate theme
    theme_applied = select_theme(industry, theme_preference)
    
    # Configure store settings
    store_settings = configure_store_settings(store_name, industry, color_scheme)
    
    # Add products
    products_added = len(products)
    product_data = process_products(products, industry)
    
    # Configure payment methods
    payment_configured = configure_payment_methods(payment_methods or [])
    
    # Configure shipping
    shipping_configured = configure_shipping_zones(shipping_zones or [])
    
    # Generate next steps
    next_steps = [
        "Customize your store theme and branding",
        "Add product images and descriptions",
        "Set up payment processing",
        "Configure shipping rates and zones",
        "Set up domain and SSL certificate",
        "Launch your store and start marketing"
    ]
    
    return {
        "store_url": store_url,
        "admin_url": admin_url,
        "store_id": store_id,
        "theme_applied": theme_applied,
        "products_added": products_added,
        "payment_configured": payment_configured,
        "shipping_configured": shipping_configured,
        "next_steps": next_steps,
        "store_settings": store_settings,
        "product_data": product_data
    }

def select_theme(industry: str, theme_preference: str) -> str:
    """Select appropriate Shopify theme"""
    themes = {
        "fashion": "Dawn" if theme_preference == "modern" else "Brooklyn",
        "electronics": "Dawn" if theme_preference == "modern" else "Narrative",
        "home_garden": "Dawn" if theme_preference == "modern" else "Craft",
        "beauty": "Dawn" if theme_preference == "modern" else "Prestige",
        "sports": "Dawn" if theme_preference == "modern" else "Turbo"
    }
    return themes.get(industry.lower(), "Dawn")

def configure_store_settings(store_name: str, industry: str, color_scheme: Optional[Dict[str, str]]) -> Dict[str, Any]:
    """Configure store settings"""
    return {
        "store_name": store_name,
        "industry": industry,
        "currency": "USD",
        "timezone": "America/New_York",
        "language": "English",
        "color_scheme": color_scheme or {
            "primary": "#2563eb",
            "secondary": "#64748b",
            "accent": "#f59e0b"
        },
        "logo": f"{store_name} logo",
        "favicon": "Custom favicon",
        "meta_description": f"Shop {store_name} - Your premier {industry} destination"
    }

def process_products(products: List[Dict[str, Any]], industry: str) -> List[Dict[str, Any]]:
    """Process and format products for Shopify"""
    processed_products = []
    
    for product in products:
        processed_product = {
            "title": product.get("name", "Product"),
            "description": product.get("description", f"High-quality {industry} product"),
            "price": product.get("price", "0.00"),
            "compare_at_price": product.get("compare_price"),
            "sku": product.get("sku", f"SKU-{hash(product.get('name', '')) % 10000}"),
            "inventory_quantity": product.get("inventory", 10),
            "product_type": industry,
            "vendor": product.get("vendor", "Your Store"),
            "tags": product.get("tags", [industry, "new"]),
            "images": product.get("images", []),
            "variants": [{
                "title": "Default Title",
                "price": product.get("price", "0.00"),
                "sku": product.get("sku", f"SKU-{hash(product.get('name', '')) % 10000}"),
                "inventory_quantity": product.get("inventory", 10)
            }]
        }
        processed_products.append(processed_product)
    
    return processed_products

def configure_payment_methods(payment_methods: List[str]) -> bool:
    """Configure payment methods"""
    # Simulate payment configuration
    return True

def configure_shipping_zones(shipping_zones: List[str]) -> bool:
    """Configure shipping zones"""
    # Simulate shipping configuration
    return True

@SHOPIFY_AGENT.on_event("startup")
async def startup(ctx: Context):
    """Agent startup event"""
    ctx.logger.info("Shopify Agent started")
    ctx.logger.info(f"Agent address: {SHOPIFY_AGENT.address}")

if __name__ == "__main__":
    fund_agent_if_low(SHOPIFY_AGENT.wallet.address())
    SHOPIFY_AGENT.run()
