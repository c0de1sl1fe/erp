# gantt_renderer.py
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Union


# def parse_date(value: Optional[str]) -> Optional[date]:
#     if not value:
#         return None
#     return date.fromisoformat(value)

def parse_date(value: Optional[Union[str, List[int]]]) -> Optional[date]:
    if not value:
        return None
    
    # Формат "2025-12-01"
    if isinstance(value, str):
        return date.fromisoformat(value)
    
    # Формат [2025, 12, 1]
    if isinstance(value, list) and len(value) == 3:
        y, m, d = value
        return date(y, m, d)
    
    raise ValueError(f"Unsupported date format: {value}")


def daterange(start: date, end: date, step_days: int = 7):
    """Генератор дат с шагом в N дней (для заголовка-тиков)."""
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=step_days)


def render_gantt1(payload: Dict[str, Any]) -> str:
    """
    Генерирует HTML-ФРАГМЕНТ с одним корневым <main> в стиле диаграммы Ганта.
    Этот фрагмент потом оборачивается в полноценный HTML шаблоном.
    """
    project_name = payload.get("name", "Проект")
    tasks: List[Dict[str, Any]] = payload.get("tasks") or []

    # Собираем даты для вычисления общего интервала
    all_dates: List[date] = []

    # Даты проекта
    for key in ("startDate", "plannedEnd", "actualEnd"):
        d = parse_date(payload.get(key))
        if d:
            all_dates.append(d)

    # Даты задач и блоков
    for t in tasks:
        for key in ("plannedStart", "plannedEnd", "actualEnd"):
            d = parse_date(t.get(key))
            if d:
                all_dates.append(d)
        for b in t.get("blocks") or []:
            for key in ("plannedStart", "plannedEnd", "actualEnd"):
                d = parse_date(b.get(key))
                if d:
                    all_dates.append(d)

    # Если нет дат — заглушка
    if not all_dates:
        return """
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <h3>Нет данных для диаграммы Ганта</h3>
</main>
        """.strip()

    min_date = min(all_dates)
    max_date = max(all_dates)
    total_days = (max_date - min_date).days + 1

    # Функция, которая переводит интервал [start; end] в проценты (left, width)
    def interval_style(start_str: Optional[str], end_str: Optional[str]) -> Optional[str]:
        if not start_str or not end_str:
            return None
        start_d = parse_date(start_str)
        end_d = parse_date(end_str)
        if not start_d or not end_d:
            return None
        if end_d < start_d:
            end_d = start_d

        left_days = (start_d - min_date).days
        duration_days = (end_d - start_d).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return f"left:{left_pct:.4f}%;width:{width_pct:.4f}%;"

    # ---------- ЛЕВАЯ КОЛОНКА (labels) ----------

    labels_rows: List[str] = []
    # (удалена служебная пустая строка — временной ряд с датами отключён)
    
    for t in tasks:
        t_name = t.get("name", "Task")
        # строка-задача
        labels_rows.append(
            f'<div class="row task">{t_name}</div>'
        )
        # строки-блоки
        for b in t.get("blocks") or []:
            b_name = b.get("name", "Block")
            labels_rows.append(
                f'<div class="row block">{b_name}</div>'
            )
    
    labels_html = "\n      ".join(labels_rows)

    # ---------- ПРАВАЯ ЧАСТЬ (chart) ----------

    # (заголовок с тиками отключён по запросу)
    ticks_html = ""

    # min-width для rows
    rows_min_width = "720px"

    rows_html_parts: List[str] = []
    # Собираем метки дат в одну строку — укороченный формат DD.MM
    date_labels: List[str] = []
    # (удалена служебная пустая строка — временной ряд с датами отключён)
    
    def interval_pct(start_str: Optional[str], end_str: Optional[str]):
        """Возвращает (left_pct, width_pct, start_date, end_date) или None"""
        if not start_str or not end_str:
            return None
        s = parse_date(start_str)
        e = parse_date(end_str)
        if not s or not e:
            return None
        if e < s:
            e = s
        left_days = (s - min_date).days
        duration_days = (e - s).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return (left_pct, width_pct, s, e)
    
    # минимальное расстояние между двумя метками в пикселях — если меньше,
    # отображаем только более позднюю (end) дату, чтобы избежать наложения.
    min_sep_px = 48
    container_px = int(rows_min_width.replace("px", "")) if isinstance(rows_min_width, str) and rows_min_width.endswith("px") else 720
    min_sep_pct = min_sep_px / container_px * 100.0
    
    for t in tasks:
        # Для group-bg задачи нужны минимальный и максимальный интервал по её блокам
        block_dates: List[date] = []
        for b in t.get("blocks") or []:
            bs = parse_date(b.get("plannedStart"))
            be = parse_date(b.get("plannedEnd"))
            if bs:
                block_dates.append(bs)
            if be:
                block_dates.append(be)
 
        group_bg_html = ""
        if block_dates:
            group_min = min(block_dates)
            group_max = max(block_dates)
            # Считаем проценты для group-bg
            left_days = (group_min - min_date).days
            duration_days = (group_max - group_min).days + 1
            left_pct = left_days / total_days * 100.0
            width_pct = duration_days / total_days * 100.0
            group_bg_html = (
                f'<div class="group-bg" style="left:{left_pct:.4f}%;'
                f' width:{width_pct:.4f}%;"></div>'
            )
 
        # 1) строка-группа для задачи (только group-bg)
        rows_html_parts.append(
            f'<div class="row">{group_bg_html}</div>'
        )
 
        # 2) строки по блокам задачи
        for b in t.get("blocks") or []:
            b_name = b.get("name", "Block")
 
            planned_style = interval_style(b.get("plannedStart"), b.get("plannedEnd"))
            actual_style = interval_style(b.get("plannedStart"), b.get("actualEnd"))
 
            bars_for_row: List[str] = []
 
            if planned_style:
                bars_for_row.append(
                    f'<div class="bar" style="{planned_style}">{b_name}</div>'
                )
 
            if actual_style:
                bars_for_row.append(
                    f'<div class="bar actual" style="{actual_style}">{b_name} (факт)</div>'
                )
 
            bars_html = "\n          ".join(bars_for_row) if bars_for_row else ""
            rows_html_parts.append(
                f'<div class="row">\n          {bars_html}\n        </div>'
            )
 
            # Для этой же строки формируем короткие подписи дат (DD.MM) и собираем их в одну строку.
            # Если две метки слишком близко (в пикселях), отображаем только более позднюю,
            # чтобы избежать визуального слипания.
            pct = interval_pct(b.get("plannedStart"), b.get("plannedEnd"))
            if pct:
                left_pct, width_pct, s_dt, e_dt = pct
                start_left = left_pct
                end_left = left_pct + width_pct
                start_label = (
                    f'<div class="date start" style="left:{start_left:.4f}%">'
                    f'{s_dt.strftime("%d.%m")}</div>'
                )
                end_label = (
                    f'<div class="date end" style="left:{end_left:.4f}%">'
                    f'{e_dt.strftime("%d.%m")}</div>'
                )
                # Если расстояние между метками меньше порога — показываем только более позднюю
                if (end_left - start_left) < min_sep_pct:
                    date_labels.append(end_label)
                else:
                    date_labels.append(start_label)
                    date_labels.append(end_label)
            # если у блока нет валидных дат — ничего не добавляем
 
    rows_html = "\n        ".join(rows_html_parts)
    # Объединяем все метки в одну строку
    if date_labels:
        dates_html = "<div class=\"date-row\">\\n          " + "\\n          ".join(date_labels) + "\\n        </div>"
    else:
        dates_html = "<div class=\"date-row\"></div>"

    # ---------- СБОРКА HTML-ФРАГМЕНТА (один <main>) ----------

    html_fragment = f"""
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <style>
    :root {{
      --row-h: 40px;
      --labels-w: 260px;
      --chart-w: 920px;
      --accent-planned: #2b9cf3;
      --accent-actual: #f39c12;
      --accent-group: #e9eef6;
    }}

    .gantt {{
      display: flex;
      gap: 12px;
      align-items: flex-start;
      width: 100%;
      max-width: 1200px;
    }}

    .labels {{
      width: var(--labels-w);
      min-width: var(--labels-w);
      box-sizing: border-box;
    }}

    .labels .row {{
      height: var(--row-h);
      min-height: var(--row-h);
      max-height: var(--row-h);
      overflow: hidden;
      line-height: 1.3;
      display: flex;
      align-items: center;
      padding: 0 8px;
      border-bottom: 1px dashed #eee;
      box-sizing: border-box;
      white-space: nowrap;
      text-overflow: ellipsis;
    }}
    
    .rows .row {{
      position: relative; /* each row is a positioning context for absolute children (bars/group-bg) */
      height: var(--row-h);
      min-height: var(--row-h);
      max-height: var(--row-h);
      line-height: 1.3;
      display: flex;
      align-items: center;
      padding: 0 8px;
      border-bottom: 1px dashed #eee;
      box-sizing: border-box;
      overflow: hidden;
    }}

    .labels .task {{
      font-weight: 700;
      color: #111;
    }}

    .labels .block {{
      padding-left: 12px;
      color: #444;
      font-size: 0.95em;
    }}

    .chart-wrap {{
      border: 1px solid #efefef;
      width: var(--chart-w);
      overflow: auto;
    }}

    .chart-header {{
      display: flex;
      height: var(--row-h);
      border-bottom: 1px solid #ddd;
      background: white;
    }}

    .tick {{
      flex: 0 0 60px;
      text-align: center;
      padding-top: 8px;
      font-size: 12px;
      border-right: 1px solid #f5f5f5;
      box-sizing: border-box;
    }}

    .rows {{
      position: relative;
      min-width: {rows_min_width};
    }}
 
    /* .rows .row moved to combined selector above */
 
    .dates {{
      border-top: 1px solid #eee;
    }}
    .date-row {{
      position: relative;
      height: var(--row-h);
      min-height: var(--row-h);
      display: block;
      box-sizing: border-box;
      font-size: 12px;
      color: #222;
    }}
    .date {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      padding: 2px 6px;
      white-space: nowrap;
      font-size: 12px;
      color: #222;
      pointer-events: none;
    }}
    .date.end {{
      transform: translate(-100%, -50%);
    }}
 
    .group-bg {{
      position: absolute;
      height: 12px;
      top: 50%;
      left: 0;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-group);
      opacity: 0.8;
    }}

    .bar {{
      position: absolute;
      white-space: normal;
      line-height: 1.3;
      height: auto;
      min-height: 20px;
      padding: 4px 8px;
      top: 50%;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-planned);
      color: white;
      display: flex;
      align-items: center;
      font-size: 12px;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.06);
      overflow: visible;
      box-sizing: border-box;
    }}

    .bar.actual {{
      background: transparent;
      border: 2px dashed var(--accent-actual);
      color: var(--accent-actual);
    }}

    .legend {{
      margin-top: 12px;
      font-size: 13px;
    }}

    .legend .item {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      margin-right: 16px;
    }}

    .sw {{
      width: 22px;
      height: 12px;
      border-radius: 3px;
      display: inline-block;
    }}

    .sw.group {{
      background: var(--accent-group);
    }}

    .sw.planned {{
      background: var(--accent-planned);
    }}

    .sw.actual {{
      border: 2px dashed var(--accent-actual);
      background: transparent;
    }}

    @media (max-width:1024px) {{
      :root {{
        --chart-w: 720px;
      }}
    }}
  </style>

  <h3 style="margin:0 0 12px 0">{project_name}</h3>

  <div class="gantt">
    <div class="labels" aria-hidden="true">
      {labels_html}
    </div>

    <div class="chart-wrap" role="img" aria-label="Gantt chart">

      <div class="rows">
        {rows_html}
      </div>
      <div class="dates" aria-hidden="true">
        {dates_html}
      </div>
    </div>
  </div>

  <div class="legend" aria-hidden="true">
    <span class="item"><span class="sw group"></span> Задача (интервал по блокам)</span>
    <span class="item"><span class="sw planned"></span> Плановый интервал блока</span>
    <span class="item"><span class="sw actual"></span> Фактический интервал (пунктир)</span>
  </div>
</main>
    """.strip()

    return html_fragment


