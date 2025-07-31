# | Категорія боргу | 10–20% | 20–40% | 40–60%   | 60–80%   |
# | --------------- | ------ | ------ | -------- | -------- |
# | 1–2,5k          | -30%   | -20%   | -20%     | -20%     |
# | 2,5–5k          | -30%   | -20%   | -20%     | -20%     |
# | 5–10k           | -35%   | -25%   | -25%     | -15%     |
# | 10–20k          | -35%   | -25%   | -25%     | -15%     |
# | 20–40k          | -35%   | -25%   | -25%     | -15%     |
# | 40–80k          | -40%   | -30%   | -25%     | -20%     |
# | 80–125k         | -40%   | -30%   | Тіло+20% | Тіло+10% |
# | 125–150k        | -40%   | -30%   | Тіло+20% | Тіло+10% |
# | 150–250k        | -50%   | -35%   | Тіло+15% | Тіло+5%  |
# | 250–800k        | -50%   | -35%   | Тіло+15% | Тіло+5%  |
from sympy.strategies.core import switch
from decimal import Decimal, ROUND_HALF_UP, getcontext

# Приклад
#
# Сума боргу 21000
# Тіло 5600
#
# Категорія Богу: пʼята (20-40к)
# Категорія % тіла: 57% (тіло/борг) третя категорія (40-60%)
#
# Скидка згідно таблиці: -25% від суми боргу
#
# Дисконт дорівнює борг*75%=15750
getcontext().prec = 10
class DiscountCalculator:
    def __init__(self, debt_amount, body_amount):
        self.debt_amount = self._clean_decimal(debt_amount)
        self.body_amount = self._clean_decimal(body_amount)
    def _clean_decimal(self, value):
        try:
            value_str = str(value).replace(" ", "").replace(",", ".")
            return Decimal(value_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except:
            return Decimal('0.00')

    def get_the_category(self):
        if self.debt_amount < 2500:
            return 1
        elif self.debt_amount < 5000:
            return 2
        elif self.debt_amount < 10000:
            return 3
        elif self.debt_amount < 20000:
            return 4
        elif self.debt_amount < 40000:
            return 5
        elif self.debt_amount < 80000:
            return 6
        elif self.debt_amount < 125000:
            return 7
        elif self.debt_amount < 150000:
            return 8
        elif self.debt_amount < 250000:
            return 9
        else:
            return 10

#Категорія % тіла: % (тіло / борг)
    # 10–20 % | 20–40 % | 40–60 % | 60–80 %
    def get_the_body_category(self):
        ratioPrecent = (self.body_amount / self.debt_amount) * 100
        if ratioPrecent < 10:
            return 1
        elif ratioPrecent < 20:
            return 2
        elif ratioPrecent < 40:
            return 3
        elif ratioPrecent < 60:
            return 4
        elif ratioPrecent < 80:
            return 5
        return None

    def get_the_discount(self):
        _category = self.get_the_category()
        _body_category = self.get_the_body_category()

        if _category == 1 or _category == 2:
            return 0.3
        elif _category in (3, 4, 5):
            if _body_category in (1, 2):
                return 0.35
            elif _body_category in (3, 4):
                return 0.25
            else:
                return 0.15
        elif _category in (6, 7):
            if _body_category in (1, 2):
                return 0.4
            elif _body_category in (3, 4):
                return 0.3
            else:
                return 0.2
        elif _category in (8, 9):
            if _body_category in (1, 2):
                return 0.4
            elif _body_category in (3, 4):
                return 0.3
            else:
                return 0.2
        else:
            if _body_category in (1, 2):
                return 0.5
            elif _body_category in (3, 4):
                return 0.35
            else:
                return 0.15

    def calculate_discount(self):
        """
        >>> DiscountCalculator(21000, 5600).calculate_discount()
        Decimal('15750.00')
        >>> DiscountCalculator(900000, 5000).calculate_discount()
        Decimal('5000.00')
        """
        discount_percentage = Decimal(str(self.get_the_discount()))
        result = self.debt_amount * (Decimal("1.00") - discount_percentage)
        _discount = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if self.debt_amount  <1000 or self.debt_amount  > 800000:
            _discount = self.body_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return _discount

if __name__ == "__main__":

    import doctest
    doctest.testmod(verbose=True)
    #exit()
    # Example usage
    debt = 25036.87  # Example debt amount
    body = 8540.11   # Example body amount

    calculator = DiscountCalculator(debt, body)



    category=calculator.get_the_category()
    body_category = calculator.get_the_body_category()
    discount_via_table = calculator.get_the_discount()
    discount = calculator.calculate_discount()

    print(f"Original Debt: {debt}")
    print(f"Body Amount: {body}")
    print(f"Debt Category: {category}")
    print(f"Body Category: {body_category}")
    print(f"Discount Percentage: {discount_via_table * 100}%")
    print(f"Discounted Amount: {discount:.2f}")

    print()