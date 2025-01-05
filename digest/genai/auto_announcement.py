"""
Код, который позволяет подготовить текст дайджеста по существующей схеме.
"""

from typing import Any

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from digest.genai.utils import get_llm
from digest.models import ISSUE_STATUS_ACTIVE, ITEM_STATUS_ACTIVE, Issue

__all__ = [
    "generate_announcement",
]


def format_issue(issue):
    return {
        "id": issue.id,
        "announcement": issue.announcement,
        "news": [
            {
                "category": x.section.title,
                "link": x.link,
                "title": x.title,
                "description": x.description,
            }
            for x in issue.item_set.filter(status=ITEM_STATUS_ACTIVE).iterator()
        ],
    }


def get_examples() -> list[dict[str, Any]]:
    examples_size = 4
    qs_issue = Issue.objects.filter(
        status=ISSUE_STATUS_ACTIVE,
    ).order_by(
        "-published_at"
    )[:examples_size]
    return [format_issue(x) for x in qs_issue]


def get_example_prompt() -> PromptTemplate:
    template = """```
<< Дайджест. Анонс #{{ id }} >>
{{ announcement }}

<< Дайджест. Новости #{{ id }} >>
{% for item in news %}- {{ item.title }}
{% endfor %}```
"""
    return PromptTemplate.from_template(template, template_format="jinja2")


"""
Описание: {{ item.description | default('Нет описания') }}"""


def get_question_template():
    return """Составь текст анонса для дайджеста с номером {{id}} используя ТОЛЬКО новости ниже.

```
<< Структура анонса >>
#python #pydigest
IT-новости про Python перед вами.

Часть материалов из выпуска Python Дайджест:

- Сначала 3-5 новости-статьи
- Затем новости-видео
- После чего новости об инструментах
- Завершает 1-2 новости-релизы ПО

Заходите в гости - {{url}}
```

```
<< Дайджест. Новости #{{id}} >>
{% for item in news %}- {{ item.title }}
{% endfor %}```

Выбери не больше 14 новостей.
Убедись, что в итоговом тексте анонса используются ТОЛЬКО новости из списка для Дайджеста {{ id }}.
Убедись, что не переводишь название новостей.
Убедись, что новости выводишь списком без разделов.
"""


def generate_announcement(digest_id: int) -> str:
    issue = Issue.objects.get(pk=digest_id)
    issue_data = format_issue(issue)
    news = [
        {
            "title": x.get("title"),
        }
        for x in issue_data["news"]
    ]

    # Load and process the text
    llm = get_llm()

    examples = get_examples()
    example_prompt = get_example_prompt()
    prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Ты опытный редактор новостей, который умеет выбрать наиболее интересные новости для составления дайджеста. Ты модерируешь сайт, который агрегирует ИТ-новости про Python экосистему. Сейчас я тебе покажу примеры составления дайджеста: итоговый текст и новости, которые использовались при составлении дайджеста. ",
        suffix=get_question_template(),
        input_variables=["news"],
        template_format="jinja2",
    )

    query = prompt.invoke(
        {
            "news": news,
            "id": digest_id,
            "url": f"https://pythondigest.ru/issue/{digest_id}/",
        }
    ).to_string()

    result: str = llm.invoke(query)
    return result