def render_stats(payload: Dict[str, Any]) -> str:
    """
    Рендерит HTML-блок со статистикой проекта:
    - задачи в работе / не начатые / завершённые
    - блоки в работе / не начатые / завершённые

    Ожидает, что у задач и блоков в JSON есть поле "status".
    """
    project_name = payload.get("name", "Проект")
    tasks: List[Dict[str, Any]] = payload.get("tasks") or []

    # Счётчики задач
    tasks_in_progress = 0
    tasks_not_started = 0
    tasks_completed = 0

    # Счётчики блоков
    blocks_in_progress = 0
    blocks_not_started = 0
    blocks_completed = 0

    # Маппинги статусов
    TASK_IN_PROGRESS = {"IN_PROGRESS"}
    TASK_COMPLETED = {"COMPLETED"}
    TASK_NOT_STARTED = {"DRAFT", "ON_HOLD", None, ""}

    BLOCK_IN_PROGRESS = {"IN_PROGRESS"}
    BLOCK_COMPLETED = {"COMPLETED"}
    BLOCK_NOT_STARTED = {"WAITING", "READY", None, ""}

    for t in tasks:
        t_status = (t.get("status") or "").upper() or None

        if t_status in TASK_COMPLETED:
            tasks_completed += 1
        elif t_status in TASK_IN_PROGRESS:
            tasks_in_progress += 1
        else:
            # Всё остальное считаем "не начато/отложено"
            tasks_not_started += 1

        for b in t.get("blocks") or []:
            b_status = (b.get("status") or "").upper() or None

            if b_status in BLOCK_COMPLETED:
                blocks_completed += 1
            elif b_status in BLOCK_IN_PROGRESS:
                blocks_in_progress += 1
            else:
                blocks_not_started += 1

    def fmt(n: int) -> str:
        return "—" if n == 0 else str(n)

    html_fragment = f"""
<section class="stats-root" style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#0f172a;">
  <style>
    .stats-root {{
      font-family: Inter, Roboto, Arial, sans-serif;
      color: #0f172a;
    }}

    .stats-card {{
      background: #ffffff;
      border-radius: 20px;
      box-shadow: 0 20px 40px rgba(15, 23, 42, 0.06);
      padding: 20px 24px;
      max-width: 100%;
      box-sizing: border-box;
    }}

    .stats-title-main {{
      font-size: 22px;
      font-weight: 700;
      margin: 0 0 12px 0;
    }}

    .stats-title-sub {{
      font-size: 16px;
      font-weight: 600;
      margin: 0 0 16px 0;
    }}

    .stats-row {{
      display: flex;
      gap: 12px;
      overflow-x: auto;
      padding-bottom: 4px;
    }}

    .stat-item {{
      min-width: 170px;
      background: #f9fafb;
      border-radius: 16px;
      padding: 14px 16px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
      text-align: center;
      box-sizing: border-box;
    }}

    .stat-value {{
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 4px;
    }}

    .stat-label {{
      font-size: 13px;
      color: #6b7280;
    }}

    @media (max-width: 768px) {{
      .stats-card {{
        padding: 16px 16px;
      }}
      .stats-title-main {{
        font-size: 20px;
      }}
      .stats-row {{
        gap: 8px;
      }}
      .stat-item {{
        min-width: 150px;
      }}
    }}
  </style>

  <div class="stats-card">
    <h2 class="stats-title-main">Статистика</h2>
    <h3 class="stats-title-sub">Статистика проекта: {project_name}</h3>

    <div class="stats-row">
      <div class="stat-item">
        <div class="stat-value">{fmt(tasks_in_progress)}</div>
        <div class="stat-label">Задачи в работе</div>
      </div>

      <div class="stat-item">
        <div class="stat-value">{fmt(tasks_not_started)}</div>
        <div class="stat-label">Не начатые задачи</div>
      </div>

      <div class="stat-item">
        <div class="stat-value">{fmt(tasks_completed)}</div>
        <div class="stat-label">Завершённые задачи</div>
      </div>

      <div class="stat-item">
        <div class="stat-value">{fmt(blocks_in_progress)}</div>
        <div class="stat-label">Блоки в работе</div>
      </div>

      <div class="stat-item">
        <div class="stat-value">{fmt(blocks_not_started)}</div>
        <div class="stat-label">Не начатые блоки</div>
      </div>

      <div class="stat-item">
        <div class="stat-value">{fmt(blocks_completed)}</div>
        <div class="stat-label">Завершённые блоки</div>
      </div>
    </div>
  </div>
</section>
    """.strip()

    return html_fragment


