'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  SpeakerWaveIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface ProgressTrackerProps {
  jobId: string
  onComplete: () => void
}

interface ProgressData {
  progress: number
  message: string
  status: 'processing' | 'completed' | 'failed'
  details?: string[]
}

export default function ProgressTracker({ jobId, onComplete }: ProgressTrackerProps) {
  const [progress, setProgress] = useState<ProgressData>({
    progress: 0,
    message: 'Đang khởi tạo...',
    status: 'processing'
  })
  const [details, setDetails] = useState<string[]>([])

  useEffect(() => {
    // Simulate progress updates (in real app, this would be WebSocket)
    const progressSteps = [
      { progress: 10, message: 'Đang trích xuất văn bản từ PDF...', delay: 1000 },
      { progress: 25, message: 'Đang lọc nội dung...', delay: 2000 },
      { progress: 40, message: 'Đang phát hiện chương...', delay: 1500 },
      { progress: 55, message: 'Đang chuẩn bị văn bản cho TTS...', delay: 1000 },
      { progress: 70, message: 'Đang chuyển đổi văn bản thành giọng nói...', delay: 5000 },
      { progress: 85, message: 'Đang kết hợp các đoạn audio...', delay: 2000 },
      { progress: 95, message: 'Đang xuất file MP3...', delay: 1500 },
      { progress: 100, message: 'Hoàn thành!', delay: 500 },
    ]

    let currentStep = 0
    const updateProgress = () => {
      if (currentStep < progressSteps.length) {
        const step = progressSteps[currentStep]
        setProgress(prev => ({
          ...prev,
          progress: step.progress,
          message: step.message,
          status: step.progress === 100 ? 'completed' : 'processing'
        }))
        
        setDetails(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${step.message}`])
        
        if (step.progress === 100) {
          setTimeout(onComplete, 1000)
        } else {
          setTimeout(() => {
            currentStep++
            updateProgress()
          }, step.delay)
        }
      }
    }

    updateProgress()
  }, [jobId, onComplete])

  const getStatusIcon = () => {
    switch (progress.status) {
      case 'completed':
        return <CheckCircleIcon className="h-8 w-8 text-green-500" />
      case 'failed':
        return <ExclamationCircleIcon className="h-8 w-8 text-red-500" />
      default:
        return (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            <SpeakerWaveIcon className="h-8 w-8 text-primary-500" />
          </motion.div>
        )
    }
  }

  const getStatusColor = () => {
    switch (progress.status) {
      case 'completed':
        return 'text-green-600'
      case 'failed':
        return 'text-red-600'
      default:
        return 'text-primary-600'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card p-8"
    >
      <div className="text-center mb-8">
        <div className="flex justify-center mb-4">
          {getStatusIcon()}
        </div>
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">
          Đang chuyển đổi
        </h2>
        <p className="text-gray-600">
          Vui lòng đợi trong khi chúng tôi tạo podcast audio cho bạn
        </p>
      </div>

      {/* Progress Bar */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className={`text-lg font-medium ${getStatusColor()}`}>
            {progress.message}
          </span>
          <span className="text-2xl font-bold text-primary-600">
            {Math.round(progress.progress)}%
          </span>
        </div>
        
        <div className="progress-bar h-4 mb-4">
          <motion.div
            className="progress-fill h-full"
            initial={{ width: 0 }}
            animate={{ width: `${progress.progress}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </div>

        {/* Estimated Time */}
        <div className="flex items-center justify-center text-sm text-gray-500">
          <ClockIcon className="h-4 w-4 mr-1" />
          <span>
            {progress.progress < 100 
              ? `Ước tính còn ${Math.max(1, Math.round((100 - progress.progress) / 10))} phút`
              : 'Hoàn thành!'
            }
          </span>
        </div>
      </div>

      {/* Progress Details */}
      <div className="bg-gray-50 rounded-lg p-4 max-h-48 overflow-y-auto">
        <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center">
          <ClockIcon className="h-4 w-4 mr-2" />
          Chi tiết quá trình
        </h4>
        <div className="space-y-1">
          {details.map((detail, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="text-xs text-gray-600 font-mono"
            >
              {detail}
            </motion.div>
          ))}
        </div>
      </div>

      {/* Fun Facts */}
      <div className="mt-6 p-4 bg-pastel-blue rounded-lg border border-blue-200">
        <h4 className="text-sm font-medium text-blue-800 mb-2">💡 Bạn có biết?</h4>
        <p className="text-xs text-blue-700">
          Hệ thống AI của chúng tôi có thể nhận diện và bỏ qua các phần không cần thiết như 
          mục lục, lời cảm ơn, và chỉ mục để tạo ra một audiobook mượt mà và dễ nghe.
        </p>
      </div>

      {/* Cancel Button */}
      {progress.status === 'processing' && (
        <div className="mt-6 text-center">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="btn-secondary text-sm"
            onClick={() => {
              // Handle cancellation
              setProgress(prev => ({
                ...prev,
                status: 'failed',
                message: 'Đã hủy bởi người dùng'
              }))
            }}
          >
            Hủy chuyển đổi
          </motion.button>
        </div>
      )}
    </motion.div>
  )
}
