import { NextApiRequest, NextApiResponse } from 'next'
import { ConversionResponse, ConversionSettings } from '@/types'

// Mock job storage (in production, use a database)
const jobs = new Map()

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ConversionResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      success: false, 
      message: 'Method not allowed' 
    })
  }

  try {
    const { jobId, settings }: { jobId: string; settings: ConversionSettings } = req.body

    if (!jobId) {
      return res.status(400).json({ 
        success: false, 
        message: 'Job ID is required' 
      })
    }

    // Validate settings
    if (!settings.ttsService || !['openai', 'google'].includes(settings.ttsService)) {
      return res.status(400).json({ 
        success: false, 
        message: 'Invalid TTS service' 
      })
    }

    // Check API keys
    if (settings.ttsService === 'openai' && !process.env.OPENAI_API_KEY) {
      return res.status(400).json({ 
        success: false, 
        message: 'OpenAI API key not configured' 
      })
    }

    if (settings.ttsService === 'google' && !process.env.GOOGLE_CLOUD_CREDENTIALS) {
      return res.status(400).json({ 
        success: false, 
        message: 'Google Cloud credentials not configured' 
      })
    }

    // Store job settings
    jobs.set(jobId, {
      id: jobId,
      settings,
      status: 'processing',
      progress: 0,
      startedAt: new Date().toISOString(),
    })

    // Start background processing (in production, use a queue)
    processConversion(jobId, settings)

    res.status(200).json({ 
      success: true, 
      message: 'Conversion started successfully',
      jobId 
    })
  } catch (error) {
    console.error('Conversion start error:', error)
    res.status(500).json({ 
      success: false, 
      message: 'Failed to start conversion' 
    })
  }
}

// Mock conversion process
async function processConversion(jobId: string, settings: ConversionSettings) {
  try {
    const job = jobs.get(jobId)
    if (!job) return

    // Simulate conversion steps
    const steps = [
      { progress: 10, message: 'Extracting text from PDF...', delay: 1000 },
      { progress: 25, message: 'Filtering content...', delay: 2000 },
      { progress: 40, message: 'Detecting chapters...', delay: 1500 },
      { progress: 55, message: 'Preparing text for TTS...', delay: 1000 },
      { progress: 70, message: 'Converting text to speech...', delay: 5000 },
      { progress: 85, message: 'Combining audio chunks...', delay: 2000 },
      { progress: 95, message: 'Exporting MP3...', delay: 1500 },
      { progress: 100, message: 'Completed!', delay: 500 },
    ]

    for (const step of steps) {
      await new Promise(resolve => setTimeout(resolve, step.delay))
      
      job.progress = step.progress
      job.message = step.message
      
      if (step.progress === 100) {
        job.status = 'completed'
        job.completedAt = new Date().toISOString()
        job.outputFile = `/tmp/${jobId}.mp3`
      }
      
      jobs.set(jobId, job)
    }
  } catch (error) {
    console.error('Conversion error:', error)
    const job = jobs.get(jobId)
    if (job) {
      job.status = 'failed'
      job.error = 'Conversion failed'
      jobs.set(jobId, job)
    }
  }
}
