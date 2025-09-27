"use client";

import * as React from "react";
import { useState, useEffect, useRef, useMemo } from "react";
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  ArrowUp,
  Loader2,
  Paperclip,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ToolCallProgress, ToolCall } from '@/components/ToolCallProgress';

interface ChatProps {
  className?: string;
}

const MarkdownContent = ({ children }: { children: string }) => {
  return (
    <div className="markdown-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => <h1 className="text-lg font-semibold mt-4 mb-2 first:mt-0 text-gray-900">{children}</h1>,
          h2: ({ children }) => <h2 className="text-base font-semibold mt-3 mb-2 first:mt-0 text-gray-900">{children}</h2>,
          h3: ({ children }) => <h3 className="text-sm font-semibold mt-3 mb-1 first:mt-0 text-gray-800">{children}</h3>,
          h4: ({ children }) => <h4 className="text-sm font-medium mt-2 mb-1 first:mt-0 text-gray-800">{children}</h4>,
          h5: ({ children }) => <h5 className="text-sm font-medium mt-2 mb-1 first:mt-0 text-gray-800">{children}</h5>,
          h6: ({ children }) => <h6 className="text-sm font-medium mt-2 mb-1 first:mt-0 text-gray-800">{children}</h6>,
          p: ({ children }) => <p className="my-2 first:mt-0 last:mb-0 leading-relaxed text-gray-700">{children}</p>,
          ul: ({ children }) => <ul className="my-2 space-y-1 list-disc pl-4">{children}</ul>,
          ol: ({ children }) => <ol className="my-2 space-y-1 list-decimal pl-4">{children}</ol>,
          li: ({ children }) => <li className="leading-relaxed text-gray-700">{children}</li>,
          strong: ({ children }) => <strong className="font-semibold text-gray-900">{children}</strong>,
          em: ({ children }) => <em className="italic text-gray-700">{children}</em>,
          code: ({ children, className }) => {
            const isInline = !className;
            return isInline ? (
              <code className="bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded text-sm font-mono">{children}</code>
            ) : (
              <code className={className}>{children}</code>
            );
          },
          pre: ({ children }) => (
            <pre className="bg-gray-100 border border-gray-200 p-3 rounded-lg overflow-x-auto my-3">
              {children}
            </pre>
          ),
          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-gray-800 underline"
            >
              {children}
            </a>
          ),
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-gray-300 pl-4 my-3 italic text-gray-600">
              {children}
            </blockquote>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
};


