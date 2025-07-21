# ⚡ Quick Start - Podcastify

## 🚀 Cách Nhanh Nhất (5 phút)

### Option 1: Deploy Ngay (Không cần code)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/podcastify)

1. Click nút "Deploy with Vercel" ở trên
2. Login Vercel bằng GitHub
3. Set environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
4. Click "Deploy"
5. Đợi 2-3 phút → Done! 🎉

### Option 2: Setup Local + Deploy (10 phút)

#### Windows:
```cmd
# 1. Clone project
git clone https://github.com/your-username/podcastify.git
cd podcastify

# 2. Chạy setup script
setup.bat

# 3. Edit .env.local với API keys
# 4. Test: npm run dev
# 5. Deploy: vercel --prod
```

#### Mac/Linux:
```bash
# 1. Clone project
git clone https://github.com/your-username/podcastify.git
cd podcastify

# 2. Chạy setup script
chmod +x setup.sh
./setup.sh

# 3. Edit .env.local với API keys
# 4. Test: npm run dev
# 5. Deploy: vercel --prod
```

## 🔑 Lấy API Keys (2 phút)

### OpenAI API Key (Bắt buộc)
1. 🔗 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Login → "Create new secret key"
3. Copy key: `sk-...`

### Google Cloud TTS (Tùy chọn)
1. 🔗 [console.cloud.google.com](https://console.cloud.google.com)
2. Create project → Enable Text-to-Speech API
3. Create Service Account → Download JSON
4. Copy JSON content

## 🧪 Test Nhanh

### 1. Tạo file PDF test
```
Chương 1: Test

Đây là nội dung test để kiểm tra chức năng chuyển đổi PDF sang audio.
Hệ thống sẽ đọc nội dung này bằng AI text-to-speech.

Chương 2: Kết thúc

Đây là chương cuối của file test.
```

### 2. Upload và test
1. Mở app: `http://localhost:3000`
2. Drag & drop file PDF
3. Chọn settings → Start conversion
4. Download MP3 khi xong

## 🎯 Checklist Hoàn Thành

- [ ] ✅ App chạy local: `npm run dev`
- [ ] ✅ Upload PDF hoạt động
- [ ] ✅ TTS conversion hoạt động
- [ ] ✅ Download MP3 hoạt động
- [ ] ✅ UI responsive trên mobile
- [ ] ✅ Deploy lên Vercel thành công

## 🆘 Troubleshooting Nhanh

### "API Key invalid"
```bash
# Kiểm tra .env.local
cat .env.local

# Restart server
npm run dev
```

### "Module not found"
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### "Port 3000 in use"
```bash
# Sử dụng port khác
npm run dev -- -p 3001
```

### "Build failed"
```bash
# Check errors
npm run lint
npx tsc --noEmit
```

## 📱 Test Devices

### Desktop
- ✅ Chrome/Firefox/Safari
- ✅ 1920x1080, 1366x768

### Mobile
- ✅ iPhone (375x667)
- ✅ Android (360x640)

## 🔗 Links Hữu Ích

- 📖 [Full Documentation](./GETTING_STARTED.md)
- 🚀 [Deployment Guide](./DEPLOYMENT.md)
- 📚 [Git Setup](./GIT_SETUP.md)
- 🐛 [Report Issues](https://github.com/your-username/podcastify/issues)

## 💡 Pro Tips

### Development
```bash
# Hot reload với TypeScript checking
npm run dev

# Build và test production
npm run build && npm start

# Lint và fix
npm run lint -- --fix
```

### Deployment
```bash
# Deploy với Vercel CLI
npm i -g vercel
vercel --prod

# Hoặc push lên GitHub (auto deploy)
git push origin main
```

### Performance
- 📊 Lighthouse score > 90
- ⚡ First load < 3s
- 📱 Mobile-friendly
- 🔍 SEO optimized

## 🎉 Success!

Khi mọi thứ hoạt động:
1. 🎧 App chạy mượt mà
2. 🎨 UI pastel đẹp mắt
3. 🚀 Deploy thành công
4. 📱 Responsive hoàn hảo

→ **Bạn đã có một PDF-to-Audio converter professional!**

---

**Need help?** 
- 💬 [Create an issue](https://github.com/your-username/podcastify/issues)
- 📧 Email: support@yourproject.com
- 🐦 Twitter: @yourhandle
