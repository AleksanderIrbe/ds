import pandas as pd
import numpy as np
import json


def get_customer_info(df, result):
    column_list = ['fullName', 'shortName', 'inn', 'legalAddress', 'iko']

    for column in column_list:
        result[column] = df['customer'].map(lambda x: x.get(column))
    return result


def get_purchase_info(df, result):
    result['purchaseInfo_name'] = df['purchaseInfo'].map(lambda x: x.get('name'))
    return result


def get_price_info(df, result):
    result['price'] = df['price']
    return result


def get_suppliers_org_name(x):
    if isinstance(x, list):
        return x[0].get('organizationName')
    else:
        return np.nan


def get_suppliers_org_inn(x):
    if isinstance(x, list):
        return x[0].get('inn')
    else:
        return np.nan


def get_suppliers_info(df, result):
    result['sup_organizationName'] = df['suppliers'].map(get_suppliers_org_name)
    result['sup_inn'] = df['suppliers'].map(get_suppliers_org_inn)
    return result


# def get_suppliers_org_name(x):
#     if isinstance(x, list):
#         return x[0].get('organizationName')
#     else:
#         return np.nan

def get_product_info_OKEI(products):
    if isinstance(products, list) and isinstance(products[0], dict):
        temp = products[0].get('OKEI')
        if isinstance(temp, dict):
            return temp.get('name')
    return np.nan


def get_product_info_OKDP(products):
    if isinstance(products, list) and isinstance(products[0], dict):
        temp = products[0].get('OKDP')
        if isinstance(temp, dict):
            return temp.get('name')
    return np.nan


def get_product_info_quantity(products):
    if isinstance(products, list) and isinstance(products[0], dict):
        return products[0].get('quantity')
    return np.nan


def get_product_info(df, result):
    if isinstance(df['products'][0], list):
        result['products_OKEI_name'] = df['products'].map(get_product_info_OKEI)
        result['products_OKDP_name'] = df['products'].map(get_product_info_OKDP)
        result['products_quantity'] = df['products'].map(get_product_info_quantity)
        return result
    return np.nan


def fill_df(df):
    print("Creating data frame ...")
    result = pd.DataFrame()
    print("Getting customer info ...")
    result = get_customer_info(df, result)
    print("Getting purchase info ...")
    result = get_purchase_info(df, result)
    print("Getting price info ...")
    result = get_price_info(df, result)
    print("Getting suppliers info ...")
    result = get_suppliers_info(df, result)
    print("Getting product info ...")
    result = get_product_info(df, result)
    print("Parsing complete")
    return result


def get_clean_data(file):
    with open(file) as f:
        data = f.readlines()

    data_clean = []
    error_count = 0
    for index, line in enumerate(data):
        try:
            data_clean.append(json.loads(data[index]))
        except:
            error_count += 1
    print("error", error_count)
    print("all", index)
    return pd.DataFrame(data_clean)


def do_short_table(file):
    df = get_clean_data(file)
    df = df[df['attachments'].notna()]

    df['attachments'] = df['attachments'].map(lambda x: x['attachment'])
    # print(df.columns)
    # print(df['suppliers'].isnull().sum())
    short_df = fill_df(df)
    print(short_df.columns)
    short_df.to_csv('20210323_file_full.csv')


def do_full_table(file):
    df = get_clean_data(file)
    print(df.columns)
    print(df.shape)
    df.to_csv('file_full.csv')


if __name__ == '__main__':
    do_short_table('contracts_223fz_202102-20210313.jsonl')
    # do_full_table('contracts_223fz_202102-20210313.jsonl')

