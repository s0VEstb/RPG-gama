from enum import Enum
from random import randint, choice


class SuperAbility(Enum):
    CRITICAL_DAMAGE = 1
    BOOST = 2
    HEAL = 3
    BLOCK_DAMAGE_AND_REVERT = 4
    STUN = 5
    REVIVE = 6
    SAITAMA = 7
    KILL_HERO = 8
    BOOM = 9


class GameEntity:
    def __init__(self, name, health, damage):
        self.__name = name
        self.__health = health
        self.__damage = damage

    @property
    def name(self):
        return self.__name

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        if value < 0:
            self.__health = 0
        else:
            self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    def __str__(self):
        return (f'{self.__name} HEALTH: {self.__health} '
                f'DAMAGE: {self.__damage}')


class Boss(GameEntity):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage)
        self.__defence = None
        self.__stun = False
        self.max_healt = self.health

    @property
    def stun(self):
        return self.__stun

    @stun.setter
    def stun(self, value):
        self.__stun = value

    @property
    def defence(self):
        return self.__defence

    def choose_defence(self, heroes: list):
        hero: Hero = choice(heroes)
        self.__defence = hero.ability

    def attack(self, heroes: list):
        if not self.__stun:
            for hero in heroes:
                if hero.health > 0:
                    if (hero.ability == SuperAbility.BLOCK_DAMAGE_AND_REVERT
                            and self.__defence != SuperAbility.BLOCK_DAMAGE_AND_REVERT):
                        hero.blocked_damage = int(self.damage * 0.1)
                        hero.health -= (self.damage - hero.blocked_damage)
                    else:
                        hero.health -= self.damage

    def __str__(self):
        return 'BOSS ' + super().__str__() + f' DEFENCE: {self.__defence}'


class Hero(GameEntity):
    def __init__(self, name, health, damage, ability):
        super().__init__(name, health, damage)
        if type(ability) == SuperAbility:
            self.__ability = ability

    @property
    def ability(self):
        return self.__ability

    def attack(self, boss: Boss):
        if self.health > 0 and boss.health > 0:
            boss.health -= self.damage

    def apply_super_power(self, boss: Boss, heroes: list):
        pass


class Warrior(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.CRITICAL_DAMAGE)

    def apply_super_power(self, boss: Boss, heroes: list):
        coeff = randint(2, 5)
        boss.health -= coeff * self.damage
        print(f'Warrior {self.name} hits critically: {coeff * self.damage}')


class Magic(Hero):
    def __init__(self, name, health, damage, boost_points):
        super().__init__(name, health, damage, SuperAbility.BOOST)
        self.__boost_points = boost_points

    def apply_super_power(self, boss: Boss, heroes: list):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                boss.health -= (hero.damage * (self.__boost_points * 1))
                print(f'Magic {self.name} boosted {hero.name}: {int(hero.damage * (self.__boost_points * 1))}')


class Medic(Hero):
    def __init__(self, name, health, damage, heal_points):
        super().__init__(name, health, damage, SuperAbility.HEAL)
        self.__heal_points = heal_points

    def apply_super_power(self, boss: Boss, heroes: list):
        for hero in heroes:
            if hero.health > 0 and self != hero:
                hero.health += self.__heal_points


class Berserk(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage,
                         SuperAbility.BLOCK_DAMAGE_AND_REVERT)
        self.__blocked_damage = 0

    @property
    def blocked_damage(self):
        return self.__blocked_damage

    @blocked_damage.setter
    def blocked_damage(self, value):
        self.__blocked_damage = value

    def apply_super_power(self, boss: Boss, heroes: list):
        boss.health -= self.__blocked_damage
        print(f'Berserk {self.name} reverted: {self.__blocked_damage}')

#ERROR
class Thor(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.STUN)

    def apply_super_power(self, boss: Boss, heroes: list):
        coeff = randint(1, 3)
        if coeff == 1:
            boss.stun = True
            print(f'------------Thor {self.name} has stunned: {boss.damage}---------')


def new_round_no_stun(boss: Boss):
    boss.stun = False

#ERROR
class Witcher(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.REVIVE)

    def apply_super_power(self, boss: Boss, heroes: list):
        dead_hero = None

        for hero in heroes:
            if hero.health == 0:
                dead_hero = hero
                break

            if dead_hero:
                chance = randint(1, 1)
                if chance == 1:
                    dead_hero.health = 300
                    self.health = 0
                    print(f'Witcher {self.name} revived: {dead_hero}')
                else:
                    print(f'Witcher {self.name} attempted revival but failed.')
            return dead_hero


class King(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.SAITAMA)

    def apply_super_power(self, boss: Boss, heroes: list):
        coeff = randint(1, 10)
        if coeff == 1:
            boss.health = 0
            print(f" \33[31m Saitama ONEPUNCHED {boss.name}  ")


# Когда у Boss hp < 50%, Imposter убивает Magic с вероятностью 20%.
# Он будет Совершать попытку убийство пока Magic не умрёт
class Imposter(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.KILL_HERO)

    def apply_super_power(self, boss: Boss, heroes: list):
        if boss.health < boss.max_healt / 2:
            coeff = randint(1, 5)
            if coeff == 1:
                for hero in heroes:
                    if hero.ability == SuperAbility.BOOST and hero.health > 0:
                        hero.health = 0
                        self.health = 0
                        print(f"==========Imposter {self.name} KILLED Magic==========")


class Bomber(Hero):
    def __init__(self, name, health, damage):
        super().__init__(name, health, damage, SuperAbility.BOOM)

    def apply_super_power(self, boss: Boss, heroes: list):
        if self.health == 0:
            boss.health -= 100
            print(f"==========Bomber {self.name} hits 100==========")




round_number = 0


def show_statistics(boss: Boss, heroes: list):
    print(f'ROUND: {round_number} -----------')
    print(boss)
    for hero in heroes:
        print(hero)


def play_round(boss: Boss, heroes: list):
    global round_number
    round_number += 1
    boss.choose_defence(heroes)
    boss.attack(heroes)
    for hero in heroes:
        if boss.defence != hero.ability and hero.health > 0:
            hero.attack(boss)
            hero.apply_super_power(boss, heroes)
    show_statistics(boss, heroes)
    new_round_no_stun(boss)


def is_game_over(boss: Boss, heroes: list):
    if boss.health <= 0:
        print('Heroes won!!!')
        return True
    all_heroes_dead = True
    for hero in heroes:
        if hero.health > 0:
            all_heroes_dead = False
            break
    if all_heroes_dead:
        print('Boss won!!!')
    return all_heroes_dead


def start_game():
    boss = Boss('Tiran', 10000, 50)
    warrior_1 = Warrior('Gats', 280, 10)
    warrior_2 = Warrior('Thorfin', 270, 15)
    magic = Magic('Estes', 250, 20, 1.2)
    doc = Medic('Hazzard', 250, 5, 15)
    berserk = Berserk('Tigril', 260, 10)
    assistant = Medic('Jun', 300, 5, 5)
    thor = Thor("Thor", 250, 15)
    witcher = Witcher("Vladislav", 300, 0)
    king = King("King", 300, 0)
    imposter = Imposter("Loki", 300, 5)
    bomber = Bomber("Kriko", 190, 15)
    heroes_list = [warrior_1, warrior_2, magic, doc,berserk, assistant,
                   thor, witcher, king, imposter, bomber]

    show_statistics(boss, heroes_list)
    while not is_game_over(boss, heroes_list):
        play_round(boss, heroes_list)


start_game()
