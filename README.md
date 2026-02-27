📖 Overview.
When working with Geotab hardware, finding specific technical specs (like voltage limits or operating temperatures) usually requires digging through extensive PDF manuals or web documentation.

Geotab Tech Assistant simplifies this by providing a conversational interface. Powered by the Gemini SDK, it delivers precise, concise, and accurate answers sourced directly from Geotab’s official documentation.

✨ Key Features / Características Principales
        -🚀 Instant Support: Get answers to questions like "What is the max voltage for GO9?" in seconds.
        -✅ Verified Sources: Information extracted directly from official Geotab pages to prevent AI hallucinations.
        -🎨 Intuitive UI: Clean and modern interface built with Streamlit.
        -🛠️ Hardware Focused: Specialized in GO9 and GO FOCUS devices.

🎯 Target Audience
        -Field Technicians: Who need quick answers while installing devices in the field.
        -Fleet Managers: Looking to understand hardware capabilities for their vehicles.
        -Support Engineers: Who want to streamline their workflow and avoid manual document searching.
        -Geotab Partners: Developers and resellers needing fast access to technical specifications.

🛠️ Tech Stack
        -Core AI: Gemini 2.0 Flash (via Vertex AI)
        -Framework: Streamlit
        -Language: Python 3.12
        -Cloud: Google Cloud Platform (Vertex AI & Storage)
        -Tools: BeautifulSoup4 & PyPDF (for data extraction)

🚀 Getting Started
1. Environment Setup
Create a .env file in the root directory with the following variables:
PROJECT_ID="your-google-cloud-project-id"
GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"

2. Installation
---Bash---
pip install -r requirements.txt
# Or manually:
pip install streamlit google-genai google-cloud-storage python-dotenv requests beautifulsoup4 pypdf

3. Execution
---Bash---
python -m streamlit run main.py

📝 Future Improvements
        -[ ] Integration with more Geotab hardware models.
        -[ ] Voice-to-text queries for field technicians.
        -[ ] Offline caching for remote installations.
