from abc import ABC, abstractmethod


class Row(ABC):    

    def __init__(self, header):
        self.header = header
    
    @abstractmethod
    def add_empty(self):
        pass

    @abstractmethod
    def add_static(self):
        pass


class MainRow(Row):
    
    empty_items = {
        "Custom label (SKU)" : "",
        "Relationship" : "",
        "P:UPC" : "",
        "P:ISBN" : "",
        "P:EAN" : "",
        "P:EPID" : "",
        "Start price" : "",
        "Quantity" : "",
        "Buy It Now price" : "",
        "Paypal accepted" : "",
        "Paypal email address" : "",
        "Immediate pay required" : "",
        "Payment instructions" : "",
        "Shipping service 1 option" : "",
        "Shipping service 1 cost" : "",
        "Shipping service 1 priority" : "",
        "Shipping service 2 option" : "",
        "Shipping service 2 cost" : "",
        "Shipping service 2 priority" : "",
        "Returns accepted option" : "",
        "Returns within option" : "",
        "Refund option" : "",
        "Return shipping cost paid by" : "",
        "C:Size" : "",
        "C:Style" : "" }
    static_items = {
        "*Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193)" : "Add",
        "Condition ID" : "1000",
        "Format" : "FixedPrice",
        "Duration" : "GTC",
        "VAT%" : "20",
        "Location" : "Wyboston, Beds",
        "Shipping profile name" : "Kilim 24 ( 3-5 working days )",
        "Return profile name" : "Returns Accepted,Buyer,30 days",
        "Payment profile name" : "PayPal:Immediate pay#0",
        "C:Brand" : "Xrug",
        "C:Type" : "Rug",
        "C:Regional Design" : "English",
        "Max dispatch time" : "3"}

    def __init__(self, header):
        super().__init__(header)
    
    def add_empty(self):
        for item, value in self.empty_items.items():
            self.header[item].append(value)

    def add_static(self):
        for item, value in self.static_items.items():
            self.header[item].append(value)
    

class VariantRow(Row):

    empty_items = {
        "*Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193)" : "",
        "Item photo URL" : "",
        "Category ID" : "",
        "P:UPC" : "",
        "P:ISBN" : "",
        "P:EPID" : "",
        "Condition ID" : "",
        "Description" : "",
        "Format" : "",
        "Duration" : "",
        "Buy It Now price" : "",
        "VAT%" : "",
        "Paypal accepted" : "",
        "Paypal email address" : "",
        "Immediate pay required" : "",
        "Payment instructions" : "",
        "Location" : "",
        "Shipping service 1 option" : "",
        "Shipping service 1 cost" : "",
        "Shipping service 1 priority" : "",
        "Shipping service 2 option" : "",
        "Shipping service 2 cost" : "",
        "Shipping service 2 priority" : "",
        "Max dispatch time" : "",
        "Returns accepted option" : "",
        "Returns within option" : "",
        "Refund option" : "",
        "Return shipping cost paid by" : "",
        "Shipping profile name" : "",
        "Return profile name" : "",
        "Payment profile name" : "",
        "C:Brand" : "",
        "C:Type" : "",
        "C:Regional Design" : "",
        "C:Colour" : "",
        "C:Material" : "",
        "C:Size" : "",
        "C:Style" : "",
        "C:Room" : "",
        "C:Department" : "",
        "C:Item Width" : "",
        "C:Item Length" : "",
        "C:MPN" : "",
        "C:Model" : ""}
    static_items = {"Relationship" : "Variation"}

    def __init__(self, header):
        super().__init__(header)

    def add_empty(self):
        for item, value in self.empty_items.items():
            self.header[item].append(value)

    def add_static(self):
        for item, value in self.static_items.items():
            self.header[item].append(value)
