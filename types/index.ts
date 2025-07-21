export interface ConversionJob {
  id: string
  filename: string
  fileSize: number
  status: 'uploaded' | 'processing' | 'completed' | 'failed'
  progress: number
  message?: string
  error?: string
  metadata?: {
    title?: string
    author?: string
    subject?: string
    pageCount?: number
  }
  settings?: ConversionSettings
  createdAt: string
  completedAt?: string
  outputFile?: string
}

export interface ConversionSettings {
  ttsService: 'openai' | 'google'
  voice?: string
  speed: number
  skipToc: boolean
  skipAcknowledgments: boolean
  skipCopyright: boolean
  skipIndex: boolean
}

export interface TTSService {
  name: string
  displayName: string
  voices: Voice[]
  available: boolean
}

export interface Voice {
  name: string
  description: string
  language?: string
  gender?: 'male' | 'female' | 'neutral'
}

export interface ProgressUpdate {
  jobId: string
  progress: number
  message: string
  status: 'processing' | 'completed' | 'failed'
  details?: string
}

export interface AudioMetadata {
  title: string
  author: string
  album?: string
  year?: string
  genre: string
  duration?: number
}

export interface UploadResponse {
  success: boolean
  job?: ConversionJob
  error?: string
}

export interface ConversionResponse {
  success: boolean
  message: string
  jobId?: string
  error?: string
}
