import { createClient } from '@/lib/supabase'

export interface UploadResult {
  url: string
  path: string
  error?: string
}

export async function uploadImageToStorage(
  file: File,
  bucketName: string = 'product_images'
): Promise<UploadResult> {
  try {
    const supabase = createClient()
    
    // Generate unique filename
    const fileExt = file.name.split('.').pop()
    const fileName = `${Date.now()}-${Math.random().toString(36).substring(2)}.${fileExt}`
    const filePath = `products/${fileName}`
    
    // Upload file to Supabase storage
    const { data, error } = await supabase.storage
      .from(bucketName)
      .upload(filePath, file, {
        cacheControl: '3600',
        upsert: false
      })
    
    if (error) {
      throw new Error(`Upload failed: ${error.message}`)
    }
    
    // Get public URL
    const { data: urlData } = supabase.storage
      .from(bucketName)
      .getPublicUrl(filePath)
    
    return {
      url: urlData.publicUrl,
      path: filePath
    }
  } catch (error) {
    return {
      url: '',
      path: '',
      error: error instanceof Error ? error.message : 'Unknown upload error'
    }
  }
}

export async function uploadMultipleImages(
  files: FileList,
  bucketName: string = 'product_images'
): Promise<UploadResult[]> {
  const uploadPromises = Array.from(files).map(file => 
    uploadImageToStorage(file, bucketName)
  )
  
  return Promise.all(uploadPromises)
}
