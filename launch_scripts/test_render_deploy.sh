#!/bin/bash
# Quick test before deploying to Render

echo "🧪 Testing AI Nutrition Advisor before Render deployment..."
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version

# Check if all dependencies are installed
echo ""
echo "✓ Checking dependencies..."
pip list | grep -E "Flask|gunicorn|tensorflow"

# Test database initialization
echo ""
echo "✓ Testing database initialization..."
python -c "import database as db; db.initialize_database(); print('Database OK!')"

# Test Flask app import
echo ""
echo "✓ Testing Flask app..."
python -c "from flask_app import app; print('Flask app OK!')"

# Check environment variables
echo ""
echo "✓ Checking environment variables..."
if [ -f .env ]; then
    echo "  .env file found ✓"
    grep -E "GEMINI_API_KEY|USDA_API_KEY" .env | sed 's/=.*/=***/' || echo "  Warning: API keys not set"
else
    echo "  ⚠️ .env file not found (will use Render env vars)"
fi

echo ""
echo "✅ Pre-deployment checks complete!"
echo ""
echo "📋 Next steps:"
echo "1. Push to GitHub: git add . && git commit -m 'Ready for Render' && git push"
echo "2. Go to Render: https://dashboard.render.com/"
echo "3. Create new Web Service and connect your repo"
echo "4. Set environment variables in Render dashboard"
echo "5. Deploy! 🚀"
