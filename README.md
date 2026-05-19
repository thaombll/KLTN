# KLTN - Cấu Trúc Dự Án

##  Tổng Quan

Đây là cấu trúc thư mục cho dự án **KLTN (Khóa Luận Tốt Nghiệp)** với các thành phần được tổ chức một cách khoa học để hỗ trợ quy trình nghiên cứu, xây dựng mô hình, và đánh giá hiệu năng.

---

##  Cấu Trúc Chi Tiết

```
KLTN/
├── baseline/                 # Mô hình cơ sở để so sánh
├── data/                     # Thư mục quản lý dữ liệu
│   ├── input/                # Dữ liệu đầu vào 
│   └── output/               # Dữ liệu đầu ra 
├── evaluation/               # Đánh giá mô hình
├── model/                    # Các file gọi mô hình ngôn ngữ lớn
├── our_method/               # Mô hình của phương pháp đề xuất
├── plot/                     # Visualizations và biểu đồ
├── result_evaluation/        # Thư mục chứa kết quả đánh giá
│   ├── RQ1/                  # Trả lời câu hỏi nghiên cứu 1
│   ├── RQ2/                  # Trả lời câu hỏi nghiên cứu 2
│   └── RQ3/                  # Trả lời câu hỏi nghiên cứu 3
├── README.md                 # File này - hướng dẫn dự án
└── requirements.txt          # Dependencies (thư viện Python cần thiết)
```

---

##  Mô Tả Từng Thư Mục

### 🔹 **baseline/**
- **Mục đích**: Chứa mô hình baseline (mô hình cơ sở)
- **Nội dung**: Các mô hình simple hoặc thuật toán cơ sở dùng để so sánh kết quả
- **Ứng dụng**: So sánh hiệu năng với mô hình đề xuất

### 🔹 **data/**
Quản lý tất cả dữ liệu của dự án:

- **input/**: 
  - Dữ liệu dạng bảng (Tableau Table)

- **output/**: 
  - Dữ liệu đã xử lý (processed/cleaned data)
  - Dữ liệu đã được chuẩn bị để training
  - Output từ data pipeline

### 🔹 **evaluation/**
- **Mục đích**: Chứa code và script đánh giá mô hình
- **Nội dung**: Các metrics, hàm evaluate, cross-validation logic
- **Ví dụ**: Accuracy, F1-score, Precision, Recall, confusion matrix

### 🔹 **model/**
- **Mục đích**: Lưu trữ các file mô hình đã train
- **Nội dung**: Saved models (.pkl, .h5, .pt, etc.)
- **Ứng dụng**: Load model để predict trên dữ liệu mới

### 🔹 **pipeline/**
- **Mục đích**: Xây dựng quy trình xử lý dữ liệu (Data Pipeline)
- **Nội dung**: Scripts cho preprocessing, feature engineering, transformation
- **Quy trình**: Raw data → Cleaned data → Feature preparation → Training ready

### 🔹 **plot/**
- **Mục đích**: Lưu các biểu đồ và visualizations
- **Nội dung**: Hình ảnh, charts, graphs (.png, .jpg, .pdf)
- **Ứng dụng**: Trực quan hóa kết quả, trend analysis

### 🔹 **result_evaluation/**
Kết quả đánh giá chi tiết cho các câu hỏi nghiên cứu:

- **RQ1/**: Research Question 1
  - Kết quả của câu hỏi nghiên cứu thứ 1
  - Biểu đồ, số liệu, phân tích

- **RQ2/**: Research Question 2
  - Kết quả của câu hỏi nghiên cứu thứ 2
  - Biểu đồ, số liệu, phân tích

- **RQ3/**: Research Question 3
  - Kết quả của câu hỏi nghiên cứu thứ 3
  - Biểu đồ, số liệu, phân tích

### 🔹 **venv/**
- **Mục đích**: Python virtual environment
- **Nội dung**: Các thư viện Python cô lập cho dự án
- **Sử dụng**: Tránh xung đột dependencies giữa các dự án

### 🔹 **requirements.txt**
- **Mục đích**: Danh sách các thư viện Python cần thiết
- **Ví dụ**:
  ```
  numpy==1.21.0
  pandas==1.3.0
  scikit-learn==0.24.0
  matplotlib==3.4.0
  tensorflow==2.6.0
  ```
- **Sử dụng**: `pip install -r requirements.txt`

---

##  Quy Trình Làm Việc Được Gợi Ý

```
1. Data Preparation
   data/input → pipeline → data/output

2. Model Training
   data/output → model/ (train & save)

3. Evaluation
   model + test_data → evaluation/ → results

4. Results Analysis
   results → plot/ (visualization)
           → result_evaluation/ (RQ1, RQ2, RQ3)

5. Documentation
   README.md + results → Final Report
```

---

##  Hướng Dẫn Sử Dụng

### 1. **Chuẩn bị môi trường**
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Kích hoạt (Windows)
venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. **Xử lý dữ liệu**
```bash
# Đặt raw data vào: data/input/
# Chạy pipeline script
python pipeline/process_data.py
# Output sẽ tạo ra: data/output/
```

### 3. **Training mô hình**
```bash
python model/train.py
# Mô hình đã train sẽ lưu vào: model/
```

### 4. **Đánh giá kết quả**
```bash
python evaluation/evaluate.py
# Kết quả lưu vào: result_evaluation/RQ1/, RQ2/, RQ3/
```

### 5. **Visualize kết quả**
```bash
python plot/generate_plots.py
# Hình ảnh lưu vào: plot/
```

---

##  Best Practices

 **Luôn giữ dữ liệu thô trong `data/input/`** - Đừng sửa đổi trực tiếp  
 **Lưu mô hình đã train trong `model/`** - Dễ dàng tái sử dụng  
 **Tách rõ code pipeline và evaluation** - Dễ debug và maintain  
 **Sử dụng virtual environment** - Tránh xung đột dependencies  
 **Cập nhật `requirements.txt`** - Khi thêm thư viện mới  
 **Tổ chức kết quả theo RQ** - Dễ theo dõi cho khóa luận  

---

##  Công Cụ & Thư Viện Gợi Ý

- **Data Processing**: pandas, numpy
- **Machine Learning**: scikit-learn, TensorFlow, PyTorch
- **Visualization**: matplotlib, seaborn, plotly
- **Experiment Tracking**: MLflow, Weights & Biases
- **Documentation**: Jupyter Notebook

---

##  Liên Hệ & Hỗ Trợ

Nếu có câu hỏi về cấu trúc dự án, vui lòng tham khảo hướng dẫn của giáo viên hướng dẫn hoặc các thành viên nhóm.

---

**Ngày cập nhật**: 2026  
**Status**: Active Development
