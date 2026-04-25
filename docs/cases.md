# Use Cases & Solutions

## Case 1: Nhóm đi chơi, 1 người thanh toán, chia tiền qua group chat

### Mô tả
- Nhóm N người đi chơi/ăn uống
- A thanh toán toàn bộ
- Về nhà, A gửi vào group chat: mã QR ngân hàng + 1 link
- Các thành viên thanh toán bằng bất kỳ cách nào (MoMo, chuyển khoản, tiền mặt)
- Sau khi thanh toán xong → click link → xác nhận nhanh → gửi
- Không cần đăng nhập

### Yêu cầu
- Link gọn, mở nhanh trên mobile
- Form xác nhận tối giản (không tốn thời gian)
- Không yêu cầu đăng nhập
- Hỗ trợ cả tiền mặt lẫn chuyển khoản (không cần phân biệt — trust-based, chỉ cần xác nhận đã trả)

### Giải pháp đề xuất
- A tạo phiên → nhập tên chuyến, tổng tiền, danh sách tên thành viên
- Hệ thống sinh link dạng: `https://app.com/pay/:sessionId`
- A gửi link vào group kèm QR ngân hàng của mình
- Thành viên click link → chọn tên → nhập số tiền → bấm Xác nhận
- Dashboard của A cập nhật real-time