def render_gantt2(payload: Dict[str, Any]) -> str:
    """
    Генерирует HTML-ФРАГМЕНТ с одним корным <main> в стиле диаграммы Ганта.
    Этот фрагмент потом оборачивается в полноценный HTML шаблоном.
    """
    project_name = payload.get("name", "Проект")
    tasks: List[Dict[str, Any]] = payload.get("tasks") or []

    # Собираем даты для вычисления общего интервала
    all_dates: List[date] = []

    # Даты проекта
    for key in ("startDate", "plannedEnd", "actualEnd"):
        d = parse_date(payload.get(key))
        if d:
            all_dates.append(d)

    # Даты задач и блоков
    for t in tasks:
        for key in ("plannedStart", "plannedEnd", "actualEnd"):
            d = parse_date(t.get(key))
            if d:
                all_dates.append(d)
        for b in t.get("blocks") or []:
            for key in ("plannedStart", "plannedEnd", "actualEnd"):
                d = parse_date(b.get(key))
                if d:
                    all_dates.append(d)

    # Если нет дат — заглушка
    if not all_dates:
        return """
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <h3>Нет данных для диаграммы Ганта</h3>
</main>
        """.strip()

    min_date = min(all_dates)
    max_date = max(all_dates)
    total_days = (max_date - min_date).days + 1

    # Функция, которая переводит интервал [start; end] в проценты (left, width)
    def interval_style(start_str: Optional[str], end_str: Optional[str]) -> Optional[str]:
        if not start_str or not end_str:
            return None
        start_d = parse_date(start_str)
        end_d = parse_date(end_str)
        if not start_d or not end_d:
            return None
        if end_d < start_d:
            end_d = start_d

        left_days = (start_d - min_date).days
        duration_days = (end_d - start_d).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return f"left:{left_pct:.4f}%;width:{width_pct:.4f}%;"

    # ---------- ЛЕВАЯ КОЛОНКА (labels) ----------

    labels_rows: List[str] = []
    for t in tasks:
        t_name = t.get("name", "Task")
        labels_rows.append(f'<div class="row task">{t_name}</div>')
        for b in t.get("blocks") or []:
            b_name = b.get("name", "Block")
            labels_rows.append(f'<div class="row block">{b_name}</div>')
    
    labels_html = "\n      ".join(labels_rows)

    # ---------- ПРАВАЯ ЧАСТЬ (chart) ----------

    rows_min_width = "720px"
    container_px = 720  # фиксированная ширина для расчёта min_sep

    rows_html_parts: List[str] = []
    # Новый список: все подписи дат как (left_pct, html)
    all_date_labels: List[tuple[float, str]] = []

    def interval_pct(start_str: Optional[str], end_str: Optional[str]):
        if not start_str or not end_str:
            return None
        s = parse_date(start_str)
        e = parse_date(end_str)
        if not s or not e:
            return None
        if e < s:
            e = s
        left_days = (s - min_date).days
        duration_days = (e - s).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return (left_pct, width_pct, s, e)

    for t in tasks:
        # Для group-bg задачи нужны минимальный и максимальный интервал по её блокам
        block_dates: List[date] = []
        for b in t.get("blocks") or []:
            bs = parse_date(b.get("plannedStart"))
            be = parse_date(b.get("plannedEnd"))
            if bs:
                block_dates.append(bs)
            if be:
                block_dates.append(be)
 
        group_bg_html = ""
        if block_dates:
            group_min = min(block_dates)
            group_max = max(block_dates)
            left_days = (group_min - min_date).days
            duration_days = (group_max - group_min).days + 1
            left_pct = left_days / total_days * 100.0
            width_pct = duration_days / total_days * 100.0
            group_bg_html = (
                f'<div class="group-bg" style="left:{left_pct:.4f}%;'
                f' width:{width_pct:.4f}%;"></div>'
            )
 
        rows_html_parts.append(f'<div class="row">{group_bg_html}</div>')
 
        for b in t.get("blocks") or []:
            b_name = b.get("name", "Block")
 
            planned_style = interval_style(b.get("plannedStart"), b.get("plannedEnd"))
            actual_style = interval_style(b.get("plannedStart"), b.get("actualEnd"))
 
            bars_for_row: List[str] = []
 
            if planned_style:
                bars_for_row.append(
                    f'<div class="bar" style="{planned_style}">{b_name}</div>'
                )
 
            if actual_style:
                bars_for_row.append(
                    f'<div class="bar actual" style="{actual_style}">{b_name} (факт)</div>'
                )
 
            bars_html = "\n          ".join(bars_for_row) if bars_for_row else ""
            rows_html_parts.append(
                f'<div class="row">\n          {bars_html}\n        </div>'
            )
 
            # === СОБИРАЕМ ДАТЫ В ОБЩИЙ СПИСОК ===
            pct = interval_pct(b.get("plannedStart"), b.get("plannedEnd"))
            if pct:
                left_pct, width_pct, s_dt, e_dt = pct
                start_left = left_pct
                end_left = left_pct + width_pct

                start_label_html = (
                    f'<div class="date start" style="left:{start_left:.4f}%">'
                    f'{s_dt.strftime("%d.%m")}</div>'
                )
                end_label_html = (
                    f'<div class="date end" style="left:{end_left:.4f}%">'
                    f'{e_dt.strftime("%d.%m")}</div>'
                )

                all_date_labels.append((start_left, start_label_html))
                all_date_labels.append((end_left, end_label_html))

    rows_html = "\n        ".join(rows_html_parts)

    # === ФИЛЬТРАЦИЯ ДАТ ПО ВИЗУАЛЬНОМУ РАССТОЯНИЮ ===
    min_sep_px = 48
    min_sep_pct = min_sep_px / container_px * 100.0

    # Сортируем по позиции
    all_date_labels.sort(key=lambda x: x[0])

    filtered_date_labels: List[str] = []
    last_used_left = -float('inf')

    for left_pct, html in all_date_labels:
        if left_pct - last_used_left >= min_sep_pct:
            filtered_date_labels.append(html)
            last_used_left = left_pct

    dates_html = "<div class=\"date-row\">\n          " + "\n          ".join(filtered_date_labels) + "\n        </div>"
    dates_html = "<div class=\"date-row\">\\n          " + "\\n          ".join(filtered_date_labels) + "\\n        </div>"

    # ---------- СБОРКА HTML-ФРАГМЕНТА (один <main>) ----------

    html_fragment = f"""
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <style>
    :root {{
      --row-h: 40px;
      --labels-w: 260px;
      --chart-w: 920px;
      --accent-planned: #2b9cf3;
      --accent-actual: #f39c12;
      --accent-group: #e9eef6;
    }}

    .gantt {{
      display: flex;
      gap: 12px;
      align-items: flex-start;
      width: 100%;
      max-width: 1200px;
    }}

    .labels {{
      width: var(--labels-w);
      min-width: var(--labels-w);
      box-sizing: border-box;
    }}

    .labels .row {{
      height: var(--row-h);
      min-height: var(--row-h);
      max-height: var(--row-h);
      overflow: hidden;
      line-height: 1.3;
      display: flex;
      align-items: center;
      padding: 0 8px;
      border-bottom: 1px dashed #eee;
      box-sizing: border-box;
      white-space: nowrap;
      text-overflow: ellipsis;
    }}
    
    .rows .row {{
      position: relative;
      height: var(--row-h);
      min-height: var(--row-h);
      max-height: var(--row-h);
      line-height: 1.3;
      display: flex;
      align-items: center;
      padding: 0 8px;
      border-bottom: 1px dashed #eee;
      box-sizing: border-box;
      overflow: hidden;
    }}

    .labels .task {{
      font-weight: 700;
      color: #111;
    }}

    .labels .block {{
      padding-left: 12px;
      color: #444;
      font-size: 0.95em;
    }}

    .chart-wrap {{
      border: 1px solid #efefef;
      width: var(--chart-w);
      overflow: auto;
    }}

    .rows {{
      position: relative;
      min-width: {rows_min_width};
    }}
 
    .dates {{
      border-top: 1px solid #eee;
    }}
    .date-row {{
      position: relative;
      height: var(--row-h);
      min-height: var(--row-h);
      display: block;
      box-sizing: border-box;
      font-size: 12px;
      color: #222;
    }}
    .date {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      padding: 2px 6px;
      white-space: nowrap;
      font-size: 12px;
      color: #222;
      pointer-events: none;
      z-index: 10;
    }}
    .date.end {{
      transform: translate(-100%, -50%);
    }}
 
    .group-bg {{
      position: absolute;
      height: 12px;
      top: 50%;
      left: 0;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-group);
      opacity: 0.8;
    }}

    .bar {{
      position: absolute;
      white-space: normal;
      line-height: 1.3;
      height: auto;
      min-height: 20px;
      padding: 4px 8px;
      top: 50%;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-planned);
      color: white;
      display: flex;
      align-items: center;
      font-size: 12px;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.06);
      overflow: visible;
      box-sizing: border-box;
    }}

    .bar.actual {{
      background: transparent;
      border: 2px dashed var(--accent-actual);
      color: var(--accent-actual);
    }}

    .legend {{
      margin-top: 12px;
      font-size: 13px;
    }}

    .legend .item {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      margin-right: 16px;
    }}

    .sw {{
      width: 22px;
      height: 12px;
      border-radius: 3px;
      display: inline-block;
    }}

    .sw.group {{
      background: var(--accent-group);
    }}

    .sw.planned {{
      background: var(--accent-planned);
    }}

    .sw.actual {{
      border: 2px dashed var(--accent-actual);
      background: transparent;
    }}

    @media (max-width:1024px) {{
      :root {{
        --chart-w: 720px;
      }}
    }}
  </style>

  <h3 style="margin:0 0 12px 0">{project_name}</h3>

  <div class="gantt">
    <div class="labels" aria-hidden="true">
      {labels_html}
    </div>

    <div class="chart-wrap" role="img" aria-label="Gantt chart">
      <div class="rows">
        {rows_html}
      </div>
      <div class="dates" aria-hidden="true">
        {dates_html}
      </div>
    </div>
  </div>

  <div class="legend" aria-hidden="true">
    <span class="item"><span class="sw group"></span> Задача (интервал по блокам)</span>
    <span class="item"><span class="sw planned"></span> Плановый интервал блока</span>
    <span class="item"><span class="sw actual"></span> Фактический интервал (пунктир)</span>
  </div>
</main>
    """.strip()

    return html_fragment

