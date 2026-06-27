\# 🚢 Fleet Intelligence Platform



> Real-Time Maritime Fleet Monitoring, Anomaly Detection, and Predictive Maintenance using Apache Kafka, Apache Flink, InfluxDB, Grafana, and PyTorch.



\---



## 📖 Overview



Fleet Intelligence Platform is a real-time data engineering and machine learning project designed to simulate, monitor, and analyze maritime vessel telemetry.



The platform ingests live telemetry from multiple vessels, processes streaming data using Apache Kafka and Apache Flink, stores metrics in InfluxDB, visualizes fleet operations through Grafana dashboards, and uses an LSTM-based predictive maintenance model to forecast equipment failures.



\---



\## 🏗️ System Architecture



```text

Ship Telemetry Simulator

&#x20;           │

&#x20;           ▼

&#x20;     Apache Kafka

&#x20;           │

&#x20;           ▼

&#x20;     Apache Flink

&#x20;           │

&#x20;           ▼

&#x20;       InfluxDB

&#x20;           │

&#x20;           ▼

&#x20;       Grafana

&#x20;           │

&#x20;           ▼

LSTM Predictive Maintenance

```



\---



\## ⚙️ Tech Stack



\### Streaming \& Event Processing



\* Apache Kafka

\* Apache Flink



\### Time-Series Storage



\* InfluxDB



\### Monitoring \& Visualization



\* Grafana



\### Machine Learning



\* PyTorch

\* NumPy

\* Pandas

\* Scikit-Learn



\### Development Tools



\* Python

\* Docker

\* Docker Compose

\* Git

\* GitHub



\---



\## 🚢 Fleet Monitored



The platform continuously monitors:



\* MSC Bellissima

\* MSC Grandiosa

\* MSC Seashore



\---



\## 📡 Telemetry Metrics



Each vessel streams:



\* Engine RPM

\* Coolant Temperature

\* Fuel Consumption

\* HVAC Pressure

\* Vibration Levels

\* GPS Latitude

\* GPS Longitude



\---



\# 📸 Project Screenshots



\## Smart Fleet Monitoring Dashboard



Real-time fleet monitoring dashboard built with Grafana.



!\[Smart Fleet Monitoring Dashboard](screenshots/dashboard.png)



Dashboard includes:



\* Fleet Coolant Temperature

\* Fleet Engine RPM

\* Fleet Vibration Monitoring

\* Fleet Fuel Consumption

\* Fleet HVAC Pressure

\* Fleet GPS Tracking



\---



\## Apache Kafka Topics



Kafka acts as the central event streaming platform.



!\[Kafka Topics](screenshots/kafka-topics.png)



Topics:



| Topic          | Purpose                  |

| -------------- | ------------------------ |

| ship-telemetry | Vessel telemetry stream  |

| ship-alerts    | Anomaly detection alerts |



Current Kafka statistics:



\* ship-telemetry → 19,308+ messages

\* ship-alerts → 641+ messages



\---



\## Apache Flink Stream Processing



Real-time stream analytics and anomaly detection.



!\[Apache Flink Job](screenshots/flink-job.png)



Running Job:



```text

FleetAnomalyDetector

```



Capabilities:



\* Event Stream Processing

\* Fleet Monitoring

\* Alert Generation

\* Telemetry Analytics



\---



\## LSTM Predictive Maintenance Results



Machine learning model used for equipment failure prediction.



!\[ML Results](screenshots/ml-results.png)



\### Model Performance



```text

Accuracy : 0.9880

Precision: 0.9318

Recall   : 0.9535

```



\---



\# 🔄 Data Pipeline



\### Step 1 — Telemetry Simulation



Generates vessel telemetry data:



```json

{

&#x20; "ship\_id": "MSC-BELLISSIMA",

&#x20; "engine\_rpm": 1828,

&#x20; "coolant\_temp": 80.3,

&#x20; "fuel\_flow\_lpm": 12.9,

&#x20; "hvac\_pressure": 4.2,

&#x20; "vibration\_mms": 0.83,

&#x20; "gps\_lat": 43.3,

&#x20; "gps\_lon": 5.43

}

```



