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
📄 generateDocs - Generates legal documents (privacy policy, terms of service, etc.)
💳 configurePayment - Sets up payment methods for the store
📦 setupInventory - Creates sample products and sets up inventory

When a user asks you to:
- Set up a store → Use setupStore first, then generateDocs
- Create a complete e-commerce setup → Chain all tools: setupStore → generateDocs → configurePayment → setupInventory
- Generate documents for an existing store → Use generateDocs
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
        generateDocs: {
          description: "Generate legal documents for the store",
          inputSchema: z.object({ 
            storeUrl: z.string().describe("The URL of the store"),
            docTypes: z.array(z.string()).optional().describe("Types of documents to generate")
          }),
          execute: async ({ storeUrl, docTypes = ["privacy", "terms"] }) => {
            // Simulate API call delay
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            return { 
              success: true,
              status: "done", 
              docs: docTypes.map((type: string) => `${type}.pdf`),
              message: `Generated ${docTypes.length} legal documents for ${storeUrl}`
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
        }
      },
      onStepFinish: async (step) => {
        console.log('Step finished:', {
          toolCalls: step.toolCalls,
          toolResults: step.toolResults,
          finishReason: step.finishReason
        });
      }
    });

    return result.toUIMessageStreamResponse();
  } catch (error) {
    console.error('Chat API error:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}