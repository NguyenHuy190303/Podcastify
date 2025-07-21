import { NextApiRequest, NextApiResponse } from 'next'
import { ConversionJob } from '@/types'

// Mock job storage (in production, use a database)
const jobs = new Map()

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ConversionJob | { error: string }>
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

    res.status(200).json(job)
  } catch (error) {
    console.error('Status check error:', error)
    res.status(500).json({ error: 'Failed to get job status' })
  }
}