\---



\### Step 2 — Kafka Ingestion



Telemetry is published to:



```text

ship-telemetry

```



Alerts are published to:



```text

ship-alerts

```



\---



\### Step 3 — Flink Processing



Apache Flink:



\* Consumes Kafka events

\* Detects anomalies

\* Aggregates metrics

\* Generates alerts



\---



\### Step 4 — InfluxDB Storage



Processed telemetry is stored in InfluxDB for:



\* Historical analysis

\* Dashboarding

\* Trend monitoring



\---



\### Step 5 — Grafana Visualization



Grafana visualizes:



\* Engine RPM

\* Coolant Temperature

\* Fuel Consumption

\* HVAC Pressure

\* Vibration

\* GPS Tracking



\---



\### Step 6 — Predictive Maintenance



LSTM model predicts:



\* Equipment degradation

\* Potential failures

\* Maintenance requirements



\---



\# 📂 Project Structure



```text

fleet-intelligence-platform/

│

├── dashboard/

│

├── ingestion/

│

├── simulator/

│

├── streaming/

│

├── flink-jars/

│

├── ml/

│   ├── data/

│   ├── models/

│   ├── generate\_backfill\_data.py

│   ├── prepare\_sequences.py

│   ├── lstm\_model.py

│   ├── train.py

│   └── server\_model.py

│

├── screenshots/

│   ├── dashboard.png

│   ├── kafka-topics.png

│   ├── flink-job.png

│   └── ml-results.png

│

├── docker-compose.yml

├── Dockerfile.flink

├── README.md

└── .env

```



\---



\# 🚀 Getting Started



\## Clone Repository



```bash

git clone https://github.com/YOUR\_USERNAME/fleet-intelligence-platform.git

cd fleet-intelligence-platform

```



\---



\## Start Infrastructure



```bash

docker compose up -d

```



\---



\## Verify Containers



```bash

docker ps

```



Expected services:



\* Kafka

\* Zookeeper

\* Flink JobManager

\* Flink TaskManager

\* InfluxDB

\* Grafana

\* Kafka UI



\---



\## Run Telemetry Simulator



```bash

python simulator/simulator.py

```



\---



\## Train Predictive Maintenance Model



```bash

python ml/train.py

```



\---



\# 📈 Key Achievements



✅ Real-Time Telemetry Streaming



✅ Apache Kafka Event Pipeline



✅ Apache Flink Stream Processing



✅ InfluxDB Time-Series Storage



✅ Grafana Fleet Dashboard



✅ Real-Time GPS Tracking



✅ Fleet Anomaly Detection



✅ Predictive Maintenance using LSTM



✅ 98.8% Accuracy



✅ Dockerized Infrastructure



\---



\# 💼 Resume Project Entry



\### Fleet Intelligence Platform | Apache Kafka, Apache Flink, InfluxDB, Grafana, PyTorch



\* Built a real-time maritime fleet monitoring platform processing live telemetry from simulated vessels.

\* Developed Kafka-based ingestion and Apache Flink streaming pipelines for anomaly detection.

\* Stored telemetry in InfluxDB and visualized operational metrics using Grafana dashboards.

\* Implemented an LSTM predictive maintenance model achieving 98.8% accuracy for equipment fault prediction.

\* Monitored engine RPM, coolant temperature, vibration, HVAC pressure, fuel consumption, and vessel location in real time.

\* Designed an end-to-end streaming architecture using modern cloud-native data engineering tools.



\---



\# 🎯 Future Improvements



\* Deploy on Microsoft Azure

\* Deploy on AWS

\* Containerize ML Inference API

\* Add Grafana Alerting

\* Add Email/SMS Notifications

\* Implement CI/CD using GitHub Actions

\* Deploy Dashboard Publicly

\* Add Kubernetes Support



\---



\# 👨‍💻 Author



\## Vivek Sagar



B.Tech Computer Science Engineering



Cloud Computing • Data Engineering • Full Stack Development • DevOps • AI/ML



GitHub: https://github.com/VivekS51



Portfolio: https://vivek-bytes.vercel.app/



