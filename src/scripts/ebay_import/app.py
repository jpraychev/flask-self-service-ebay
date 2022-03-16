import sys
import ean.utils as ean_utils
import sys
import pandas as pd
import numpy as np
from utils import header, export, rooms, models, cm_to_foot
from html import html_template
from rows import MainRow, VariantRow
from material import Material
import re
from pathlib import Path

def drop_attr(string):
    """ Drops Color_ and Size_ attributes from a string using a regex expression.
    This function replaces usage of multiple replace() calls """
    txt = re.sub('(Size_)|(Color_)', '', string)
    sep_txt = txt.replace(',', ';', 1)
    return sep_txt

def size_cm_to_ft(sizes):

    temp_arr = list()
    if isinstance(sizes, str):
        sizes = sizes.split(',')

    for size in sizes:
        size = size.strip()
        if 'x' in size:
            splitted = size.replace('cm','').split('x')
            w_cm, l_cm = splitted[0], splitted[1]
            w_ft, l_ft = cm_to_foot[w_cm], cm_to_foot[l_cm]
            string = f'{w_cm}x{l_cm}cm ({w_ft}x{l_ft})'
            temp_arr.append(string)
        else:
            splitted = size.split('cm')
            size_cm, size_type = splitted[0].strip(), splitted[1].strip()
            string = f'{size_cm}cm ({cm_to_foot[size_cm]}) {size_type.capitalize()}'
            temp_arr.append(string)

    return temp_arr

def get_relation_details(row) -> str:
    """ Tags for a shopify product should contain one of the following structures,
    anything else should be discouraged:
    - Size_120x170 cm;
    - Size_120x170cm;
    - Size_200 cm round;
    - Size_200cm round;
    """

    tags = row[1].to_dict()['Tags']
    flat_tags = [tag.replace(' cm', 'cm') for tag in tags if tag is not np.NaN]
    joined_flat_tags = ','.join(flat_tags)

    if not 'cm' in joined_flat_tags:
        raise ValueError('"cm" is missing for product size')

    flat_wo_tags = drop_attr(joined_flat_tags).split(';')
    color = flat_wo_tags[0].strip()
    size = flat_wo_tags[1].strip()
    
    if INCH_FLAG:
        sizes_ft = size_cm_to_ft(size)
        size = ', '.join(sizes_ft)

    tags = f'Color={color}|Size={size}'
    return tags

def get_title(row) -> str:
    title = row[1].to_dict()['Title']
    flat_title = [val for val in title if val is not np.NaN][0]
    if len(flat_title) > 80:
        raise ValueError("Title's length has to be below 80 characters\n", flat_title, len(flat_title))
    return flat_title

def get_images(row) -> str:
    if ACCOUNT == 'xrug':
        urls = [
            'https://rugsdropshipping.uk/wp-content/uploads/export/xrug/xrug_five.jpg',
            'https://rugsdropshipping.uk/wp-content/uploads/export/xrug/xrug_size.jpg'
        ]
    else:
        urls = ['https://www.rugsdropshipping.uk/wp-content/uploads/export/xrug/magicrug.jpg']

    images = row[1].to_dict()['Image Src']
    flat_images = [val for val in images if val is not np.NaN]
    [flat_images.append(url) for url in urls]
    join_images = ','.join(flat_images).replace(',','|')
    return (join_images)

def get_color(row) -> str:
    tags = row[1].to_dict()['Tags']
    flat_tags = [val.replace(' ', '') for val in tags if val is not np.NaN]
    drop_comma = [val.replace(',', ';', 1) for val in flat_tags]
    color = drop_comma[0].split(';')[0].split('_')[1]
    return color

def get_prices(row):
    prices = row[1].to_dict()['Variant Price']
    p_arr = [p for p in prices if p >= 0]
    min_elem = sorted(p_arr)[0]
    new_prices = list()
    for price in p_arr:
        if price == min_elem:
            price = price * 1.00
        else:
            price = price * 1.25
        new_prices.append(round(price,2))
    return new_prices

def get_sizes(row, s_type=None):
    """Sizes located in Option1 Value should have the following structure,
    anything else should be discouraged:
        - 80x150 cm;
        - 80x150cm;
        - 120 cm round/square;
        - 120cm round/square;
    """

    sizes = row[1].to_dict()['Option1 Value']

    flat_size = [size for size in sizes if size is not np.NaN]
    if not 'cm' in ','.join(flat_size):
        raise ValueError('"cm" is missing for product size')

    cm_size = [size.replace(' cm','cm') for size in flat_size]
    if s_type is not None:
        return cm_size
    final_size = cm_size if not INCH_FLAG else size_cm_to_ft(cm_size)

    return final_size

