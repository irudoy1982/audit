import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Технический аудит 2026", layout="wide")

st.title("📋 Опросник: Технический аудит ИТ и ИБ (2026)")
data = {}

# --- Вспомогательная функция для варианта "Другое" ---
def get_choice_with_other(label, options, key):
    choice = st.selectbox(label, options + ["Другое"], key=f"sel_{key}")
    if choice == "Другое":
        return st.text_input(f"Укажите ваш вариант ({label}):", key=f"other_{key}")
    return choice

def get_multichoice_with_other(label, options, key):
    choices = st.multiselect(label, options + ["Другое"], key=f"msel_{key}")
    final_choices = [c for c in choices if c != "Другое"]
    if "Другое" in choices:
        other_val = st.text_input(f"Укажите другие варианты ({label}):", key=f"mother_{key}")
        if other_val:
            final_choices.append(other_val)
    return ", ".join(final_choices)

# --- Блок 1: Общая информация ---
st.header("Блок 1: Общая информация и масштаб")
data['Сотрудников в штате'] = st.number_input("1. Укажите общее количество сотрудников в штате:", min_value=0, step=1)

has_it = st.toggle("2. В компании есть выделенный ИТ-департамент?", key="it_toggle")
data['Наличие ИТ-департамента'] = "Да" if has_it else "Нет"

if has_it:
    col1, col2 = st.columns(2)
    with col1:
        data['Кол-во АРМ'] = st.number_input("1.1. Количество конечных точек (АРМ):", min_value=0)
        data['Серверы физ (кол-во)'] = st.number_input("1.2. Количество серверов (Физических):", min_value=0)
        data['ОС Nix (кол-во)'] = st.number_input("1.3. Серверные операционные системы (*Nix):", min_value=0)
        data['Среда виртуализации'] = get_multichoice_with_other("1.4. Среда виртуализации:", ["VMware", "Hyper-V", "Proxmox"], "virt")
        data['Тикет-системы'] = st.text_input("1.5. Тикет системы:")
    with col2:
        st.write("") # Выравнивание
        st.write("") 
        data['Серверы вирт (кол-во)'] = st.number_input("1.2. Количество серверов (Виртуальных):", min_value=0)
        data['ОС Windows (кол-во)'] = st.number_input("1.3. Серверные операционные системы (MS Windows):", min_value=0)
        data['Мониторинг системы'] = st.text_input("1.6. Мониторинг системы:")
        data['Почтовые системы'] = get_choice_with_other("1.7. Почтовые системы:", ["Cloud", "On-Prem", "Hybride"], "mail")

# --- Блок 2: Сетевая инфраструктура ---
st.header("Блок 2: Сетевая инфраструктура и Интернет")
has_net = st.toggle("3. Компания управляет собственной сетевой инфраструктурой?", key="net_toggle")
data['Своя сеть'] = "Да" if has_net else "Нет"

if has_net:
    st.subheader("2.1. Каналы связи (Интернет)")
    data['Тип канала'] = get_multichoice_with_other("Тип канала:", ["Оптика", "Радиорелейная", "Спутник", "4G/5G бэкап"], "channel")
    data['Скорость канала'] = st.number_input("Скорость основного канала (Мбит/с):", min_value=0)
    
    st.subheader("2.2. Архитектура сети (Tiered Network Design)")
    data['Core (Ядро)'] = st.text_input("Core (Ядро) - Укажите вендора/модель")
    data['Distribution'] = st.text_input("Distribution (Распределение) - Укажите вендора/модель")
    data['Access'] = st.text_input("Access (Доступ) - Укажите вендора/модель")
    
    st.subheader("2.3. Оборудование и технологии")
    col3, col4 = st.columns(2)
    with col3:
        data['Switch L2'] = st.number_input("Switch L2 (кол-во):", min_value=0)
        data['Switch L3'] = st.number_input("Switch L3 (кол-во):", min_value=0)
        data['Сетевые технологии'] = get_multichoice_with_other("Сетевые технологии:", ["VLAN", "STP", "OSPF/BGP", "SD-WAN"], "net_tech")
    with col4:
        data['Router'] = st.number_input("Router (кол-во):", min_value=0)
        st.write("2.4. Безопасность периметра (NGFW)")
        data['NGFW Производитель'] = st.text_input("Производитель (NGFW):")
        data['NGFW Количество'] = st.number_input("Количество (NGFW):", min_value=0)

    st.subheader("2.5. Беспроводные сети")
    has_wifi = st.toggle("Наличие Wi-Fi?", key="wifi_toggle")
    if has_wifi:
        has_controller = st.checkbox("2.5.1. Контроллер точек доступа")
        data['Wi-Fi Контроллер'] = st.text_input("Наименование контроллера:") if has_controller else "Нет"
        data['Wi-Fi Кол-во точек'] = st.number_input("2.5.2. Кол-во точек доступа:", min_value=0)
        data['Тип Wi-Fi'] = get_choice_with_other("2.5.3. Тип Wi-Fi:", ["Wi-Fi 5+", "Wi-Fi N", "Wi-Fi b/G"], "wifi_type")

