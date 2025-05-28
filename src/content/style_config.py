"""
Configuration file for personal writing style.
This file contains templates, phrases, and style elements that define your unique voice.
"""

# Personal style characteristics
STYLE_CONFIG = {
    # Brand DNA and tone of voice
    "brand_dna": {
        "archetype": "Эксперт-инноватор",
        "values": ["инновации", "технологии", "прогресс", "аналитика", "экспертность"],
        "unique_features": ["глубокое понимание стартап-экосистемы", "доступное объяснение сложных технологий", "прогнозирование трендов"]
    },
    
    # Big Idea - основной посыл бренда
    "big_idea": "Технологические инновации меняют мир к лучшему, а мы делаем их понятными для всех",
    
    # Overall tone of your content
    "tone": [
        "enthusiastic", 
        "inspirational", 
        "visionary", 
        "analytical",
        "expert",
        "forward-thinking",
        "accessible",
        "trustworthy",
        "informative",
        "concrete"
    ],
    
    # Signature phrases you often use - короткие, эмоциональные, запоминающиеся
    "phrases": [
        "Инновации меняют мир!", 
        "Технологии будущего уже здесь!", 
        "Стартап-экосистема развивается стремительно!",
        "Предприниматели, которые меняют правила игры!",
        "Вдохновляющая история успеха!",
        "Революционное решение для рынка!",
        "Будущее создается сегодня!",
        "Технологии — это новая нефть!",
        "Инвестиции в инновации — путь к успеху!",
        "Стартапы — это двигатель прогресса!",
        "От идеи до миллионов: путь стартапа",
        "Технологии, которые решают реальные проблемы",
        "Факты вместо лозунгов — вот наш подход",
        "Конкретные кейсы говорят громче слов"
    ],
    
    # Дубский Рейтинг - уникальная система оценки стартапов
    "dubskiy_rating": {
        "name": "Рейтинг Дубского",
        "english_name": "Dubskiy Rating",
        "scale": [
            {"score": 1, "symbol": "🚀", "description": "Интересная идея, но нужна серьезная доработка", "english_description": "Interesting idea, but needs serious refinement"},
            {"score": 2, "symbol": "🚀🚀", "description": "Перспективный проект с хорошим потенциалом", "english_description": "Promising project with good potential"},
            {"score": 3, "symbol": "🚀🚀🚀", "description": "Сильное решение с реальными бизнес-перспективами", "english_description": "Strong solution with real business prospects"},
            {"score": 4, "symbol": "🚀🚀🚀🚀", "description": "Отличный стартап с высокой вероятностью успеха", "english_description": "Excellent startup with high probability of success"},
            {"score": 5, "symbol": "🚀🚀🚀🚀🚀", "description": "Революционный проект, способный изменить индустрию", "english_description": "Revolutionary project that can change the industry"}
        ],
        "format": "\n\n📊 **Рейтинг Дубского**: {symbol} ({score}/5)\n{description}",
        "english_format": "\n\n📊 **Dubskiy Rating**: {symbol} ({score}/5)\n{description}"
    },
    
    # Introduction templates with placeholders - цепляющие первые 3-5 строк
    "intro_templates": [
        "🚀 Друзья! Сегодня хочу поделиться интересной историей о стартапе, который {action}.",
        "💡 Инновации никогда не спят! Сегодня в фокусе внимания {company}, который {action}.",
        "🔥 Горячие новости из мира стартапов! {company} только что {action}.",
        "👨‍💻 Технологические предприниматели снова удивляют! {company} {action}.",
        "🌟 Вдохновляющая история дня: как {company} {action}.",
        "🚀 Прорыв в мире технологий! {company} {action} и меняет правила игры.",
        "💎 Нашел для вас жемчужину! {company} {action} и заслуживает вашего внимания.",
        "🔍 Мой радар инноваций обнаружил: {company} {action}.",
        "⚡️ Энергия предпринимательства в действии! {company} {action}.",
        "💰 Инвестиционный кейс дня: {company} {action} и вот почему это важно.",
        "🧠 Разбираем по полочкам: как {company} {action} и что это значит для рынка.",
        "📊 Конкретные цифры: {company} {action} и вот результаты в цифрах.",
        "🎯 Кейс из практики: как {company} {action} и какие уроки мы можем извлечь."
    ],
    
    # Middle section templates - структурированные, с визуальными разделителями
    "body_templates": [
        "Почему это важно? {reason}\n\nКлючевые моменты:\n✅ {point1}\n✅ {point2}\n✅ {point3}",
        "Что делает этот проект особенным?\n\n{special_feature}\n\nПочему стоит следить за развитием:\n👉 {reason1}\n👉 {reason2}",
        "Мой анализ как эксперта:\n\n{analysis}\n\nПотенциал роста: {potential}",
        "Три причины, почему это интересно:\n\n1️⃣ {reason1}\n2️⃣ {reason2}\n3️⃣ {reason3}",
        "Как технологический аналитик, я вижу в этом проекте:\n\n✨ {poetic_view}\n\nКак предприниматель, замечаю:\n💼 {business_view}",
        "Разбор по пунктам:\n\n📌 Проблема: {problem}\n📌 Решение: {solution}\n📌 Инновация: {innovation}\n📌 Перспективы: {prospects}",
        "Для тех, кто следит за трендами:\n\n📊 Рыночная ниша: {market}\n📈 Потенциал роста: {growth}\n🔄 Как это меняет индустрию: {impact}",
        "Конкретный пример из практики:\n\n🔍 Ситуация: {situation}\n🛠️ Действия: {actions}\n📈 Результат: {result}\n💡 Выводы: {insights}",
        "Давайте разберем факты:\n\n📊 Было: {before}\n📈 Стало: {after}\n💹 Рост: {growth_percentage}%\n🔮 Прогноз: {forecast}"
    ],
    
    # Conclusion templates - с четким призывом к действию
    "conclusion_templates": [
        "Как вы думаете, какое будущее ждет этот стартап? Делитесь мнениями в комментариях! 💬",
        "Следите за обновлениями! Технологическая революция продолжается! 🚀",
        "Подписывайтесь на канал, чтобы быть в курсе самых интересных историй из мира стартапов! ✨",
        "Какие инновационные проекты вдохновляют вас? Поделитесь в комментариях! 🔥",
        "Хотите узнать больше о подобных проектах? Ставьте лайк и делитесь с друзьями! 👍",
        "Инновации — это путь в будущее. Давайте вместе следить за развитием технологий! 🌐",
        "Как эксперт в технологиях, я вижу большой потенциал в этом направлении. А вы что думаете? 💭",
        "Сохраняйте этот пост, если хотите следить за развитием этого стартапа! 🔖",
        "Отметьте в комментариях друга, которому будет интересна эта история! 👥",
        "Какой опыт из этого кейса вы можете применить в своих проектах? Поделитесь в комментариях! 📝",
        "Если у вас есть вопросы по этой теме — задавайте их в комментариях, отвечу каждому! 🙋‍♂️"
    ],
    
    # Hashtags to use - релевантные, не слишком общие
    "hashtags": [
        "#стартапы #инновации #технологии #евгенийдубский #эрартаэйай #erartaai",
        "#бизнес #инвестиции #стартап #евгенийдубский #эрартаэйай #erartaai",
        "#технологии #будущее #инновации #евгенийдубский #эрартаэйай #erartaai",
        "#предпринимательство #стартапы #успех #евгенийдубский #эрартаэйай #erartaai",
        "#венчурныеинвестиции #технологии #инновации #евгенийдубский #эрартаэйай #erartaai",
        "#финтех #стартапы #технологии #евгенийдубский #эрартаэйай #erartaai",
        "#цифровизация #инновации #будущее #евгенийдубский #эрартаэйай #erartaai",
        "#технологическиетренды #стартапы #бизнес #евгенийдубский #эрартаэйай #erartaai",
        "#технологическийпрорыв #инновации #будущеесегодня #евгенийдубский #эрартаэйай #erartaai",
        "#стартапэкосистема #технологическиерешения #бизнесидеи #евгенийдубский #эрартаэйай #erartaai",
        "#аналитика #бизнескейсы #стартапопыт #евгенийдубский #эрартаэйай #erartaai",
        "#технологииразвития #инновационныерешения #цифроваятрансформация #евгенийдубский #эрартаэйай #erartaai"
    ],
    
    # English hashtags
    "english_hashtags": [
        "#startups #innovation #technology #evgeniydubskiy #erartaai",
        "#business #investments #startup #evgeniydubskiy #erartaai",
        "#technology #future #innovation #evgeniydubskiy #erartaai",
        "#entrepreneurship #startups #success #evgeniydubskiy #erartaai",
        "#venturecapital #technology #innovation #evgeniydubskiy #erartaai",
        "#fintech #startups #technology #evgeniydubskiy #erartaai",
        "#digitalization #innovation #future #evgeniydubskiy #erartaai",
        "#techtrends #startups #business #evgeniydubskiy #erartaai",
        "#techbreakthrough #innovation #futuretoday #evgeniydubskiy #erartaai",
        "#startupecosystem #techsolutions #businessideas #evgeniydubskiy #erartaai",
        "#analytics #businesscases #startupexperience #evgeniydubskiy #erartaai",
        "#techdevelopment #innovativesolutions #digitaltransformation #evgeniydubskiy #erartaai"
    ],
    
    # Social media links
    "social_links": {
        "russian": "\n\nПодписывайтесь на мой Telegram канал: @https://t.me/evgeniydubskiy",
        "english": "\n\nFollow me on social media:\nInstagram: @https://www.instagram.com/erarta.ai/\nX: @https://x.com/evgeniydubskiy"
    },
    
    # Post structures based on content goals
    "post_structures": {
        "привлечение": {
            "description": "Для привлечения новой аудитории",
            "elements": ["интригующий заголовок", "актуальная проблема", "краткое решение", "призыв подписаться"]
        },
        "активация": {
            "description": "Для вовлечения существующей аудитории",
            "elements": ["обращение к подписчикам", "полезная информация", "вопрос для обсуждения", "призыв к комментариям"]
        },
        "удержание": {
            "description": "Для удержания интереса аудитории",
            "elements": ["эксклюзивная информация", "глубокий анализ", "экспертное мнение", "ссылки на дополнительные материалы"]
        },
        "продажа": {
            "description": "Для конвертации в продажи",
            "elements": ["конкретная проблема", "детальное решение", "преимущества продукта", "четкий призыв к действию"]
        },
        "доверие": {
            "description": "Для повышения доверия к бренду",
            "elements": ["конкретный кейс", "реальные примеры", "цифры и факты", "отзывы клиентов"]
        }
    },
    
    # Instagram reel script templates - структурированные, с четкими блоками
    "instagram_reel_templates": [
        {
            "hook": "Знаете ли вы, что {interesting_fact}? Сегодня расскажу о {topic}!",
            "body": "Представьте: {visualization}. Это {topic} в действии!",
            "conclusion": "Подписывайтесь, чтобы узнавать о самых интересных стартапах первыми!"
        },
        {
            "hook": "Стартап за 30 секунд! {company} делает то, что изменит {industry}!",
            "body": "Вот как это работает: {explanation}. Представляете масштаб?",
            "conclusion": "Лайк, если считаете, что за такими решениями будущее!"
        },
        {
            "hook": "Этот стартап привлек ${amount} миллионов! Хотите узнать почему?",
            "body": "Секрет в том, что {secret}. Инвесторы это понимают!",
            "conclusion": "Комментируйте, если хотите больше историй о успешных стартапах!"
        },
        {
            "hook": "3 секунды, чтобы удивить вас: {company} решает проблему, с которой сталкивается каждый!",
            "body": "Проблема: {problem}\nРешение: {solution}\nРезультат: {result}",
            "conclusion": "Сохраняйте этот ролик, если вам тоже надоела эта проблема!"
        },
        {
            "hook": "Вот как выглядит будущее {industry} — стартап {company} уже делает это реальностью!",
            "body": "Раньше: {before}\nТеперь: {after}\nА представьте через 5 лет: {future}",
            "conclusion": "Отметьте друга, который оценит эту инновацию!"
        },
        {
            "hook": "Реальный кейс: как {company} увеличил {metric} на {percentage}% за {time_period}!",
            "body": "Шаг 1: {step1}\nШаг 2: {step2}\nШаг 3: {step3}\nРезультат: {outcome}",
            "conclusion": "Сохраняйте, если хотите применить эту стратегию в своем бизнесе!"
        }
    ],
    
    # Visual elements guidelines
    "visual_guidelines": {
        "colors": ["#0A2463", "#3E92CC", "#FFFAFF", "#D8315B", "#1E1B18"],
        "image_style": "минималистичный с акцентом на технологии",
        "recommended_elements": ["графики", "схемы", "иконки", "фото продуктов", "команды стартапов"],
        "text_on_image": "краткий, контрастный, не более 5-7 слов"
    },
    
    # Telegram specific formats
    "telegram_formats": {
        "short_news": "📰 {title}\n\n{brief_description}\n\n👉 Подробнее: {link}",
        "deep_dive": "🔍 РАЗБОР: {title}\n\n{detailed_analysis}\n\n💡 Ключевой вывод: {conclusion}",
        "quick_insight": "💎 ИНСАЙТ ДНЯ\n\n{insight}\n\n🤔 А вы как думаете?",
        "case_study": "📊 КЕЙС: {company_name}\n\n🎯 Задача: {task}\n🛠️ Решение: {solution}\n📈 Результат: {result}\n\n💡 Ключевой вывод: {insight}"
    },
    
    # Writing principles from information style (habr article)
    "information_style_principles": {
        "clarity": "Используйте простые и понятные формулировки, избегайте двусмысленности",
        "concreteness": "Приводите конкретные примеры, цифры, факты вместо общих фраз",
        "structure": "Структурируйте текст логично, используя заголовки, списки и выделения",
        "relevance": "Фокусируйтесь на информации, которая действительно важна для читателя",
        "brevity": "Излагайте мысли кратко, избегайте лишних слов и отступлений"
    },
    
    # Trust-building elements (marhr article)
    "trust_building_elements": {
        "real_examples": "Приводите конкретные примеры из жизни вместо общих лозунгов",
        "case_studies": "Описывайте реальные кейсы с деталями и результатами",
        "expert_opinion": "Подкрепляйте утверждения мнением экспертов или исследованиями",
        "data_visualization": "Используйте графики и диаграммы для наглядности данных",
        "social_proof": "Включайте отзывы, истории успеха и упоминания клиентов",
        "transparency": "Будьте честны о возможных ограничениях и сложностях"
    }
}

# Function to access style elements
def get_style_element(element_type, index=None):
    """
    Get a style element from the configuration.
    
    Args:
        element_type (str): Type of style element to retrieve
        index (int, optional): Specific index to retrieve. If None, returns the entire list.
        
    Returns:
        The requested style element or list of elements.
    """
    if element_type not in STYLE_CONFIG:
        return None
        
    if index is not None and 0 <= index < len(STYLE_CONFIG[element_type]):
        return STYLE_CONFIG[element_type][index]
    
    return STYLE_CONFIG[element_type] 