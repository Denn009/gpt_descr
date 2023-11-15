import g4f
import gspread
import asyncio


# cookies = {
#     'SID': 'cwhE5Z_yny9qQHg7JB7GXYkf-GDiSMpZmCx4e_uj7EyCv61PDk_JZ7j9NZuMKP3nmcHPLw.',
#     '__Secure-1PSID': 'cwhE5Z_yny9qQHg7JB7GXYkf-GDiSMpZmCx4e_uj7EyCv61PQLhva2TO-zH6B6tAgP8mqw.',
#     '__Secure-3PSID': 'cwhE5Z_yny9qQHg7JB7GXYkf-GDiSMpZmCx4e_uj7EyCv61PYopN_ZN54qTno3H6V2anwQ.',
#     'HSID': 'A8sPwR3Sdlxrg7Ttm',
#     'SSID': 'AI_yRWgJDjflSmtw2',
#     'APISID': 'lV_ckuTesdSc2Y1q/AIBO4_T4WD9ITfdFU',
#     'SAPISID': 'nOPWb_rWZC8nsAHb/AzqmD_vil_GwMuKOs',
#     '__Secure-1PAPISID': 'nOPWb_rWZC8nsAHb/AzqmD_vil_GwMuKOs',
#     '__Secure-3PAPISID': 'nOPWb_rWZC8nsAHb/AzqmD_vil_GwMuKOs',
#     'SEARCH_SAMESITE': 'CgQI1JkB',
#     'AEC': 'Ackid1R-TdK-ewLGHaKqv9vxhqLvsHNg74IY_d0Jp65-Qij1r9XQgW7-DA',
#     'OTZ': '7284305_44_44_123780_40_436260',
#     '1P_JAR': '2023-11-07-15',
#     '__Secure-1PSIDTS': 'sidts-CjEBNiGH7pKNm0cGTKodglQ-UmJNyLHrd8fiTGZ-vOfsEZq7pLq3h753eZ4Hb1Q_Q7gnEAA',
#     '__Secure-3PSIDTS': 'sidts-CjEBNiGH7pKNm0cGTKodglQ-UmJNyLHrd8fiTGZ-vOfsEZq7pLq3h753eZ4Hb1Q_Q7gnEAA',
#     'NID': '511=Inl4u3uFd3u_KuIb3P-1PifJgEOK8IJdfuO0W93Zh0z3tjh7c1nuC0vuO8iCOaWd57fIcJ80b4EJjNZelkt43Gikk0BDv8MER3y7KWwppoT_4vHOiOy5ziy_0YRV-GO5sbHlCUlbKG31VXVkecaM6EsUCJ0zfbk4yL3xe27bN-5ON4I4fCGLXAbz2N4XmEUKcApVpEY8bHKAn6ll-Y_RZGUl1_JW90uKGz4p-ZD3WW_EgECYefOe5T_stIh-LLt-GJlyR9ugnVDxaBX8dzCymnWKi-YDcpIpSDounxmTQ9s1CI0PgToJOtpksxTXYeYJS7ocYRlI1rIEAaAMz8ff6NFKjT3LJCHTeZNPnTEG2DyzOIr14LOBc56NrUsHsAgbVZz-bH3uheRiZEZKLq-nRbkbvfwsstcRQTZ3QF6M3It7cKwRYqHH2dTMRyKm_6nxmBqAmRNobJ4',
#     'DV': 'cwsb3-PUXLNbQAgxTl7ANXagjMmlulidS42dMzB-KAEAANC4rjw1Rz9lcQAAAOw7mDvytuuRLgAAAFgvVcgWkPXiEQAAAA',
#     'SIDCC': 'ACA-OxNlLYdJPBx6BkjvGXxa0zzCEm0Y0XS3nIc2jrzj83aklOtrdFgQTuFt20Q240byMSg6tQ',
#     '__Secure-1PSIDCC': 'ACA-OxOzdpYeekbKmtasARyvrC6VK0r0PUDOwXfvlEWlbEkM55Cef7x8ZioyF7iTaFKJYEe_mA',
#     '__Secure-3PSIDCC': 'ACA-OxOOpIJEFEzUQGrrgrLhk3tqQCANa2ROSkDWPZJrAY1WdKFYz0Y0AI9LSVGbKYrc2qTpFrw',
# }


def get_value_gs(name_product, description_product, worksheet):
    # Получаем все заголовки
    row_value = worksheet.row_values(1)
    # Ищем заголовок с названием name_product
    column_name = row_value.index(name_product) + 1
    # Ищем заголовок с названием description_product
    column_description = row_value.index(description_product) + 1

    # Забираем все значение из столбца(column_name) и формируем список
    column_values = worksheet.col_values(column_name)
    return column_values[1:], column_description


def response_gpt(column_values, column_description, prompt, worksheet):
    for count, value in enumerate(column_values):
        # Получаем значение из клетки в которую хотим записать значение
        write_cell = worksheet.cell(count + 2, column_description).value

        # Проверка на наличие а клетке значение: если не пустая - пропускаем
        if write_cell:
            print(f"Пропуск товара {count + 1}, строки {count + 2}")
            continue

        try:
            # Запрос к GPT
            response = g4f.ChatCompletion.create(
                model=g4f.models.default,
                messages=[{"role": "user", "content": f"{prompt}: {value}"}],
                timeout=120,
                # cookies=cookies
            )

            # Вызов функции записи в google sheets
            writer_gs(response, count, column_description, worksheet)
            print(f"Записан элемент {count + 1}, в строку {count + 2}")

        except Exception as error:
            print(error)


def writer_gs(response, count, column_description, worksheet):
    # Записываем полученное значение в google sheets
    worksheet.update_cell(count + 2, column_description, response)


def gpt_main(list_data):
    # Prompt значения
    print(list_data)
    if list_data[0] == '1':
        spreadsheet_url = "https://docs.google.com/spreadsheets/d/12t6QQwvklFvwAf6R1hwbjvkiJAJW9UNAWAg93yey7j0/edit?pli=1#gid=0"
    else:
        spreadsheet_url = list_data[0]

    if list_data[1] == '1':
        prompt = "Напишите описание товара на 300 символов: "
    else:
        prompt = list_data[1]

    if list_data[2] == '1':
        name_product = "Название элемента"
    else:
        name_product = list_data[2]

    if list_data[3] == '1':
        description_product = "Подробное описание"
    else:
        description_product = list_data[3]

    gc = gspread.service_account('service_account_1.json')
    spreadsheet = gc.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet("Лист1")

    column_values, column_description = get_value_gs(name_product, description_product, worksheet)
    response_gpt(column_values, column_description, prompt, worksheet)