# --- Блок 3: Информационная Безопасность ---
st.header("Блок 3: Информационная Безопасность (ИБ)")
has_is = st.toggle("4. В компании внедрены специализированные системы защиты информации?", key="is_toggle")
data['Системы ИБ'] = "Да" if has_is else "Нет"

if has_is:
    st.info("Отметьте внедренные системы и укажите их наименования:")
    
    if st.checkbox("3.1. Защита от утечек (DLP)"): data['DLP'] = st.text_input("Наименование (DLP):")
    else: data['DLP'] = "Нет"
        
    if st.checkbox("3.2. Контроль привилегий (PAM)"): data['PAM'] = st.text_input("Наименование (PAM):")
    else: data['PAM'] = "Нет"
        
    if st.checkbox("3.3. Мониторинг (SIEM/SOC)"): data['SIEM/SOC'] = st.text_input("Наименование (SIEM/SOC):")
    else: data['SIEM/SOC'] = "Нет"
    
    data['MFA'] = get_choice_with_other("3.4. Аутентификация:", ["MFA/2FA внедрена", "Только пароли"], "mfa")
    
    if st.checkbox("3.5. WAF"): data['WAF'] = st.text_input("Наименование (WAF):")
    else: data['WAF'] = "Нет"
        
    if st.checkbox("3.6. Anti-DDoS"): data['Anti-DDoS'] = st.text_input("Наименование (Anti-DDoS):")
    else: data['Anti-DDoS'] = "Нет"
        
    if st.checkbox("3.7. Шифрование дисков, БД"): data['Шифрование'] = st.text_input("Наименование (Шифрование):")
    else: data['Шифрование'] = "Нет"
        
    if st.checkbox("3.8. Antimalware/EDR/XDR"): data['Antimalware'] = st.text_input("Наименование (Antimalware/EDR/XDR):")
    else: data['Antimalware'] = "Нет"
        
    if st.checkbox("3.9. Системы резервного копирования"): data['Бэкап'] = st.text_input("Наименование (СРК):")
    else: data['Бэкап'] = "Нет"
        
    if st.checkbox("3.10. Другие системы"): data['Другие ИБ системы'] = st.text_area("Укажите другие системы:")
    else: data['Другие ИБ системы'] = "Нет"

# --- Блок 4: Web-ресурсы ---
st.header("Блок 4: Web-ресурсы и Сайты")
has_web = st.toggle("5. У компании есть собственные сайты, порталы или внешние web-сервисы?", key="web_toggle")
if has_web:
    data['Хостинг'] = get_choice_with_other("4.1. Место размещения (Хостинг):", ["Собственный ЦОД", "Облако (KZ)", "Облако (Global)"], "hosting")
    data['CMS'] = get_choice_with_other("4.2. Платформа (CMS/Framework):", ["Bitrix", "WordPress", "Самопис (PHP/Python/JS)"], "cms")
    data['БД Сайта'] = get_multichoice_with_other("4.3. Базы данных:", ["PostgreSQL", "MySQL", "MS SQL", "Oracle"], "db")
    data['Web-сервер'] = get_multichoice_with_other("4.4. Тип web сервера:", ["Apache", "Nginx", "IIS"], "web_server")

# --- Блок 5: Разработка ---
st.header("Блок 5: Разработка и DevSecOps")
has_dev = st.toggle("6. В компании ведется внутренняя разработка ПО?", key="dev_toggle")
if has_dev:
    data['Кол-во разработчиков'] = st.number_input("5.1. Количество разработчиков:", min_value=0)
    data['Стек разработки'] = get_multichoice_with_other("5.2. Стек:", ["Java", ".NET", "Python", "Go", "Frontend (Nuxt/React)"], "stack")
    data['Анализ кода'] = get_multichoice_with_other("5.3. Анализ кода:", ["SAST", "DAST", "Проверка OpenSource библиотек"], "code_sec")
    data['Контейнеры'] = st.text_input("5.4. Контейнеры (наименование):")

# --- ПРЕДПРОСМОТР И ЭКСПОРТ ---
st.divider()
st.subheader("Предпросмотр данных")
df = pd.DataFrame([data])
st.dataframe(df)

if st.button("Сформировать отчет Excel"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.success("Таблица сформирована!")
    st.download_button(label="📥 Скачать Excel", data=output.getvalue(), file_name="Audit_Full_2026.xlsx")