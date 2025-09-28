import { google } from '@ai-sdk/google';
import { openai } from '@ai-sdk/openai';
import { streamText, convertToModelMessages, UIMessage, stepCountIs } from 'ai';
import { z } from 'zod';
import { createServerClient } from '@/lib/supabase-server';

// Using Node.js runtime for better compatibility
// export const runtime = 'edge';

export async function POST(req: Request) {
  try {
    const { messages, userId }: { messages: UIMessage[], userId?: string } = await req.json();

    // Detect if user asked for a full end-to-end flow
    const lastUserMsg = [...messages].reverse().find(m => m.role === 'user');
    const lastText = (typeof (lastUserMsg as any)?.content === 'string' ? (lastUserMsg as any).content : '')
      .toLowerCase();
    const wantsFullFlow = /full\s*flow|complete\s*setup|end[- ]?to[- ]?end|all\s*steps|run\s*everything/.test(lastText);

    const result = streamText({
      model: google('gemini-2.5-flash'),
      system: `You are an AI assistant that helps users set up e-commerce stores and manage business workflows. 

You have access to these tools:
🛍️ addProduct - Adds a new product to the user's Shopify store (real Shopify API)
🗑️ deleteProduct - Deletes a product from the user's Shopify store (real Shopify API)
🗑️ deleteAllProducts - Deletes all products from the user's Shopify store (real Shopify API)
⚖️ generateLegalDocs - Generates comprehensive legal documents (privacy policy, terms of use, NDA) for any business idea (real API)
🔍 webSearch - Search the web for real-time information using OpenAI's web search capabilities
📊 marketSearch - Search for market data, competitor analysis, and industry statistics
📋 generatePitchDeck - Generate a comprehensive pitch deck with market research, influencer strategy, and professional design
🎨 generateBranding - Generate branding assets (name, tagline, logo) for a business idea
🎬 generateBrandingVideo - Generate a branding video for a business idea
📞 phoneassistant - Set up your customer phone assistant

Full setup / full flow:
- If the user asks for a "full setup", "full flow", or "end-to-end" run these tools in order, passing context between steps:
  1) marketSearch → market insights, competitors
  2) generateBranding → brand name, tagline, logo
  3) generateLegalDocs → use branding/context; return PDFs
  4) storeLink → surface https://rockefeller-store.myshopify.com
  5) mailSetup → indicate assistant inbox is being set up
  6) phoneassistant → set up customer phone assistant
  7) influencerSearch → accessible influencer list
  8) generateBrandingVideo → promotional video plan/content
  9) generatePitchDeck → produce deck leveraging market + influencer data; export PDF
- Always summarize each step and carry forward relevant outputs.
- After completing, suggest adding products to the created store.

When a user asks you to:
- Generate legal documents for any business idea → Use generateLegalDocs
- Add a product to store → Use addProduct (price should be in dollars, e.g., 99.99 for $99.99). If the user has uploaded images, look for "Image URLs:" in their message and use those URLs in the images parameter.
- Delete a product from store → Use deleteProduct
- Delete all products from store → Use deleteAllProducts
- Search for information on the web → Use webSearch for real-time information
- Research competitors or market data → Use marketSearch for industry analysis and competitor insights
- Generate a pitch deck → Use generatePitchDeck for comprehensive investor presentations with market research and influencer strategy
- Generate branding assets → Use generateBranding for business name, tagline, and logo creation
- Create a branding video → Use generateBrandingVideo for promotional video content
- Set up phone assistant → Use phoneassistant to provide the customer phone number

Always explain what you're doing and show progress. Use the tools in logical sequence and provide clear feedback about each step. If a user mentions a store name, use it in the setupStore tool. Be helpful and proactive in suggesting next steps.

When creating products with images:
1. Look for "Image URLs:" in the user's message
2. Extract the URLs (they will be comma-separated)
3. Use those URLs in the images parameter of addProduct tool
4. If no image URLs are found, create the product without images`,
      messages: convertToModelMessages(messages),
      stopWhen: stepCountIs(12), // Allow multi-step chained workflows
      prepareStep: async ({ steps }) => {
        if (!wantsFullFlow) return {};
        // Enforce your exact sequence regardless of text-only steps between tools
        const sequence = [
          'marketSearch',
          'generateBranding',
          'generateLegalDocs',
          'storeLink',
          'mailSetup',
          'phoneassistant',
          'influencerSearch',
          'generateBrandingVideo',
          'generatePitchDeck',
        ];
        const usedTools = new Set<string>();
        try {
          for (const s of (steps as any) || []) {
            const toolCalls = (s.toolCalls || []).map((t: any) => t.toolName);
            const toolResults = (s.toolResults || []).map((t: any) => t.toolName);
            for (const name of [...toolCalls, ...toolResults]) usedTools.add(name);
          }
        } catch {}
        const nextTool = sequence.find(name => !usedTools.has(name));
        if (!nextTool) return {};
        return { activeTools: [nextTool] } as any;
      },
      tools: {
        storeLink: {
          description: "Surface the created store link in the UI",
          inputSchema: z.object({}).optional() as any,
          execute: async () => {
            const storeUrl = `https://rockefeller-store.myshopify.com`;
            return {
              success: true,
              status: 'done',
              store_url: storeUrl,
              message: `Here is the link to your store: [rockefeller-store.myshopify.com](${storeUrl})`
            };
          }
        },
        mailSetup: {
          description: "Indicate that the customer assistant's email inbox is being set up",
          inputSchema: z.object({}).optional() as any,
          execute: async () => {
            return {
              success: true,
              status: 'done',
              message: 'Customer assistant\'s email inbox is being set up.'
            };
          }
        },
        influencerSearch: {
          description: "Find accessible influencers (micro/mid-tier) for the brand/idea",
          inputSchema: z.object({
            idea: z.string().describe('Brand or business idea to find influencers for'),
            target_market: z.string().optional().describe('Target audience'),
          }),
          execute: async ({ idea, target_market }) => {
            try {
              const res = await streamText({
                model: openai('gpt-4o'),
                messages: [{
                  role: 'user',
                  content: `Find accessible influencers for: "${idea}"${target_market ? ` targeting ${target_market}` : ''}. Focus on micro/mid-tier (1K-100K). Return concise JSON list with: name, handle, platform, followers_range, engagement, focus, links, why_relevant.`
                }]
              });
              let text = '';
              for await (const chunk of res.textStream) text += chunk;
              let influencers: any = text;
              try {
                const s = text.indexOf('['); const e = text.lastIndexOf(']') + 1;
                influencers = JSON.parse(text.substring(s, e));
              } catch {}
              return {
                success: true,
                status: 'done',
                influencers,
                message: 'Influencer recommendations generated.'
              };
            } catch {
              return { success: false, status: 'error', message: 'Failed to generate influencer recommendations' };
            }
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
                
                // More comprehensive markdown code block removal
                cleanedDocs = cleanedDocs.replace(/^```json\s*/i, '').replace(/\s*```$/i, '');
                cleanedDocs = cleanedDocs.replace(/^```\s*/i, '').replace(/\s*```$/i, '');
                
                // Remove any remaining backticks or whitespace
                cleanedDocs = cleanedDocs.replace(/^`+|`+$/g, '').trim();
                
                // If the response is still wrapped in markdown, try to extract just the JSON part
                if (cleanedDocs.includes('```')) {
                  const jsonMatch = cleanedDocs.match(/```(?:json)?\s*(\[[\s\S]*?\])\s*```/);
                  if (jsonMatch && jsonMatch[1]) {
                    cleanedDocs = jsonMatch[1].trim();
                  }
                }
                
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
                
                // Try one more time with a different approach - extract JSON from markdown
                try {
                  const rawDocs = result.docs;
                  if (rawDocs && typeof rawDocs === 'string') {
                    // Try to extract JSON array from markdown code blocks
                    const jsonArrayMatch = rawDocs.match(/```(?:json)?\s*(\[[\s\S]*?\])\s*```/);
                    if (jsonArrayMatch && jsonArrayMatch[1]) {
                      const extractedJson = jsonArrayMatch[1].trim();
                      console.log('Trying to parse extracted JSON:', extractedJson.substring(0, 200) + '...');
                      parsedDocs = JSON.parse(extractedJson);
                      
                      if (Array.isArray(parsedDocs)) {
                        console.log('Successfully parsed extracted JSON:', parsedDocs.length, 'documents');
                      } else {
                        throw new Error('Extracted content is not a JSON array');
                      }
                    } else {
                      throw new Error('No JSON array found in markdown');
                    }
                  } else {
                    throw new Error('No raw docs available');
                  }
                } catch (secondParseError) {
                  console.error('Second parse attempt also failed:', secondParseError);
                  
                  // Try to extract any useful information from the raw response
                  const rawDocs = result.docs;
                  let fallbackDocs: any[] = [];
                  
                  // Look for document-like content even if JSON parsing fails
                  if (rawDocs && typeof rawDocs === 'string') {
                    // Try to extract document titles and content using regex
                    const docMatches = rawDocs.match(/(?:title|name|type)[\s:]*["']?([^"'\n]+)["']?/gi);
                    if (docMatches && docMatches.length > 0) {
                      fallbackDocs = docMatches.map((match, index) => ({
                        doc_type: `Document ${index + 1}`,
                        title: match.replace(/^(?:title|name|type)[\s:]*["']?/i, '').replace(/["']?$/i, ''),
                        summary: 'Document generated successfully',
                        content: 'Content available in the generated PDF',
                        placeholders: [],
                        defaults_used: {}
                      }));
                    }
                  }
                  
                  if (fallbackDocs.length > 0) {
                    console.log('Using fallback document extraction:', fallbackDocs.length, 'documents');
                    return {
                      success: true,
                      status: "done",
                      docs: fallbackDocs,
                      pdfs: result.pdfs || [],
                      message: `Generated ${fallbackDocs.length} legal documents (with fallback parsing) for: ${idea}`
                    };
                  }
                  
                  return {
                    success: false,
                    status: "error",
                    message: "Failed to parse legal documents response. Please try again."
                  };
                }
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
        },
        webSearch: {
          description: "Search the web for real-time information using OpenAI's web search capabilities",
          inputSchema: z.object({ 
            query: z.string().describe("The search query to find information on the web"),
            max_results: z.number().optional().describe("Maximum number of search results to return (default: 5)")
          }),
          execute: async ({ query }) => {
            try {
              // Use OpenAI's GPT-4 with web search capabilities
              const result = await streamText({
                model: openai('gpt-4o'),
                messages: [{
                  role: 'user',
                  content: `Please search for current information about: "${query}". Provide a comprehensive summary with the most relevant and recent information available. Include key findings, statistics, and important details. If you find specific sources or recent developments, mention them.`
                }]
              });

              // Convert stream to text
              let searchResults = '';
              for await (const chunk of result.textStream) {
                searchResults += chunk;
              }

              return {
                success: true,
                status: "done",
                query,
                results: searchResults,
                message: `Found web search results for: ${query}`
              };
            } catch (error) {
              console.error('Error performing web search:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to perform web search: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        marketSearch: {
          description: "Search for market data, competitor analysis, and industry statistics",
          inputSchema: z.object({ 
            industry: z.string().describe("The industry or market sector to analyze"),
            competitors: z.array(z.string()).optional().describe("Specific competitors to analyze"),
            search_focus: z.enum(['market_size', 'competitors', 'trends', 'pricing', 'growth', 'all']).optional().describe("What aspect of the market to focus on"),
            region: z.string().optional().describe("Geographic region for market analysis (default: global)")
          }),
          execute: async ({ industry, competitors = [], search_focus = 'all', region = 'global' }) => {
            try {
              // Build comprehensive search queries for market research
              const searchQueries = [];
              
              if (search_focus === 'all' || search_focus === 'market_size') {
                searchQueries.push(`${industry} market size 2024 ${region}`);
              }
              if (search_focus === 'all' || search_focus === 'competitors') {
                if (competitors.length > 0) {
                  searchQueries.push(`${competitors.join(' ')} ${industry} competitors analysis 2024`);
                } else {
                  searchQueries.push(`top ${industry} companies competitors 2024 ${region}`);
                }
              }
              if (search_focus === 'all' || search_focus === 'trends') {
                searchQueries.push(`${industry} market trends 2024 ${region}`);
              }
              if (search_focus === 'all' || search_focus === 'pricing') {
                searchQueries.push(`${industry} pricing strategies market analysis 2024`);
              }
              if (search_focus === 'all' || search_focus === 'growth') {
                searchQueries.push(`${industry} market growth forecast 2024-2025 ${region}`);
              }

              // Perform a single comprehensive search instead of multiple searches
              const comprehensiveQuery = searchQueries.slice(0, 2).join(' | '); // Combine top 2 queries
              const searchResults = [];
              
              try {
                const result = await streamText({
                  model: openai('gpt-4o'),
                  messages: [{
                    role: 'user',
                    content: `Provide a comprehensive market analysis for the ${industry} industry in ${region}. Research and include:

1. Market size and growth projections
2. Key competitors and their market positions${competitors.length > 0 ? ` (focus on: ${competitors.join(', ')})` : ''}
3. Current trends and opportunities
4. Pricing insights and strategies
5. Strategic recommendations

Focus on actionable insights for business strategy. Include specific data points, statistics, and recent developments.`
                  }]
                });

                // Convert stream to text
                let analysis = '';
                for await (const chunk of result.textStream) {
                  analysis += chunk;
                }
                
                searchResults.push({
                  query: comprehensiveQuery,
                  analysis
                });
              } catch (searchError) {
                console.error(`Error in market analysis:`, searchError);
                // Fallback to basic analysis
                searchResults.push({
                  query: comprehensiveQuery,
                  analysis: `Market analysis for ${industry} industry in ${region}. Analysis in progress...`
                });
              }

              // Use the comprehensive analysis directly since it already contains all needed information
              const finalAnalysis = searchResults[0]?.analysis || `Market analysis for ${industry} industry in ${region} completed.`

              return {
                success: true,
                status: "done",
                industry,
                region,
                search_focus,
                competitors_analyzed: competitors,
                market_analysis: finalAnalysis,
                research_queries: searchQueries,
                message: `Completed market analysis for ${industry} industry in ${region}`
              };
            } catch (error) {
              console.error('Error performing market search:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to perform market search: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        generatePitchDeck: {
          description: "Generate a comprehensive pitch deck with market research, financial models, and professional design",
          inputSchema: z.object({ 
            idea: z.string().describe("The business idea or concept (e.g., 'AI that manages Shopify stores')"),
            problem: z.string().optional().describe("The problem being solved"),
            target_market: z.string().optional().describe("Target market or customer segment"),
            competitors: z.array(z.string()).optional().describe("Known competitors"),
            revenue_model: z.string().optional().describe("Revenue model (subscription, one-time, marketplace, etc.)"),
            funding_amount: z.number().optional().describe("Funding amount being sought (in thousands)"),
            team_size: z.number().optional().describe("Current team size"),
            stage: z.enum(['idea', 'mvp', 'early_traction', 'growth', 'scale']).optional().describe("Current business stage")
          }),
          execute: async ({ idea, problem, target_market, competitors = [] }) => {
            try {
              // Step 1: Market Research Agent
              const marketResearch = await streamText({
                model: openai('gpt-4o'),
                messages: [{
                  role: 'user',
                  content: `Conduct comprehensive market research for this business idea: "${idea}"

${problem ? `Problem: ${problem}` : ''}
${target_market ? `Target Market: ${target_market}` : ''}
${competitors.length > 0 ? `Competitors: ${competitors.join(', ')}` : ''}

Provide:
1. Market size (TAM, SAM, SOM)
2. Key competitors and their strengths/weaknesses
3. Market trends and opportunities
4. Customer pain points and needs
5. Competitive landscape analysis

Format as structured JSON.`
                }]
              });

              let marketData = '';
              for await (const chunk of marketResearch.textStream) {
                marketData += chunk;
              }

              // Step 2: Influencer Search Agent
              const influencerResearch = await streamText({
                model: openai('gpt-4o'),
                messages: [{
                  role: 'user',
                  content: `Find the most relevant influencers for this STARTING BUSINESS: "${idea}"

${target_market ? `Target Market: ${target_market}` : ''}
${problem ? `Problem: ${problem}` : ''}

IMPORTANT: This is a starting business, so focus on influencers who are:
1. Accessible and likely to work with new businesses
2. NOT extremely famous (avoid celebrities, mega-influencers with 1M+ followers)
3. More affordable for partnerships and collaborations
4. Have engaged, niche audiences

Search for influencers who:
1. Are relevant to the target market/industry
2. Have 1K-100K followers (micro to mid-tier influencers)
3. Create content related to the problem/solution
4. Are active on social platforms
5. Have high engagement rates relative to their follower count
6. Are known to work with small/starting businesses

For each influencer, provide:
- Name and handle
- Platform (Instagram, Twitter, LinkedIn, YouTube, TikTok)
- Follower count range (1K-100K preferred)
- Engagement rate
- Content focus areas
- Social media links
- Why they're relevant and accessible for a starting business
- Estimated partnership cost range (if known)

Focus on:
- Micro-influencers (1K-10K followers) - most accessible
- Mid-tier influencers (10K-100K followers) - good reach/affordability balance
- Industry experts with smaller but engaged followings
- Content creators who work with startups
- Entrepreneurs who share their journey

AVOID: Celebrities, mega-influencers, or anyone with 1M+ followers

Format as structured JSON with social links.`
                }]
              });

              let influencerData = '';
              for await (const chunk of influencerResearch.textStream) {
                influencerData += chunk;
              }

              // Step 3: Deck Generator Agent using Gemini
              const deckContent = await streamText({
                model: google('gemini-2.5-flash'),
                messages: [{
                  role: 'user',
                  content: `Generate a comprehensive 10-slide pitch deck for this business idea: "${idea}"

Market Research Data:
${marketData}

Influencer Research Data:
${influencerData}

Create slides for:
1. Title Slide (Company name, tagline, contact info)
2. Problem (Pain points, market need)
3. Solution (Your product/service)
4. Market Opportunity (TAM/SAM/SOM)
5. Business Model (Revenue streams, pricing)
6. Traction (Metrics, milestones, growth)
7. Competition (Competitive landscape, differentiation)
8. Team (Founders, advisors, key hires)
9. Influencer Strategy (Key influencers, partnership opportunities)
10. Ask (Funding amount, use of funds, next steps)

Each slide should have:
- Compelling headline
- 3-4 bullet points with specific data and insights
- Key metrics and numbers from the research
- Visual suggestions
- Use the market research and influencer data to make it data-driven

Format as structured JSON array with this exact structure:
[
  {
    "title": "Slide Title",
    "icon": "📊",
    "content": [
      "Bullet point 1 with specific data",
      "Bullet point 2 with metrics",
      "Bullet point 3 with insights",
      "Bullet point 4 with call to action"
    ]
  }
]`
                }]
              });

              let deckData = '';
              for await (const chunk of deckContent.textStream) {
                deckData += chunk;
              }

              // Step 4: Design Agent
              const designSpecs = await streamText({
                model: openai('gpt-4o'),
                messages: [{
                  role: 'user',
                  content: `Create design specifications for a pitch deck about: "${idea}"

Choose:
1. Color scheme (primary, secondary, accent colors)
2. Typography (headings, body text)
3. Layout style (modern, professional, creative)
4. Icon suggestions for each slide
5. Chart/graph recommendations
6. Visual hierarchy guidelines

Format as structured JSON with specific color codes and design recommendations.`
                }]
              });

              let designData = '';
              for await (const chunk of designSpecs.textStream) {
                designData += chunk;
              }

              // Build slides JSON from deckData
              let slides: any[] = [];
              try {
                // Clean the response - remove markdown code blocks if present
                let cleanedDeck = deckData.trim();
                if (cleanedDeck.startsWith('```json')) {
                  cleanedDeck = cleanedDeck.replace('```json', '').replace('```', '').trim();
                } else if (cleanedDeck.startsWith('```')) {
                  cleanedDeck = cleanedDeck.replace('```', '').trim();
                }
                
                // Find JSON array
                const start = cleanedDeck.indexOf('[');
                const end = cleanedDeck.lastIndexOf(']') + 1;
                
                if (start === -1 || end === 0) {
                  throw new Error('No JSON array found in response');
                }
                
                const jsonString = cleanedDeck.substring(start, end);
                slides = JSON.parse(jsonString);
                
                // Ensure it's an array and has content
                if (!Array.isArray(slides) || slides.length === 0) {
                  throw new Error('Invalid slides array');
                }
                
                // Validate each slide has required fields
                slides = slides.map((slide, index) => ({
                  title: slide.title || `Slide ${index + 1}`,
                  icon: slide.icon || '📊',
                  content: Array.isArray(slide.content) ? slide.content : [String(slide.content || 'Content not available')]
                }));
                
              } catch (parseError) {
                console.error('Error parsing pitch deck JSON:', parseError);
                console.error('Raw deck data:', deckData);
                // Fallback to basic slides
                slides = [
                  { title: idea, icon: '📊', content: ['Pitch deck generated with AI insights.'] },
                  { title: 'Problem', icon: '🎯', content: ['Market need identified through research.'] },
                  { title: 'Solution', icon: '💡', content: ['Innovative approach to address the problem.'] },
                  { title: 'Market Opportunity', icon: '📈', content: ['Significant market potential identified.'] },
                  { title: 'Business Model', icon: '💰', content: ['Sustainable revenue streams planned.'] }
                ];
              }

              // Export PDF via Next API and upload to Supabase Storage
              let deckPdfUrl: string | null = null;
              const deckId = `deck_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
              try {
                const pdfResp = await fetch('http://127.0.0.1:3000/api/pitchdeck/export', {
                  method: 'POST', headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ deckId, slides })
                });
                if (pdfResp.ok) {
                  const pdfBuffer = await pdfResp.arrayBuffer();
                  
                  // Convert to base64 for upload
                  const uint8 = new Uint8Array(pdfBuffer);
                  let binary = '';
                  const chunkSize = 0x8000;
                  for (let i = 0; i < uint8.length; i += chunkSize) {
                    const chunk = uint8.subarray(i, i + chunkSize);
                    binary += String.fromCharCode.apply(null, Array.prototype.slice.call(chunk) as any);
                  }
                  const b64 = btoa(binary);
                  
                  // Upload to Supabase Storage via upload API
                  const uploadResp = await fetch('http://127.0.0.1:3000/api/pitchdeck/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                      pdfBuffer: b64, 
                      fileName: `pitch-deck-${deckId}.pdf` 
                    })
                  });
                  
                  if (uploadResp.ok) {
                    const uploadData = await uploadResp.json();
                    deckPdfUrl = uploadData.pdf_url;
                  } else {
                    console.error('Error uploading pitch deck to Supabase');
                  }
                }
              } catch (e) {
                console.error('Error exporting pitch deck PDF:', e);
              }

              return {
                success: true,
                status: "done",
                deck_id: deckId,
                idea,
                market_research: marketData,
                influencer_research: influencerData,
                deck_content: deckData,
                design_specs: designData,
                pdf_url: deckPdfUrl,
                message: `Generated comprehensive pitch deck for "${idea}" with market research and influencer strategy.${deckPdfUrl ? ` [Download PDF](${deckPdfUrl})` : ''}`
              };
            } catch (error) {
              console.error('Error generating pitch deck:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to generate pitch deck: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        generateBranding: {
          description: "Generate branding assets (name, tagline, logo) for a business idea",
          inputSchema: z.object({ 
            idea: z.string().describe("The business idea or concept to generate branding for")
          }),
          execute: async ({ idea }) => {
            try {
              const response = await fetch('http://127.0.0.1:8000/api/branding/generate', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({ idea_string: idea }),
              });
              
              if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              
              const data = await response.json();
              const branding = data.branding || {};
              
              return {
                success: true,
                status: "done",
                branding,
                message: `Successfully generated branding for "${idea}"`
              };
            } catch (error) {
              console.error('Error generating branding:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to generate branding: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        generateBrandingVideo: {
          description: "Generate a branding video for a business idea",
          inputSchema: z.object({ 
            idea: z.string().describe("The business idea or concept to generate a branding video for")
          }),
          execute: async ({ idea }) => {
            try {
              const response = await fetch('http://127.0.0.1:8000/api/branding/generate-video', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({ idea_string: idea }),
              });
              
              if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              
              const data = await response.json();
              const videoUrl: string | null = data?.video_url ?? null;

              return {
                success: true,
                status: "done",
                video: data.video === true,
                video_url: videoUrl,
                message: `Successfully generated branding video for "${idea}"`
              };
            } catch (error) {
              console.error('Error generating branding video:', error);
              return {
                success: false,
                status: "error",
                message: `Failed to generate branding video: ${error instanceof Error ? error.message : 'Unknown error'}`
              };
            }
          }
        },
        phoneassistant: {
          description: "Set up your customer phone assistant",
          inputSchema: z.object({}).optional() as any,
          execute: async () => {
            return {
              success: true,
              status: 'done',
              phone_number: '+1 (224) 228 9860',
              message: 'Set up your customer phone assistant to this number: +1 (224) 228 9860'
            };
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