def get_single_variation(row):
    color = get_color(row)
    sizes = get_sizes(row)
    temp_arr = list()

    for size in sizes:
        temp_arr.append(f"Color={color}|Size={size}")
    return temp_arr

def get_ean() -> int:
    if isinstance(DRY_RUN, str):
        dr = eval(DRY_RUN)
    if dr:
        return 123456789
    # if len(ean.unused_numbers) < 100:
        # raise ValueError('EAN numbers are less than 100.')
    num = EAN_NUMS.pop()
    return num 

def get_width_length(row):
    sizes = get_sizes(row, 'cm')
    sizes = [size.replace(' ','') for size in sizes if size is not np.NaN]
    w = [f"{size.split('x')[0]}cm" for size in sizes if 'x' in size]
    l = [size.split('x')[1] for size in sizes if 'x' in size]
    widths = (', ').join(w)
    lengths = (', ').join(l)
    if len(widths) > 65 or len(lengths) > 65:
        raise ValueError("Maximum allowed 65 characters for lengths/widths is exceeded.")
    return widths, lengths

def get_room(product_title:str) -> str:
    
    room = list()
    title = product_title.lower()

    for key, value in rooms.items():
        if key in title:
            room.append(value)
    
    out_rooms = ', '.join(room) if len(room) > 0 else rooms['livingroom']
    return out_rooms

def get_sku(row):
    skus = row[1].to_dict()['Variant SKU']
    sku_arr = [sku for sku in skus if sku is not np.NaN]
    return sku_arr

def get_desc_list(row):
    html = row[1].to_dict()['Body (HTML)'][0]
    start = html.find('<ul>')
    end = html.find('</ul>')
    list_items = html[start:end].replace('<ul>', '').strip()
    start_p, end_p = '<p> - ', '</p>'
    desc_list = list_items.replace('<li>', start_p).replace('</li>', end_p)
    return desc_list

def rug_category(title:str) -> str:
    """ Determine the rugs category based on its title """

    lower_title = title.lower()

    if 'kitchen' in lower_title:
        cat = 'kitchen'
    elif 'children' in lower_title or 'kids' in lower_title or 'nursery' in lower_title:
        cat = 'children'
    elif 'indoor' in lower_title or 'outdoor' in lower_title:
        cat = 'indoor_outdoor'
    else:
        cat = 'livingroom'

    return cat

def replace_html(title:str, desc_list:str) -> str:
    """ Builds a dynamic HTML template for particular category of rugs. """
    
    cat = rug_category(title)
    
    try:
        full_html = html_template['full']['xrug']
        if ACCOUNT == 'magicrug':
            full_html = html_template['full']['magicrug']
    except KeyError:
        raise ValueError('Invalid account used for html template retrieval.')


    cat_html = html_template[cat]
    html = full_html.replace('__RUG_DESC_FULL', cat_html)
    title_placeholder = '__RUG_TITLE'
    desc_placeholder = '__RUG_DESC_LIST'
    return html.replace(title_placeholder, title).replace(desc_placeholder, desc_list)

def get_model_mpn(product_title:str) -> str:
    title = product_title.lower()
    for key, value in models.items():
        if key in title:
            return value, value + 'Rug'
    return '', ''

def get_quantities(row):
    quantities = row[1].to_dict()['Variant Inventory Qty']
    qa = [int(q) for q in quantities if q >= 0]
    return qa

def get_department(product_title:str) -> str:
    title = product_title.lower().split()
    childs = ['children', 'child', 'baby', 'girl', 'boy']
    depart = 'Children' if any(child in title for child in childs) else 'Adults'
    return depart

def get_material(row:str) -> str:
    html = row[1].to_dict()['Body (HTML)'][0].lower()
    mat = Material(html)
    return mat.get_material()

def category(cat_type):
    """ Returns rug's category
    Categories are downloaded from https://www.ebay.co.uk/sh/reports/uploads
    by generating a template for certain category
    Kids - Home, Furniture & DIY > Children's Home & Furniture > Home Décor & Organisation > Rugs & Carpets
    Normal - Home, Furniture & DIY > Rugs & Carpets > Rugs
    """

    categories = {
            "regular" : "45510",
            "kids" : "177062"
        }

    try:
        return categories[cat_type.lower()]
    except KeyError:
        raise ValueError('No such category. Supported categories: Regular (45510) and Kids (177062).')

