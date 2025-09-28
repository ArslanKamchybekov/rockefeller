import { google } from '@ai-sdk/google';
import { streamText, convertToModelMessages, UIMessage, stepCountIs } from 'ai';
import { z } from 'zod';
import { createServerClient } from '@/lib/supabase-server';

// IMPORTANT! Set the runtime to edge
export const runtime = 'edge';

export async function POST(req: Request) {
  try {
    const { messages, userId }: { messages: UIMessage[], userId?: string } = await req.json();

    const result = streamText({
      model: google('gemini-2.5-flash'),
      system: `You are an AI assistant that helps users set up e-commerce stores and manage business workflows. 

You have access to these tools:

🏪 setupStore - Creates and configures a Shopify store (simulated)
💳 configurePayment - Sets up payment methods for the store (simulated)
📦 setupInventory - Creates sample products and sets up inventory (simulated)
🛍️ addProduct - Adds a new product to the user's Shopify store (real Shopify API)
🗑️ deleteProduct - Deletes a product from the user's Shopify store (real Shopify API)
🗑️ deleteAllProducts - Deletes all products from the user's Shopify store (real Shopify API)
⚖️ generateLegalDocs - Generates comprehensive legal documents (privacy policy, terms of use, NDA) for any business idea (real API)

When a user asks you to:
- Set up a store → Use setupStore first, then generateLegalDocs
- Create a complete e-commerce setup → Chain all tools: setupStore → generateLegalDocs → configurePayment → setupInventory
- Generate legal documents for any business idea → Use generateLegalDocs
- Configure payments → Use configurePayment
- Set up inventory → Use setupInventory
- Add a product to store → Use addProduct (price should be in dollars, e.g., 99.99 for $99.99). If the user has uploaded images, look for "Image URLs:" in their message and use those URLs in the images parameter.
- Delete a product from store → Use deleteProduct
- Delete all products from store → Use deleteAllProducts

Always explain what you're doing and show progress. Use the tools in logical sequence and provide clear feedback about each step. If a user mentions a store name, use it in the setupStore tool. Be helpful and proactive in suggesting next steps.

When creating products with images:
1. Look for "Image URLs:" in the user's message
2. Extract the URLs (they will be comma-separated)
3. Use those URLs in the images parameter of addProduct tool
4. If no image URLs are found, create the product without images`,
      messages: convertToModelMessages(messages),
      stopWhen: stepCountIs(10), // Allow up to 10 steps for multi-tool workflows
      tools: {
        setupStore: {
          description: "Create and configure a Shopify store",
          inputSchema: z.object({ 
            name: z.string().describe("The name of the store to create"),
            plan: z.string().optional().describe("The store plan (basic, professional, enterprise)")
          }),
          execute: async ({ name, plan = "basic" }) => {
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            return { 
              success: true,
              status: "done", 
              storeUrl: `https://${name.toLowerCase().replace(/\s+/g, '-')}.myshopify.com`,
              plan,
              message: `Store "${name}" created successfully with ${plan} plan`
            };
          }
        },
        configurePayment: {
          description: "Configure payment methods for the store",
          inputSchema: z.object({ 
            storeUrl: z.string().describe("The URL of the store"),
            paymentMethods: z.array(z.string()).optional().describe("Payment methods to enable")
          }),
          execute: async ({ storeUrl, paymentMethods = ["credit_card", "paypal"] }) => {
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            return { 
              success: true,
              status: "done", 
              enabledMethods: paymentMethods,
              message: `Configured ${paymentMethods.length} payment methods for ${storeUrl}`
            };
          }
        },
        setupInventory: {
          description: "Set up initial inventory and product catalog",
          inputSchema: z.object({ 
            storeUrl: z.string().describe("The URL of the store"),
            productCount: z.number().optional().describe("Number of sample products to create")
          }),
          execute: async ({ storeUrl, productCount = 5 }) => {
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 1800));
            
            return { 
              success: true,
              status: "done", 
              productsCreated: productCount,
              message: `Created ${productCount} sample products in ${storeUrl}`
            };
          }
        },
        generateLegalDocs: {
          description: "Generate legal documents (privacy policy, terms of service, NDA) for a business idea",
          inputSchema: z.object({ 
            idea: z.string().describe("The business idea or description to generate legal documents for")
          }),
          execute: async ({ idea }) => {
            try {
              const response = await fetch('http://127.0.0.1:8000/api/docs/generate', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({ idea }),
              });
              
              if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              
              const result = await response.json();
              
              // Parse the JSON string to extract individual documents
              let parsedDocs;
              try {
                // Clean the response - remove markdown code blocks if present
                let cleanedDocs = result.docs.trim();
                
                // Remove markdown code block markers more aggressively
                cleanedDocs = cleanedDocs.replace(/^```json\s*/, '').replace(/\s*```$/, '');
                cleanedDocs = cleanedDocs.replace(/^```\s*/, '').replace(/\s*```$/, '');
                
                // Remove any leading/trailing backticks or whitespace
                cleanedDocs = cleanedDocs.replace(/^`+|`+$/g, '').trim();
                
                // Find the JSON array within the response
                const jsonStart = cleanedDocs.indexOf('[');
                const jsonEnd = cleanedDocs.lastIndexOf(']') + 1;
                
                if (jsonStart === -1 || jsonEnd === 0) {
                  throw new Error('No JSON array found in response');
                }
                
                const jsonString = cleanedDocs.substring(jsonStart, jsonEnd);
                
                // Validate that we have a valid JSON array
                if (!jsonString.startsWith('[')) {
                  throw new Error('Response is not valid JSON array');
                }
                
                console.log('Parsing JSON string:', jsonString.substring(0, 200) + '...');
                parsedDocs = JSON.parse(jsonString);
                
                // Ensure it's an array
                if (!Array.isArray(parsedDocs)) {
                  throw new Error('Response is not a JSON array');
                }
                
                console.log('Successfully parsed', parsedDocs.length, 'documents');
              } catch (parseError) {
                console.error('Error parsing legal docs JSON:', parseError);
                console.error('Raw response:', result.docs);
                return {
                  success: false,
                  status: "error",
                  message: "Failed to parse legal documents response"
                };
              }
              
              // Format the documents for better display
              const formattedDocs = parsedDocs.map((doc: any) => ({
                type: doc.doc_type,
                title: doc.title,
                summary: doc.summary,
                content: doc.content,
                placeholders: doc.placeholders || [],
                defaults_used: doc.defaults_used || {}
              }));
              
              return { 
                success: true,
                status: "done", 
                docs: formattedDocs,
                pdfs: result.pdfs || [],
                message: `Generated ${formattedDocs.length} legal documents for: ${idea}`
              };
            } catch (error) {
              console.error('Error generating legal docs:', error);
              return { 
                success: false,
                status: "error", 
                message: `Failed to generate legal documents: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        addProduct: {
          description: "Add a new product to the user's Shopify store",
          inputSchema: z.object({ 
            title: z.string().describe("The product title/name"),
            description: z.string().optional().describe("Product description"),
            price: z.number().describe("Product price in dollars (e.g., 19.99 for $19.99)"),
            sku: z.string().optional().describe("Product SKU"),
            inventory_quantity: z.number().optional().describe("Initial inventory quantity (defaults to 10 if not specified)"),
            product_type: z.string().optional().describe("Product type/category"),
            vendor: z.string().optional().describe("Product vendor/brand"),
            tags: z.array(z.string()).optional().describe("Product tags"),
            images: z.array(z.string()).optional().describe("Product image URLs")
          }),
          execute: async ({ title, description, price, sku, inventory_quantity = 10, product_type, vendor, tags, images }) => {
            try {
              if (!userId) {
                return {
                  success: false,
                  status: "error",
                  message: "User ID is required to add products"
                };
              }

              // Get user's Shopify integration from Supabase
              const supabase = createServerClient();
              const { data: shopifyIntegration, error } = await supabase
                .from('integrations')
                .select('*')
                .eq('user_id', userId)
                .eq('integration_type', 'shopify')
                .eq('is_active', true)
                .single();

              if (error || !shopifyIntegration) {
                return {
                  success: false,
                  status: "error",
                  message: "No active Shopify integration found. Please connect your Shopify store first."
                };
              }

              // Extract shop domain from external_id (assuming it's stored as shop.myshopify.com)
              const shopDomain = shopifyIntegration.external_id;
              const accessToken = shopifyIntegration.access_token;

              // Prepare product data for Shopify API
              const productData = {
                product: {
                  title,
                  body_html: description ? `<p>${description}</p>` : undefined,
                  vendor,
                  product_type,
                  tags: tags ? tags.join(', ') : undefined,
                  variants: [{
                    price: price.toFixed(2), // Price is already in dollars
                    sku,
                    inventory_quantity,
                    inventory_management: "shopify"
                  }],
                  images: images ? images.map((url: string) => ({ src: url })) : undefined
                }
              };

              // Make API call to Shopify
              const response = await fetch(`https://${shopDomain}/admin/api/2023-10/products.json`, {
                method: 'POST',
                headers: {
                  'X-Shopify-Access-Token': accessToken,
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
              });

              if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`Shopify API error: ${response.status} - ${errorData}`);
              }

              const result = await response.json();
              const product = result.product;

              return {
                success: true,
                status: "done",
                product: {
                  id: product.id,
                  title: product.title,
                  handle: product.handle,
                  price: product.variants[0]?.price,
                  sku: product.variants[0]?.sku,
                  inventory_quantity: product.variants[0]?.inventory_quantity,
                  admin_url: `https://${shopDomain}/admin/products/${product.id}`,
                  store_url: `https://${shopDomain}/products/${product.handle}`
                },
                message: `Successfully added product "${title}" to your Shopify store`
              };
            } catch (error) {
              console.error('Error adding product to Shopify:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to add product: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        deleteProduct: {
          description: "Delete a product from the user's Shopify store",
          inputSchema: z.object({ 
            product_id: z.string().describe("The Shopify product ID to delete"),
            product_title: z.string().optional().describe("The product title for confirmation (optional)")
          }),
          execute: async ({ product_id, product_title }) => {
            try {
              if (!userId) {
                return {
                  success: false,
                  status: "error",
                  message: "User ID is required to delete products"
                };
              }

              // Get user's Shopify integration from Supabase
              const supabase = createServerClient();
              const { data: shopifyIntegration, error } = await supabase
                .from('integrations')
                .select('*')
                .eq('user_id', userId)
                .eq('integration_type', 'shopify')
                .eq('is_active', true)
                .single();

              if (error || !shopifyIntegration) {
                return {
                  success: false,
                  status: "error",
                  message: "No active Shopify integration found. Please connect your Shopify store first."
                };
              }

              // Extract shop domain from external_id
              const shopDomain = shopifyIntegration.external_id;
              const accessToken = shopifyIntegration.access_token;

              // Make API call to Shopify to delete the product
              const response = await fetch(`https://${shopDomain}/admin/api/2023-10/products/${product_id}.json`, {
                method: 'DELETE',
                headers: {
                  'X-Shopify-Access-Token': accessToken,
                  'Content-Type': 'application/json',
                }
              });

              if (!response.ok) {
                if (response.status === 404) {
                  return {
                    success: false,
                    status: "error",
                    message: `Product with ID ${product_id} not found. It may have already been deleted.`
                  };
                }
                const errorData = await response.text();
                throw new Error(`Shopify API error: ${response.status} - ${errorData}`);
              }

              return {
                success: true,
                status: "done",
                product_id,
                message: `Successfully deleted product${product_title ? ` "${product_title}"` : ''} (ID: ${product_id}) from your Shopify store`
              };
            } catch (error) {
              console.error('Error deleting product from Shopify:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to delete product: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        deleteAllProducts: {
          description: "Delete all products from the user's Shopify store",
          inputSchema: z.object({ 
            confirm: z.boolean().optional().describe("Confirmation to delete all products (defaults to true)")
          }),
          execute: async ({ confirm = true }) => {
            try {
              if (!userId) {
                return {
                  success: false,
                  status: "error",
                  message: "User ID is required to delete products"
                };
              }

              if (!confirm) {
                return {
                  success: false,
                  status: "error",
                  message: "Operation cancelled - confirmation required to delete all products"
                };
              }

              // Get user's Shopify integration from Supabase
              const supabase = createServerClient();
              const { data: shopifyIntegration, error } = await supabase
                .from('integrations')
                .select('*')
                .eq('user_id', userId)
                .eq('integration_type', 'shopify')
                .eq('is_active', true)
                .single();

              if (error || !shopifyIntegration) {
                return {
                  success: false,
                  status: "error",
                  message: "No active Shopify integration found. Please connect your Shopify store first."
                };
              }

              // Extract shop domain from external_id
              const shopDomain = shopifyIntegration.external_id;
              const accessToken = shopifyIntegration.access_token;

              // First, fetch all products
              const productsResponse = await fetch(`https://${shopDomain}/admin/api/2023-10/products.json?limit=250`, {
                method: 'GET',
                headers: {
                  'X-Shopify-Access-Token': accessToken,
                  'Content-Type': 'application/json',
                }
              });

              if (!productsResponse.ok) {
                const errorData = await productsResponse.text();
                throw new Error(`Failed to fetch products: ${productsResponse.status} - ${errorData}`);
              }

              const productsData = await productsResponse.json();
              const products = productsData.products || [];

              if (products.length === 0) {
                return {
                  success: true,
                  status: "done",
                  deleted_count: 0,
                  message: "No products found in your store to delete"
                };
              }

              // Delete all products one by one
              const deletedProducts = [];
              const failedProducts = [];

              for (const product of products) {
                try {
                  const deleteResponse = await fetch(`https://${shopDomain}/admin/api/2023-10/products/${product.id}.json`, {
                    method: 'DELETE',
                    headers: {
                      'X-Shopify-Access-Token': accessToken,
                      'Content-Type': 'application/json',
                    }
                  });

                  if (deleteResponse.ok) {
                    deletedProducts.push({
                      id: product.id,
                      title: product.title
                    });
                  } else {
                    failedProducts.push({
                      id: product.id,
                      title: product.title,
                      error: `HTTP ${deleteResponse.status}`
                    });
                  }
                } catch (error) {
                  failedProducts.push({
                    id: product.id,
                    title: product.title,
                    error: error instanceof Error ? error.message : 'Unknown error'
                  });
                }
              }

              return {
                success: true,
                status: "done",
                deleted_count: deletedProducts.length,
                failed_count: failedProducts.length,
                deleted_products: deletedProducts,
                failed_products: failedProducts,
                message: `Successfully deleted ${deletedProducts.length} products from your Shopify store${failedProducts.length > 0 ? ` (${failedProducts.length} failed)` : ''}`
              };
            } catch (error) {
              console.error('Error deleting all products from Shopify:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to delete all products: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        }
      },
    });

    return result.toUIMessageStreamResponse();
  } catch (error) {
    console.error('Chat API error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}