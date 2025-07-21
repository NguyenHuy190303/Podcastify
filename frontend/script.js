// Podcastify Frontend JavaScript
class PodcastifyApp {
    constructor() {
        this.socket = null;
        this.currentJobId = null;
        this.services = {};
        
        this.initializeElements();
        this.setupEventListeners();
        this.connectWebSocket();
        this.loadServices();
    }
    
    initializeElements() {
        // File upload elements
        this.uploadArea = document.getElementById('upload-area');
        this.fileInput = document.getElementById('file-input');
        this.fileInfo = document.getElementById('file-info');
        this.bookMetadata = document.getElementById('book-metadata');
        
        // Settings elements
        this.settingsSection = document.getElementById('settings-section');
        this.ttsServiceSelect = document.getElementById('tts-service');
        this.voiceSelect = document.getElementById('voice-select');
        this.speedSlider = document.getElementById('speed-slider');
        this.speedValue = document.getElementById('speed-value');
        this.startConversionBtn = document.getElementById('start-conversion');
        
        // Progress elements
        this.progressSection = document.getElementById('progress-section');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.progressPercentage = document.getElementById('progress-percentage');
        this.progressDetails = document.getElementById('progress-details');
        
        // Download elements
        this.downloadSection = document.getElementById('download-section');
        this.downloadBtn = document.getElementById('download-btn');
        this.newConversionBtn = document.getElementById('new-conversion');
        
        // Error elements
        this.errorSection = document.getElementById('error-section');
        this.errorMessage = document.getElementById('error-message');
        this.retryBtn = document.getElementById('retry-conversion');
        
        // Status elements
        this.connectionStatus = document.getElementById('connection-status');
        this.connectionText = document.getElementById('connection-text');
    }
    
    setupEventListeners() {
        // File upload
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleFileDrop(e));
        
        // Settings
        this.ttsServiceSelect.addEventListener('change', () => this.updateVoiceOptions());
        this.speedSlider.addEventListener('input', (e) => {
            this.speedValue.textContent = e.target.value + 'x';
        });
        this.startConversionBtn.addEventListener('click', () => this.startConversion());
        