def render_gantt_good(payload: Dict[str, Any]) -> str:
    """
    Генерирует HTML-фрагмент диаграммы Ганта с синхронизированной высотой строк.
    """
    project_name = payload.get("name", "Проект")
    tasks: List[Dict[str, Any]] = payload.get("tasks") or []

    # Собираем даты для вычисления общего интервала
    all_dates: List[date] = []

    for key in ("startDate", "plannedEnd", "actualEnd"):
        d = parse_date(payload.get(key))
        if d:
            all_dates.append(d)

    for t in tasks:
        for key in ("plannedStart", "plannedEnd", "actualEnd"):
            d = parse_date(t.get(key))
            if d:
                all_dates.append(d)
        for b in t.get("blocks") or []:
            for key in ("plannedStart", "plannedEnd", "actualEnd"):
                d = parse_date(b.get(key))
                if d:
                    all_dates.append(d)

    if not all_dates:
        return """
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <h3>Нет данных для диаграммы Ганта</h3>
</main>
        """.strip()

    min_date = min(all_dates)
    max_date = max(all_dates)
    total_days = (max_date - min_date).days + 1

    def interval_style(start_str: Optional[str], end_str: Optional[str]) -> Optional[str]:
        if not start_str or not end_str:
            return None
        start_d = parse_date(start_str)
        end_d = parse_date(end_str)
        if not start_d or not end_d:
            return None
        if end_d < start_d:
            end_d = start_d
        left_days = (start_d - min_date).days
        duration_days = (end_d - start_d).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return f"left:{left_pct:.4f}%;width:{width_pct:.4f}%;"

    def interval_pct(start_str: Optional[str], end_str: Optional[str]):
        if not start_str or not end_str:
            return None
        s = parse_date(start_str)
        e = parse_date(end_str)
        if not s or not e:
            return None
        if e < s:
            e = s
        left_days = (s - min_date).days
        duration_days = (e - s).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return (left_pct, width_pct, s, e)

    # === СОБИРАЕМ СТРОКИ КАК СПИСОК ЭЛЕМЕНТОВ ===
    gantt_rows: List[str] = []
    all_date_labels: List[tuple[float, str]] = []

    for t in tasks:
        # --- 1. Строка задачи (заголовок группы) ---
        task_name = t.get("name", "Task")
        block_dates: List[date] = []
        for b in t.get("blocks") or []:
            bs = parse_date(b.get("plannedStart"))
            be = parse_date(b.get("plannedEnd"))
            if bs:
                block_dates.append(bs)
            if be:
                block_dates.append(be)

        group_bg_style = ""
        if block_dates:
            group_min = min(block_dates)
            group_max = max(block_dates)
            left_days = (group_min - min_date).days
            duration_days = (group_max - group_min).days + 1
            left_pct = left_days / total_days * 100.0
            width_pct = duration_days / total_days * 100.0
            group_bg_style = f"left:{left_pct:.4f}%; width:{width_pct:.4f}%;"

        gantt_rows.append(f"""
          <div class="gantt-row">
            <div class="label-cell task">{task_name}</div>
            <div class="chart-cell">
              {f'<div class="group-bg" style="{group_bg_style}"></div>' if group_bg_style else ''}
            </div>
          </div>
        """.strip())

        # --- 2. Строки блоков ---
        for b in t.get("blocks") or []:
            b_name = b.get("name", "Block")
            planned_style = interval_style(b.get("plannedStart"), b.get("plannedEnd"))
            actual_style = interval_style(b.get("plannedStart"), b.get("actualEnd"))

            bars_html = ""
            if planned_style:
                bars_html += f'<div class="bar" style="{planned_style}">{b_name}</div>'
            if actual_style:
                bars_html += f'<div class="bar actual" style="{actual_style}">{b_name} (факт)</div>'

            gantt_rows.append(f"""
              <div class="gantt-row">
                <div class="label-cell block">{b_name}</div>
                <div class="chart-cell">
                  {bars_html}
                </div>
              </div>
            """.strip())

            # Собираем даты
            pct = interval_pct(b.get("plannedStart"), b.get("plannedEnd"))
            if pct:
                left_pct, width_pct, s_dt, e_dt = pct
                start_left = left_pct
                end_left = left_pct + width_pct
                start_label = f'<div class="date start" style="left:{start_left:.4f}%">{s_dt.strftime("%d.%m")}</div>'
                end_label = f'<div class="date end" style="left:{end_left:.4f}%">{e_dt.strftime("%d.%m")}</div>'
                all_date_labels.append((start_left, start_label))
                all_date_labels.append((end_left, end_label))

    rows_html = "\n        ".join(gantt_rows)

    # === ФИЛЬТРАЦИЯ ДАТ ===
    container_px = 720
    min_sep_px = 48
    min_sep_pct = min_sep_px / container_px * 100.0
    all_date_labels.sort(key=lambda x: x[0])
    filtered_date_labels = []
    last_used = -float('inf')
    for left, html in all_date_labels:
        if left - last_used >= min_sep_pct:
            filtered_date_labels.append(html)
            last_used = left

    dates_html = "<div class=\"date-row\">\n          " + "\n          ".join(filtered_date_labels) + "\n        </div>"

    # === ГЕНЕРАЦИЯ HTML ===
    html_fragment = f"""
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <style>
    :root {{
      --labels-w: 260px;
      --chart-w: 920px;
      --accent-planned: #2b9cf3;
      --accent-actual: #f39c12;
      --accent-group: #e9eef6;
      --row-min-h: 40px;
    }}

    .gantt-container {{
      max-width: 1200px;
      width: 100%;
      display: flex;
      flex-direction: column;
    }}

    .gantt-rows {{
      display: grid;
      grid-template-columns: var(--labels-w) 1fr;
      width: calc(var(--labels-w) + var(--chart-w));
      min-width: calc(var(--labels-w) + 720px);
    }}

    .gantt-row {{
      display: contents; /* делает ячейки прямыми детьми grid-контейнера */
    }}

    .label-cell {{
      padding: 8px;
      border-bottom: 1px dashed #eee;
      box-sizing: border-box;
      word-break: break-word;
      white-space: normal;
      line-height: 1.4;
      min-height: var(--row-min-h);
      display: flex;
      align-items: flex-start;
    }}

    .label-cell.task {{
      font-weight: 700;
      color: #111;
    }}

    .label-cell.block {{
      padding-left: 12px;
      color: #444;
      font-size: 0.95em;
    }}

    .chart-cell {{
      position: relative;
      padding: 0 8px;
      border-bottom: 1px dashed #eee;
      min-height: var(--row-min-h);
      box-sizing: border-box;
    }}

    .chart-wrap {{
      border: 1px solid #efefef;
      width: var(--chart-w);
      overflow: auto;
    }}

    .dates {{
      border-top: 1px solid #eee;
      width: var(--chart-w);
      min-width: 720px;
    }}

    .date-row {{
      position: relative;
      height: 40px;
      min-height: 40px;
      display: block;
      box-sizing: border-box;
      font-size: 12px;
      color: #222;
    }}

    .date {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      padding: 2px 6px;
      white-space: nowrap;
      font-size: 12px;
      color: #222;
      pointer-events: none;
      z-index: 10;
    }}

    .date.end {{
      transform: translate(-100%, -50%);
    }}

    .group-bg {{
      position: absolute;
      height: 12px;
      top: 50%;
      left: 0;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-group);
      opacity: 0.8;
    }}

    .bar {{
      position: absolute;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      height: 24px;
      min-height: 24px;
      max-height: 24px;
      padding: 0 8px;
      top: 50%;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-planned);
      color: white;
      display: flex;
      align-items: center;
      font-size: 12px;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.06);
      box-sizing: border-box;
    }}

    .bar.actual {{
      background: transparent;
      border: 2px dashed var(--accent-actual);
      color: var(--accent-actual);
    }}

    .legend {{
      margin-top: 12px;
      font-size: 13px;
    }}

    .legend .item {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      margin-right: 16px;
    }}

    .sw {{
      width: 22px;
      height: 12px;
      border-radius: 3px;
      display: inline-block;
    }}

    .sw.group {{
      background: var(--accent-group);
    }}

    .sw.planned {{
      background: var(--accent-planned);
    }}

    .sw.actual {{
      border: 2px dashed var(--accent-actual);
      background: transparent;
    }}

    @media (max-width:1024px) {{
      :root {{
        --chart-w: 720px;
      }}
      .gantt-rows {{
        min-width: calc(var(--labels-w) + 720px);
      }}
      .chart-wrap,
      .dates {{
        width: 720px;
      }}
    }}
  </style>

  <h3 style="margin:0 0 12px 0">{project_name}</h3>

  <div class="gantt-container">
    <div class="chart-wrap">
      <div class="gantt-rows">
        {rows_html}
      </div>
    </div>
    <div class="dates" aria-hidden="true">
      {dates_html}
    </div>
  </div>

  <div class="legend" aria-hidden="true">
    <span class="item"><span class="sw group"></span> Задача (интервал по блокам)</span>
    <span class="item"><span class="sw planned"></span> Плановый интервал блока</span>
    <span class="item"><span class="sw actual"></span> Фактический интервал (пунктир)</span>
  </div>
</main>
    """.strip()

    return html_fragment
