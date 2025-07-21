# 🎯 Hướng Dẫn Bắt Đầu - Podcastify

## 📋 Yêu Cầu Hệ Thống

- **Node.js**: 18.0.0 trở lên
- **npm** hoặc **yarn**
- **Git**
- **OpenAI API Key** (bắt buộc)
- **Google Cloud TTS** (tùy chọn)

## 🛠️ Cài Đặt Local

### 1. Clone Repository
```bash
# Clone project về máy
git clone https://github.com/your-username/podcastify.git
cd podcastify
```

### 2. Cài Đặt Dependencies
```bash
# Sử dụng npm
npm install

# Hoặc yarn
yarn install
```

### 3. Cấu Hình Environment Variables
```bash
# Copy file example
cp .env.example .env.local

# Mở file .env.local và điền thông tin
```

**Nội dung file .env.local:**
```env
# OpenAI API Key (BẮT BUỘC)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Google Cloud TTS (TÙY CHỌN)
GOOGLE_CLOUD_CREDENTIALS={"type":"service_account",...}

# Next.js Config
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key
```

### 4. Chạy Development Server
```bash
# Start dev server
npm run dev

# Hoặc
yarn dev
```

### 5. Mở Trình Duyệt
Truy cập: **http://localhost:3000**

## 🔑 Lấy API Keys

### OpenAI API Key
1. Truy cập: https://platform.openai.com/api-keys
2. Đăng nhập hoặc tạo tài khoản
3. Click "Create new secret key"
4. Copy key và paste vào `.env.local`

### Google Cloud TTS (Tùy chọn)
1. Truy cập: https://console.cloud.google.com
2. Tạo project mới
3. Bật Text-to-Speech API
4. Tạo Service Account:
   - IAM & Admin → Service Accounts
   - Create Service Account
   - Role: "Text-to-Speech Client"
5. Tạo JSON key
6. Copy toàn bộ nội dung JSON vào `.env.local`

## 🧪 Test Ứng Dụng

### Test Cơ Bản
1. **Upload PDF**: Kéo thả file PDF vào upload area
2. **Kiểm tra metadata**: Xem thông tin sách được extract
3. **Cấu hình settings**: Chọn TTS service và voice
4. **Start conversion**: Click "Bắt đầu chuyển đổi"
5. **Monitor progress**: Theo dõi progress bar
6. **Download**: Tải file MP3 khi hoàn thành

### Test Files Mẫu
Tạo file PDF test đơn giản:
```
Chương 1: Giới Thiệu

Đây là nội dung chương đầu tiên của cuốn sách mẫu.
Nội dung này sẽ được chuyển đổi thành audio.

Chương 2: Nội Dung Chính

Đây là chương thứ hai với nhiều nội dung hơn.
Hệ thống sẽ tự động phát hiện các chương và tạo pause phù hợp.
```

## 🐛 Troubleshooting

### Lỗi Thường Gặp

#### "Module not found"
```bash
# Xóa node_modules và reinstall
rm -rf node_modules package-lock.json
npm install
```

#### "API Key invalid"
- Kiểm tra API key trong `.env.local`
- Đảm bảo key chưa hết hạn
- Restart dev server sau khi thay đổi env

#### "Port 3000 already in use"
```bash
# Sử dụng port khác
npm run dev -- -p 3001
```

#### "Build failed"
```bash
# Check TypeScript errors
npm run lint
npx tsc --noEmit
```

### Debug Tips
1. Mở Developer Tools (F12)
2. Kiểm tra Console tab cho errors
3. Kiểm tra Network tab cho API calls
4. Xem terminal cho server logs

## 📱 Test Responsive

### Desktop
- Chrome, Firefox, Safari
- Độ phân giải: 1920x1080, 1366x768

### Tablet
- iPad (768x1024)
- Android tablets

### Mobile
- iPhone (375x667, 414x896)
- Android phones (360x640)

## 🔧 Development Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint

# Type checking
npx tsc --noEmit     # Check TypeScript

# Dependencies
npm install <package>    # Add new package
npm update              # Update packages
```

## 📊 Performance Testing

### Lighthouse Audit
1. Mở Chrome DevTools
2. Lighthouse tab
3. Generate report
4. Aim for scores > 90

### Load Testing
```bash
# Install artillery (optional)
npm install -g artillery

# Test API endpoints
artillery quick --count 10 --num 2 http://localhost:3000/api/services
```

## 🚀 Sẵn Sàng Deploy

Khi test local thành công:
1. ✅ Upload PDF hoạt động
2. ✅ TTS conversion hoạt động  
3. ✅ Download MP3 hoạt động
4. ✅ UI responsive trên mobile
5. ✅ No console errors

→ **Tiếp tục với bước Deploy lên Vercel!**

## 📞 Hỗ Trợ

### Nếu gặp vấn đề:
1. Kiểm tra [Issues](https://github.com/your-username/podcastify/issues)
2. Tạo issue mới với:
   - Mô tả lỗi
   - Steps to reproduce
   - Screenshots (nếu có)
   - Browser/OS info

### Resources
- [Next.js Docs](https://nextjs.org/docs)
- [Vercel Docs](https://vercel.com/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
