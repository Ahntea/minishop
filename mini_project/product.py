class Product():
    """
    Product 클래스 
    요소
    id_ , product_name , price, remains , regdate
    """
    
    def __init__(self, id_, product_name, price,remains,regdate):
        self.id_ = id_
        self.product_name = product_name
        self.price = price
        self.remains = remains
        self.regdate = regdate
    
    def order(self, count):
        self.remains = int(self.remains) - count

    def get_id(self):
        return self.id_

    def get_product_name(self):
        return self.product_name
    
    def get_remains(self):
        return self.remains

    def get_price(self):
        return self.price

    def get_regdate(self):
        return self.regdate
