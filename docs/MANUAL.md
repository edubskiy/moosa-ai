# MOOSA AI User Manual

## Introduction

MOOSA AI is a system for automated content creation about startups in the style of Evgeniy Dubskiy. The platform uses artificial intelligence to generate unique content based on news from menabytes.com.

## Style Features

### Core Principles:
1. **Expertise and Analytical Approach**
   - Focus on specific metrics and data
   - Deep analysis of business models
   - Structured information presentation

2. **Content Structure**
   - Clear separation into introduction, main part, and conclusion
   - Use of subheadings for readability
   - Inclusion of concrete examples and cases

3. **Tone**
   - Professional yet accessible
   - Analytical but not dry
   - Expert but not arrogant

## Content Generation

### 1. Preparation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp config/.env.example .env
# Edit the .env file and add your OpenAI API key
```

### 2. Generating Posts

#### For Telegram:
```bash
python main.py --platform telegram --article-id <ARTICLE_ID>
```

#### For LinkedIn:
```bash
python main.py --platform linkedin --article-id <ARTICLE_ID>
```

#### For Instagram:
```bash
python main.py --platform instagram --article-id <ARTICLE_ID>
```

### 3. Generating Reels

```bash
python main.py --generate-reel --article-id <ARTICLE_ID>
```

## Style Configuration

Content style is configured in `src/content/style_config.py`. Main parameters:

1. **Tone**
   - expert_analyst: Expert analytical style
   - informative: Informative style
   - concrete: Concrete style with examples

2. **Structure**
   - hook: Attention-grabbing hook
   - body: Main analytical part
   - conclusion: Conclusion with a call to action

3. **Formatting**
   - Use of emojis for visual separation
   - Structured lists
   - Highlighting key metrics

## Content Storage

The platform supports two storage options:

1. **Excel**
   - Local storage
   - Simple integration
   - Suitable for small projects

2. **Google Sheets**
   - Cloud storage
   - Collaborative access
   - Suitable for teams

## Automation

### Scheduler

Set up automatic content generation:

```bash
python src/core/scheduler.py
```

Set the launch time in the .env file:
```
SCHEDULER_TIME=09:00
```

## Best Practices

1. **Article Selection**
   - Focus on significant funding rounds
   - Choose innovative business models
   - Pay attention to regional specifics

2. **Content Optimization**
   - Use relevant hashtags
   - Add calls to action
   - Include statistics and metrics

3. **Performance Analysis**
   - Track engagement
   - Analyze popular topics
   - Adjust style based on feedback

## Troubleshooting

1. **Generation Issues**
   - Check your OpenAI API key
   - Ensure you have an internet connection
   - Check logs in the logs/ folder

2. **Storage Issues**
   - Check file access permissions
   - Verify Google Sheets settings
   - Check data format

## Updates

See CHANGELOG.md for updates. New versions may include:
- Improved content generation
- New templates and styles
- Performance optimizations
- Bug fixes 