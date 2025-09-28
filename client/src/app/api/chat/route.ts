import { google } from '@ai-sdk/google';
import { streamText, convertToModelMessages, UIMessage, stepCountIs } from 'ai';
import { z } from 'zod';

// IMPORTANT! Set the runtime to edge
export const runtime = 'edge';

export async function POST(req: Request) {
  try {
    const { messages }: { messages: UIMessage[] } = await req.json();

    const result = streamText({
      model: google('gemini-2.5-flash'),
      system: `You are an AI assistant that helps users set up e-commerce stores and manage business workflows. 

You have access to several tools that can be chained together to complete complex tasks:

🏪 setupStore - Creates and configures a Shopify store
💳 configurePayment - Sets up payment methods for the store
📦 setupInventory - Creates sample products and sets up inventory
⚖️ generateLegalDocs - Generates comprehensive legal documents (privacy policy, terms of use, NDA) for any business idea

When a user asks you to:
- Set up a store → Use setupStore first, then generateLegalDocs
- Create a complete e-commerce setup → Chain all tools: setupStore → generateLegalDocs → configurePayment → setupInventory
- Generate legal documents for any business idea → Use generateLegalDocs
- Configure payments → Use configurePayment
- Set up inventory → Use setupInventory

Always explain what you're doing and show progress. Use the tools in logical sequence and provide clear feedback about each step. If a user mentions a store name, use it in the setupStore tool. Be helpful and proactive in suggesting next steps.`,
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
                
                // Remove markdown code block markers
                if (cleanedDocs.startsWith('```json')) {
                  cleanedDocs = cleanedDocs.replace(/^```json\s*/, '').replace(/\s*```$/, '');
                } else if (cleanedDocs.startsWith('```')) {
                  cleanedDocs = cleanedDocs.replace(/^```\s*/, '').replace(/\s*```$/, '');
                }
                
                // Remove any leading/trailing backticks
                cleanedDocs = cleanedDocs.replace(/^`+|`+$/g, '');
                
                // Validate that we have a valid JSON array
                if (!cleanedDocs.startsWith('[') && !cleanedDocs.startsWith('{')) {
                  throw new Error('Response is not valid JSON');
                }
                
                parsedDocs = JSON.parse(cleanedDocs);
                
                // Ensure it's an array
                if (!Array.isArray(parsedDocs)) {
                  throw new Error('Response is not a JSON array');
                }
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
        }
      },
    });

    return result.toUIMessageStreamResponse();
  } catch (error) {
    console.error('Chat API error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}