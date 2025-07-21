'use client'

import { motion } from 'framer-motion'
import { 
  CheckCircleIcon,
  ArrowDownTrayIcon,
  PlayIcon,
  ArrowPathIcon,
  ShareIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'
import { ConversionJob } from '@/types'

interface DownloadSectionProps {
  job: ConversionJob
  onNewConversion: () => void
}

export default function DownloadSection({ job, onNewConversion }: DownloadSectionProps) {
  const handleDownload = () => {
    // Create download link
    const link = document.createElement('a')
    link.href = `/api/download/${job.id}`
    link.download = `${job.filename.replace('.pdf', '')}.mp3`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Podcastify - PDF to Audio',
          text: `Tôi vừa chuyển đổi "${job.metadata?.title}" thành audiobook!`,
          url: window.location.href,
        })
      } catch (error) {
        console.log('Error sharing:', error)
      }
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Success Message */}
      <motion.div
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2 }}
        className="card p-8 text-center"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
          className="flex justify-center mb-6"
        >
          <div className="relative">
            <CheckCircleIcon className="h-20 w-20 text-green-500" />
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.5 }}
              className="absolute -top-2 -right-2 w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center"
            >
              <PlayIcon className="h-4 w-4 text-white" />
            </motion.div>
          </div>
        </motion.div>

        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          🎉 Hoàn thành!
        </h2>
        <p className="text-lg text-gray-600 mb-6">
          Audiobook của bạn đã được tạo thành công
        </p>

        {/* Download Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleDownload}
          className="btn-primary text-lg px-8 py-4 mb-4 inline-flex items-center space-x-3"
        >
          <ArrowDownTrayIcon className="h-6 w-6" />
          <span>Tải xuống MP3</span>
        </motion.button>

        <div className="flex justify-center space-x-4">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleShare}
            className="btn-secondary flex items-center space-x-2"
          >
            <ShareIcon className="h-4 w-4" />
            <span>Chia sẻ</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onNewConversion}
            className="btn-secondary flex items-center space-x-2"
          >
            <ArrowPathIcon className="h-4 w-4" />
            <span>Chuyển đổi file khác</span>
          </motion.button>
        </div>
      </motion.div>

      {/* File Info */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <InformationCircleIcon className="h-5 w-5 mr-2 text-primary-500" />
          Thông tin file audio
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="space-y-3">
            <div>
              <span className="font-medium text-gray-600">Tên file gốc:</span>
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
          </div>
          
          <div className="space-y-3">
            <div>
              <span className="font-medium text-gray-600">Định dạng:</span>
              <p className="text-gray-800">MP3 (192 kbps)</p>
            </div>
            <div>
              <span className="font-medium text-gray-600">Thời lượng ước tính:</span>
              <p className="text-gray-800">~{Math.round((job.fileSize / 1024 / 1024) * 2)} phút</p>
            </div>
            <div>
              <span className="font-medium text-gray-600">Trạng thái:</span>
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                <CheckCircleIcon className="h-3 w-3 mr-1" />
                Hoàn thành
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Tips */}
      <div className="card p-6 bg-gradient-to-r from-pastel-purple to-pastel-pink">
        <h4 className="text-lg font-semibold text-gray-800 mb-3">
          💡 Mẹo sử dụng
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div>
            <h5 className="font-medium mb-2">🎧 Nghe audiobook:</h5>
            <ul className="space-y-1 text-xs">
              <li>• Sử dụng ứng dụng podcast yêu thích</li>
              <li>• Điều chỉnh tốc độ phát theo sở thích</li>
              <li>• Tạo bookmark cho các chương quan trọng</li>
            </ul>
          </div>
          <div>
            <h5 className="font-medium mb-2">📱 Chia sẻ:</h5>
            <ul className="space-y-1 text-xs">
              <li>• Upload lên Google Drive hoặc Dropbox</li>
              <li>• Chia sẻ với bạn bè qua AirDrop</li>
              <li>• Đồng bộ với thiết bị khác</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Feedback */}
      <div className="text-center">
        <p className="text-sm text-gray-500 mb-2">
          Bạn hài lòng với kết quả?
        </p>
        <div className="flex justify-center space-x-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <motion.button
              key={star}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="text-2xl text-gray-300 hover:text-yellow-400 transition-colors"
            >
              ⭐
            </motion.button>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
