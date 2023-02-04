from module.utils import Utils
maxDeliveryValue = 1500
class Delivery(object):
    cart_value = None
    delivery_distance = None
    number_of_items = None
    time = None
    shippingFee = None
    def __init__(self, query_components):
        'could cart value be 0 or less?'
        (cart_value, delivery_distance, number_of_items, time) = Delivery.validateData(query_components)
        self.cart_value = cart_value
        self.delivery_distance = delivery_distance
        self.number_of_items = number_of_items
        self.time = time
        self.shippingFee = 0
        self.updateShippingFee()
    def getShippingFee(self):
        return self.shippingFee
    def updateShippingFee(self):
        if self.cart_value > 100000:
            return
        'if the cart value is less than 10 eur, add to the shippping fee the difference between 10 and cart value'
        if(self.cart_value < 1000):
            self.shippingFee += 1000 - self.cart_value
        
        'shippping distance (2 eur fixed)'
        self.shippingFee += 200
        'count how many times the courier has to travel 500m excluding the first 1000m'
        times = ((self.delivery_distance-1000) // 500) + 1
        if(self.delivery_distance % 500 == 0): times -=1
        if(times>0):
            self.shippingFee += times * 100

        extraItems = self.number_of_items - 4
        'if there are more then 12 total items, set the extra items to 9 and add the bulk fee'
        if extraItems >= 9: 
            extraItems = 9
            self.shippingFee += 120
        if extraItems > 0: self.shippingFee += extraItems * 50

        if(Utils.isFridayRush(self.time)):
            self.shippingFee = int(self.shippingFee * 1.2)

        if self.shippingFee > maxDeliveryValue: self.shippingFee = maxDeliveryValue
            
        return
    @staticmethod
    def validateData(query_components):
        try:
            cart_value = int(query_components["cart_value"][0]) if len(query_components["cart_value"]) > 0 else None
            delivery_distance = int(query_components["delivery_distance"][0]) if len(query_components["delivery_distance"]) > 0 else None
            number_of_items = int(query_components["number_of_items"][0]) if len(query_components["number_of_items"]) > 0 else None
            time = query_components["time"][0] if len(query_components["time"]) > 0 else None
        except KeyError:
            raise ValueError("Parameter missing")
        except TypeError:
            raise ValueError("Wrong data type")
        if(cart_value<=0 or delivery_distance<=0 or number_of_items<=0):
            raise ValueError("Invalid value provided")
        if(not Utils.validateISO8601Date(time)):
            raise ValueError("Invalid date provided")
        return (cart_value, delivery_distance, number_of_items, time)


        