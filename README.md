# Prompt Repository

Репозиторий с промптами и навыками (skills) для агентной разработки.

## Что внутри

- `prompts/product-engineering.md` — базовый промпт для задач продуктовой разработки: формат работы, требования к качеству кода, порядок проверки и структура итогового отчёта.
- `skills/change-code/` — входной навык для изменений в коде: определяет стек проекта и выбирает доступный workflow или reference-профиль для Java Maven/Gradle, Spring Java, React/Next.js, JS/TS, Bash/shell и смешанных репозиториев в рамках этих профилей.
- `skills/create-agents-md/` — навык для подготовки `AGENTS.md` с правилами работы агента в проекте.
- `skills/java-change-code/` — специализированный навык для внесения изменений в Java-код в существующих Maven/Gradle-репозиториях.
- `skills/spring-java-change-code/` — Spring-specific overlay поверх `java-change-code` для Spring Boot, web/API, security, configuration, framework wiring, Spring testing и application behavior.
- `skills/react-next-change-code/` — специализированный навык для внесения изменений в React и Next.js-код в существующих репозиториях, включая UI, components, hooks, App Router, Pages Router, Server/Client Components, route handlers, Server Functions, Server Actions, кеширование, metadata, UI-тесты и accessibility.

## Структура навыка

Каждый навык обычно включает:

- `SKILL.md` — назначение навыка, условия применения и рабочий процесс.
- `references/` — материалы с правилами и примерами.
- `agents/openai.yaml` — конфигурацию агента.
- `EVALS.md` (если есть) — критерии и заметки по оценке качества.

## Как использовать

1. Определите задачу и выберите подходящий навык.
2. Для языконезависимых или смешанных задач в поддерживаемом scope начните с `skills/change-code/`.
3. Для Java Maven/Gradle-задач используйте `skills/java-change-code/` напрямую или примените его workflow через `change-code`, если отдельная активация навыка недоступна.
4. Для Spring Java задач, где важны Spring Boot, web/API, security, configuration, persistence, framework wiring или Spring testing behavior, используйте `skills/spring-java-change-code/` напрямую или примените его overlay через `change-code`.
5. Для React и Next.js-задач используйте `skills/react-next-change-code/` напрямую или примените его workflow через `change-code`, если отдельная активация навыка недоступна.
6. Для остальных JS/TS и Bash/shell-задач используйте `change-code` вместе с соответствующими reference-файлами внутри навыка.
7. Откройте `SKILL.md` выбранного навыка.
8. Выполняйте задачу по инструкциям навыка и локальным правилам проекта.

## Принципы

- Инструкции ориентированы на практическое применение.
- Изменения должны быть безопасными и проверяемыми.
- Входные навыки должны выбирать более специфичный workflow или reference-профиль, когда он есть, не полагаясь на гарантированную runtime-активацию другого навыка.
- Framework-навыки должны работать как слой поверх базового language skill, не копируя его полностью.
- Приоритет у локальных правил проекта, установленных версий библиотек и текущей архитектуры.
- Практики для React/Next.js и Spring должны применяться с учётом реально установленных версий библиотек, а не через принудительное обновление проекта.
