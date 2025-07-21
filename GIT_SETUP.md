# 📚 Hướng Dẫn Setup Git và Push Code

## 🎯 Bước 1: Khởi Tạo Git Repository

### Trong thư mục dự án:
```bash
# Khởi tạo git repository
git init

# Thêm tất cả files
git add .

# Commit đầu tiên
git commit -m "🎉 Initial commit: Podcastify - PDF to Audio Converter with Pastel UI"
```

## 🌐 Bước 2: Tạo Repository trên GitHub

### Cách 1: Qua GitHub Website
1. Truy cập: https://github.com
2. Click nút **"New"** (màu xanh)
3. Điền thông tin:
   - **Repository name**: `podcastify`
   - **Description**: `🎧 Modern PDF to Audio Converter with Beautiful Pastel UI`
   - **Visibility**: Public (để deploy free trên Vercel)
4. **KHÔNG** check "Add a README file" (vì đã có)
5. Click **"Create repository"**

### Cách 2: Qua GitHub CLI (nếu đã cài)
```bash
# Cài GitHub CLI (nếu chưa có)
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: apt install gh

# Login
gh auth login

# Tạo repo
gh repo create podcastify --public --description "🎧 Modern PDF to Audio Converter with Beautiful Pastel UI"
```

## 🔗 Bước 3: Kết Nối Local với GitHub

```bash
# Thêm remote origin (thay YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/podcastify.git

# Kiểm tra remote
git remote -v

# Push code lên GitHub
git branch -M main
git push -u origin main
```

## 📝 Bước 4: Tạo README.md Đẹp

### Cập nhật README với thông tin repository:
```bash
# Mở file README.md và thêm:
```

**Thêm vào đầu README.md:**
```markdown
# 🎧 Podcastify

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/podcastify)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/podcastify?style=social)](https://github.com/YOUR_USERNAME/podcastify)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🎨 Modern PDF to Audio Converter with Beautiful Pastel UI

[🚀 Live Demo](https://podcastify-your-username.vercel.app) | [📖 Documentation](./GETTING_STARTED.md) | [🐛 Report Bug](https://github.com/YOUR_USERNAME/podcastify/issues)
```

## 🏷️ Bước 5: Tạo Tags và Releases

```bash
# Tạo tag cho version đầu tiên
git tag -a v1.0.0 -m "🎉 Release v1.0.0: Initial release with pastel UI"

# Push tag lên GitHub
git push origin v1.0.0
```

### Tạo Release trên GitHub:
1. Vào repository trên GitHub
2. Click **"Releases"** → **"Create a new release"**
3. Chọn tag `v1.0.0`
4. Title: `🎉 Podcastify v1.0.0 - Initial Release`
5. Description:
```markdown
## ✨ Features
- 🎨 Beautiful pastel UI design
- 📄 PDF to audio conversion
- 🤖 OpenAI & Google TTS integration
- 📱 Fully responsive design
- ⚡ Serverless architecture
- 🚀 One-click Vercel deployment

## 🚀 Quick Start
1. Click the "Deploy with Vercel" button
2. Set your OpenAI API key
3. Start converting PDFs to audio!

## 📖 Documentation
See [Getting Started Guide](./GETTING_STARTED.md) for detailed instructions.
```

## 🔄 Bước 6: Workflow cho Development

### Branching Strategy:
```bash
# Tạo branch cho feature mới
git checkout -b feature/new-feature

# Làm việc và commit
git add .
git commit -m "✨ Add new feature"

# Push branch
git push origin feature/new-feature

# Tạo Pull Request trên GitHub
# Merge vào main sau khi review
```

### Commit Message Convention:
```bash
# Sử dụng emoji và format chuẩn
git commit -m "✨ feat: add new TTS voice options"
git commit -m "🐛 fix: resolve upload progress issue"
git commit -m "📝 docs: update API documentation"
git commit -m "🎨 style: improve pastel color scheme"
git commit -m "⚡ perf: optimize PDF processing"
git commit -m "🔧 config: update Vercel settings"
```

## 📊 Bước 7: Setup GitHub Actions (Optional)

### Tạo file `.github/workflows/ci.yml`:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Type check
      run: npx tsc --noEmit
    
    - name: Build
      run: npm run build
```

## 🔒 Bước 8: Security và Best Practices

### Tạo file `.gitignore` (đã có):
```gitignore
# Environment variables
.env*.local
.env

# Dependencies
node_modules/

# Build outputs
.next/
out/
dist/

# Logs
*.log
```

### Tạo file `SECURITY.md`:
```markdown
# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability, please send an email to security@yourproject.com instead of using the issue tracker.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Measures

- API keys are stored securely in environment variables
- File uploads are validated and size-limited
- CORS is properly configured
- No sensitive data is logged
```

## 📋 Checklist Hoàn Thành

- [ ] ✅ Git repository initialized
- [ ] ✅ Code pushed to GitHub
- [ ] ✅ README.md updated with badges
- [ ] ✅ Release v1.0.0 created
- [ ] ✅ Documentation complete
- [ ] ✅ .gitignore configured
- [ ] ✅ Security policy added
- [ ] ✅ GitHub Actions setup (optional)

## 🎯 Tiếp Theo: Deploy lên Vercel

Sau khi hoàn thành Git setup, bạn có thể:

1. **Test local**: `npm run dev`
2. **Deploy Vercel**: Xem file `DEPLOYMENT.md`
3. **Share project**: Chia sẻ GitHub repo với team

## 🆘 Troubleshooting Git

### Lỗi authentication:
```bash
# Setup SSH key (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
# Copy và add vào GitHub Settings > SSH Keys

# Hoặc sử dụng personal access token
# GitHub Settings > Developer settings > Personal access tokens
```

### Lỗi push:
```bash
# Force push (cẩn thận!)
git push --force-with-lease origin main

# Hoặc pull trước
git pull origin main --rebase
git push origin main
```

🎉 **Xong! Repository đã sẵn sàng cho development và deployment!**
