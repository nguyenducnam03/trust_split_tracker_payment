# Future Ideas

## Session Templates (Preset)

Payer hay tạo cùng một loại phiên nhiều lần (VD: cầu lông mỗi tuần) → cần tính năng lưu template để tái sử dụng.

### Ý tưởng
- Payer lưu template: tên loại phiên + danh sách cost items quen dùng
- Khi tạo phiên mới → chọn template → tự điền sẵn:
  - Tên phiên = tên template + ngày hôm nay (chọn ngày)
  - Cost items = danh sách từ template (vẫn chỉnh được)
  - Số người = từ template (vẫn chỉnh được)

### Ví dụ
Template "Cầu lông":
- Tên phiên: "Cầu lông {date}" → chọn ngày → "Cầu lông 19/04"
- Cost items: Sân, Cầu, Nước, Ăn uống
- Click vào template → form điền sẵn, chỉ cần nhập số tiền + tick người

## Member Suggestions (Autocomplete tên)

Nhập tên từng người mỗi lần tạo phiên rất tốn thời gian, nhất là nhóm hay đi cùng nhau.

### Ý tưởng
- Hệ thống lưu lại danh sách tên từ các phiên trước
- Không cần nhập số người trước — mở trang tạo phiên → hiện luôn danh sách người quen (từ lịch sử)
- Tick chọn ai tham gia → tự sinh rows trong grid
- Người mới chưa có trong danh sách → nhập tay thêm
- Hoặc kết hợp với template: template lưu luôn danh sách thành viên thường xuyên → tạo phiên mới → tick bỏ ai không tham gia lần này
