'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  SpeakerWaveIcon,
  Cog6ToothIcon,
  PlayIcon,
  ArrowLeftIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'
import { ConversionJob, TTSService } from '@/types'

interface ConversionSettingsProps {
  job: ConversionJob
  onStart: () => void
  onBack: () => void
}

export default function ConversionSettings({ job, onStart, onBack }: ConversionSettingsProps) {
  const [services, setServices] = useState<TTSService[]>([])
  const [selectedService, setSelectedService] = useState('openai')
  const [selectedVoice, setSelectedVoice] = useState('')
  const [speed, setSpeed] = useState(1.0)
  const [settings, setSettings] = useState({
    skipToc: true,
    skipAcknowledgments: true,
    skipCopyright: true,
    skipIndex: true,
  })
  const [starting, setStarting] = useState(false)

  useEffect(() => {
    loadServices()
  }, [])

  const loadServices = async () => {
    try {
      const response = await fetch('/api/services')
      const data = await response.json()
      setServices(data)
    } catch (error) {
      console.error('Error loading services:', error)
      toast.error('Không thể tải danh sách dịch vụ TTS')
    }
  }

  const handleStart = async () => {
    setStarting(true)
    
    try {
      const response = await fetch('/api/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jobId: job.id,
          settings: {
            ttsService: selectedService,
            voice: selectedVoice,
            speed,
            ...settings,
          },
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to start conversion')
      }

      toast.success('Bắt đầu chuyển đổi!')
      onStart()
    } catch (error) {
      console.error('Conversion start error:', error)
      toast.error('Lỗi khi bắt đầu chuyển đổi')
    } finally {
      setStarting(false)
    }
  }

  const currentService = services.find(s => s.name === selectedService)

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Book Info */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <InformationCircleIcon className="h-5 w-5 mr-2 text-primary-500" />
          Thông tin sách
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-600">Tên file:</span>
            <p className="text-gray-800">{job.filename}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">Tiêu đề:</span>
            <p className="text-gray-800">{job.metadata?.title || 'Không xác định'}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">Tác giả:</span>
            <p className="text-gray-800">{job.metadata?.author || 'Không xác định'}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">Kích thước:</span>
            <p className="text-gray-800">{(job.fileSize / 1024 / 1024).toFixed(1)} MB</p>
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-6 flex items-center">
          <Cog6ToothIcon className="h-5 w-5 mr-2 text-primary-500" />
          Cài đặt chuyển đổi
        </h3>

        <div className="space-y-6">
          {/* TTS Service */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dịch vụ Text-to-Speech
            </label>
            <select
              value={selectedService}
              onChange={(e) => {
                setSelectedService(e.target.value)
                setSelectedVoice('')
              }}
              className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
            >
              {services.map((service) => (
                <option key={service.name} value={service.name}>
                  {service.displayName}
                </option>
              ))}
            </select>
          </div>

          {/* Voice Selection */}
          {currentService && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Giọng đọc
              </label>
              <select
                value={selectedVoice}
                onChange={(e) => setSelectedVoice(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
              >
                <option value="">Giọng mặc định</option>
                {currentService.voices.map((voice) => (
                  <option key={voice.name} value={voice.name}>
                    {voice.description}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Speed Control */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tốc độ đọc: {speed}x
            </label>
            <input
              type="range"
              min="0.5"
              max="2.0"
              step="0.1"
              value={speed}
              onChange={(e) => setSpeed(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Chậm (0.5x)</span>
              <span>Bình thường (1.0x)</span>
              <span>Nhanh (2.0x)</span>
            </div>
          </div>

          {/* Content Filtering */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Lọc nội dung
            </label>
            <div className="space-y-3">
              {[
                { key: 'skipToc', label: 'Bỏ qua mục lục' },
                { key: 'skipAcknowledgments', label: 'Bỏ qua lời cảm ơn' },
                { key: 'skipCopyright', label: 'Bỏ qua trang bản quyền' },
                { key: 'skipIndex', label: 'Bỏ qua chỉ mục' },
              ].map((option) => (
                <label key={option.key} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={settings[option.key as keyof typeof settings]}
                    onChange={(e) => setSettings(prev => ({
                      ...prev,
                      [option.key]: e.target.checked
                    }))}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <span className="ml-3 text-sm text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-between">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onBack}
          className="btn-secondary flex items-center space-x-2"
        >
          <ArrowLeftIcon className="h-4 w-4" />
          <span>Quay lại</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleStart}
          disabled={starting}
          className="btn-primary flex items-center space-x-2 disabled:opacity-50"
        >
          {starting ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Đang bắt đầu...</span>
            </>
          ) : (
            <>
              <PlayIcon className="h-4 w-4" />
              <span>Bắt đầu chuyển đổi</span>
            </>
          )}
        </motion.button>
      </div>
    </motion.div>
  )
}
