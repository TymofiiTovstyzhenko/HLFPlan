# in one month new независимый партнер
# Partner = 'независимый партнер'
# Volumes
class Strategy:
    def __init__(self
                 , self_eating
                 , average_client
                 , plus_clients
                 , minus_clients
                 , max_one_row_clients
                 , client_to_np_conversion):
        self.self_eating = self_eating
        self.average_client = average_client
        self.plus_clients = plus_clients
        self.minus_clients = minus_clients
        self.max_one_row_clients = max_one_row_clients
        self.client_to_np_conversion = client_to_np_conversion

    # todo: calculate clients growth dynamics
    def clients_in_month(self, age):
        if age == 0:
            return 0
        return min(self.max_one_row_clients,
                   self.plus_clients * age - self.minus_clients * (age - 1))

    def month_volume(self, age):
        return self.self_eating + self.clients_in_month(age) * self.average_client

    def limited_personal_volume(self, pv, age):
        return self.month_volume(age)

def empty_organization():
    return []

# [personal, organization, age, sum(tv), status, strategy, 2500 consequentally, 5000 consequentally, 10000 consequentally,
# countdown from last 10000, 20000 ov consequentally, 50000 ov consequentally, 80000 ov consequentally, 150000 ov consequentally, 200000 ov consequentally,
# non converted clients, number of conversions]
def new_partner(strategy: Strategy) -> object:
    return [0, empty_organization(), 0, 0, "p", strategy, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def next_conversion_number(partner):
    partner[16] +=1
    return partner[16]

def non_converted_clients(partner):
    return partner[15]

def clients(partner):
    return partner[17]

def convert_clients(partner):
    partner[15] -= strategy(partner).client_to_np_conversion

def new_np_conversion_satisfied(partner):
    conversion_limit = strategy(partner).client_to_np_conversion
    return conversion_limit and non_converted_clients(partner) >= strategy(partner).client_to_np_conversion

def grow_organization(partner, strategy_selector):
    organization = partner[1]
    for p in organization:
        grow(p, 1, strategy_selector)
    # appearing of new partners
    if new_np_conversion_satisfied(partner):
        organization.append(new_partner(strategy_selector(next_conversion_number(partner))))
        convert_clients(partner)

def grow(partner, months, strategy_selector):
    if months == 0:
        return partner
    # promo
    if status(partner) != "p":
        partner[6] = partner[6] + 1 if tv(partner) >= 2500 else 0
        partner[7] = partner[7] + 1 if tv(partner) >= 5000 else 0
        partner[8] = partner[8] + 1 if tv(partner) >= 10000 else 0
        partner[9] = 6 if ov(partner) >= 10000 else partner[9] - 1 if partner[9] > 0 else 0
        partner[10] = partner[10] + 1 if tv(partner) >= 2500 and ov(partner) >= 20000 else 0
        partner[11] = partner[11] + 1 if tv(partner) >= 2500 and ov(partner) >= 50000 else 0
        partner[12] = partner[12] + 1 if tv(partner) >= 2500 and ov(partner) >= 80000 else 0
        partner[13] = partner[13] + 1 if tv(partner) >= 2500 and ov(partner) >= 150000 else 0
        partner[14] = partner[14] + 1 if tv(partner) >= 2500 and ov(partner) >= 200000 else 0
        if partner[14] == 3:
            partner[4] = "pre"
        else:
            if partner[13] == 3:
                partner[4] = "m+"
            else:
                if partner[12] == 4:
                    partner[4] = "mio"
                else:
                    if partner[11] == 3:
                        partner[4] = "g+"
                    else:
                        if partner[10] == 3:
                            partner[4] = "get"
                        else:
                            if partner[6] == 6 and partner[9] > 0 and (partner[7] >= 2 or partner[8] >= 1):
                                partner[4] = "awt"

    if status(partner) == "sv" and partner[6] == 4:
        partner[4] = "wt"
    if partner[3] >= 4000 and status(partner) == "p":
        partner[4] = "sv"
    if partner[2] == 12 and partner[3] < 4000:
        partner[2] = 0
        partner[3] = 0
        partner[4] = "p"
        partner[6] = 0
        partner[7] = 0
        partner[8] = 0
        partner[9] = 0
        partner[10] = 0
        partner[11] = 0
        partner[12] = 0
        partner[13] = 0
        partner[14] = 0
        #partner[15]  w/o changes
    # age
    partner[2] += 1
    # non converted clients
    partner[15] += strategy(partner).plus_clients
    # clients
    partner[17] += strategy(partner).plus_clients
    # growth of PV
    partner[0] = strategy(partner).limited_personal_volume(partner[0], partner[2])
    # growth of organization
    grow_organization(partner, strategy_selector)
    # sum of TV for SV promo
    partner[3] += tv(partner)
    # next step
    return grow(partner, months - 1, strategy_selector)

def status(partner):
    return partner[4]

def strategy(partner):
    return partner[5]

def age(partner):
    return partner[2]

def organization(partner):
    return partner[1]


def pv(partner):
    return partner[0]

def tv(partner, level = 3 + 1):
    if level == 0:
        return 0
    s = pv(partner)
    for p in partner[1]:
        if p[4] == "p":
            s += tv(p, level - 1)
    return s

def ov(partner, level = 3 + 1):
    if level == 0:
        return 0
    s = 0
    for p in partner[1]:
        if p[4] != "p":
            s += pv(p) + ov(p, level - 1)
    return s

from collections import Counter

def count(partner):
    return Counter([status(p) for p in organization(partner)])

def count_organization(partner, level = 3 + 1):
    if level == 0:
        return []
    result = [status(p) for p in organization(partner)]
    for p in organization(partner):
        result += count_organization(p, level - 1)
    return Counter([p for p in result])

def organization_clients(partner, level = 3 + 1):
    if level == 0:
        return 0
    result = sum([clients(p) for p in organization(partner)])
    for p in organization(partner):
        result += organization_clients(p, level - 1)
    return result

def first_line_sv_count(partner):
    return dict(count(partner))["sv"]

def first_line_wt_count(partner):
    return dict(count(partner))["wt"]

def earns(partner):
    return 13.2 * (pv(partner) - strategy(partner).self_eating) + 4 *(tv(partner) -  pv(partner)) + 1* ov(partner)


class Partner:
    def __init__(self, data : object, level : int = 0, max_level = 3):
        self.data = data
        self.level = level
        self.max_level = max_level
    def __str__(self):
        org = ("Org:" + "".join(["\r\n" + str(Partner(i, self.level + 1, self.max_level)) if (tv(i) > 0 or ov(i) > 0)
                                else "" for i in organization(self.data)])) \
            if self.level < self.max_level and sum([tv(i) > 0 or ov(i) > 0 for i in organization(self.data)]) > 0 else ""
        return "\t" * self.level + "{0:3}: pv {1} tv {2} ov {3} age {4} {5} clients {6} earns {7} {8} ".format(
            status(self.data), pv(self.data), tv(self.data), ov(self.data), age(self.data), dict(count(self.data)), clients(self.data), earns(self.data),  org)

def main():
    StrongPartner = Strategy(200, 100, 5, 2, 15, 5)
    strong_partner_selector = lambda months : StrongPartner
    partner = grow(new_partner(StrongPartner), 15, strong_partner_selector)
    print("If strongs only 15 months\r\n", Partner(partner, 0, 1))

    Zero = Strategy(0, 0, 0, 0, 0, 0)
    Eater = Strategy(300, 0, 0, 0, 0, 0)
    Weak = Strategy(300, 100, 1, 1, 5, 5)
    strong_zero_eater_weak_selector = lambda age : StrongPartner if (age-1) % 4 == 0 else Zero if (age-1) % 4 == 1 else Eater if (age-1) % 4 == 2 else Weak
    partner = grow(new_partner(StrongPartner), 15, strong_zero_eater_weak_selector)
    print("If me is strong and organization is strong_zero_eater_weak 15 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(StrongPartner), 24, strong_zero_eater_weak_selector)
    print("If me is strong and the organization is strong_zero_eater_weak 24 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(StrongPartner), 36, strong_zero_eater_weak_selector)
    print("If me is strong and the organization is strong_zero_eater_weak 36 months\r\n", Partner(partner, 0, 1))

    #Avg = Strategy(300, 100, 3, 1, 7, 5)
    Avg = Strategy(300, 100, 2, 1, 10, 5)
    avg_zero_eater_weak_selector = lambda age: Avg if (age - 1) % 4 == 0 else Zero if (age - 1) % 4 == 1 else Eater if (age - 1) % 4 == 2 else Weak

    partner = grow(new_partner(StrongPartner), 12, avg_zero_eater_weak_selector)
    print("If me is strong and the organization is avg_zero_eater_weak 12 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(StrongPartner), 24, avg_zero_eater_weak_selector)
    print("If me is strong and the organization is avg_zero_eater_weak 24 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(StrongPartner), 36, avg_zero_eater_weak_selector)
    print("If me is strong and the organization is avg_zero_eater_weak 36 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(Avg), 12, avg_zero_eater_weak_selector)
    print("If me is average and the organization is average_zero_eater_weak 12 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(Avg), 24, avg_zero_eater_weak_selector)
    print("If me is average and the organization is average_zero_eater_weak 24 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(Avg), 36, avg_zero_eater_weak_selector)
    print("If me is average and the organization is average_zero_eater_weak 36 months\r\n", Partner(partner, 0, 1))

    partner = grow(new_partner(Avg), 48, avg_zero_eater_weak_selector)
    print("If me is average and the organization is average_zero_eater_weak 48 months\r\n", Partner(partner, 0, 1))

    once_a_5_sv = lambda age: {1: Avg, 2: Zero, 3: Eater, 4: Eater, 5: Weak}
    partner = grow(new_partner(Avg), 48, once_a_5_sv)
    once_a_5_sv = lambda age: {1 : Avg, 2 : Zero, 3 : Eater, 4 : Eater, 5:Weak}
    print("If me is average and the organization is average_zero_eater_weak 48 months\r\n", Partner(partner, 0, 1))

def YG():
    Zero = Strategy(0, 0, 0, 0, 0, 0)
    Eater = Strategy(300, 0, 0, 0, 0, 0)
    Weak = Strategy(300, 100, 1, 1, 5, 5)
    Avg = Strategy(500, 100, 3, 1, 10, 6)

    once_a_5_sv = lambda age: {0: Zero, 1: Eater, 2: Weak, 3:Zero, 4: Avg}[(age -1)%5]
    partner = grow(new_partner(Avg), 80, once_a_5_sv)
    print("If me is average and the organization is average_zero_eater_weak 80 months\r\n", Partner(partner, 0, 1))
    print("Full organization {0} clients {1}".format(dict(count_organization(partner)), organization_clients(partner)))

def dream():
    Zero = Strategy(0, 0, 0, 0, 0, 0)
    Eater = Strategy(300, 0, 0, 0, 0, 0)
    Weak = Strategy(300, 100, 1, 1, 5, 5)
    Avg = Strategy(500, 100, 3, 1, 10, 6)

    once_a_4_sv = lambda age: {0: Zero, 1: Eater, 2: Weak, 3:Avg}[(age -1)%4]
    partner = grow(new_partner(Avg), 70, once_a_4_sv)
    print("If me is average and the organization is average_zero_eater_weak 80 months\r\n", Partner(partner, 0, 1))
    print("Full organization {0} clients {1}".format(dict(count_organization(partner)), organization_clients(partner)))

def mega_dream():
    Cool = Strategy(300, 100, 5, 1, 10, 5)
    once_a_4_sv = lambda age: Cool
    partner = grow(new_partner(Cool), 20, once_a_4_sv)
    print("If me is average and the organization is average_zero_eater_weak 80 months\r\n", Partner(partner, 0, 1))
    print("Full organization {0} clients {1}".format(dict(count_organization(partner)), organization_clients(partner)))


if __name__ == '__main__':
    mega_dream()


