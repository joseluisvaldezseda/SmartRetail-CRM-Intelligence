# 🎯 Customer Intelligence System

> **Advanced ML-powered customer analytics platform for strategic CRM decision-making**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌐 Live Demo

**[🚀 Try the Live Dashboard](https://smartretail-crm-intelligence.streamlit.app/)** - Experience the full analytics platform in action!

> *Explore real customer segmentation, churn predictions, and campaign strategies without any installation.*

A comprehensive customer intelligence platform that combines **RFM segmentation**, **churn prediction**, **lifetime value forecasting**, and **product recommendation engines** into a unified, actionable dashboard.

> **💡 Quick Start:** [Access Live Demo](https://smartretail-crm-intelligence.streamlit.app/) | [View Documentation](#-installation--setup)

---

## 🚀 Key Features

### **Strategic CRM Campaigns**
Pre-configured campaign templates for immediate deployment:
- 🛡️ **Gold Shield** - VIP retention for high-value at-risk customers
- ⚡ **Quick Cash** - Conversion optimization for high-propensity buyers
- 💎 **Rough Diamonds** - Upselling strategies for high-potential new customers
- 🔄 **Operation Lazarus** - Reactivation campaigns for dormant valuable accounts

### **Advanced Analytics**
- **RFM Segmentation**: 20-tier customer classification system
- **Churn Prediction**: Probabilistic risk scoring with 90-day horizon
- **CLV Forecasting**: Customer lifetime value projections
- **Product Recommendations**: AI-powered cross-sell engine with confidence scoring

### **Interactive Visualizations**
- Real-time portfolio composition analysis
- Predictive scatter plots (Propensity vs Expected Value)
- Risk distribution heatmaps
- Individual customer deep-dive explorer

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA PIPELINE                            │
│  (run_pipeline.py - Automated Notebook Orchestration)        │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┬──────────┬──────────┐
        │                     │          │          │
    ┌───▼────┐         ┌──────▼───┐  ┌──▼────┐  ┌──▼────────┐
    │  RFM   │         │  Churn   │  │  LTV  │  │   Reco    │
    │Segment │         │  Model   │  │ Model │  │  Engine   │
    └───┬────┘         └──────┬───┘  └──┬────┘  └──┬────────┘
        │                     │         │          │
        └──────────┬──────────┴─────────┴──────────┘
                   │
        ┌──────────▼──────────────────────┐
        │  Unified Dataset (Parquet/CSV)  │
        └──────────┬──────────────────────┘
                   │
        ┌──────────▼──────────────────────┐
        │  Streamlit Dashboard (UI)       │
        │  - Real-time filtering          │
        │  - Campaign presets             │
        │  - Exportable insights          │
        └─────────────────────────────────┘
```

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Pipeline Orchestration** | Papermill | Automated notebook execution |
| **Data Processing** | Pandas, NumPy | ETL and feature engineering |
| **Machine Learning** | Scikit-learn | Churn/LTV models |
| **Visualization** | Plotly Express | Interactive charts |
| **Frontend** | Streamlit | Real-time dashboard |
| **Data Storage** | Parquet/CSV | Optimized analytics dataset |

---

## 📁 Project Structure

```
customer-intelligence-system/
│
├── dashboard.py                 # Main Streamlit application
├── run_pipeline.py              # Automated ML pipeline runner
├── requirements.txt             # Python dependencies
│
├── notebooks/                   # ML workflows (Jupyter)
│   ├── segmentacion/
│   │   └── 01_Segmentacion_Cartera.ipynb
│   ├── churn_ltv/
│   │   ├── 02_Modelo_Churn.ipynb
│   │   └── 03_Modelo_LTV.ipynb
│   └── recomendacion/
│       └── 04_Engine_Recomendacion.ipynb
│
├── data/
│   └── rfm_churn_ltv.csv        # Processed analytics dataset
│
├── logs/
│   └── pipeline_log.txt         # Execution metrics
│
└── README.md
```

---

## 🔧 Installation & Setup

### **Prerequisites**
- Python 3.8+
- pip package manager

### **Quick Start**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/customer-intelligence-system.git
cd customer-intelligence-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the ML pipeline** (generates analytics dataset)
```bash
python run_pipeline.py
```

4. **Launch the dashboard**
```bash
streamlit run dashboard.py
```

5. **Access the app**
```
Navigate to: http://localhost:8501
```

### **Or Use the Live Demo**
**[🌐 Access the hosted version](https://smartretail-crm-intelligence.streamlit.app/)** - No installation required!

---

## 📈 Dashboard Usage

### **1. Select a Campaign Strategy**
Choose from pre-configured presets or use manual filtering:
- **Manual/All**: Full control over all filters
- **Gold Shield**: VIP retention focus
- **Quick Cash**: High-propensity conversion
- **Rough Diamonds**: New customer upselling
- **Operation Lazarus**: Dormant account reactivation

### **2. Apply Advanced Filters**
Fine-tune your audience with multi-dimensional segmentation:
- Business unit
- Purchase propensity tiers
- Future value levels (Bronze → Diamond)
- RFM segments (20 categories)
- Churn risk levels

### **3. Analyze Insights**
- **KPI Metrics**: Accounts selected, avg churn risk, total CLV, purchase propensity
- **Visual Analytics**: RFM distribution, value composition, propensity vs value scatter
- **Customer Explorer**: Search individual accounts with recommendations

### **4. Export & Act**
- Download filtered customer lists
- Review product recommendations with confidence scores
- Identify cross-sell opportunities

---

## 🤖 ML Pipeline Details

### **Automated Execution**
The `run_pipeline.py` script orchestrates the complete analytics workflow:

```python
# Sequential execution of ML notebooks
1. RFM Segmentation      → Customer lifecycle classification
2. Churn Model          → 90-day risk probability
3. LTV Model            → Revenue forecasting
4. Recommendation Engine → Product affinities
```

### **Pipeline Features**
- ✅ Error handling & retry logic
- ✅ Progress tracking
- ✅ Execution logging with metrics
- ✅ Output validation
- ✅ Reproducible runs

### **Sample Log Output**
```
################################################################################
EJECUCIÓN SISTEMA DE INTELIGENCIA: 2026-01-09 14:30:00
================================================================================
MÉTRICAS DE RENDIMIENTO:
Tiempo de procesamiento: 1.25 horas

DATASET PROCESADO:
Registros: 45,203
Variables: 18
Tamaño: 12.45 MB
================================================================================
Status: Pipeline completado satisfactoriamente.
################################################################################
```

---

## 🎨 Dashboard Highlights

### **Aesthetic Design**
- Minimalist, corporate-grade UI
- Responsive layout for all screen sizes
- Custom CSS styling with soft shadows and borders
- Color-coded metrics (green = positive, red = critical)

### **Performance Optimizations**
- `@st.cache_data` for instant data loading
- Parquet format for compressed analytics
- Lazy loading of large datasets
- Efficient filtering with pandas masks

### **User Experience**
- One-click campaign deployment
- Collapsible filter sections
- Search functionality for individual accounts
- Hover tooltips with detailed customer data

---

## 📊 Sample Insights

### **RFM Segmentation Tiers**
```
1. Campeones              → Top-tier active buyers
2. VIPs Leales            → Loyal high-value customers
3. Alto Potencial         → High-frequency recent buyers
...
18. Baja Prioridad        → Low engagement
19. A Punto de Dormir     → At-risk dormant
20. Hibernando            → Inactive accounts
```

### **Value Classification**
- 💎 **Diamante**: Top 25% CLV
- 🥇 **Oro**: 50th-75th percentile
- 🥈 **Plata**: 25th-50th percentile
- 🥉 **Bronce**: Bottom 25%

### **Propensity Scoring**
- **Muy Alta**: 75-100% purchase probability
- **Alta**: 50-75%
- **Media**: 25-50%
- **Baja**: 0-25%

---

## 🔐 Data Privacy & Security

- ✅ No hardcoded credentials
- ✅ Anonymized file paths for GitHub
- ✅ Local data processing (no cloud uploads)
- ✅ GDPR-compliant data handling practices

---

## 📝 Requirements

```txt
streamlit==1.28.0
pandas==2.0.3
plotly==5.17.0
numpy==1.24.3
papermill==2.4.0
jupyter==1.0.0
scikit-learn==1.3.0
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Jose Luis Valdez Seda**  
📧 Email: joseluisvaldezseda@gmail.com  
🔗 LinkedIn: [linkedin.com/in/jose-luis-valdez-seda](https://linkedin.com/in/jose-luis-valdez-seda)  
🐙 GitHub: [@joseluisvaldezseda](https://github.com/joseluisvaldezseda)

---

## 🙏 Acknowledgments

- Built with ❤️ using Streamlit
- Inspired by modern CRM analytics best practices
- Special thanks to the open-source ML community

---
 
<p align="center">
  <b>⭐ If you find this project useful, please consider giving it a star! ⭐</b>
</p>

<p align="center">
  Made with 🧠 and ☕
</p>
