spb_price = 20_000
msc_price = 25_000
ekb_price = 18_000
do_discount = True
discount_value = 20  # В процентах

dist = input("Введите направление (spb, msc, ekb): ")
adults_cnt = int(input("Введите количество взрослых: "))
kids_cnt = int(input("Введите количество детей: "))
cnt = 2 * adults_cnt + kids_cnt

if dist == "spb":
    dist_price = spb_price
elif dist == "msc":
    dist_price = msc_price
elif dist == "ekb":
    dist_price = ekb_price

price = cnt * dist_price // 2
if do_discount:
    price = cnt * dist_price * (100 - discount_value) // 100

print("Итоговая цена " + str(price))
