# Opening the Black Box with LRP: A Hands-on Guide to Explainable AI for LLMs

### Presented by **Reduan Achtibat** & **Anton Segeler**
**Explainable AI Group at Fraunhofer HHI**

---

## 🛠️ Getting Started

To ensure a smooth start during the session, please follow these steps **before** the workshop begins:

1.  **Clone the Repository:** 
Start by cloning this repository to your local machine or working environment:

```bash
git clone https://github.com/antonsegeler/xai4llms
```
2. **Setup Environment:** Open the `demo_setup.ipynb` notebook and run all cells to install the necessary dependencies and load the model.


> **🚀 GPU Recommended:** While we originally planned to run this workshop entirely in Google Colab, the content involves processing Large Language Models. If you have access to a local machine or server with a dedicated GPU, we recommend using it for a smoother and faster experience.


---

## 📖 Abstract


While Large Language Models have demonstrated unprecedented capabilities in reasoning and retrieval, their internal decision-making processes remain largely opaque. As they grow in complexity, treating these models as 'black boxes' is no longer sufficient for building reliable, safe, and transparent systems.

Hosted by the Explainable AI group at Fraunhofer HHI, this workshop offers a practical, hands-on deep dive into the inner workings of Transformer models. We will demonstrate how to apply advanced attribution and analysis methods to demystify how LLMs process information, store knowledge, and generate predictions.

#### In this session, we will cover:

* **🔍 Faithful Attribution:**
    Going beyond input-level explanations to trace the model's reasoning from input tokens through latent concepts to the final prediction using **Layer-wise Relevance Propagation (LRP)**.

* **🧠 Anatomy of In-Context Learning:**
    Identifying how specific attention heads retrieve information from context versus storing factual knowledge.

* **🎛️ Control and Source Tracking:**
    Intervening in latent representations to steer model generation and trace information sources.