        // Download and retry
        this.downloadBtn.addEventListener('click', () => this.downloadFile());
        this.newConversionBtn.addEventListener('click', () => this.resetApp());
        this.retryBtn.addEventListener('click', () => this.retryConversion());
    }
    
    connectWebSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            this.updateConnectionStatus(true);
        });
        
        this.socket.on('disconnect', () => {
            this.updateConnectionStatus(false);
        });
        
        this.socket.on('progress_update', (data) => {
            if (data.job_id === this.currentJobId) {
                this.updateProgress(data.progress, data.message);
            }
        });
        
        this.socket.on('conversion_complete', (data) => {
            if (data.job_id === this.currentJobId) {
                this.showDownloadSection();
            }
        });
        
        this.socket.on('conversion_error', (data) => {
            if (data.job_id === this.currentJobId) {
                this.showError(data.error);
            }
        });
    }
    
    updateConnectionStatus(connected) {
        if (connected) {
            this.connectionStatus.classList.add('connected');
            this.connectionText.textContent = 'Connected';
        } else {
            this.connectionStatus.classList.remove('connected');
            this.connectionText.textContent = 'Disconnected';
        }
    }
    
    async loadServices() {
        try {
            const response = await fetch('/api/services');
            this.services = await response.json();
            this.populateServiceOptions();
        } catch (error) {
            console.error('Error loading services:', error);
        }
    }
    
    populateServiceOptions() {
        // Clear existing options
        this.ttsServiceSelect.innerHTML = '';
        
        // Add service options
        for (const [serviceName, serviceData] of Object.entries(this.services)) {
            const option = document.createElement('option');
            option.value = serviceName;
            option.textContent = serviceData.name.charAt(0).toUpperCase() + serviceData.name.slice(1);
            this.ttsServiceSelect.appendChild(option);
        }
        
        // Update voice options for default service
        this.updateVoiceOptions();
    }
    
    updateVoiceOptions() {
        const selectedService = this.ttsServiceSelect.value;
        const serviceData = this.services[selectedService];
        
        // Clear existing voice options
        this.voiceSelect.innerHTML = '<option value="">Default Voice</option>';
        
        if (serviceData && serviceData.voices) {
            serviceData.voices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.name;
                option.textContent = voice.description || voice.name;
                this.voiceSelect.appendChild(option);
            });
        }
    }
    
    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }
    
    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }
    
    handleFileDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }
    
    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }
    
    async processFile(file) {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            this.showError('Please select a PDF file.');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            this.showLoading('Uploading file...');
            
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.currentJobId = result.job_id;
                this.displayBookInfo(result.metadata, file.name);
                this.showSettingsSection();
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Upload failed: ' + error.message);
        }
    }
    
    displayBookInfo(metadata, filename) {
        this.bookMetadata.innerHTML = `
            <div class="metadata-item">
                <span class="metadata-label">Filename:</span>
                <span class="metadata-value">${filename}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">Title:</span>
                <span class="metadata-value">${metadata.title}</span>
            </div>
            <div class="metadata-item">
                <span class="metadata-label">Author:</span>
                <span class="metadata-value">${metadata.author}</span>
            </div>
            ${metadata.subject ? `
            <div class="metadata-item">
                <span class="metadata-label">Subject:</span>
                <span class="metadata-value">${metadata.subject}</span>
            </div>
            ` : ''}
        `;
        
        this.fileInfo.style.display = 'block';
    }
    
    showSettingsSection() {
        this.settingsSection.style.display = 'block';
        this.settingsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    async startConversion() {
        const settings = {
            tts_service: this.ttsServiceSelect.value,
            voice: this.voiceSelect.value,
            speed: parseFloat(this.speedSlider.value),
            skip_toc: document.getElementById('skip-toc').checked,
            skip_acknowledgments: document.getElementById('skip-acknowledgments').checked,
            skip_copyright: document.getElementById('skip-copyright').checked,
            skip_index: document.getElementById('skip-index').checked
        };
        
        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    job_id: this.currentJobId,
                    settings: settings
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.showProgressSection();
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Conversion failed to start: ' + error.message);
        }
    }
    
    showProgressSection() {
        this.hideAllSections();
        this.progressSection.style.display = 'block';
        this.progressSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    updateProgress(progress, message) {
        this.progressFill.style.width = progress + '%';
        this.progressPercentage.textContent = Math.round(progress) + '%';
        this.progressText.textContent = message;
        
        // Add to progress details
        const timestamp = new Date().toLocaleTimeString();
        this.progressDetails.innerHTML += `<div>[${timestamp}] ${message}</div>`;
        this.progressDetails.scrollTop = this.progressDetails.scrollHeight;
    }
    
    showDownloadSection() {
        this.hideAllSections();
        this.downloadSection.style.display = 'block';
        this.downloadSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    downloadFile() {
        window.location.href = `/api/download/${this.currentJobId}`;
    }
    
    showError(errorMsg) {
        this.hideAllSections();
        this.errorMessage.textContent = errorMsg;
        this.errorSection.style.display = 'block';
        this.errorSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    retryConversion() {
        this.hideAllSections();
        this.showSettingsSection();
    }
    
    resetApp() {
        this.currentJobId = null;
        this.hideAllSections();
        this.fileInput.value = '';
        this.fileInfo.style.display = 'none';
        this.progressDetails.innerHTML = '';
        document.getElementById('upload-section').style.display = 'block';
    }
    
    hideAllSections() {
        this.settingsSection.style.display = 'none';
        this.progressSection.style.display = 'none';
        this.downloadSection.style.display = 'none';
        this.errorSection.style.display = 'none';
    }
    
    showLoading(message) {
        this.progressText.textContent = message;
        this.progressFill.style.width = '0%';
        this.progressPercentage.textContent = '0%';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PodcastifyApp();
});
