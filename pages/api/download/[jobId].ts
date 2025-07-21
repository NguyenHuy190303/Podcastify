import { NextApiRequest, NextApiResponse } from 'next'
import fs from 'fs'
import path from 'path'

// Mock job storage (in production, use a database)
const jobs = new Map()

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { jobId } = req.query

    if (!jobId || typeof jobId !== 'string') {
      return res.status(400).json({ error: 'Invalid job ID' })
    }

    const job = jobs.get(jobId)
    
    if (!job) {
      return res.status(404).json({ error: 'Job not found' })
    }

    if (job.status !== 'completed') {
      return res.status(400).json({ error: 'Conversion not completed' })
    }

    // In a real implementation, you would serve the actual MP3 file
    // For demo purposes, we'll create a mock response
    const filename = `${job.filename?.replace('.pdf', '') || 'audiobook'}.mp3`
    
    // Set headers for file download
    res.setHeader('Content-Type', 'audio/mpeg')
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`)
    res.setHeader('Cache-Control', 'no-cache')

    // For demo, return a small mock MP3 file or redirect to a sample
    // In production, you would stream the actual generated MP3 file
    const mockMp3Data = Buffer.from('Mock MP3 data - replace with actual file')
    
    res.status(200).send(mockMp3Data)
  } catch (error) {
    console.error('Download error:', error)
    res.status(500).json({ error: 'Failed to download file' })
  }
}
