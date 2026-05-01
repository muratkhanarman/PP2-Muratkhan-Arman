import psycopg2
import csv
import json
import os
from datetime import datetime
from db_connect import get_connection

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        if fetch:
            result = cur.fetchall()
        else:
            conn.commit()
            result = None
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
        result = None
    finally:
        cur.close()
        conn.close()
    return result

def list_groups():
    result = execute_query("SELECT id, name FROM groups ORDER BY id", fetch=True)
    return result if result else []

def display_contacts(contacts, page=1, per_page=5):
    if not contacts:
        print("Нет контактов.")
        return
    total = len(contacts)
    start = (page-1)*per_page
    end = start + per_page
    for i, c in enumerate(contacts[start:end], start=start+1):
        print(f"{i}. {c[0]} | Email: {c[1] or '-'} | Birthday: {c[2] or '-'} | Group: {c[3] or '-'} | Phones: {c[4] or '-'}")
    print(f"\nСтраница {page}/{(total+per_page-1)//per_page if total>0 else 1}")

def add_contact():
    name = input("Имя: ").strip()
    if not name:
        print("Имя обязательно")
        return
    email = input("Email: ").strip() or None
    birthday = input("Birthday (YYYY-MM-DD): ").strip() or None
    groups = list_groups()
    print("Группы:", ", ".join([g[1] for g in groups]))
    group_name = input("Название группы: ").strip()
    group_id = None
    if group_name:
        for g in groups:
            if g[1].lower() == group_name.lower():
                group_id = g[0]
                break
        if not group_id:
            execute_query("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (group_name,))
            result = execute_query("SELECT id FROM groups WHERE name = %s", (group_name,), fetch=True)
            group_id = result[0][0] if result else None
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                    (name, email, birthday, group_id))
        contact_id = cur.fetchone()[0]
        
        while True:
            phone = input("Телефон (оставьте пустым для завершения): ").strip()
            if not phone:
                break
            ptype = input("Тип (home/work/mobile): ").strip().lower()
            if ptype not in ('home','work','mobile'):
                ptype = 'mobile'
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                        (contact_id, phone, ptype))
        conn.commit()
        print("Контакт добавлен.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()

def search_contacts_menu():
    query = input("Введите строку поиска (имя/email/телефон): ").strip()
    if not query:
        return
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc('search_contacts', (query,))
        results = cur.fetchall()
        if results:
            for r in results:
                print(f"Имя: {r[0]}, Email: {r[1]}, ДР: {r[2]}, Группа: {r[3]}, Телефоны: {r[4]}")
        else:
            print("Не найдено.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()

def filter_by_group():
    groups = list_groups()
    print("Группы:")
    for g in groups:
        print(f"  {g[1]}")
    grp = input("Введите название группы: ").strip()
    if not grp:
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, STRING_AGG(p.phone||' ('||p.type||')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
        WHERE g.name ILIKE %s
        GROUP BY c.id, g.name
        ORDER BY c.name
    """, (grp,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    if results:
        for r in results:
            print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | Телефоны: {r[4]}")
    else:
        print("Нет контактов в этой группе.")

def sort_contacts():
    print("Сортировать по: 1 - имя, 2 - день рождения, 3 - дата добавления (id)")
    choice = input("Ваш выбор: ").strip()
    order = ""
    if choice == '1':
        order = "c.name"
    elif choice == '2':
        order = "c.birthday NULLS LAST"
    elif choice == '3':
        order = "c.id"
    else:
        print("Неверный выбор")
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.name, c.email, c.birthday, g.name, STRING_AGG(p.phone||' ('||p.type||')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
        GROUP BY c.id, g.name
        ORDER BY {order}
    """)
    results = cur.fetchall()
    cur.close()
    conn.close()
    # пагинация
    page = 1
    per_page = 5
    while True:
        display_contacts(results, page, per_page)
        cmd = input("[n]ext, [p]rev, [q]uit: ").strip().lower()
        if cmd == 'n' and page * per_page < len(results):
            page += 1
        elif cmd == 'p' and page > 1:
            page -= 1
        elif cmd == 'q':
            break
        else:
            print("Некорректно")

def export_json():
    filename = input("Имя JSON файла (например, export.json): ").strip()
    if not filename:
        filename = "contacts_export.json"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, c.email, c.birthday::text, g.name as group_name,
               json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
        GROUP BY c.id, g.name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    data = []
    for row in rows:
        data.append({
            "name": row[0],
            "email": row[1],
            "birthday": row[2],
            "group": row[3],
            "phones": row[4] if row[4] else []
        })
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Экспортировано в {filename}")

def import_json():
    filename = input("Имя JSON файла для импорта: ").strip()
    if not os.path.exists(filename):
        print("Файл не найден")
        return
    with open(filename, 'r', encoding='utf-8') as f:
        contacts = json.load(f)
    conn = get_connection()
    cur = conn.cursor()
    for contact in contacts:
        name = contact.get('name')
        if not name:
            continue

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        exists = cur.fetchone()
        if exists:
            ans = input(f"Контакт '{name}' уже существует. Пропустить (s) или перезаписать (o)? ").strip().lower()
            if ans == 's':
                continue
            elif ans == 'o':
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
            else:
                continue

        email = contact.get('email')
        birthday = contact.get('birthday')
        group_name = contact.get('group')
        group_id = None
        if group_name:
            cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (group_name,))
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            grp = cur.fetchone()
            if grp:
                group_id = grp[0]
        cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                    (name, email, birthday, group_id))
        contact_id = cur.fetchone()[0]
        for phone in contact.get('phones', []):
            pnum = phone.get('phone')
            ptype = phone.get('type', 'mobile')
            if pnum:
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                            (contact_id, pnum, ptype))
    conn.commit()
    cur.close()
    conn.close()
    print("Импорт завершен.")

