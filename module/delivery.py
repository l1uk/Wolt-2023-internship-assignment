'''
Delivery class, containing all the deliveries info and performing the Fee calculation.
'''
from module.utils import Utils
maxDeliveryFeeValue = 1500
class Delivery(object):
    cart_value = None
    delivery_distance = None
    number_of_items = None
    time = None
    shippingFee = None
    def __init__(self, query_components, cart_value = None, delivery_distance = None, number_of_items = None, time = None):
        '''
        The constructor is designed to handle both a dictionary of variables (default) or single values (non-mandatory).
        In the first case, values are extracted from the dictionary using the static method Delivery.extractDataFromDict()
        Values are first validated using the static method validateData(), 
        then assigned to the freshly create object and finally the method updateShippingFee() is called to calculate the Shipping Fee for the delivery.
        '''
        if(query_components != None):
            (cart_value, delivery_distance, number_of_items, time) = Delivery.extractDataFromDict(query_components)
        Delivery.validateData(cart_value, delivery_distance, number_of_items, time)
        self.cart_value = int(cart_value)
        self.delivery_distance = int(delivery_distance)
        self.number_of_items = int(number_of_items)
        self.time = time
        self.shippingFee = 0
        self.updateShippingFee()
            
    def getShippingFee(self):
        '''Simple getter method'''
        return self.shippingFee
    def updateShippingFee(self):
        '''
        Performs the calculation of the delivery according to the following specifications:  
        If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
        A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
        Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
        Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
        Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
        If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 1,20€
        Example 1: If the number of items is 4, no extra surcharge
        Example 2: If the number of items is 5, 50 cents surcharge is added
        Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
        Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
        The delivery fee can never be more than 15€, including possible surcharges.
        The delivery is free (0€) when the cart value is equal or more than 100€.
        During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€).
        '''
        self.shippingFee = 0
        if self.cart_value > 100000:
            return
        'if the cart value is less than 10 eur, add to the shippping fee the difference between 10 and cart value'
        if(self.cart_value < 1000):
            self.shippingFee += 1000 - self.cart_value
        
        'shippping distance (2 eur fixed)'
        self.shippingFee += 200
        'count how many times the courier has to travel 500m excluding the first 1000m, and add 1 eur for each additional 500m'
        times = ((self.delivery_distance-1000) // 500) + 1
        'this line is E.G. for accounting 1500m the same as 1499m and not the same as 1501m'
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

        if self.shippingFee > maxDeliveryFeeValue: self.shippingFee = maxDeliveryFeeValue
            
        return
    @staticmethod
    def extractDataFromDict(query_components):
        '''
        Static method used to extract the class variables from the query components dictionary, containing parameters from a parsed url.
        '''
        try:
            cart_value = query_components["cart_value"][0] if len(query_components["cart_value"]) > 0 else None
            delivery_distance = query_components["delivery_distance"][0] if len(query_components["delivery_distance"]) > 0 else None
            number_of_items = query_components["number_of_items"][0] if len(query_components["number_of_items"]) > 0 else None
            time = query_components["time"][0] if len(query_components["time"]) > 0 else None
        except KeyError:
            raise ValueError("Parameter missing")
        except TypeError:
            raise ValueError("Wrong data type")
        return (cart_value, delivery_distance, number_of_items, time)
        s
    @staticmethod
    def validateData(cart_value, delivery_distance, number_of_items, time):
        '''
        Static method used to validate the data used to instantiate the object. 
        Checks on the non-negativity of the parameters and the coherence of the date are performed. 
        '''
        if(int(cart_value)<=0 or int(delivery_distance)<=0 or int(number_of_items)<=0):
            raise ValueError("Invalid value provided")
        if(not Utils.validateISO8601Date(time)):
            raise ValueError("Invalid date provided")   