def get_brand(acc:str) -> str:
    """ Returns one of the brands defined in brands list. If not found raise
        value error """

    brands = ['xrug', 'magicrug']

    if acc in brands:
        return acc.title()
    raise ValueError(f'{acc} is not supported. Supported brand xrug and magicrug')

def business_policies(account:str):
    """ Return dict of business policies (Shipping, Return and Payment) based on 
        user provided input. """

    policies = {
        'xrug' : {
            'shipping' : 'Kilim 24 ( 3-5 working days )',
            'returns' : 'Returns Accepted,Buyer,30 days',
            'payment' : 'PayPal:Immediate pay#0'
        },
        'magicrug' : {
            'shipping' : 'Rug 24 delivery,3 working days',
            'returns' : 'Returns Accepted,Seller,30 days#0',
            'payment' : 'PayPal:Immediate pay#2'
        }
    }

    try:
        return policies[account]
    except KeyError:
        raise ValueError(f'{account} is not support. Supported brand xrug and magicrug')

def export_main_rows(df2):

    main_row = MainRow(header)

    for row in df2.iterrows():
        details = get_relation_details(row)
        color = get_color(row)
        title = get_title(row)      
        images = get_images(row)
        width, length = get_width_length(row)
        rooms = get_room(title)
        desc_list = get_desc_list(row)
        html_desc = replace_html(title=title, desc_list=desc_list)
        model, mpn = get_model_mpn(title)
        depart = get_department(title)
        material = get_material(row)
        policies = business_policies(ACCOUNT)
        header['Category ID'].append(category(CAT))
        header['Relationship details'].append(details)
        header['Title'].append(title)
        header['Item photo URL'].append(images)
        header["Description"].append(html_desc)
        header["C:Colour"].append(color)
        header["C:Material"].append(material)
        header["C:Room"].append(rooms)
        header["C:Department"].append(depart)
        header["C:Item Width"].append(width)
        header["C:Item Length"].append(length)
        header["C:MPN"].append(mpn)
        header["C:Model"].append(model)
        header["C:Brand"].append(get_brand(ACCOUNT))
        header["Shipping profile name"].append(policies['shipping'])
        header["Return profile name"].append(policies['returns'])
        header["Payment profile name"].append(policies['payment'])

        main_row.add_empty()
        main_row.add_static()

def export_variant_rows(df2):

    variant_row = VariantRow(header)

    for row in df2.iterrows():
        variations = get_single_variation(row)
        prices = get_prices(row)
        titles = get_title(row)
        skus = get_sku(row)
        quantities = get_quantities(row)

        for q in quantities:
            header["Quantity"].append(q)
            
        for price in prices:
            header['Start price'].append(price)

        for sku in skus:
            header["Custom label (SKU)"].append(sku)

        for var in variations:
            header['Relationship details'].append(var)
            header['Title'].append(titles)
            ean = get_ean()
            header["P:EAN"].append(ean)

            variant_row.add_empty()
            variant_row.add_static()

def main():
    p = Path(__file__).resolve().parent.parent.parent
    input_fname = p.joinpath('uploads/shopify_import.csv')
    df = pd.read_csv(input_fname)
    df2 = df.groupby('Handle').agg(lambda x: list(x))
    export_main_rows(df2)
    export_variant_rows(df2)
    output_fname = p.joinpath('downloads/ebay_export.csv')
    export(header, output_fname)

if __name__ == '__main__':

    dim = sys.argv[sys.argv.index('--dimension')+1]
    cat = sys.argv[sys.argv.index('--category')+1]
    dry_run = sys.argv[sys.argv.index('--dry_run')+1]
    acc = sys.argv[sys.argv.index('--account')+1]

    INCH_FLAG = True if 'inch' in dim else False
    CAT = cat
    DRY_RUN = dry_run
    ACCOUNT = acc

    curr = Path(__file__).resolve().parent
    ean_txt = curr.joinpath('ean/ean.txt')
    EAN_NUMS = ean_utils.load_data(ean_txt)
    main()

    ean_utils.save_data(fname=ean_txt, items=EAN_NUMS)
