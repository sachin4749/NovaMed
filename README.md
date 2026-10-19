<div align="center">

# 🩺 NovaMed: Enterprise AI Medical Intelligence & Pan-India Healthcare Suite

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![OpenAI GPT-4o](https://img.shields.io/badge/OpenAI_GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*An advanced, location-aware medical intelligence and multi-lingual healthcare directory platform designed to bridge everyday pharmaceutical tracking with emergency infrastructure navigation across India.*

[Explore Features](#-core-modules--architecture) • [Installation Guide](#-local-installation--setup-guide) • [Deployment](#-cloud-deployment) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents
- [About the Project](#-about-the-project)
- [Core Modules & Architecture](#-core-modules--architecture)
- [Tech Stack](#-tech-stack)
- [Project Directory Structure](#-project-directory-structure)
- [Local Installation & Setup Guide](#-local-installation--setup-guide)
- [Cloud Deployment](#-cloud-deployment)
- [Security & Privacy Best Practices](#-security--privacy-best-practices)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💡 About the Project

**NovaMed** is built to solve critical accessibility barriers in modern healthcare. By fusing state-of-the-art Large Language Models (**OpenAI GPT-4o**) with dynamic geo-spatial data routing, NovaMed provides citizens, medical students, and practitioners with an all-in-one intelligence suite. 

Whether you need to inspect an unfamiliar prescription drug composition, locate a specialized neurology center in a remote taluka, evaluate early clinical symptoms, or parse handwritten medical prescriptions—NovaMed executes it seamlessly in your preferred regional language.

---

graph TD
    %% Styling Nodes
    classDef mainHeader fill:#090d16,stroke:#0ea5e9,stroke-width:2px,color:#fff,font-weight:bold;
    classDef moduleBox fill:#02182b,stroke:#38bdf8,stroke-width:1px,color:#fff;
    classDef aiCore fill:#090d16,stroke:#818cf8,stroke-width:2px,color:#fff,font-weight:bold;

    * 🩺 **NovaMed Master Interface** *(Glassmorphic Streamlit Frontend Engine)*
  
  ├── 🌐 **Multi-Language Engine** *(Supports 22+ Scheduled Indian Languages)*
  
  ├── 💊 **Smart Pharmacy Inspector** *(Drug, Syrups, Creams & Supply Analysis)*
  
  ├── 🗺️ **Geo-Medical Map Locator** *(State/UT + City/Taluka/Village + Google Maps)*
  
  │
  
  └── 🤖 **AI Triage & OCR Core** *(Powered by GPT-4o & PyPDF/Docx Document Parsers)*
### 1. 🌐 Pan-India Multi-Language Engine
* **Universal Localization**: Seamlessly shifts UI components, error messages, medical reports, and directory listings across **22 Scheduled Indian Languages** (including Hindi, Marathi, Kannada, Telugu, Tamil, Bengali, Gujarati, etc.) alongside English.

### 2. 💊 Smart Pharmacy & Drug Inspector
* **Universal Item Analysis**: Instantly decodes brand names, generic salts, syrups, topical creams, syringes, surgical tools, and inhalers.
* **Structured Payload Output**: Returns clinical composition, primary indications, manufacturer guidelines, potential adverse side effects, and precise dosage/storage parameters.

### 3. 🗺️ Pan-India Geo-Medical Locator & Google Maps
* **Granular Navigation**: Combines a robust **State/UT selection dropdown** with a flexible **City, Taluka, or Village free-text search box** to guarantee 100% geographic coverage across India.
* **Live Spatial Rendering**: Automatically generates an interactive **Google Maps Embed view** alongside verified directory records for diagnostic labs, specialized clinical departments, government infrastructure (AIIMS, Civil Hospitals, PMBJP Kendras), and emergency blood banks.

### 4. 🤖 AI Symptom Triage Assistant
* **Clinical Guidance**: Analyzes user-described symptom patterns to recommend relevant specialist departments, triage urgency levels, and essential questions for physician consultation.

### 5. 📂 Prescription Scanner & OCR
* **Document Intelligence**: Upload PDF or Word format medical prescriptions to automatically extract text strings, isolate medication names, and execute instant background safety audits.

---

## 🛠️ Tech Stack

* **Frontend Framework**: Streamlit (Python) featuring custom CSS **Glassmorphism design tokens** (`backdrop-filter: blur`, dynamic dark-mode mesh gradients, and polished box-shadow hierarchies).
* **AI & Language Processing**: OpenAI API (`gpt-4o`) optimized with strict JSON schema outputs and multi-language systemic prompts.
* **Geospatial UI**: Google Maps Embed API.
* **Document Parsers**: `pypdf` and `python-docx` for native binary file extraction.

---

## 📂 Project Directory Structure

```text
novamed/
│
├── .streamlit/
│   └── secrets.toml          # API credentials configuration (git-ignored)
├── assets/                   # Logos, banners, and diagrams
├── app.py                    # Master application logic & UI router
├── requirements.txt          # Python package dependency manifest
└── README.md                 # Comprehensive project documentation

