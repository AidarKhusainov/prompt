# Prompt Repository

Репозиторий с промптами и навыками (skills) для агентной разработки.

## Что внутри

- `prompts/product-engineering.md` — базовый промпт для задач продуктовой разработки: формат работы, требования к качеству кода, порядок проверки и структура итогового отчёта.
- `skills/change-code/` — минимальный входной router-skill для изменений в коде. Он определяет стек и направляет задачу в самый узкий доступный навык.
- `skills/js-ts-change-code/` — базовый навык для JavaScript/TypeScript, Node.js, package tooling, shared utilities и JS/TS-тестов.
- `skills/react-change-code/` — навык для React UI, components, hooks, forms, accessibility и frontend/component tests.
- `skills/next-change-code/` — навык для Next.js: App Router, Pages Router, Server/Client boundaries, route handlers, caching, metadata, middleware/proxy и framework verification.
- `skills/react-next-change-code/` — совместимый router для старого имени навыка. Новые правила лучше добавлять в `react-change-code` или `next-change-code`.
- `skills/java-change-code/` — специализированный навык для внесения изменений в Java-код в существующих Maven/Gradle-репозиториях.
- `skills/spring-java-change-code/` — Spring-specific overlay поверх `java-change-code` для Spring Boot, web/API, security, configuration, framework wiring, Spring testing и application behavior.
- `skills/create-agents-md/` — навык для подготовки `AGENTS.md` с правилами работы агента в проекте.
- `skills/SKILL_AUTHORING.md` — правила добавления новых навыков без раздувания токенов.

## Структура навыка

Каждый навык обычно включает:

- `SKILL.md` — короткие условия применения, routing, reference loading и рабочий режим.
- `references/` — подробные правила, которые читаются только при необходимости.
- `agents/openai.yaml` — конфигурацию агента.
- `EVALS.md` — routing/reference-loading проверки и регрессионные кейсы.

## Как использовать

1. Определите задачу и выберите самый узкий навык.
2. Для языконезависимых или смешанных задач начните с `skills/change-code/`.
3. Для Java Maven/Gradle-задач используйте `skills/java-change-code/`.
4. Для Spring Java задач, где важны Spring Boot, web/API, security, configuration, persistence, framework wiring или Spring testing behavior, используйте `skills/spring-java-change-code/`.
5. Для generic JS/TS, Node.js, scripts, package tooling и shared utilities используйте `skills/js-ts-change-code/`.
6. Для React UI/components/hooks/frontend tests используйте `skills/react-change-code/`.
7. Для Next.js routing/runtime/cache/server-client work используйте `skills/next-change-code/`.
8. Для старых интеграций, которые уже вызывают `react-next-change-code`, используйте его как совместимый router.

## Принципы

- `SKILL.md` должен быть коротким и дешёвым по токенам.
- Подробные правила должны жить в `references/` и иметь явные условия чтения.
- Router-skill не должен тащить framework-specific правила без необходимости.
- Framework skill должен опираться на базовый language skill, а не копировать его полностью.
- Новые framework-навыки, например Vue/Nuxt или Spring, добавляются отдельным слоем поверх базового language skill.
- Приоритет у локальных правил проекта, установленных версий библиотек и текущей архитектуры.
