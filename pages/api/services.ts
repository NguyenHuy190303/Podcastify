import { NextApiRequest, NextApiResponse } from 'next'
import { TTSService } from '@/types'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<TTSService[]>
) {
  if (req.method !== 'GET') {
    return res.status(405).json([])
  }

  try {
    // Mock TTS services data
    const services: TTSService[] = [
      {
        name: 'openai',
        displayName: 'OpenAI TTS',
        available: !!process.env.OPENAI_API_KEY,
        voices: [
          { name: 'alloy', description: 'Alloy - Giọng cân bằng, trung tính' },
          { name: 'echo', description: 'Echo - Giọng nam' },
          { name: 'fable', description: 'Fable - Giọng Anh' },
          { name: 'onyx', description: 'Onyx - Giọng nam trầm' },
          { name: 'nova', description: 'Nova - Giọng nữ' },
          { name: 'shimmer', description: 'Shimmer - Giọng nữ mềm mại' },
        ],
      },
      {
        name: 'google',
        displayName: 'Google Cloud TTS',
        available: !!process.env.GOOGLE_CLOUD_CREDENTIALS,
        voices: [
          { name: 'en-US-Wavenet-A', description: 'Wavenet A - Giọng nữ Mỹ', gender: 'female' },
          { name: 'en-US-Wavenet-B', description: 'Wavenet B - Giọng nam Mỹ', gender: 'male' },
          { name: 'en-US-Wavenet-C', description: 'Wavenet C - Giọng nữ Mỹ', gender: 'female' },
          { name: 'en-US-Wavenet-D', description: 'Wavenet D - Giọng nam Mỹ', gender: 'male' },
          { name: 'vi-VN-Wavenet-A', description: 'Wavenet A - Giọng nữ Việt Nam', gender: 'female' },
          { name: 'vi-VN-Wavenet-B', description: 'Wavenet B - Giọng nam Việt Nam', gender: 'male' },
        ],
      },
    ]

    // Filter only available services
    const availableServices = services.filter(service => service.available)

    res.status(200).json(availableServices)
  } catch (error) {
    console.error('Error loading services:', error)
    res.status(500).json([])
  }
}
