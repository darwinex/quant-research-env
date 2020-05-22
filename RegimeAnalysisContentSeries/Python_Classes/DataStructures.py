# Module for representing a generic bar > Imports:
import json

########################################################################

class Trade:

    '''
    Represent a trade in a market, a transaction between a buyer and a seller
    in its atomic representation
    '''

    def __init__(self):

        '''
        Initializes an empty Trade object
        '''

        # Represent the symbol this trade belongs to.
        self.symbol = None 

        # Unix epoch timestamp representing the time of the trade
        self.timestamp = None 

        # The price at which the trade was carried out
        self.price = None 

        # The size (volume) of the trade
        self.size = None 

        # Whether the taggresor side of the trade is BUY or SELL
        self.tradeDirection = None 

    ######################### Overwritting Python Magic Methods #########################

    # Defines behavior for the equality operator, ==
    def __eq__(self, other):

        if(isinstance(other, Trade)):
            return ((self.symbol, self.timestamp, self.price, self.size, self.tradeDirection) == (other.symbol, other.timestamp, other.price, other.size, other.tradeDirection))
        else:
            False 

    # Defines behavior for the less-than-or-equal-to operator, <=
    def __le__(self, other):
        '''
        Trade object is defined lower equal if the price of 'other' is greater or equal than self
        '''
        return self.price <= other.price

    # Defines behavior for the less-than operator, <
    def __lt__(self, other):
        return self.price < other.price

    # Defines behavior for the greater-than-or-equal-to operator, >=
    def __ge__(self, other):
        return self.price >= other.price
    
    # Defines behavior for the greater-than operator, >
    def __gt__(self, other):
        return self.price > other.price

    # Defines behavior for when repr() is called on an instance of your class. repr() is intended to produce output that is mostly machine-readable
    def __repr__(self):

        return self.to_json()

    ######################### Overwritting Python Magic Methods #########################

    def to_dict(self) -> dict:

        '''
        Returns the python dictionary representation of this object
        '''

        dic_rpr = {}
        dic_rpr['symbol'] = self.symbol
        dic_rpr['timestamp'] = self.timestamp
        dic_rpr['price'] = self.price
        dic_rpr['size'] = self.size
        dic_rpr['tradeDirection'] = self.tradeDirection

        return dic_rpr
    
    # This means that this method can be called without declarating the object
    @staticmethod 
    def from_dict(dict_rpr: dict):

        '''
        Returns a python trade object from its dict representation

        params:

            dict_rpr - dict: The dictionary representation of Trade object
        '''

        # Declare the trade object to return
        tradObj = Trade()

        # Populate the trade object with the dictionary properties
        tradObj.symbol = dict_rpr['symbol']
        tradObj.timestamp = dict_rpr['timestamp']
        tradObj.price = dict_rpr['price']
        tradObj.size = dict_rpr['size']
        tradObj.tradeDirection = dict_rpr['tradeDirection']

        # Return the populated trade object
        return tradObj

    def to_json(self) -> str:

        '''
        Returns the json representation of this object
        '''
        # Just call the json serializer passing the dict representation of this object
        return json.dumps(self.to_dict())
    
    @staticmethod
    def from_json(json_rpr):

        '''
        Returns a Trade object from its json str representation
        
        params
            json - str: the JSON (java script object notation) representation of Trade object
        '''

        # Parse json to dict and later parse from dict
        return Trade.from_dict(json.loads(json_rpr))

########################################################################

class BaseBar:

    '''
    Represent a generic financial data structure > Candle/Bar
    '''

    def __init__(self, is_future_symbol: bool = False, price_tick: float = 0):

        '''
        Returns an empty bar

        params:

            is_future_symbol: boolean (optional)- Whether if the symbol is a future, and thus it must taken the price tick on acount, or not.
            price_tick: float (optional) - Represent the minimun price change in the market. If the is_future_symbol is set to true, the price_tick 
            must be specified.

        '''

        # Set attributes:
        self.is_future_symbol = is_future_symbol
        self.price_tick = price_tick

        # Define the empty properties of the bar
        self.opening_trade: Trade = None # Represents the opening trade of the bar
        self.high_trade: Trade = None # Represents the highest price trade within the bar
        self.low_trade: Trade = None # Represent the lowest price trade within the bar
        self.last_trade: Trade = None # Represent the last trade introduced to the bar
        self.closing_trade: Trade = None # Represent the closing trade of the bar
        self.volume: int = 0 # Represent the total number of trades within the bar
        self.type: str = None # Represent the type of bar, bullish or bearish

        # Its a callback that will be passed to the bar, that returns a boolean to determine when the bar closes
        self.closing_condition: callable[[Trade, Trade], bool] = lambda *args: False 

        # Generate the internal object that will represent the trades inside
        # a list that represents the price rows of the bar
        self.__price_rows = [] 

    def __initialize_bar(self, trade):

        '''
        Initializes the bar with the trade
        '''

        # Set the trade as opening trade
        self.opening_trade = trade

        # More to add!

    def __update_bar_properties(self):

        '''
        Updates the bar's properties (such as high_trade or volume) with the current data
        '''
        # Get the greatest trade in the greatest tick
        self.high_trade = max(max(self.__price_rows).trades)

        # Analogy, get the low trade
        self.low_trade = min(min(self.__price_rows).trades)

        # Check if bar is bullish or bearish
        if self.opening_trade < self.last_trade:
            self.type = 'Bullish'
        elif self.opening_trade > self.last_trade:
            self.type = 'Bearish'
        elif self.opening_trade.price == self.last_trade.price:
            self.type = 'Doji'
        else:
            # THIS SHOULD NEVER HAPPEN!
            self.type = 'Undefined'
        
    def __check_closing_condition(self):

        '''
        Checks if the bar should be closed according to just set closing condition
        '''
        # Return the closing condition pointer that returns the closing condition
        condition = self.closing_condition(self)
        return condition

    def set_closing_condition(self, condition):

        '''
        Set the closing condition of the bar.

        Params:
            condition - callable[[Trade, Trade], bool] : a callable function that returns a bool when 
            called with opening_trade and last_trade (both Trade objects) respectively
        '''

        self.closing_condition = condition

    def reset(self):
        
        '''
        Resets the bar to the initial state
        '''

        # Define the empty properties of the bar
        self.opening_trade: Trade = None # Represents the opening trade of the bar
        self.high_trade: Trade = None # Represents the highest price trade within the bar
        self.low_trade: Trade = None # Represent the lowest price trade within the bar
        self.last_trade: Trade = None # Represent the last trade introduced to the bar
        self.closing_trade: Trade = None # Respresents the closing trade of the bar
        self.volume: int = 0 # Represent the total number of trades within the bar
        self.type: str = None # Represnet the type of bar, bullish or bearish

        self.__price_rows = []
            
    def to_dict(self) -> dict:

        '''
        Returns the JSON representation of the bar
        '''

        dict_rpr = {}
        dict_rpr['openTrade'] = self.opening_trade.to_dict()
        dict_rpr['highTrade'] = self.high_trade.to_dict()
        dict_rpr['lowTrade'] = self.low_trade.to_dict()
        dict_rpr['closeTrade'] = self.last_trade.to_dict()
        dict_rpr['volume'] = self.volume
        dict_rpr['type'] = self.type
        dict_rpr['tickPriceInfo'] = [tick.to_dict() for tick in self.__price_rows]

        return dict_rpr

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

########################################################################

if __name__ == "__main__":

    # TODO: Develop example.
    pass