# d = {'attachment':
#          [
#              {'url':            'https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407111',
#               'docDescription': '1.8НИИ-2583-П-2012 от 26.06.2020',
#               'fileName':       '1.8НИИ-2583-П-2012 от 26.06.2020.rar',
#               'guid':           'cdc8a881-ca16-4145-af94-9ee46251ad5d'
#               },
#              {'url':            'https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407159',
#               'docDescription': '9НИИ-2583-П-2012',
#               'fileName':       '9НИИ-2583-П-2012.rar',
#               'guid':           '37245bc1-3867-49a6-ac95-7333f9635451'},
#              {'url':            'https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407110',
#               'docDescription': '8_НИИ-2583-П-2012',
#               'fileName':       '8_НИИ-2583-П-2012.rar',
#               'guid':           'e6d9921c-2b21-426c-8511-152991b0211a'},
#              {'url':            'https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407109',
#               'docDescription': '2.7_НИИ-2583-П-2012',
#               'fileName':       '2.7_НИИ-2583-П-2012.rar',
#               'guid':           '1387eeea-e17a-4019-86b5-bcd2949469b7'},
#              {'url':            'https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407108',
#               'docDescription': 'ДС №8 к Дог №2583 ТН Дальний Восток',
#               'fileName': 'ДС №8 к Дог №2583 ТН Дальний Восток.rar',
#               'guid': '9a41cc49-d18d-42fa-b3e9-6f45001f0d4a'}
#          ]
# }
#
# s = {"attachments":
#      {"attachment":
#           [
#               {"url":               "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407111",
#                "docDescription":    "1.8НИИ-2583-П-2012 от 26.06.2020",
#                "fileName":          "1.8НИИ-2583-П-2012 от 26.06.2020.rar",
#                "guid":              "cdc8a881-ca16-4145-af94-9ee46251ad5d"},
#               {"url":               "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407159",
#                "docDescription":    "9НИИ-2583-П-2012",
#                "fileName":          "9НИИ-2583-П-2012.rar",
#                "guid":              "37245bc1-3867-49a6-ac95-7333f9635451"},
#               {"url":               "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407110",
#                "docDescription":    "8_НИИ-2583-П-2012",
#                "fileName":          "8_НИИ-2583-П-2012.rar",
#                "guid":              "e6d9921c-2b21-426c-8511-152991b0211a"},
#               {"url":               "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407109",
#                "docDescription":    "2.7_НИИ-2583-П-2012",
#                "fileName":          "2.7_НИИ-2583-П-2012.rar",
#                "guid":              "1387eeea-e17a-4019-86b5-bcd2949469b7"},
#               {"url":               "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407108",
#                "docDescription":    "ДС №8 к Дог №2583 ТН Дальний Восток",
#                "fileName":          "ДС №8 к Дог №2583 ТН Дальний Восток.rar",
#                "guid":              "9a41cc49-d18d-42fa-b3e9-6f45001f0d4a"}
#           ]
#      },
#     "contractCreateDate":           "2021-02-05",
#     "createDateTime":               "2021-02-15T20:19:09Z",
#     "currency":                     {"code":        "RUB",
#                                      "name":        "Российский рубль",
#                                      "digitalCode": "643"
#                                      },
#     "customer":                     {"OKATO":       "08401375000",
#                                      "OGRN":        "1092724004944",
#                                      "legalAddress":"680020, КРАЙ ХАБАРОВСКИЙ,ГОРОД ХАБАРОВСК,УЛИЦА ЗАПАРИНА, дом 1",
#                                      "shortName":   "ООО \"ТРАНСНЕФТЬ - ДАЛЬНИЙ ВОСТОК\"",
#                                      "postalAddress":"680030, г Хабаровск, ул Запарина, дом 1",
#                                      "kpp":         "272101001",
#                                      "inn":         "2724132118",
#                                      "iko":         "62724132118272101001",
#                                      "fullName":    "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"ТРАНСНЕФТЬ - ДАЛЬНИЙ ВОСТОК\""},
#     "deliveryPlaceIndication":      "GL",
#     "economic_sectors":             [{"code":    "K",
#                                      "title":   "Деятельность по операциям с недвижимым имуществом и арендой; деятельность исследовательская и коммерческая"
#                                      }],
#     "fileVersion":                  "20210228_235959_011",
#     "fulfillmentDate":              "по 31.12.2020",
#     "fz":                           "223",
#     "id":                           "570fbecd-db1b-4a60-8b60-09df5f04827f",
#     "loadId":                       1518,
#     "lot":                          {"guid":        "8cadce6d-8323-4747-8da9-6fbe2c829c8f",
#                                      "subject":     "Оказание услуг по обследованию коррозийного состояния объектов магистрального нефтепровода (линейная части и НПС)"},
#     "misuses":                      ["prodname"],
#     "modification":                 {"description": "заключено ДС"},
#     "name":                         "9/НИИ-2583-П-2012",
#     "number":                       "31300108509-09",
#     "placer":                       {"mainInfo":
#                                          {"kpp":        "272101001",
#                                           "okato":      "08401375000",
#                                           "okpo":       "62202458",
#                                           "ogrn":       "1092724004944",
#                                           "email":      "GorodetskiyAP@dmn.transneft.ru",
#                                           "fullName":   "ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"ТРАНСНЕФТЬ - ДАЛЬНИЙ ВОСТОК\"",
#                                           "inn":        "2724132118",
#                                           "legalAddress":"680020, КРАЙ ХАБАРОВСКИЙ,ГОРОД ХАБАРОВСК,УЛИЦА ЗАПАРИНА, дом 1",
#                                           "shortName":  "ООО \"ТРАНСНЕФТЬ - ДАЛЬНИЙ ВОСТОК\"",
#                                           "postalAddress":"680030, г Хабаровск, ул Запарина, дом 1"}
#                                      },
#     "price":                        25954476.64,
#     "products":                     [
#                                     {"OKEI":            {"code":    "008",
#                                                         "name":     "Километр;^тысяча метров"},
#                                      "OKDP":            {"code":    "7422035",
#                                                          "name":"Услуги по проверке стойкости к комплексным воздействиям"},
#                                      "quantity":        "1090.588",
#                                      "OKVED":           {"code":    "74.30.4",
#                                                          "name":    "Испытания и анализ физических свойств материалов и веществ: испытания и анализ физических свойств (прочности, пластичности, электропроводности, радиоактивности) материалов (металлов, пластмасс, тканей, дерева, стекла, бетона и др,); испытания на растяжени"},
#                                      "deliveryPlace":   {"address":"Хабаровский край, Амурская область, Еврейская автономная область"},
#                                      "ordinalNumber":   "1"}
#                                     ],
#     "publishDate":                  "2021-02-15T20:20:56",
#     "purchaseInfo":                 {"purchaseNoticeNumber":    "31300108509",
#                                      "purchaseCodeName":        "Закупка у единственного поставщика (исполнителя, подрядчика)",
#                                      "name":                    "Лот №У-371-ДМН-2013 «Оказание услуг по обследованию коррозийного состояния объектов магистрального нефтепровода (линейная части и НПС)»",
#                                      "purchaseMethodCode":      "3363"},
#     "regNum":                       "31300108509-09",
#     "regionCode":                   "27",
#     "scan":                         [
#                                     {"url":                     "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407111",
#                                      "docDescription":          "1.8НИИ-2583-П-2012 от 26.06.2020",
#                                      "fileName":                "1.8НИИ-2583-П-2012 от 26.06.2020.rar"},
#                                     {"url":                     "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407159",
#                                      "docDescription":          "9НИИ-2583-П-2012",
#                                      "fileName":                "9НИИ-2583-П-2012.rar"},
#                                     {"url":                     "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407110",
#                                      "docDescription":          "8_НИИ-2583-П-2012",
#                                      "fileName":                "8_НИИ-2583-П-2012.rar"},
#                                     {"url":                     "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407109",
#                                      "docDescription":          "2.7_НИИ-2583-П-2012",
#                                      "fileName":                "2.7_НИИ-2583-П-2012.rar"},
#                                     {"url":                     "https://zakupki.gov.ru/223/purchase/public/download/download.html?id=68407108",
#                                      "docDescription":          "ДС №8 к Дог №2583 ТН Дальний Восток",
#                                      "fileName":                "ДС №8 к Дог №2583 ТН Дальний Восток.rar"}
#                                     ],
#     "schemaVersion":                "10.1",
#     "status":                       "P",
#     "suppliers":                    [
#                                         {"kpp":                 "772701001",
#                                          "inn":                 "7736607502",
#                                          "type":                "L",
#                                          "organizationName":    "ООО \"НИИ Транснефть\"",
#                                          "ogrn":                "1097746556710"}
#                                     ],
#     "type":                         "C",
#     "versionNumber":                5}
#
# y = {
#     "attachments":
#         {"attachment":      [
#             {"url":     "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75142299",
#              "docDescription":"Вх. Товарная накладная № 527 от 27 (№2255Вп-Тн от 17.02.2021) НПП ТЭЗ",
#              "fileName":"Вх. Товарная накладная № 527 от 27 (№2255Вп-Тн от 17.02.2021) НПП ТЭЗ.pdf",
#              "guid":"52108649-e1ea-4357-b89d-d2fd5ffcfad0",
#              "registrationNumber":"62539028264200001370024"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141834",
#              "docDescription":"Вх. Товарная накладная № 8031 от 2 (№581Вп-Тн от 18.01.2021) ТЭЗ3",
#              "fileName":"Вх. Товарная накладная № 8031 от 2 (№581Вп-Тн от 18.01.2021) ТЭЗ3.pdf",
#              "guid":"59263af8-bc2c-4238-9950-b2839f548e69",
#              "registrationNumber":"62539028264200001370019"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141835",
#              "docDescription":"Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ",
#              "fileName":"Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ.pdf",
#              "guid":"80aff414-9004-4c16-bfd9-c3f54d618bc4",
#              "registrationNumber":"62539028264200001370016"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141832",
#              "docDescription":"Вх. Товарная накладная № 6383 от 2 (№15213Вп-Тн от 23.11.2020) ТЭЗ",
#              "fileName":"Вх. Товарная накладная № 6383 от 2 (№15213Вп-Тн от 23.11.2020) ТЭЗ.pdf",
#              "guid":"d17ac90e-ebe1-4e0a-827b-81c67bde9399",
#              "registrationNumber":"62539028264200001370011"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141833",
#              "docDescription":"Вх. Товарная накладная № 56 от 14. (№1561Вп-Тн от 04.02.2021) ТЭЗ",
#              "fileName":"Вх. Товарная накладная № 56 от 14. (№1561Вп-Тн от 04.02.2021) ТЭЗ.pdf",
#              "guid":"52bc72cb-f0ac-4f45-808c-54414be3d82a",
#              "registrationNumber":"62539028264200001370022"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141838",
#              "docDescription":"ТЭЗ ПР",
#              "fileName":"ТЭЗ ПР.pdf",
#              "guid":"8096b396-8c11-40d0-8af6-e9cf9134214f",
#              "registrationNumber":"62539028264200001370005"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141836",
#              "docDescription":"Вх. Товарная накладная № 7390 от 2 (№579Вп-Тн от 18.01.2021) ТЭЗ2",
#              "fileName":"Вх. Товарная накладная № 7390 от 2 (№579Вп-Тн от 18.01.2021) ТЭЗ2.pdf",
#              "guid":"6772470f-6768-4649-a600-5c3e53f7d3cd",
#              "registrationNumber":"62539028264200001370018"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141837",
#              "docDescription":"Вх. Товарная накладная № 6679 от 3 (№15218Вп-Тн от 23.11.2020) ТЭЗ",
#              "fileName":"Вх. Товарная накладная № 6679 от 3 (№15218Вп-Тн от 23.11.2020) ТЭЗ.pdf",
#              "guid":"88d51e73-7ac0-48b4-aeaf-d7b3d51caf1a",
#              "registrationNumber":"62539028264200001370012"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141827",
#              "docDescription":"Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ1",
#              "fileName":"Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ1.pdf",
#              "guid":"b090c21e-5d1b-475a-bc12-769d3d6dca4a",
#              "registrationNumber":"62539028264200001370020"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141830",
#              "docDescription":"ПУР ТЭЗ",
#              "fileName":"ПУР ТЭЗ.pdf",
#              "guid":"7f2376fa-2c29-456b-98e9-1fcef4dbb6e3",
#              "registrationNumber":"62539028264200001370007"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141831",
#              "docDescription":"Платежное поручение № П4762 от 05.10.2020",
#              "fileName":"Платежное поручение № П4762 от 05.10.2020.pdf",
#              "guid":"57f5e2eb-94ce-45d5-ac9d-7ca2e5f36f69",
#              "registrationNumber":"62539028264200001370009"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141828",
#              "docDescription":"Р20357_Договор",
#              "fileName":"Р20357_Договор.pdf",
#              "guid":"adb89bad-c5f6-4237-aeee-baef5ec6aba9",
#              "registrationNumber":"62539028264200001370002"},
#             {"url":"https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141829",
#              "docDescription":"Товарная накладная ТЭЗ",
#              "fileName":"Товарная накладная ТЭЗ.pdf",
#              "guid":"e8eec009-8ba1-41b7-8934-62c65d04a3a3",
#              "registrationNumber":"62539028264200001370014"}]},
#     "createDateTime":"2021-02-17T09:43:46Z",
#     "currency":     {"code":"RUB",
#                      "name":"Российский рубль",
#                      "digitalCode":"643"},
#     "customer":     {"OGRN":"1022502117516",
#                      "OKATO":"05401000000",
#                      "fullName":"АКЦИОНЕРНОЕ ОБЩЕСТВО \"ИЗУМРУД\"",
#                      "iko":"62539028264253901001",
#                      "inn":"2539028264",
#                      "kpp":"253901001",
#                      "legalAddress":"690105, Приморский край, г Владивосток, р-н Советский, ул Русская, дом 65",
#                      "postalAddress":"690105, Приморский край, г Владивосток, р-н Советский, ул Русская, дом 65",
#                      "regNum":"13200000001",
#                      "shortName":"АО \"ИЗУМРУД\""},
#     "execution":     {"startDate":"2020-07-29",
#                       "endDate":"2020-12-31"},
#     "fileVersion":  "20210217_235959_020",
#     "fz":           "223",
#     "id":           "407195f7-e568-4198-b11f-5443929026f5",
#     "loadId":       1527,
#     "misuses":      [
#                         "prodname","nosuppliers"],
#     "modification": {"description":"исполнение договора"},
#     "name":         "Р20357",
#     "number":       "62539028264200001370023",
#     "placer":       {"mainInfo": {"kpp":    "253901001",
#                                   "okato":  "05401000000",
#                                   "okpo":   "07526952",
#                                   "ogrn":   "1022502117516",
#                                   "fullName":"АКЦИОНЕРНОЕ ОБЩЕСТВО \"ИЗУМРУД\"",
#                                   "inn":    "2539028264",
#                                   "legalAddress":"690105, Приморский край, г Владивосток, р-н Советский, ул Русская, дом 65",
#                                   "shortName":"АО \"ИЗУМРУД\"",
#                                   "postalAddress":"690105, Приморский край, г Владивосток, р-н Советский, ул Русская, дом 65"}},
#     "price":        524676.0,
#     "products":     [
#                         {"name":    "Диоды",
#                          "OKPD2":   {"code":    "26.11.21.110",
#                                      "name":    "Диоды"},
#                          "ordinalNumber":   "1"}
#                     ],
#     "protocolDate": "2020-07-29T00:00:00Z",
#     "publishDate":  "2021-02-17T09:45:05",
#     "purchaseInfo": {"purchaseNoticeNumber":"32009363123",
#                      "purchaseCodeName":    "Иной способ закупки, предусмотренный правовым актом заказчика, указанным в части 1 статьи 2 Федерального закона",
#                      "name":                "Диоды, НПП ТЭЗ",
#                      "purchaseMethodCode":  "40000"},
#     "regNum":       "62539028264200001370000",
#     "regionCode":   "25",
#     "scan":         [
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75142299",
#                          "docDescription":  "Вх. Товарная накладная № 527 от 27 (№2255Вп-Тн от 17.02.2021) НПП ТЭЗ",
#                          "fileName":        "Вх. Товарная накладная № 527 от 27 (№2255Вп-Тн от 17.02.2021) НПП ТЭЗ.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141834",
#                          "docDescription":  "Вх. Товарная накладная № 8031 от 2 (№581Вп-Тн от 18.01.2021) ТЭЗ3",
#                          "fileName":        "Вх. Товарная накладная № 8031 от 2 (№581Вп-Тн от 18.01.2021) ТЭЗ3.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141835",
#                          "docDescription":  "Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ",
#                          "fileName":        "Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141832",
#                          "docDescription":  "Вх. Товарная накладная № 6383 от 2 (№15213Вп-Тн от 23.11.2020) ТЭЗ",
#                          "fileName":        "Вх. Товарная накладная № 6383 от 2 (№15213Вп-Тн от 23.11.2020) ТЭЗ.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141833",
#                          "docDescription":  "Вх. Товарная накладная № 56 от 14. (№1561Вп-Тн от 04.02.2021) ТЭЗ",
#                          "fileName":        "Вх. Товарная накладная № 56 от 14. (№1561Вп-Тн от 04.02.2021) ТЭЗ.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141838",
#                          "docDescription":  "ТЭЗ ПР",
#                          "fileName":        "ТЭЗ ПР.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141836",
#                          "docDescription":  "Вх. Товарная накладная № 7390 от 2 (№579Вп-Тн от 18.01.2021) ТЭЗ2",
#                          "fileName":        "Вх. Товарная накладная № 7390 от 2 (№579Вп-Тн от 18.01.2021) ТЭЗ2.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141837",
#                          "docDescription":  "Вх. Товарная накладная № 6679 от 3 (№15218Вп-Тн от 23.11.2020) ТЭЗ",
#                          "fileName":        "Вх. Товарная накладная № 6679 от 3 (№15218Вп-Тн от 23.11.2020) ТЭЗ.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141827",
#                          "docDescription":  "Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ1",
#                          "fileName":        "Вх. Товарная накладная № 7053 от 2 (№16176Вп-Тн от 11.12.2020) ТЭЗ1.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141830",
#                          "docDescription":  "ПУР ТЭЗ",
#                          "fileName":        "ПУР ТЭЗ.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141831",
#                          "docDescription":  "Платежное поручение № П4762 от 05.10.2020",
#                          "fileName":        "Платежное поручение № П4762 от 05.10.2020.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141828",
#                          "docDescription":  "Р20357_Договор",
#                          "fileName":        "Р20357_Договор.pdf"},
#                         {"url":             "https://lk.zakupki.gov.ru/223/contract/private/download/download.html?id=75141829",
#                          "docDescription":  "Товарная накладная ТЭЗ",
#                          "fileName":        "Товарная накладная ТЭЗ.pdf"}
#                     ],
#     "schemaVersion":    "10.1",
#     "signDate":         "2020-07-29T00:00:00Z",
#     "status":           "P",
#     "versionNumber":    11}