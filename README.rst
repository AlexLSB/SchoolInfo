=====
Schoolinfo
=====

Мини-информационная система, поддерживающую данные о школьной образовательной системе.

Настройка и запуск
-----------

#. Установка зависимостей:

.. code-block::

    pip install -r requirements.txt


#. Создание БД:

.. code-block::

    mysql -u <db_user> -p<db_pass> -e 'CREATE DATABASE `schoolinfo` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;'
    mysql -u <db_user> -p<db_pass> schoolinfo << db_dump.sql


#. Запуск:

.. code-block::

    python manage.py runserver


#. Административная панель:

.. code-block::

    login: admin
    pass: ivorydust21