def render_gantt_pretty_good(payload: Dict[str, Any]) -> str:
    """
    Генерирует HTML-фрагмент диаграммы Ганта с синхронизированной высотой строк
    и растягиваемой по ширине диаграммой.
    """
    project_name = payload.get("name", "Проект")
    tasks: List[Dict[str, Any]] = payload.get("tasks") or []

    # Собираем даты для вычисления общего интервала
    all_dates: List[date] = []

    for key in ("startDate", "plannedEnd", "actualEnd"):
        d = parse_date(payload.get(key))
        if d:
            all_dates.append(d)

    for t in tasks:
        for key in ("plannedStart", "plannedEnd", "actualEnd"):
            d = parse_date(t.get(key))
            if d:
                all_dates.append(d)
        for b in t.get("blocks") or []:
            for key in ("plannedStart", "plannedEnd", "actualEnd"):
                d = parse_date(b.get(key))
                if d:
                    all_dates.append(d)

    if not all_dates:
        return """
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <h3>Нет данных для диаграммы Ганта</h3>
</main>
        """.strip()

    min_date = min(all_dates)
    max_date = max(all_dates)
    total_days = (max_date - min_date).days + 1

    def interval_style(start_str: Optional[str], end_str: Optional[str]) -> Optional[str]:
        if not start_str or not end_str:
            return None
        start_d = parse_date(start_str)
        end_d = parse_date(end_str)
        if not start_d or not end_d:
            return None
        if end_d < start_d:
            end_d = start_d
        left_days = (start_d - min_date).days
        duration_days = (end_d - start_d).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return f"left:{left_pct:.4f}%;width:{width_pct:.4f}%;"

    def interval_pct(start_str: Optional[str], end_str: Optional[str]):
        if not start_str or not end_str:
            return None
        s = parse_date(start_str)
        e = parse_date(end_str)
        if not s or not e:
            return None
        if e < s:
            e = s
        left_days = (s - min_date).days
        duration_days = (e - s).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return (left_pct, width_pct, s, e)

    # === СОБИРАЕМ СТРОКИ ===
    gantt_rows: List[str] = []
    all_date_labels: List[tuple[float, str]] = []

    for t in tasks:
        task_name = t.get("name", "Task")
        block_dates: List[date] = []
        for b in t.get("blocks") or []:
            bs = parse_date(b.get("plannedStart"))
            be = parse_date(b.get("plannedEnd"))
            if bs:
                block_dates.append(bs)
            if be:
                block_dates.append(be)

        group_bg_style = ""
        if block_dates:
            group_min = min(block_dates)
            group_max = max(block_dates)
            left_days = (group_min - min_date).days
            duration_days = (group_max - group_min).days + 1
            left_pct = left_days / total_days * 100.0
            width_pct = duration_days / total_days * 100.0
            group_bg_style = f"left:{left_pct:.4f}%; width:{width_pct:.4f}%;"

        gantt_rows.append(f"""
          <div class="gantt-row">
            <div class="label-cell task">{task_name}</div>
            <div class="chart-cell">
              {f'<div class="group-bg" style="{group_bg_style}"></div>' if group_bg_style else ''}
            </div>
          </div>
        """.strip())

        for b in t.get("blocks") or []:
            b_name = b.get("name", "Block")
            planned_style = interval_style(b.get("plannedStart"), b.get("plannedEnd"))
            actual_style = interval_style(b.get("plannedStart"), b.get("actualEnd"))

            bars_html = ""
            if planned_style:
                bars_html += f'<div class="bar" style="{planned_style}">{b_name}</div>'
            if actual_style:
                bars_html += f'<div class="bar actual" style="{actual_style}">{b_name} (факт)</div>'

            gantt_rows.append(f"""
              <div class="gantt-row">
                <div class="label-cell block">{b_name}</div>
                <div class="chart-cell">
                  {bars_html}
                </div>
              </div>
            """.strip())

            pct = interval_pct(b.get("plannedStart"), b.get("plannedEnd"))
            if pct:
                left_pct, width_pct, s_dt, e_dt = pct
                start_left = left_pct
                end_left = left_pct + width_pct
                start_label = f'<div class="date start" style="left:{start_left:.4f}%">{s_dt.strftime("%d.%m")}</div>'
                end_label = f'<div class="date end" style="left:{end_left:.4f}%">{e_dt.strftime("%d.%m")}</div>'
                all_date_labels.append((start_left, start_label))
                all_date_labels.append((end_left, end_label))

    rows_html = "\n        ".join(gantt_rows)

    # === ФИЛЬТРАЦИЯ ДАТ (используем относительные расстояния, не px!) ===
    # Теперь мы не можем использовать фиксированные px, потому что ширина динамическая.
    # Вместо этого фильтруем на основе минимального "процентного" расстояния.
    # Пусть минимальное расстояние = 5% (достаточно для большинства случаев)
    min_sep_pct = 5.0
    all_date_labels.sort(key=lambda x: x[0])
    filtered_date_labels = []
    last_used = -float('inf')
    for left, html in all_date_labels:
        if left - last_used >= min_sep_pct:
            filtered_date_labels.append(html)
            last_used = left

    dates_html = "<div class=\"date-row\">\n          " + "\n          ".join(filtered_date_labels) + "\n        </div>"

    # === ГЕНЕРАЦИЯ HTML ===
    html_fragment = f"""
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <style>
    :root {{
      --labels-w: 260px;
      --accent-planned: #2b9cf3;
      --accent-actual: #f39c12;
      --accent-group: #e9eef6;
      --row-min-h: 40px;
    }}

    .gantt-container {{
      width: 100%;
      max-width: 100%;
      overflow-x: auto; /* скролл только если реально не влезает */
    }}

    .gantt-rows {{
      display: grid;
      grid-template-columns: var(--labels-w) 1fr; /* левая колонка фикс, правая — всё остальное */
      width: 100%;
      min-width: 100%; /* позволяет растягиваться */
    }}

    .gantt-row {{
      display: contents;
    }}

    .label-cell {{
      padding: 8px;
      border-bottom: 1px dashed #eee;
      box-sizing: border-box;
      word-break: break-word;
      white-space: normal;
      line-height: 1.4;
      min-height: var(--row-min-h);
      display: flex;
      align-items: flex-start;
    }}

    .label-cell.task {{
      font-weight: 700;
      color: #111;
    }}

    .label-cell.block {{
      padding-left: 12px;
      color: #444;
      font-size: 0.95em;
    }}

    .chart-cell {{
      position: relative;
      padding: 0 8px;
      border-bottom: 1px dashed #eee;
      min-height: var(--row-min-h);
      box-sizing: border-box;
    }}

    .chart-wrap {{
      border: 1px solid #efefef;
      width: 100%;
      overflow-x: auto;
    }}

    .dates {{
      border-top: 1px solid #eee;
      width: 100%;
      padding-left: var(--labels-w);
      box-sizing: border-box;
    }}

    .date-row {{
      position: relative;
      height: 40px;
      min-height: 40px;
      display: block;
      box-sizing: border-box;
      font-size: 12px;
      color: #222;
    }}

    .date {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      padding: 2px 6px;
      white-space: nowrap;
      font-size: 12px;
      color: #222;
      pointer-events: none;
      z-index: 10;
    }}

    .date.end {{
      transform: translate(-100%, -50%);
    }}

    .group-bg {{
      position: absolute;
      height: 12px;
      top: 50%;
      left: 0;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-group);
      opacity: 0.8;
    }}

    .bar {{
      position: absolute;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      height: 24px;
      min-height: 24px;
      max-height: 24px;
      padding: 0 8px;
      top: 50%;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-planned);
      color: white;
      display: flex;
      align-items: center;
      font-size: 12px;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.06);
      box-sizing: border-box;
    }}

    .bar.actual {{
      background: transparent;
      border: 2px dashed var(--accent-actual);
    }}

    .legend {{
      margin-top: 12px;
      font-size: 13px;
    }}

    .legend .item {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      margin-right: 16px;
    }}

    .sw {{
      width: 22px;
      height: 12px;
      border-radius: 3px;
      display: inline-block;
    }}

    .sw.group {{
      background: var(--accent-group);
    }}

    .sw.planned {{
      background: var(--accent-planned);
    }}

    .sw.actual {{
      border: 2px dashed var(--accent-actual);
      background: transparent;
    }}

    @media (max-width:768px) {{
      :root {{
        --labels-w: 200px;
      }}
    }}
  </style>

  <h3 style="margin:0 0 12px 0">{project_name}</h3>

  <div class="gantt-container">
    <div class="chart-wrap">
      <div class="gantt-rows">
        {rows_html}
      </div>
    </div>
    <div class="dates" aria-hidden="true">
      {dates_html}
    </div>
  </div>

  <div class="legend" aria-hidden="true">
    <span class="item"><span class="sw group"></span> Задача (интервал по блокам)</span>
    <span class="item"><span class="sw planned"></span> Плановый интервал блока</span>
    <span class="item"><span class="sw actual"></span> Фактический интервал (пунктир)</span>
  </div>
</main>
    """.strip()

    return html_fragment

