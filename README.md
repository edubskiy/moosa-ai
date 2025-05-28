# MOOSA AI

A platform for automated content creation about startups in the style of Evgeniy Dubskiy.

## Features

- 🤖 AI-powered content generation
- 📊 Analytical approach to content
- 📱 Multi-platform support (Telegram, LinkedIn, Instagram)
- 🎥 Script generation for Instagram Reels
- 📅 Content scheduling
- 💾 Flexible storage (Excel/Google Sheets)
- 📈 Metrics tracking and analytics

## Project Structure

```
moosa-ai/
├── src/                    # Source code
│   ├── core/              # Core components
│   ├── storage/           # Storage systems
│   ├── content/           # Content generation
│   └── utils/             # Utility functions
├── scripts/               # Data scripts
├── templates/             # Content templates
├── config/                # Configuration files
├── docs/                  # Documentation
├── tests/                 # Tests
├── data/                  # Data
├── media/                 # Media files
├── output/                # Output files
└── logs/                  # Logs
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/edubskiy/moosa-ai.git
cd moosa-ai
```

2. Create a virtual environment:
```bash
python -m venv python_env
source python_env/bin/activate  # Linux/Mac
# or
python_env\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp config/.env.example .env
# Edit the .env file with your credentials
```

## Usage

See the detailed user manual in [docs/MANUAL.md](docs/MANUAL.md).

### Quick Start

1. Run the main process:
```bash
python main.py
```

2. Generate content for a specific platform:
```bash
python main.py --platform telegram --article-id <ARTICLE_ID>
```

3. Generate Reels script:
```bash
python main.py --generate-reel --article-id <ARTICLE_ID>
```

## Data Storage

The platform supports two storage options:

1. **Excel** (default)
   - Local storage
   - Simple integration
   - Suitable for small projects

2. **Google Sheets**
   - Cloud storage
   - Collaborative access
   - Suitable for teams

## Automation

Set up automatic content generation:
```bash
python src/core/scheduler.py
```

## Documentation

- [User Manual](docs/MANUAL.md)
- [API Documentation](docs/API.md)
- [Changelog](CHANGELOG.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Create a pull request

## License

MIT

## Contacts

Evgeniy Dubskiy
- Telegram: [@evgeniydubskiy](https://t.me/evgeniydubskiy)
- LinkedIn: [evgeniydubskiy](https://linkedin.com/in/evgeniydubskiy) 