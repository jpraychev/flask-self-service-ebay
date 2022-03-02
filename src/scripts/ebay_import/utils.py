header = {
    "*Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193)": [],
    "Custom label (SKU)": [],
    "Category ID": [],
    "Title": [],
    "Relationship": [],
    "Relationship details": [],
    "P:UPC": [],
    "P:ISBN": [],
    "P:EAN": [],
    "P:EPID": [],
    "Start price": [],
    "Quantity": [],
    "Item photo URL": [],
    "Condition ID": [],
    "Description": [],
    "Format": [],
    "Duration": [],
    "Buy It Now price": [],
    "VAT%": [],
    "Paypal accepted": [],
    "Paypal email address": [],
    "Immediate pay required": [],
    "Payment instructions": [],
    "Location": [],
    "Shipping service 1 option": [],
    "Shipping service 1 cost": [],
    "Shipping service 1 priority": [],
    "Shipping service 2 option": [],
    "Shipping service 2 cost": [],
    "Shipping service 2 priority": [],
    "Max dispatch time": [],
    "Returns accepted option": [],
    "Returns within option": [],
    "Refund option": [],
    "Return shipping cost paid by": [],
    "Shipping profile name": [],
    "Return profile name": [],
    "Payment profile name": [],
    "C:Brand": [],
    "C:Type": [],
    "C:Regional Design": [],
    "C:Colour": [],
    "C:Material": [],
    "C:Size": [],
    "C:Style": [],
    "C:Room": [],
    "C:Department": [],
    "C:Item Width": [],
    "C:Item Length": [],
    "C:MPN": [],
    "C:Model": []
}

rooms = {
    'basement' : 'Basement',
    'bathroom' : 'Bathroom',
    'livingroom' : 'Living room',
    'living' : 'Living room',
    'children' : 'Children',
    'bedroom' : 'Bedroom',
    'diningroom' : 'Dining room',
    'indoor' : 'Indoor/Outdoor',
    'outdoor' : 'Indoor/Outdoor',
    'kitchen' : 'Kitchen',
    'nursery' : 'Nursery',
    'any' : 'Any Room'
}

models = {
    "geometric" : "Geometric",
    "floral" : "Floral",
    "border" : "Border",
    "striped" : "Striped",
    "oriental" : "Oriental",
    "moroccan" : "Moroccan",
    "trellis" : "Trellis",
    "diamond" : "Diamond",
    "solid" : "Solid",
    "monochrome" : "Monochrome",
    "patchwork" : "Patchwork",
    "vintage" : "Vintage",
    "retro" : "Retro",
    "check" : "Check",
    "zigzag" : "ZigZag",
    "chevron" : "Chevron",
    "berber" : "Berber"
}

duplicate_regex = '^(.*)(\r?\n\1)+$'
design_removal = 'Design_[\w\d\s]*,'
inch_removal = """cm\s\([\d'"x]+\)"""

cm_to_foot = {
    "10" : "0'3''",
    "20" : "0'7''",
    "30" : "1'",
    "40" : "1'3''",
    "50" : "1'6''",
    "60" : "2'",
    "70" : "2'3''",
    "80" : "2'6''",
    "90" : "3'",
    "100" : "3'3''",
    "110" : "3'6''",
    "120" : "3'9''",
    "130" : "4'3''",
    "133" : "4'4''",
    "140" : "4'6''",
    "150" : "4'9''",
    "160" : "5'2''",
    "170" : "5'6''",
    "180" : "5'9''",
    "190" : "6'2''",
    "200" : "6'6''",
    "210" : "6'9''",
    "220" : "7'2''",
    "230" : "7'5''",
    "240" : "7'9''",
    "250" : "8'2''",
    "260" : "8'5''",
    "270" : "8'9''",
    "280" : "9'2''",
    "290" : "9'5''",
    "300" : "9'8''",
    "310" : "10'2''",
    "320" : "10'5''",
    "330" : "10'8''",
    "340" : "11'2''",
    "350" : "11'5''",
    "360" : "11'8''",
    "370" : "12'1''",
    "380" : "12'5''",
    "390" : "12'8''",
    "400" : "13'1''",
    "410" : "13'5''",
    "420" : "13'8''",
    "430" : "14'1''",
    "440" : "14'4''",
    "450" : "14'8''",
    "460" : "15'1''",
    "470" : "15'4''",
    "480" : "15'7''",
    "490" : "16'1''",
    "500" : "16'4''",
    "510" : "16'7''",
    "520" : "17'1''",
    "530" : "17'4''",
    "540" : "17'7''",
    "550" : "18'",
    "560" : "18'4''",
    "570" : "18'7''",
    "580" : "19'",
    "590" : "19'4''",
    "600" : "19'7''",
    "610" : "20'",
    "620" : "20'3''",
    "630" : "20'7''",
    "640" : "21'",
    "650" : "21'3''",
    "660" : "21'7''",
    "670" : "22'",
    "680" : "22'3''",
    "690" : "22'6''",
    "700" : "23'",
    "710" : "23'3''",
    "720" : "23'6''",
    "730" : "24'",
    "740" : "24'3''",
    "750" : "24'6''",
    "760" : "24'9''",
    "770" : "25'3''",
    "780" : "25'6''",
    "790" : "25'9''",
    "800" : "26'2''",
    "810" : "26'6''",
    "820" : "26'9''",
    "830" : "27'2''",
    "840" : "27'6''",
    "850" : "27'9''",
    "860" : "28'2''",
    "870" : "28'5''",
    "880" : "28'9''",
    "890" : "29'2''",
    "900" : "29'5''",
    "910" : "29'9''",
    "920" : "30'2''",
    "930" : "30'5''",
    "940" : "30'8''",
    "950" : "31'2''",
    "960" : "31'5''",
    "970" : "31'8''",
    "980" : "32'2''",
    "990" : "32'5''"
}

def flatten_dict_list(arr:list) -> list:
    import operator
    from functools import reduce
    return reduce(operator.concat, arr)

def export(data, fname:str):
    import pandas as pd
    df = pd.DataFrame.from_dict(data)
    sorted_df = df.sort_values(by=['Title', 'Category ID'], ascending=[True, False])
    sorted_df.to_csv(fname, index=False)

def transform_to_ul() -> str:

    with open('desc_list.txt') as f:
        lines = f.readlines()

    a = [line for line in lines if not line.startswith('\n')]
    b = [line.replace('-','').replace('\n','') for line in a]

    print('<ul>')
    for line in b:
        print(f'<li>{line}</li>')
    print('</ul>')