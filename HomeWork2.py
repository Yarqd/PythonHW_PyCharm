#TaskOne
word0 = "test"
word1 = "testing"
my_string = word1 #Тут можно поменять слово
if len(my_string) % 2 == 0:
    print(my_string[(len(my_string)) // 2 - 1 : len(my_string) // 2 + 1])
else:
    print(my_string[(len(my_string)) // 2])
    print()

#TaskTwo
boys0 = ["Peter", "Alex", "John", "Arthur", "Richard"]
boys1 = ["Peter", "Alex", "John", "Arthur", "Richard", "Michael"]
girls = ["Kate", "Liza", "Kira", "Emma", "Trisha"]

my_boys = boys0 #Тут можно поменять список мальчиков

if len(my_boys) == len(girls):
    my_boys.sort()
    girls.sort()
    print("Результат\nИдеальные пары:")
    for boy, girl in zip(my_boys, girls):
        print(boy, "и", girl)
else:
    print("Результат: Внимание, кто-то может остаться без пары.")