def import_csv():
    filename = input("Имя CSV файла (формат: name,email,birthday,group,phone,phone_type): ").strip()
    if not os.path.exists(filename):
        print("Файл не найден")
        return
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # пропустить заголовок
        for row in reader:
            if len(row) < 6:
                continue
            name, email, birthday, group_name, phone, ptype = row[:6]
            if not name:
                continue

            group_id = None
            if group_name:
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (group_name,))
                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                grp = cur.fetchone()
                if grp:
                    group_id = grp[0]
            cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) ON CONFLICT (name) DO NOTHING RETURNING id",
                        (name, email, birthday, group_id))
            contact_id = cur.fetchone()
            if contact_id:
                contact_id = contact_id[0]
                if phone:
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                                (contact_id, phone, ptype if ptype in ('home','work','mobile') else 'mobile'))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV импорт выполнен.")

def add_phone_proc():
    name = input("Имя контакта: ").strip()
    phone = input("Номер телефона: ").strip()
    ptype = input("Тип (home/work/mobile): ").strip().lower()
    if ptype not in ('home','work','mobile'):
        ptype = 'mobile'
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc('add_phone', (name, phone, ptype))
        conn.commit()
        print("Телефон добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()

def move_to_group_proc():
    name = input("Имя контакта: ").strip()
    group = input("Название группы: ").strip()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc('move_to_group', (name, group))
        conn.commit()
        print("Контакт перемещен.")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        cur.close()
        conn.close()

def main_menu():
    while True:
        print("\n=== PhoneBook Extended ===")
        print("1. Добавить контакт")
        print("2. Поиск (по имени/email/телефону)")
        print("3. Фильтр по группе")
        print("4. Сортировка и пагинация")
        print("5. Экспорт в JSON")
        print("6. Импорт из JSON")
        print("7. Импорт из CSV")
        print("8. Добавить телефон")
        print("9. Переместить в группу")
        print("0. Выход")
        choice = input("Выберите: ").strip()
        if choice == '1':
            add_contact()
        elif choice == '2':
            search_contacts_menu()
        elif choice == '3':
            filter_by_group()
        elif choice == '4':
            sort_contacts()
        elif choice == '5':
            export_json()
        elif choice == '6':
            import_json()
        elif choice == '7':
            import_csv()
        elif choice == '8':
            add_phone_proc()
        elif choice == '9':
            move_to_group_proc()
        elif choice == '0':
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main_menu()