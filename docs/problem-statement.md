# Trust Split Track Payment - Mô tả bài toán

## Bối cảnh

Một nhóm N người đi chơi/ăn uống cùng nhau. Một người đứng ra thanh toán toàn bộ chi phí, sau đó các thành viên còn lại cần hoàn tiền lại cho người đó.

Hiện tại, người thanh toán phải tự theo dõi thủ công: nhắn tin hỏi từng người, nhớ ai đã chuyển ai chưa — rất mất thời gian và dễ nhầm lẫn.

## Mục tiêu

Xây dựng hệ thống đơn giản giúp:
- **Người thanh toán** theo dõi ai đã hoàn tiền, ai chưa
- **Thành viên** xác nhận đã chuyển tiền (hoặc đưa tiền mặt) một cách nhanh gọn

## Đặc điểm hệ thống

Hệ thống hoạt động theo cơ chế **trust-based** — không kết nối API ngân hàng, không xác minh giao dịch thật. Thành viên tự báo cáo đã chuyển, hệ thống chỉ ghi nhận và tổng hợp.

## Luồng sử dụng

### Phía người thanh toán (Payer)
1. Tạo phiên mới: nhập tên chuyến, tổng số tiền, danh sách tên thành viên
2. Hệ thống sinh link chia sẻ → gửi vào group chat
3. Xem dashboard: ai đã confirm, ai chưa, tổng tiền đã nhận

### Phía thành viên (Member)
1. Click link nhận được
2. Chọn tên mình trong danh sách
3. Nhập số tiền (hoặc dùng số chia đều tự động)
4. Bấm "Đã chuyển" → xong

## Phạm vi (In Scope)

- Tạo phiên thu tiền với danh sách thành viên
- Chia sẻ link cho thành viên
- Thành viên xác nhận đã thanh toán (tiền mặt hoặc chuyển khoản)
- Dashboard tổng hợp trạng thái từng người

## Authentication

### Payer (người tạo phiên)
- Bắt buộc login bằng **Google OAuth**
- Token: access token ngắn hạn + refresh token dài hạn
- Quản lý toàn bộ phiên của mình

### Member (người xác nhận)
- **Không bắt buộc login** — click link → confirm → xong (anonymous)
- **Optional login** bằng Google OAuth → lưu lịch sử cá nhân → có thể xem lại "đã trả ai, bao nhiêu, khi nào"

## Ngoài phạm vi (Out of Scope)

- Xác minh giao dịch ngân hàng thật
- Tích hợp cổng thanh toán (PayOS, MoMo, ZaloPay,...)

## Tech Stack

| Layer | Technology | Deploy |
|-------|-----------|--------|
| Frontend | Vue 3 + Vite | Firebase Hosting |
| Backend | Python FastAPI | Cloud Run |
| Database | MongoDB Atlas | MongoDB Cloud (free M0) |
