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
from decimal import Decimal, ROUND_HALF_UP, getcontext, InvalidOperation

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
        try:
            self.debt_amount = Decimal(str(debt_amount))
        except (InvalidOperation, ValueError, TypeError):
            self.debt_amount = Decimal(0)
        try:
            self.body_amount = Decimal(str(body_amount))
        except (InvalidOperation, ValueError, TypeError):
            self.body_amount = Decimal(0)
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
            return 0
        elif ratioPrecent < 20:
            return 1
        elif ratioPrecent < 40:
            return 2
        elif ratioPrecent < 60:
            return 3
        elif ratioPrecent < 80:
            return 4
        elif ratioPrecent > 80:
            return 5
        return None

    def get_the_discount(self):
        _debt_category = self.get_the_category()
        _body_category = self.get_the_body_category()
        if _debt_category in (3,4,5) and _body_category == 4:
            return 0.15
        if _debt_category in (1, 2) and _body_category in (2,3,4):
            return 0.2
        if _debt_category ==6 and _body_category ==4:
            return 0.2
        if _debt_category in (3,4,5) and _body_category in (2,3):
            return 0.25
        if _debt_category ==6 and _body_category ==3:
            return 0.25
        if _debt_category in (1, 2) and _body_category ==1:
            return 0.3
        if _debt_category ==6 and _body_category ==2:
            return 0.3
        if _debt_category in (6,7,8) and _body_category ==2:
            return 0.3
        if _debt_category in (3, 4, 5) and _body_category == 1:
            return 0.35
        if _debt_category in (9,10) and _body_category == 2:
            return 0.35
        if _debt_category in (6, 7, 8) and _body_category == 1:
            return 0.4
        if _debt_category in (9, 10) and _body_category == 1:
            return 0.5
        if _debt_category==1 and _body_category == 2:
            return 0.2
        if _debt_category in (7,8) and _body_category == 3:
            return -1.2
        if _debt_category in (9,10) and _body_category == 3:
            return -1.15
        if _debt_category in (7,8) and _body_category == 4:
            return -1.1
        if _debt_category in (9,10) and _body_category == 4:
            return -1.05
        return 1

    def calculate_discount(self):
        discount_percentage = Decimal(str(self.get_the_discount()))
        result = self.debt_amount * (Decimal("1.00") - discount_percentage)
        _discount = result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if discount_percentage<-1:
            _discount = (self.body_amount*discount_percentage*-1).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if (self.body_amount / self.debt_amount) * 100  <10 \
                or (self.body_amount / self.debt_amount) * 100 > 80:
            _discount = self.body_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        if self.debt_amount <1000 or self.debt_amount >800_000 :
            _discount = self.body_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return _discount

if __name__ == "__main__":

    # import doctest
    # doctest.testmod(verbose=True)
    #exit()
    # Example usage
    debt = 60000


   # Example debt amount
    body = 15020

   # Example body amount

    calculator = DiscountCalculator(debt, body)



    category=calculator.get_the_category()
    body_category = calculator.get_the_body_category()
    discount_via_table = calculator.get_the_discount()
    discount = calculator.calculate_discount()

    print(f"Original Debt: {debt}")
    print(f"Body Amount: {body}")
    print(f"Debt Category: {category}")
    print(f"Body Category: {body_category}")
    print(f"Ratio of Body to Debt: {(body / debt) * 100:.2f}%")
    print(f"Discount Percentage: {discount_via_table * 100}%")
    print(f"Discounted Amount: {discount:.2f}")

    print()