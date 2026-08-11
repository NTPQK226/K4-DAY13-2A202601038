# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm:
- Repository URL:
- Commit SHA cuối:
- Thành viên và vai trò:

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: ~10+ (Đã cấu hình thành công Langfuse)
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: [Điền link dashboard public của nhóm vào đây]

## 3. Logging và tracing

- Evidence correlation ID: ![Correlation ID](evidence/log_correlation_id.png)
- Evidence PII redaction: ![PII Score](evidence/validate_logs_score.png)
- Evidence trace waterfall: ![Trace Waterfall](evidence/traces.png) (hoặc ![First Waterfall](evidence/first_waterfall.png))
- Giải thích một span đáng chú ý: Span `retrieve` (từ file `app/mock_rag.py`) là đáng chú ý nhất vì đây là bước mô phỏng gọi DB Vector để lấy context. Trong các tình huống thực tế, span này dễ trở thành nút thắt cổ chai về mặt hiệu năng.

## 4. Prompt versioning

- Prompt name: day13-chat
- Version/label baseline: v1 (production)
- Version/label candidate: v2 (candidate)
- Trace ID của mỗi version: [Copy Paste 2 Trace ID từ Langfuse UI vào đây]
- Bằng chứng đổi label hoặc rollback: ![Rollback](evidence/rollback.png) (và ![2 Versions](evidence/2ver_prompts.png))

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: HỢP LỆ (6/6 panel)
- Evidence dashboard: ![Dashboard Spec](evidence/dashboard_spec.png)
- SLO đã chọn và lý do: Chọn SLO `latency_p95_ms` < 3000ms. Lý do: API tích hợp RAG cần đảm bảo 95% request phải phản hồi dưới 3 giây để người dùng không cảm thấy ứng dụng bị treo, đảm bảo User Experience.
- Alert rules và runbook: Đã cấu hình các rule như `high_latency_p95` (latency > 3s liên tục trong 5 phút) và `elevated_error_rate` (lỗi > 2%). Runbook để xử lý các alert này nằm ở `docs/alerts.md`.

## 6. Điều tra challenge

- Challenge ID: day13-k4-observability-v1
- Triệu chứng từ metrics: P99 Latency tăng vọt lên mức ~2600ms - 3000ms cho các request `/chat` (vượt ngưỡng SLO 2000ms).
- Trace ID liên quan: req-ffc5a52a (hoặc các request bị chậm tương tự)
- Log line/correlation ID liên quan: correlation_id: `req-ffc5a52a` (log ghi nhận `event="response_sent"` báo `latency_ms` = 2914)
- Root cause: Hệ thống truy xuất RAG (Vector Store) bị chậm. Cụ thể span `retrieve` trong `app/mock_rag.py` tốn ~2.5 giây.
- Fix action: Xử lý dứt điểm sự cố từ phía Vector Store (tăng resource, tối ưu index). Ở góc độ code, có thể gỡ bỏ nút thắt cổ chai, tối ưu lại luồng query RAG.
- Preventive measure: Thiết lập timeout chặt chẽ (vd: 1.5s) cho block gọi RAG để tránh block toàn bộ request. Thêm alert cảnh báo riêng cho metrics của span `retrieve`.

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| | | | |
