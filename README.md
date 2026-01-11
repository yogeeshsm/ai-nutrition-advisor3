# AI Nutrition Advisor

A comprehensive AI-powered nutrition advisory system designed for child malnutrition detection, meal planning, and nutritional recommendations.

## 🚀 Features

### Core Functionality
- **Malnutrition Prediction**: ML-based detection using child health metrics
- **Meal Optimization**: AI-powered meal planning based on nutritional needs
- **AI Chatbot**: Gemini & Groq powered nutritional advice chatbot
- **USDA Integration**: Real-time nutrition data from USDA API
- **Child Health Tracking**: Monitor growth, immunization, and health records
- **Price Tracking**: Mandi price API integration for ingredient costs
- **QR Code System**: Child identity and health card management

### Advanced Features
- Emergency alert system for severe malnutrition cases
- Village economy integration
- WHO immunization tracking
- Translation support for multilingual access
- Interactive health visualizations

## 📂 Project Structure

```
ai-nutrition-advisor3/
├── app/                    # Main application servers (20 files)
├── chatbots/              # AI chatbot implementations (4 files)
├── models/                # ML models and training (13 files)
├── tests/                 # Test suite (35 files)
├── scripts/               # Setup & maintenance (29 files)
├── utils/                 # Utility functions (13 files)
├── launch_scripts/        # Startup scripts (.bat/.sh)
├── logs/                  # Application logs
├── docs/                  # Documentation
├── templates/             # HTML templates
├── static/                # Static assets
└── model_accuracy_graphs/ # Model performance visualizations
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/yogeeshsm/ai-nutrition-advisor3.git
cd ai-nutrition-advisor3

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### Windows

```bash
# Start the full application
launch_scripts\START_FULL_APP.bat

# Or start individual components
launch_scripts\START_SERVER.bat
launch_scripts\START_MALNUTRITION.bat
```

### Linux/Mac

```bash
# Make scripts executable
chmod +x launch_scripts/*.sh

# Run the application
./launch_scripts/build.sh
```

### Python Direct Launch

```bash
# Option 1: Full server
python app/production_server.py

# Option 2: Simple server
python app/simple_server.py

# Option 3: Quick start
python app/quick_start.py
```

## 📊 ML Models

The system uses trained machine learning models for:
- Malnutrition risk prediction
- Meal recommendations
- Nutritional analysis

Train or update models:
```bash
python models/train_malnutrition_model.py
python models/prepare_dataset.py
```

## 🤖 AI Chatbot

The chatbot provides intelligent nutritional advice using:
- **Gemini AI**: Google's advanced language model
- **Groq**: High-performance AI inference

Configure API keys in environment variables or config files.

## 🧪 Testing

Run comprehensive tests:
```bash
# All tests
python tests/test_all.py

# Specific test suites
python tests/test_malnutrition_api.py
python tests/test_ml_system.py
python tests/test_food_system.py
```

## 📈 Database

The system supports:
- SQLite (default, lightweight)
- MySQL (production, scalable)

Migrate to MySQL:
```bash
python scripts/migrate_to_mysql.py
```

Initialize production data:
```bash
python scripts/init_production_data.py
```

## 🔧 Configuration

Key configuration files:
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version for deployment
- `utils/db_config.py` - Database configuration

## 📝 Scripts

### Maintenance Scripts (scripts/)
- `add_*.py` - Add sample/test data
- `check_*.py` - Verify database and data integrity
- `debug_*.py` - Debug tools and profilers
- `update_*.py` - Update nutrition and health data

### Launch Scripts (launch_scripts/)
- `START_SERVER.bat` - Start main server
- `START_FULL_APP.bat` - Launch full application
- `START_MALNUTRITION.bat` - Malnutrition predictor
- `run.bat` - Quick run script
- `build.sh` - Linux/Mac build script

## 🌐 API Integrations

- **USDA FoodData Central**: Nutrition information
- **Mandi Price API**: Ingredient pricing
- **WHO**: Immunization guidelines
- **Google Gemini**: AI chatbot
- **Groq**: AI inference

## 📊 Monitoring & Logs

Application logs are stored in the `logs/` directory:
- `server_log.txt` - Server operations
- `server_output.txt` - Server output
- `test_output.txt` - Test results

## 🚀 Deployment

### Render Deployment
```bash
launch_scripts\DEPLOY_TO_RENDER.bat
```

### Production Server
```bash
python app/production_server.py
```

The application is configured for deployment on:
- Render
- Railway
- Heroku
- Azure
- AWS

## 👥 Target Users

- Healthcare workers in rural areas
- Nutritionists and dietitians
- Government health programs
- NGOs working on child malnutrition
- Anganwadi centers

## 🔐 Security

- Input validation on all user data
- Secure API key management
- Database query sanitization
- Health data privacy compliance

## 📖 Documentation

Additional documentation available in `docs/`:
- `USER_GUIDE.txt` - User manual

## 🤝 Contributing

Contributions welcome! Please ensure:
1. Tests pass: `python tests/test_all.py`
2. Code follows project structure
3. Documentation updated

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**S M Yogesh**
- GitHub: [@yogeeshsm](https://github.com/yogeeshsm)

## 🙏 Acknowledgments

- USDA for nutrition data API
- Google Gemini for AI capabilities
- WHO for immunization guidelines
- Open-source ML libraries (scikit-learn, pandas, numpy)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check `docs/USER_GUIDE.txt`

## 🔄 Version

Current Version: 3.0

---

**Made with ❤️ for improving child nutrition**
