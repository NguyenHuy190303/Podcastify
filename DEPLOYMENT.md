# 🚀 Hướng dẫn Deploy Podcastify lên Vercel

## Chuẩn bị

### 1. Tạo tài khoản và API Keys

#### OpenAI API Key (Bắt buộc)
1. Truy cập [OpenAI Platform](https://platform.openai.com/api-keys)
2. Đăng nhập hoặc tạo tài khoản
3. Tạo API key mới
4. Sao chép và lưu key an toàn

#### Google Cloud TTS (Tùy chọn)
1. Truy cập [Google Cloud Console](https://console.cloud.google.com)
2. Tạo project mới hoặc chọn project hiện có
3. Bật Text-to-Speech API
4. Tạo Service Account:
   - IAM & Admin > Service Accounts
   - Create Service Account
   - Gán role "Text-to-Speech Client"
5. Tạo JSON key và tải về

### 2. Fork Repository
1. Fork repository này về GitHub của bạn
2. Clone về máy local (nếu muốn test local)

## Deploy lên Vercel

### Bước 1: Kết nối với Vercel
1. Truy cập [vercel.com](https://vercel.com)
2. Đăng nhập bằng GitHub
3. Click "New Project"
4. Import repository đã fork

### Bước 2: Cấu hình Environment Variables
Trong Vercel dashboard, vào Settings > Environment Variables và thêm:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Nếu sử dụng Google Cloud TTS:
```
GOOGLE_CLOUD_CREDENTIALS={"type":"service_account","project_id":"..."}
```

**Lưu ý**: Với Google Cloud, paste toàn bộ nội dung JSON file vào biến môi trường.

### Bước 3: Deploy
1. Click "Deploy"
2. Vercel sẽ tự động build và deploy
3. Chờ vài phút để hoàn thành

### Bước 4: Kiểm tra
1. Truy cập URL được cung cấp
2. Test upload file PDF
3. Kiểm tra chức năng chuyển đổi

## Cấu hình Domain (Tùy chọn)

### Domain tùy chỉnh
1. Trong Vercel dashboard, vào Settings > Domains
2. Thêm domain của bạn
3. Cấu hình DNS theo hướng dẫn

### SSL Certificate
Vercel tự động cung cấp SSL certificate cho tất cả domains.

## Monitoring và Logs

### Xem Logs
1. Trong Vercel dashboard, vào Functions tab
2. Click vào function để xem logs
3. Monitor errors và performance

### Analytics
1. Bật Vercel Analytics trong Settings
2. Theo dõi traffic và performance

## Tối ưu Performance

### Caching
- Static assets được cache tự động
- API responses có thể cache với headers phù hợp

### Function Timeout
- Upload: 30 giây
- Convert: 5 phút (300 giây)
- Download: 1 phút

### Memory Limits
- Vercel Pro: 1GB RAM per function
- Hobby: 1GB RAM per function

## Troubleshooting

### Lỗi thường gặp

#### "API Key not found"
- Kiểm tra environment variables
- Đảm bảo key được set đúng tên
- Redeploy sau khi thay đổi env vars

#### "Function timeout"
- File PDF quá lớn
- Giảm kích thước file hoặc upgrade Vercel plan

#### "Build failed"
- Kiểm tra dependencies trong package.json
- Xem build logs để debug

#### "Memory limit exceeded"
- File PDF quá phức tạp
- Tối ưu code xử lý PDF

### Debug Tips
1. Sử dụng console.log trong API functions
2. Kiểm tra Network tab trong browser
3. Xem Vercel function logs
4. Test local trước khi deploy

## Scaling

### Vercel Plans
- **Hobby**: Free, giới hạn 100GB bandwidth/tháng
- **Pro**: $20/tháng, 1TB bandwidth, priority support
- **Enterprise**: Custom pricing, advanced features

### Database (Nếu cần)
- Vercel KV (Redis)
- Vercel Postgres
- External databases (MongoDB, Supabase)

### File Storage
- Vercel Blob Storage
- AWS S3
- Google Cloud Storage

## Security

### Environment Variables
- Không commit API keys vào code
- Sử dụng Vercel environment variables
- Rotate keys định kỳ

### CORS
- Cấu hình trong vercel.json
- Chỉ allow origins cần thiết

### Rate Limiting
- Implement trong API functions
- Sử dụng Vercel Edge Config

## Backup và Recovery

### Code Backup
- Repository trên GitHub
- Vercel tự động backup deployments

### Data Backup
- Export environment variables
- Backup database (nếu có)

## Updates và Maintenance

### Auto Deploy
- Push code lên GitHub sẽ tự động deploy
- Cấu hình branch protection

### Monitoring
- Set up alerts cho errors
- Monitor API usage và costs

### Updates
- Cập nhật dependencies định kỳ
- Test trước khi deploy production

## Support

### Vercel Support
- Documentation: [vercel.com/docs](https://vercel.com/docs)
- Community: [github.com/vercel/vercel](https://github.com/vercel/vercel)

### API Support
- OpenAI: [platform.openai.com/docs](https://platform.openai.com/docs)
- Google Cloud: [cloud.google.com/text-to-speech/docs](https://cloud.google.com/text-to-speech/docs)

---

🎉 **Chúc mừng! Bạn đã deploy thành công Podcastify lên Vercel!**
