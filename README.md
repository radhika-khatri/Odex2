# 📊 ODeX Data Analytics Dashboard

An interactive data analytics dashboard built for ODeX, a trade finance and documentation platform. It takes a dummy dataset covering customer transactions, pricing plans, and support data, and turns it into a set of visual insights across five analytical sections.

The app is deployed on Streamlit and accessible live at the link below.

---

## 🔗 Live App

👉 [radhika07.streamlit.app](https://radhika07.streamlit.app/)

---

## 🧠 What the Dashboard Covers

The sidebar lets you navigate between five sections:

**Overview**
A high-level summary of the customer base, including active vs dormant customers, total transactions, customer distribution by country and type, and monthly transaction trends.

**Revenue Analysis**
Breaks down total revenue by customer and by module. Highlights the top 10 revenue contributors and includes a yield analysis (revenue per transaction) scatter plot.

**Pricing and Discounts**
Compares standard prices against contracted prices to surface revenue leakage. Shows how discounts are distributed across the customer base and whether higher discounts actually drive more transactions.

**Product Adoption**
Looks at how many customers use each module and which modules generate the most revenue versus the most usage.

**Behavioral Insights**
Analyzes support ticket volume, failed transactions, payment failures, and resolution times to understand which customers create operational friction and what it costs.

---

## 📁 Repo Structure

```
Odex2/
├── app2.py                                  # Main Streamlit application
├── ODeX_Data_Analytics_Case_Dummy_Dataset.xlsx  # Dataset with 4 sheets
└── requirements.txt                         # Python dependencies
```

The dataset has four sheets: Customer Master, Transaction Data, Support Data, and Pricing Plans.

---

## ⚙️ Requirements

```bash
pip install -r requirements.txt
```

Key libraries used: `streamlit`, `pandas`, `plotly`, `numpy`, `openpyxl`

---

## 🚀 Running It Locally

### 1. Clone the repo

```bash
git clone https://github.com/radhika-khatri/Odex2.git
cd Odex2
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app2.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🖥️ How to Use It

1. Open the app (locally or via the live link).
2. Use the sidebar to navigate between sections.
3. Each section loads automatically with charts and metrics from the dataset.
4. Charts are interactive. You can hover over data points, zoom in, and toggle legend items.
5. Quick stats (total revenue and customer count) are always visible in the sidebar.

---

## 🛠️ Built With

- **Streamlit** for the web app interface
- **Plotly** for interactive charts
- **Pandas** for data processing
- **NumPy** for calculations
- **OpenPyXL** for reading the Excel dataset

---

## 👤 Author

**Radhika Khatri**  
[GitHub Profile](https://github.com/radhika-khatri)