export default function ChatPage({ className }: ChatProps) {
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [files, setFiles] = useState<FileList | undefined>(undefined);
  const [toolCalls, setToolCalls] = useState<ToolCall[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const transport = useMemo(() => new DefaultChatTransport({
    api: '/api/chat',
    fetch: async (url, init) => {
      const body = JSON.parse((init?.body as string) || '{}');
      return fetch(url, {
        ...init,
        body: JSON.stringify({
          ...body,
          model: 'gemini-1.5-flash',
        }),
      });
    },
  }), []);

  // Build options as 'any' to allow onToolResult even if type definitions lag behind
  const chatOptions: any = {
    transport,
    onToolCall: ({ toolCall }: any) => {
      console.log('Tool call started:', { toolCall });
      const { toolCallId, toolName } = toolCall;
      // Add new tool call to state or update existing one
      setToolCalls((prev) => {
        const existingIndex = prev.findIndex((tc) => tc.id === toolCallId);
        if (existingIndex >= 0) {
          return prev.map((tc, index) =>
            index === existingIndex
              ? { ...tc, status: 'running' as const, startTime: Date.now() }
              : tc
          );
        }
        // Mark any currently running tool as completed before adding the next one
        const progressed = prev.map((tc) =>
          tc.status === 'running'
            ? { ...tc, status: 'completed' as const, endTime: Date.now() }
            : tc
        );

        const newToolCall: ToolCall = {
          id: toolCallId || `tool-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
          toolName,
          status: 'running',
          startTime: Date.now(),
        };
        return [...progressed, newToolCall];
      });
    },
    onToolResult: ({ toolCallId, result }: any) => {
      console.log('onToolResult received:', { toolCallId, result });
      setToolCalls((prev) =>
        prev.map((tc) =>
          tc.id === toolCallId
            ? { ...tc, status: 'completed' as const, result, endTime: Date.now() }
            : tc
        )
      );
    },
    onError: (error: any) => {
      console.error('Chat error:', error);
      setToolCalls((prev) =>
        prev.map((tc) =>
          tc.status === 'running'
            ? { ...tc, status: 'error' as const, endTime: Date.now() }
            : tc
        )
      );
    },
  };

  const { messages, sendMessage, status } = useChat(chatOptions);

  // Reset thinking state when status changes
  useEffect(() => {
    if (status === 'ready') {
      setIsThinking(false);
      // Ensure any remaining running tool (usually the last one) is marked completed
      setToolCalls((prev) =>
        prev.map((tc) =>
          tc.status === 'running'
            ? { ...tc, status: 'completed' as const, endTime: Date.now() }
            : tc
        )
      );
    }
  }, [status]);

  // Clear tool calls when starting a new conversation
  useEffect(() => {
    if (messages.length === 0) {
      setToolCalls([]);
    }
  }, [messages.length]);

  // Debug tool calls state changes
  useEffect(() => {
    console.log('Tool calls state updated:', toolCalls);
  }, [toolCalls]);

  // Track processed tool results to avoid duplicate updates
  const processedToolResultsRef = useRef<Set<string>>(new Set());

  // Monitor messages for tool call completions (per tool) by scanning parts as they arrive
  useEffect(() => {
    const last = messages[messages.length - 1];
    if (!last) return;
    const parts = (last as any).parts || [];
    parts.forEach((part: any) => {
      if (part?.type === 'tool-result' && part.toolCallId && !processedToolResultsRef.current.has(part.toolCallId)) {
        processedToolResultsRef.current.add(part.toolCallId);
        setToolCalls((prev) =>
          prev.map((tc) =>
            tc.id === part.toolCallId
              ? { ...tc, status: 'completed' as const, result: part.result, endTime: Date.now() }
              : tc
          )
        );
      }
    });
  }, [messages]);

  // Auto-scroll to bottom when messages change or streaming
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, status]);

  const hasMessages = messages.length > 0;

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() && (!files || files.length === 0)) return;
    
    setIsThinking(true);
    const fileParts = files && files.length > 0
      ? []
      : [];
    await sendMessage({
      role: 'user',
      parts: [
        { type: 'text', text: input },
        ...fileParts,
      ],
    });
    setInput('');
  };

  return (
    <div className={cn("h-screen flex flex-col overflow-hidden", className)}>
      {!hasMessages ? (
        <div className="flex-1 flex flex-col items-center justify-center px-4 py-8 overflow-y-auto">
          {/* Initial prompt area when no messages */}
          <div className="w-full max-w-2xl mx-auto">
            {/* Greeting */}
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-3">
                How can I help you today?
              </h1>
              <p className="text-gray-600 text-lg mb-6">
                Ask me anything about your business, data analysis, or get general assistance.
              </p>
              
              {/* Example prompts for tool calling */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                <button
                  onClick={() => setInput("Set up a new Shopify store called 'My Fashion Store' and generate all the legal documents")}
                  className="p-3 text-left bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">🏪 Set up a store</div>
                  <div className="text-sm text-gray-600">Create store + generate docs</div>
                </button>
                <button
                  onClick={() => setInput("Create a complete e-commerce setup with inventory and payment configuration")}
                  className="p-3 text-left bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">🛒 Full setup</div>
                  <div className="text-sm text-gray-600">Store + docs + payments + inventory</div>
                </button>
              </div>
            </div>

            {/* Chat Input Container */}
            <div className="bg-gray-50 rounded-2xl border border-gray-200 shadow-sm p-6">
              <form onSubmit={onSubmit} className="space-y-4">
                {/* File Upload */}
                <input
                  type="file"
                  accept="image/*,application/pdf"
                  className="hidden"
                  onChange={(event) => {
                    if (event.target.files) {
                      setFiles(event.target.files);
                    }
                  }}
                  multiple
                  ref={fileInputRef}
                />
                
                {/* Selected Files Display */}
                {files && files.length > 0 && (
                  <div className="space-y-2">
                    <div className="text-sm font-medium text-gray-700">Selected files:</div>
                    <div className="flex flex-wrap gap-2">
                      {Array.from(files).map((file, index) => (
                        <div
                          key={index}
                          className="flex items-center gap-2 bg-gray-100 text-gray-800 px-3 py-1 rounded-lg text-sm"
                        >
                          <span className="truncate max-w-32">{file.name}</span>
                          <button
                            type="button"
                            onClick={() => {
                              const dt = new DataTransfer();
                              Array.from(files).forEach((f, i) => {
                                if (i !== index) dt.items.add(f);
                              });
                              setFiles(dt.files.length > 0 ? dt.files : undefined);
                            }}
                            className="text-gray-600 hover:text-gray-800"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Message Input */}
                <div className="space-y-3">
                  <Input
                    type="text"
                    placeholder="e.g., 'Analyze my Shopify sales data' or 'Help me with business insights'"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    disabled={status === 'streaming'}
                    className="border-0 bg-transparent p-0 text-lg placeholder:text-gray-500 focus-visible:ring-0 focus-visible:ring-offset-0 h-10 shadow-none"
                  />
                </div>

                {/* Tools and Send */}
                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center gap-2">
                    {/* File Upload Button */}
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => fileInputRef.current?.click()}
                      className="flex items-center gap-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100"
                    >
                      <Paperclip className="h-4 w-4" />
                      Attach files
                    </Button>
                  </div>

                  {/* Send Button */}
                  <Button
                    type="submit"
                    size="sm"
                    disabled={(!input.trim() && (!files || files.length === 0)) || status === 'streaming'}
                    className="h-8 w-8 p-0 rounded-full bg-gray-900 text-white hover:bg-gray-800 disabled:bg-gray-300"
                  >
                    {status === 'streaming' ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <ArrowUp className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex-1 flex flex-col min-h-0">
          {/* Messages Area - Scrollable */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
            {messages.map((message) => (
              <div
                key={message.id}
                className={cn(
                  "flex gap-3",
                  message.role === 'user' ? "justify-end" : "justify-start"
                )}
              >
                <div
                  className={cn(
                    "max-w-[80%] rounded-lg px-4 py-2",
                    message.role === 'user'
                      ? "bg-gray-900 text-white"
                      : "bg-gray-50 text-gray-900 border border-gray-200"
                  )}
                >
                  {(message.parts ?? []).map((part: { type: string; text?: string }, i: number) => {
                    if (part?.type !== 'text') return <React.Fragment key={i}></React.Fragment>;
                    const text = (part as { type: 'text'; text: string }).text;
                    return message.role === 'user' ? (
                      <p key={i} className="text-sm whitespace-pre-wrap">{text}</p>
                    ) : (
                      <MarkdownContent key={i}>{text}</MarkdownContent>
                    );
                  })}
                </div>

              </div>
            ))}

            {/* Tool Call Progress */}
            {toolCalls.length > 0 && (
              <div className="flex gap-3 justify-start">
                <div className="bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 max-w-[80%]">
                  <ToolCallProgress toolCalls={toolCalls} />
                </div>
              </div>
            )}

            {/* Thinking/Loading Indicator */}
            {(isThinking || status === 'streaming') && toolCalls.length === 0 && (
              <div className="flex gap-3 justify-start">
                <div className="bg-gray-50 border border-gray-200 rounded-lg px-4 py-2">
                  <div className="flex items-center gap-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                    <span className="text-sm text-gray-700">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
            
            {/* Invisible element for auto-scrolling */}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area - Fixed at bottom */}
          <div className="flex-shrink-0 border-t border-gray-200 bg-white p-4 pb-6">
            <form onSubmit={onSubmit} className="space-y-3">
              {/* File Upload */}
              <input
                type="file"
                accept="image/*,application/pdf"
                className="hidden"
                onChange={(event) => {
                  if (event.target.files) {
                    setFiles(event.target.files);
                  }
                }}
                multiple
                ref={fileInputRef}
              />
              
              {/* Selected Files Display */}
              {files && files.length > 0 && (
                <div className="space-y-2">
                  <div className="text-sm font-medium text-gray-700">Selected files:</div>
                  <div className="flex flex-wrap gap-2">
                    {Array.from(files).map((file, index) => (
                      <div
                        key={index}
                        className="flex items-center gap-2 bg-gray-100 text-gray-800 px-3 py-1 rounded-lg text-sm"
                      >
                        <span className="truncate max-w-32">{file.name}</span>
                        <button
                          type="button"
                          onClick={() => {
                            const dt = new DataTransfer();
                            Array.from(files).forEach((f, i) => {
                              if (i !== index) dt.items.add(f);
                            });
                            setFiles(dt.files.length > 0 ? dt.files : undefined);
                          }}
                          className="text-gray-600 hover:text-gray-800"
                        >
                          <X className="h-3 w-3" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="flex gap-2 items-center">
                {/* File Upload Button */}
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => fileInputRef.current?.click()}
                  className="border-gray-300 text-gray-600 hover:bg-gray-50"
                >
                  <Paperclip className="h-4 w-4" />
                </Button>

                <Input
                  placeholder="Type your message..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={status === 'streaming'}
                  className="flex-1 border-gray-200 focus:border-gray-400 focus:ring-gray-400"
                />
                
                <Button
                  type="submit"
                  disabled={(!input.trim() && (!files || files.length === 0)) || status === 'streaming'}
                  className="bg-gray-900 hover:bg-gray-800 text-white"
                >
                  {status === 'streaming' ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <ArrowUp className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}