def render_gantt(payload: Dict[str, Any]) -> str:
    """
    Генерирует HTML-фрагмент диаграммы Ганта с синхронизированной высотой строк,
    растягиваемой по ширине диаграммой, и корректным отображением плана/факта.
    """
    project_name = payload.get("name", "Проект")
    tasks: List[Dict[str, Any]] = payload.get("tasks") or []

    # Собираем даты для вычисления общего интервала
    all_dates: List[date] = []

    for key in ("startDate", "plannedEnd", "actualEnd"):
        d = parse_date(payload.get(key))
        if d:
            all_dates.append(d)

    for t in tasks:
        for key in ("plannedStart", "plannedEnd", "actualEnd"):
            d = parse_date(t.get(key))
            if d:
                all_dates.append(d)
        for b in t.get("blocks") or []:
            for key in ("plannedStart", "plannedEnd", "actualEnd"):
                d = parse_date(b.get(key))
                if d:
                    all_dates.append(d)

    if not all_dates:
        return """
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <h3>Нет данных для диаграммы Ганта</h3>
</main>
        """.strip()

    min_date = min(all_dates)
    max_date = max(all_dates)
    total_days = (max_date - min_date).days + 1

    def interval_style(start_str: Optional[str], end_str: Optional[str]) -> Optional[str]:
        if not start_str or not end_str:
            return None
        start_d = parse_date(start_str)
        end_d = parse_date(end_str)
        if not start_d or not end_d:
            return None
        if end_d < start_d:
            end_d = start_d
        left_days = (start_d - min_date).days
        duration_days = (end_d - start_d).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return f"left:{left_pct:.4f}%;width:{width_pct:.4f}%;"

    def interval_pct(start_str: Optional[str], end_str: Optional[str]):
        if not start_str or not end_str:
            return None
        s = parse_date(start_str)
        e = parse_date(end_str)
        if not s or not e:
            return None
        if e < s:
            e = s
        left_days = (s - min_date).days
        duration_days = (e - s).days + 1
        left_pct = left_days / total_days * 100.0
        width_pct = duration_days / total_days * 100.0
        return (left_pct, width_pct, s, e)

    # === СОБИРАЕМ СТРОКИ ===
    gantt_rows: List[str] = []
    all_date_labels: List[tuple[float, str]] = []

    for t in tasks:
        task_name = t.get("name", "Task")
        block_dates: List[date] = []
        for b in t.get("blocks") or []:
            bs = parse_date(b.get("plannedStart"))
            be = parse_date(b.get("plannedEnd"))
            if bs:
                block_dates.append(bs)
            if be:
                block_dates.append(be)

        group_bg_style = ""
        if block_dates:
            group_min = min(block_dates)
            group_max = max(block_dates)
            left_days = (group_min - min_date).days
            duration_days = (group_max - group_min).days + 1
            left_pct = left_days / total_days * 100.0
            width_pct = duration_days / total_days * 100.0
            group_bg_style = f"left:{left_pct:.4f}%; width:{width_pct:.4f}%;"

        gantt_rows.append(f"""
          <div class="gantt-row">
            <div class="label-cell task">{task_name}</div>
            <div class="chart-cell">
              {f'<div class="group-bg" style="{group_bg_style}"></div>' if group_bg_style else ''}
            </div>
          </div>
        """.strip())

        for b in t.get("blocks") or []:
            b_name = b.get("name", "Block")
            planned_style = interval_style(b.get("plannedStart"), b.get("plannedEnd"))
            actual_style = interval_style(b.get("plannedStart"), b.get("actualEnd"))

            bars_for_row = []

            # Сначала — фактический интервал (только рамка, без текста)
            if actual_style:
                bars_for_row.append(
                    f'<div class="bar actual" style="{actual_style}"></div>'
                )

            # Потом — плановый (с текстом поверх)
            if planned_style:
                bars_for_row.append(
                    f'<div class="bar" style="{planned_style}">{b_name}</div>'
                )

            gantt_rows.append(f"""
              <div class="gantt-row">
                <div class="label-cell block">{b_name}</div>
                <div class="chart-cell">
                  {''.join(bars_for_row)}
                </div>
              </div>
            """.strip())

            # Собираем даты только из планового интервала
            pct = interval_pct(b.get("plannedStart"), b.get("plannedEnd"))
            if pct:
                left_pct, width_pct, s_dt, e_dt = pct
                start_left = left_pct
                end_left = left_pct + width_pct
                start_label = f'<div class="date start" style="left:{start_left:.4f}%">{s_dt.strftime("%d.%m")}</div>'
                end_label = f'<div class="date end" style="left:{end_left:.4f}%">{e_dt.strftime("%d.%m")}</div>'
                all_date_labels.append((start_left, start_label))
                all_date_labels.append((end_left, end_label))

    rows_html = "\n        ".join(gantt_rows)

    # === ФИЛЬТРАЦИЯ ДАТ ПО ПРОЦЕНТАМ (минимум 5%) ===
    min_sep_pct = 5.0
    all_date_labels.sort(key=lambda x: x[0])
    filtered_date_labels = []
    last_used = -float('inf')
    for left, html in all_date_labels:
        if left - last_used >= min_sep_pct:
            filtered_date_labels.append(html)
            last_used = left

    dates_html = "<div class=\"date-row\">\n          " + "\n          ".join(filtered_date_labels) + "\n        </div>"

    # === ГЕНЕРАЦИЯ HTML ===
    html_fragment = f"""
<main style="font-family: Inter, Roboto, Arial, sans-serif; padding:16px; color:#222;">
  <style>
    :root {{
      --labels-w: 260px;
      --accent-planned: #2b9cf3;
      --accent-actual: #f39c12;
      --accent-group: #e9eef6;
      --row-min-h: 40px;
    }}

    .gantt-container {{
      width: 100%;
      max-width: 100%;
      overflow-x: auto;
    }}

    .gantt-rows {{
      display: grid;
      grid-template-columns: var(--labels-w) 1fr;
      width: 100%;
      min-width: 100%;
    }}

    .gantt-row {{
      display: contents;
    }}

    .label-cell {{
      padding: 8px;
      border-bottom: 1px dashed #eee;
      box-sizing: border-box;
      word-break: break-word;
      white-space: normal;
      line-height: 1.4;
      min-height: var(--row-min-h);
      display: flex;
      align-items: flex-start;
    }}

    .label-cell.task {{
      font-weight: 700;
      color: #111;
    }}

    .label-cell.block {{
      padding-left: 12px;
      color: #444;
      font-size: 0.95em;
    }}

    .chart-cell {{
      position: relative;
      padding: 0 8px;
      border-bottom: 1px dashed #eee;
      min-height: var(--row-min-h);
      box-sizing: border-box;
    }}

    .chart-wrap {{
      border: 1px solid #efefef;
      width: 100%;
      overflow-x: auto;
    }}

    .dates {{
      border-top: 1px solid #eee;
      width: 100%;
      padding-left: var(--labels-w);
      box-sizing: border-box;
    }}

    .date-row {{
      position: relative;
      height: 40px;
      min-height: 40px;
      display: block;
      box-sizing: border-box;
      font-size: 12px;
      color: #222;
    }}

    .date {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: transparent;
      padding: 2px 6px;
      white-space: nowrap;
      font-size: 12px;
      color: #222;
      pointer-events: none;
      z-index: 10;
    }}

    .date.end {{
      transform: translate(-100%, -50%);
    }}

    .group-bg {{
      position: absolute;
      height: 12px;
      top: 50%;
      left: 0;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-group);
      opacity: 0.8;
    }}

    .bar {{
      position: absolute;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      height: 24px;
      min-height: 24px;
      max-height: 24px;
      padding: 0 8px;
      top: 50%;
      transform: translateY(-50%);
      border-radius: 4px;
      background: var(--accent-planned);
      color: white;
      display: flex;
      align-items: center;
      font-size: 12px;
      box-shadow: 0 1px 0 rgba(0, 0, 0, 0.06);
      box-sizing: border-box;
      z-index: 2;
    }}

    .bar.actual {{
      background: transparent;
      border: 2px dashed var(--accent-actual);
      /* Без текста — пустой блок */
      z-index: 1;
    }}

    .legend {{
      margin-top: 12px;
      font-size: 13px;
    }}

    .legend .item {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      margin-right: 16px;
    }}

    .sw {{
      width: 22px;
      height: 12px;
      border-radius: 3px;
      display: inline-block;
    }}

    .sw.group {{
      background: var(--accent-group);
    }}

    .sw.planned {{
      background: var(--accent-planned);
    }}

    .sw.actual {{
      border: 2px dashed var(--accent-actual);
      background: transparent;
    }}

    @media (max-width:768px) {{
      :root {{
        --labels-w: 200px;
      }}
    }}
  </style>

  <h3 style="margin:0 0 12px 0">{project_name}</h3>

  <div class="gantt-container">
    <div class="chart-wrap">
      <div class="gantt-rows">
        {rows_html}
      </div>
    </div>
    <div class="dates" aria-hidden="true">
      {dates_html}
    </div>
  </div>

  <div class="legend" aria-hidden="true">
    <span class="item"><span class="sw group"></span> Задача (интервал по блокам)</span>
    <span class="item"><span class="sw planned"></span> Плановый интервал блока</span>
    <span class="item"><span class="sw actual"></span> Фактический интервал (пунктир)</span>
  </div>
</main>
    """.strip()

    return html_fragment



