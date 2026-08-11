# Alert và Runbook

Mỗi alert dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert 1: High Latency P95

- **Tên:** High Latency P95
- **Severity:** warning
- **SLI/SLO liên quan:** latency_p95_ms > 3000ms (target 99.5% requests)
- **Điều kiện:** latency_p95 > 3000ms trong 5 phút liên tục
- **Ảnh hưởng tới người dùng:** Response time vượt ngưỡng chấp nhận, người dùng thấy hệ thống chậm hoặc timeout
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra `/metrics` — xác nhận P95 thực sự cao hơn 3000ms
  2. Mở một trace bất thường trên Langfuse → xem span nào gây chậm (RAG retrieve hay LLM generate)
  3. Tìm log cùng correlation_id → xác nhận nguyên nhân (incident bật, RAG slow, hay network)
- **Mitigation tạm thời:**
  - Kiểm tra `GET /incidents` — nếu incident rag_slow đang bật → `POST /incidents/rag_slow/disable`
  - Restart service nếu không có incident đang chạy
- **Owner:** on-call-engineer

## Alert 2: Elevated Error Rate

- **Tên:** Elevated Error Rate
- **Severity:** critical
- **SLI/SLO liên quan:** error_rate_pct > 2% (target 99.0% requests thành công)
- **Điều kiện:** error_rate_pct > 2% trong 3 phút liên tục
- **Ảnh hưởng tới người dùng:** Người dùng nhận HTTP 500 hoặc không nhận được response
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra `/metrics` → xác nhận error_rate_pct thực sự cao
  2. Kiểm tra `/health` → xem incidents nào đang enabled
  3. Mở một trace lỗi trên Langfuse → đọc error payload → xác định error_type
- **Mitigation tạm thời:**
  - Kiểm tra incident tool_fail → `POST /incidents/tool_fail/disable`
  - Restart service để clear state
- **Owner:** on-call-engineer

## Alert 3: Cost Budget Exceeded

- **Tên:** Cost Budget Exceeded
- **Severity:** warning
- **SLI/SLO liên quan:** daily_cost_usd > $2.5 (target 100% ngân sách)
- **Điều kiện:** daily_cost_usd vượt $2.5 tại bất kỳ thời điểm nào
- **Ảnh hưởng tới người dùng:** Không ảnh hưởng trực tiếp nhưng vượt ngân sách vận hành
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra `/metrics` → xác nhận total_cost_usd cao bất thường
  2. Kiểm tra incident cost_spike → `POST /incidents/cost_spike/disable`
  3. Xem token count trong traces → kiểm tra prompt_versions có token bloat không
- **Mitigation tạm thời:**
  - Tắt incident cost_spike nếu đang bật
  - Hạn chế request rate nếu do traffic tăng đột biến
- **Owner:** team-lead
