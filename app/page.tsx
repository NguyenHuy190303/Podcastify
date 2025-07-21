'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  CloudArrowUpIcon, 
  SpeakerWaveIcon, 
  DocumentTextIcon,
  SparklesIcon,
  HeartIcon
} from '@heroicons/react/24/outline'
import FileUpload from '@/components/FileUpload'
import ConversionSettings from '@/components/ConversionSettings'
import ProgressTracker from '@/components/ProgressTracker'
import DownloadSection from '@/components/DownloadSection'
import { ConversionJob } from '@/types'

export default function Home() {
  const [currentJob, setCurrentJob] = useState<ConversionJob | null>(null)
  const [step, setStep] = useState<'upload' | 'settings' | 'processing' | 'complete'>('upload')

  const handleFileUploaded = (job: ConversionJob) => {
    setCurrentJob(job)
    setStep('settings')
  }

  const handleConversionStart = () => {
    setStep('processing')
  }

  const handleConversionComplete = () => {
    setStep('complete')
  }

  const handleNewConversion = () => {
    setCurrentJob(null)
    setStep('upload')
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-500/20 to-secondary-500/20" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <div className="flex justify-center items-center mb-6">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="relative"
              >
                <SpeakerWaveIcon className="h-16 w-16 text-primary-500" />
                <SparklesIcon className="h-6 w-6 text-secondary-500 absolute -top-1 -right-1" />
              </motion.div>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold gradient-text mb-4">
              Podcastify
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Chuyển đổi sách PDF thành podcast audio chất lượng cao với AI
            </p>
            
            <div className="flex justify-center items-center space-x-8 text-sm text-gray-500">
              <div className="flex items-center space-x-2">
                <DocumentTextIcon className="h-5 w-5" />
                <span>PDF thông minh</span>
              </div>
              <div className="flex items-center space-x-2">
                <SpeakerWaveIcon className="h-5 w-5" />
                <span>Audio chất lượng cao</span>
              </div>
              <div className="flex items-center space-x-2">
                <SparklesIcon className="h-5 w-5" />
                <span>AI tiên tiến</span>
              </div>
            </div>
          </motion.div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="space-y-8">
          
          {/* Step Indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-center"
          >
            <div className="flex items-center space-x-4">
              {[
                { key: 'upload', label: 'Tải lên', icon: CloudArrowUpIcon },
                { key: 'settings', label: 'Cài đặt', icon: SparklesIcon },
                { key: 'processing', label: 'Xử lý', icon: SpeakerWaveIcon },
                { key: 'complete', label: 'Hoàn thành', icon: HeartIcon },
              ].map((stepItem, index) => {
                const isActive = step === stepItem.key
                const isCompleted = ['upload', 'settings', 'processing'].indexOf(step) > 
                                  ['upload', 'settings', 'processing'].indexOf(stepItem.key)
                
                return (
                  <div key={stepItem.key} className="flex items-center">
                    <div className={`
                      flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all
                      ${isActive ? 'border-primary-500 bg-primary-500 text-white' : 
                        isCompleted ? 'border-green-500 bg-green-500 text-white' :
                        'border-gray-300 bg-white text-gray-400'}
                    `}>
                      <stepItem.icon className="h-5 w-5" />
                    </div>
                    <span className={`ml-2 text-sm font-medium ${
                      isActive ? 'text-primary-600' : 
                      isCompleted ? 'text-green-600' : 'text-gray-400'
                    }`}>
                      {stepItem.label}
                    </span>
                    {index < 3 && (
                      <div className={`w-8 h-0.5 mx-4 ${
                        isCompleted ? 'bg-green-500' : 'bg-gray-300'
                      }`} />
                    )}
                  </div>
                )
              })}
            </div>
          </motion.div>

          {/* Content Sections */}
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {step === 'upload' && (
              <FileUpload onFileUploaded={handleFileUploaded} />
            )}

            {step === 'settings' && currentJob && (
              <ConversionSettings
                job={currentJob}
                onStart={handleConversionStart}
                onBack={() => setStep('upload')}
              />
            )}

            {step === 'processing' && currentJob && (
              <ProgressTracker
                jobId={currentJob.id}
                onComplete={handleConversionComplete}
              />
            )}

            {step === 'complete' && currentJob && (
              <DownloadSection
                job={currentJob}
                onNewConversion={handleNewConversion}
              />
            )}
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 text-center text-gray-500">
        <div className="max-w-4xl mx-auto px-4">
          <p className="text-sm">
            Được tạo với <HeartIcon className="h-4 w-4 inline text-red-400" /> bởi Podcastify Team
          </p>
          <p className="text-xs mt-2 opacity-75">
            Sử dụng OpenAI và Google Cloud Text-to-Speech APIs
          </p>
        </div>
      </footer>
    </div>
  )
}
