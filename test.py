import plan
import pytest

# регулируем конверсию sv стратегией развития партнеров
# каждый месяц 5 клиентов + и 2 минус
StrongPartner = plan.Strategy(200, 100, 5, 2, 15, 5)
ZeroEater = plan.Strategy(0, 0, 0, 0, 0, 0)

def strong_partner_selector(month : int):
    return StrongPartner

def grow(age, strategy_selector):
    return plan.grow(plan.new_partner(strategy_selector(1)), age, strategy_selector)


@pytest.mark.parametrize("months", [1, 5])
def test_WhenXMonthsPasses_Then_XPartnerAppears(months):
    assert len(grow(months, strong_partner_selector)[1]) == months


@pytest.mark.parametrize("months", [1, 10])
def test_In1MonthPartnerHasSubtreeWith1Partner(months):
    assert len(grow(months, strong_partner_selector)[1][months - 1]) > 0


@pytest.mark.parametrize("months, volume", [(1, 700), (2, 1000), (10, 1700)])
def test_PersonalVolumeOverMonths(months, volume):
    assert plan.pv(grow(months, strong_partner_selector)) == volume


@pytest.mark.parametrize("months, volume, sum_volume, comment"
    , [(1, 700, 700, ""), (2, 1700, 2400, ""), (3, 3700, 6100, ""), (4, 7700, 13800, ""),
       (5, 7800, 21600, "should be truncated by SV")])
def test_TotalVolumeOverMonths(months, volume, sum_volume, comment):
    partner = grow(months, strong_partner_selector)
    assert plan.tv(partner) == volume
    assert partner[3] == sum_volume

@pytest.mark.parametrize("months, status", [(1, "p"), (2, "p"), (3, "p"), (4, "sv")])
def test_status(months, status):
    partner = grow(months, strong_partner_selector)
    assert partner[4] == status

# todo: ограничение tv по глубине
@pytest.mark.parametrize("months, volume, sum_volume, comment"
    , [(1, 400, 400, ""), (2, 900, 1300, ""), (3, 1900, 3200, ""), (4, 3900, 7100, ""), (5, 7500, 14600, "ограничение tv по глубине")])
def test_TotalVolumeLimitedByDebth(months, volume, sum_volume, comment):
    SlowPartner = plan.Strategy(200, 100, 2, 1, 10, 2)
    slow_partner_selector = lambda months : SlowPartner
    partner = grow(months, slow_partner_selector)
    assert plan.tv(partner) == volume
    assert partner[3] == sum_volume

@pytest.mark.parametrize("months, volume, comment"
    , [(1, 0, ""), (2, 0, ""), (3, 0, ""), (4, 2200, ""), (5, 6900, ""), (6, 16300, ""), (7, 35100, ""), (8, 70500, "limited by 3 levels")])
def test_OV(months, volume, comment):
    FastPartner = plan.Strategy(500, 100, 7, 2, 20, 7)
    selector = lambda months : FastPartner
    partner = grow(months, selector)
    assert plan.ov(partner) == volume

@pytest.mark.parametrize("months, status", [(1, "p"), (9, "sv"), (13, "sv")])
def test_SVRecvalificationOk(months, status):
    selector = lambda months : plan.Strategy(500, 0, 0, 0, 0, 0)
    partner = grow(months, selector)
    assert plan.status(partner) == status


@pytest.mark.parametrize("months, status", [(1, "p"), (12, "p"), (15, "p")])
def test_SVRecvalificationNotOk(months, status):
    selector = lambda months : plan.Strategy(300, 0, 0, 0, 0, 0)
    partner = grow(months, selector)
    assert plan.status(partner) == status

# конверсия партнеров 3->1
def test_each_third_ip_becames_sv():
    selector = lambda age : StrongPartner if (age-1) % 3 == 0 else ZeroEater
    partner = grow(13, selector)
    assert plan.first_line_sv_count(partner) == 3

@pytest.mark.parametrize("months, status", [(3, "p"), (4, "sv"), (7, "sv"), (8, "wt"), (9, "wt"), (10, "awt"), (11, "get"), (13, "g+"), (14, "m+"), (15, "pre")])
def test_strong_partner_becomes_wt_at_8_month(months, status):
    partner = grow(months, strong_partner_selector)
    print(plan.Partner(partner, 0, 1))
    assert plan.status(partner) == status

# конверсия супервайзеров 2->1
# sv 5  8 11 14 16 19
# wt 9 12 15
def test_each_second_sv_becames_wt():
    selector = lambda age : plan.Strategy(300, 100, 5, 2, 15, 5) if (age-1) % 3 == 0 else ZeroEater
    partner = grow(12, selector)
    #print(plan.Partner(partner, 0, 1))
    assert plan.first_line_wt_count(partner) == 2
