'use client'

import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline'
import { toast } from 'react-hot-toast'
import { ConversionJob } from '@/types'

interface FileUploadProps {
  onFileUploaded: (job: ConversionJob) => void
}

export default function FileUpload({ onFileUploaded }: FileUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    if (file.type !== 'application/pdf') {
      toast.error('Vui lòng chọn file PDF')
      return
    }

    if (file.size > 50 * 1024 * 1024) { // 50MB limit
      toast.error('File quá lớn. Vui lòng chọn file nhỏ hơn 50MB')
      return
    }

    setUploading(true)
    setUploadProgress(0)

    try {
      const formData = new FormData()
      formData.append('file', file)

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 200)

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const result = await response.json()
      
      toast.success('Tải file thành công!')
      
      setTimeout(() => {
        onFileUploaded(result)
      }, 500)

    } catch (error) {
      console.error('Upload error:', error)
      toast.error('Lỗi khi tải file. Vui lòng thử lại.')
    } finally {
      setUploading(false)
      setUploadProgress(0)
    }
  }, [onFileUploaded])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false,
    disabled: uploading
  })

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card p-8"
    >
      <div className="text-center mb-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">
          Tải lên sách PDF
        </h2>
        <p className="text-gray-600">
          Chọn file PDF để chuyển đổi thành audio podcast
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`
          upload-area p-12 text-center cursor-pointer transition-all duration-300
          ${isDragActive ? 'dragover' : ''}
          ${uploading ? 'pointer-events-none opacity-75' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <motion.div
          animate={uploading ? { scale: [1, 1.1, 1] } : {}}
          transition={{ duration: 1, repeat: uploading ? Infinity : 0 }}
          className="mb-4"
        >
          {uploading ? (
            <div className="relative">
              <CloudArrowUpIcon className="h-16 w-16 text-primary-400 mx-auto" />
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-20 h-20 border-4 border-primary-200 border-t-primary-500 rounded-full animate-spin" />
              </div>
            </div>
          ) : (
            <DocumentTextIcon className="h-16 w-16 text-primary-400 mx-auto float" />
          )}
        </motion.div>

        {uploading ? (
          <div className="space-y-4">
            <p className="text-lg font-medium text-gray-700">
              Đang tải lên... {uploadProgress}%
            </p>
            <div className="progress-bar h-3 max-w-xs mx-auto">
              <motion.div
                className="progress-fill h-full"
                initial={{ width: 0 }}
                animate={{ width: `${uploadProgress}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-lg font-medium text-gray-700">
              {isDragActive ? 'Thả file vào đây...' : 'Kéo thả file PDF hoặc click để chọn'}
            </p>
            <p className="text-sm text-gray-500">
              Hỗ trợ file PDF tối đa 50MB
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary inline-flex items-center space-x-2"
              type="button"
            >
              <CloudArrowUpIcon className="h-5 w-5" />
              <span>Chọn file PDF</span>
            </motion.button>
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="mt-6 p-4 bg-pastel-yellow rounded-lg border border-yellow-200">
        <div className="flex items-start space-x-3">
          <ExclamationTriangleIcon className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-yellow-800">
            <p className="font-medium mb-1">Lưu ý:</p>
            <ul className="space-y-1 text-xs">
              <li>• File PDF không được bảo vệ bằng mật khẩu</li>
              <li>• Nội dung tiếng Việt hoặc tiếng Anh được hỗ trợ tốt nhất</li>
              <li>• Hệ thống sẽ tự động lọc bỏ mục lục, lời cảm ơn và các phần không cần thiết</li>
            </ul>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
