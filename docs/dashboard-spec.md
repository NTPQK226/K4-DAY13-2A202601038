# Yêu cầu dashboard

Contract có thể kiểm tra bằng máy nằm tại `config/dashboard.yaml`. Hướng dẫn dựng và kiểm tra runtime nằm tại [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md).

Dashboard chính cần đủ 6 nhóm thông tin:

1. Latency P50/P95/P99.
2. Traffic: request count hoặc QPS.
3. Error rate và breakdown theo loại lỗi.
4. Cost theo thời gian.
5. Tổng token input/output.
6. Quality proxy.

Tiêu chuẩn trình bày:

- Khoảng thời gian mặc định: 1 giờ.
- Tự refresh mỗi 15–30 giây nếu công cụ hỗ trợ.
- Có threshold hoặc SLO line.
- Ghi rõ đơn vị.
- Chỉ giữ 6–8 panel quan trọng ở lớp chính.
- Screenshot phải nhìn được tên panel và khoảng thời gian.

## Chi tiết 6 panel theo nguồn /metrics

Mỗi panel lấy dữ liệu từ endpoint `/metrics`:

```
GET http://localhost:8000/metrics
```

Dữ liệu trả về bao gồm: `traffic`, `latency_p50`, `latency_p95`, `latency_p99`,
`error_rate_pct`, `error_breakdown`, `total_cost_usd`, `avg_cost_usd`,
`tokens_in_total`, `tokens_out_total`, `quality_avg`.

Ví dụ dữ liệu thực tế:
```json
{
  "traffic": 1,
  "latency_p50": 585.0,
  "latency_p95": 585.0,
  "latency_p99": 585.0,
  "avg_cost_usd": 0.0024,
  "total_cost_usd": 0.0024,
  "tokens_in_total": 24,
  "tokens_out_total": 156,
  "error_rate_pct": 0.0,
  "error_breakdown": {},
  "quality_avg": 0.8
}
```

### Panel 1: Latency P50/P95/P99

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | `/metrics` → latency_p50, latency_p95, latency_p99 |
| Đơn vị | ms |
| Biểu đồ | Line chart hoặc Single Value |
| Threshold | P95 ≤ 3000ms (SLO: 99.5% requests) |
| Công cụ | Langfuse dashboard, Grafana, hoặc Streamlit |

### Panel 2: Traffic

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | `/metrics` → traffic |
| Đơn vị | requests/minute hoặc QPS |
| Threshold | ≥ 1 request/minute |

### Panel 3: Error Rate

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | `/metrics` → error_rate_pct, error_breakdown |
| Đơn vị | percent (%) |
| Threshold | error_rate_pct ≤ 2% |

### Panel 4: Cost

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | `/metrics` → total_cost_usd, avg_cost_usd |
| Đơn vị | USD |
| Threshold | total_cost_usd ≤ $2.5/ngày |

### Panel 5: Tokens

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | `/metrics` → tokens_in_total, tokens_out_total |
| Đơn vị | tokens |

### Panel 6: Quality

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | `/metrics` → quality_avg |
| Đơn vị | score (0–1) |
| Threshold | quality_avg ≥ 0.75 |

## Evidence bắt buộc

- Ảnh dashboard chụp đủ 6 panel
- Trong ảnh phải thấy: tên panel, khoảng thời gian (60 phút), đơn vị, threshold/SLO line
- Lưu vào `submission/evidence/dashboard.png`
