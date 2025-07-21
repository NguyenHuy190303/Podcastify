import { NextApiRequest, NextApiResponse } from 'next'
import formidable from 'formidable'
import fs from 'fs'
import path from 'path'
import { ConversionJob, UploadResponse } from '@/types'
import { generateJobId } from '@/lib/utils'

// Disable default body parser
export const config = {
  api: {
    bodyParser: false,
  },
}

// Simple PDF metadata extraction (placeholder)
const extractPDFMetadata = async (filePath: string) => {
  try {
    // In a real implementation, you would use a PDF parsing library
    // For now, return mock metadata
    return {
      title: 'Sample Book Title',
      author: 'Sample Author',
      subject: 'Sample Subject',
      pageCount: 100,
    }
  } catch (error) {
    console.error('Error extracting PDF metadata:', error)
    return {
      title: 'Unknown Title',
      author: 'Unknown Author',
      pageCount: 0,
    }
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<UploadResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' })
  }

  try {
    // Parse the uploaded file
    const form = formidable({
      maxFileSize: 50 * 1024 * 1024, // 50MB
      uploadDir: '/tmp',
      keepExtensions: true,
    })

    const [fields, files] = await form.parse(req)
    const file = Array.isArray(files.file) ? files.file[0] : files.file

    if (!file) {
      return res.status(400).json({ success: false, error: 'No file uploaded' })
    }

    // Validate file type
    if (!file.originalFilename?.toLowerCase().endsWith('.pdf')) {
      return res.status(400).json({ success: false, error: 'Only PDF files are allowed' })
    }

    // Generate job ID
    const jobId = generateJobId()
    
    // Extract metadata
    const metadata = await extractPDFMetadata(file.filepath)

    // Create job object
    const job: ConversionJob = {
      id: jobId,
      filename: file.originalFilename || 'unknown.pdf',
      fileSize: file.size || 0,
      status: 'uploaded',
      progress: 0,
      metadata,
      createdAt: new Date().toISOString(),
    }

    // Store file info (in production, you'd save to database)
    // For now, we'll store in memory or temporary storage
    
    res.status(200).json({ success: true, job })
  } catch (error) {
    console.error('Upload error:', error)
    res.status(500).json({ 
      success: false, 
      error: 'Upload failed. Please try again.' 
    })
  }
}
