# Введение
Мета-вопросы - это вопросы о вопросах, т.е. вопросы, которые подразумевают другие вопросы. В данном документе описывается проект по созданию Telegram-бота, который будет автоматически отвечать на мета-вопросы в чате ссылкой на сайт [nometa.xyz](https://nometa.xyz/). В документе рассмотрены постановка проблемы и цели проекта, определены метрики, а также описаны способы сбора данных, анализа ошибок и этапы интеграции модели.
# Проблемы и цель проекта
Проблема мета-вопросов в больших чатах, где одновременно общаются как начинающие специалисты той или иной области, так и опытные ребята, является распространенной. В общении при личных встречах, люди стараются быть вежливыми, не переходя сразу к проблеме, но общение в чате - это совсем другое. Вместо проявления вежливости, пользователи вынуждены ждать, пока кто-то сформулирует свой вопрос. Это приводит к потере производительности и недовольству участников. Цель проекта - интегрировать Telegram-бота в чат, который автоматически детектирует и отвечает на мета-вопросы, тем самым мотивируя пользователя задавать вопросы грамотно и уменьшая количество мета-вопросов в чате.
# Метрики и лоссы
1. Онлайн метрики
    - Колличество ложных срабатываний
    - Колличество пропущенных мета-вопросов

2. Оффлайн метрики
    - Recall@k
    - Recall@specificity > N%
    - Recall@precision   > N%
3. Технические
    - Скорость ответа
    - Потребление ОЗУ
    - Потребление disk-memory
4. Лоссы
    - LogLoss


# Сбор данных
В качестве данных будут использованы данные из чата [karpov.courses](https://t.me/karpovcourseschat). Данные будут чиститься от ненужных символов и преобразовываться в удобный формат для дальнейшего использования. Для увеличения количества примеров будут генерироваться новые сообщения с помощью ChatGPT.

# Baseline модель
Для решения поставленной задачи мы будем использовать предобученную на русскоязычных текстах легковесную LLM в качестве базовой модели. Она будет получать на вход запросы и классифицировать их на соответствующие категории, а затем на основе ответа модели мы определяем, нужно ли отвечать в чате ссылкой или нет.

# Анализ ошибок
Для анализа ошибок будет проведен анализ влияния различных параметров на качество работы бота, а также определены наиболее часто встречающиеся ошибки и способы их устранения.

# Интеграция и развертывание
После обучения и отладки модели, она будет интегрирована в Telegram-бота и развернута на сервере. Будет проведена интеграционная проверка и настройка, а также определены методы масштабирования, чтобы обеспечить стабильную работу бота при увеличении нагрузки.

В итоге, разработанный Telegram-бот будет обладать способностью автоматически отвечать на мета-вопросы в чате, что поможет уменьшить количество мета-вопросов и улучшить эффективность общения в чате.