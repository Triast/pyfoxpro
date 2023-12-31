# Changelog

Все значимые изменения данного проекта будут задокументированы в этом файле.

Данный формат основан на [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
и этот проект следует [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.4] - 2024-01-08

### Изменено

- Убрана замена пробельных строк на функцию SPACE() в поле "expr" в отчётах.

## [0.3.3] - 2024-01-08

### Добавлено

- Добавлено правило для "_PAGENO".

## [0.3.2] - 2024-01-08

### Изменено

- Возвращено изменение двойных кавычек на одинарные в поле "supexpr" в отчётах.

## [0.3.1] - 2024-01-05

### Исправлено

- Убрано форматирование строковых литералов в поле "expr" в отчётах.

## [0.3.0] - 2024-01-05

### Добавлено

- Добавлены новые правила для форматирования.
- Добавлена возможность форматирования файлов меню "*.mnx".
- Добавлена возможность форматирования файлов библиотек классов "*.vcx".
- Добавлена возможность форматирования файлов отчётов "*.frx".

### Исправлено

- Правило "SAVE" поставлено перед ".Save(", так как правило "SAVE" перезаписывало изменения по правилу ".Save(".

## [0.2.0] - 2023-11-02

### Добавлено

- Возможность вызова приложения следующей командой: `python -m pyfoxpro [OPTIONS] /path/to/file`.

## [0.1.0] - 2023-09-08

### Добавлено

- Форматирование форм с помощью команды `pyfoxpro /path/to/file.scx`.
- Форматирование текстовых с помощью команды `pyfoxpro /path/to/file.prg`.

[0.3.4]: http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/compare/v0.3.3...v0.3.4?from_project_id=13&straight=false
[0.3.3]: http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/compare/v0.3.2...v0.3.3?from_project_id=13&straight=false
[0.3.2]: http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/compare/v0.3.1...v0.3.2?from_project_id=13&straight=false
[0.3.1]: http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/compare/v0.3.0...v0.3.1?from_project_id=13&straight=false
[0.3.0]: http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/compare/v0.2.0...v0.3.0?from_project_id=13&straight=false
[0.2.0]: http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/compare/v0.1.0...v0.2.0?from_project_id=13&straight=false
[0.1.0]: http://gitlab.sbyt.gomelenergo.by/i.kamarets/pyfoxpro/-/releases/v0.1.0
