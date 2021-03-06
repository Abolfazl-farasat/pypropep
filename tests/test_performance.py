import pytest


@pytest.fixture
def pypropep():
    import pypropep
    pypropep.init()
    return pypropep


def test_simp_performance(pypropep):
    p = pypropep.RocketPerformance()
    return p.__str__()

def test_shifting_performance(pypropep):
    p = pypropep.ShiftingPerformance()
    lh2 = pypropep.PROPELLANTS['HYDROGEN (CRYOGENIC)']
    lox = pypropep.PROPELLANTS['OXYGEN (LIQUID)']
    # The below is from Sutton pg. 181
    OF = 5.551
    m_lh2 = 1.0
    m_lox = OF
    p.add_propellants_by_mass([(lh2, m_lh2), (lox, m_lox)])
    p.set_state(P=53.317*0.986923, Ae_At=25.)
    assert p.performance.Isp == pytest.approx(4124, 1e-2)
    assert p.performance.Ivac == pytest.approx(4348, 1e-2)
    assert p.performance.cstar == pytest.approx(2332.1, 1e-3)
    assert p.properties[0].T == pytest.approx(3389, 1e-2)
    assert p.properties[2].T == pytest.approx(1468, 1e-2)
    assert p.composition['exit'][0][1] > 0.1
    assert len(p.composition_condensed['exit']) == 0


def test_frozen_performance(pypropep):
    p = pypropep.FrozenPerformance()
    lh2 = pypropep.PROPELLANTS['HYDROGEN (CRYOGENIC)']
    lox = pypropep.PROPELLANTS['OXYGEN (LIQUID)']
    # The below is from Sutton pg. 181
    OF = 5.551
    N_lh2 = 1.0 / lh2.mw
    N_lox = OF / lox.mw
    p.add_propellants([(lh2, N_lh2), (lox, N_lox)])
    p.set_state(P=53.317*0.986923, Ae_At=25.)
    #assert p.performance.cstar == pytest.approx(2332.1, 1e-2)
    assert p.properties[0].T == pytest.approx(3389, 1e-2)
    assert p.composition['exit'][0][1] > 0.1
    assert len(p.composition_condensed['exit']) == 0
    print(p)

def test_properties(pypropep):
    p = pypropep.FrozenPerformance()
    ps = pypropep.ShiftingPerformance()
    e = pypropep.Equilibrium()
    lh2 = pypropep.PROPELLANTS['RP-1 (RPL)']
    lox = pypropep.PROPELLANTS['OXYGEN (LIQUID)']
    OF = 0.13
    p.add_propellants_by_mass([(lh2, 1.0), (lox, OF)])
    p.set_state(P=30, Ae_At=25.)
    ps.add_propellants_by_mass([(lh2, 1.0), (lox, OF)])
    ps.set_state(P=30, Ae_At=25.)
    e.add_propellants_by_mass([(lh2, 1.0), (lox, OF)])
    e.set_state(P=30, type='HP')
    assert p.properties[0].T == pytest.approx(ps.properties[0].T, 1e-2)
    assert p.properties[0].Cp == pytest.approx(ps.properties[0].Cp, 1e-2)
    assert p.properties[0].Isex == pytest.approx(ps.properties[0].Isex, 1e-2)
    assert p.properties[0].Cv == pytest.approx(ps.properties[0].Cv, 1e-2)

    assert p.properties[0].T == pytest.approx(e.properties.T, 1e-2)
    assert p.properties[0].Cp == pytest.approx(e.properties.Cp, 1e-2)
    assert p.properties[0].Isex == pytest.approx(e.properties.Isex, 1e-2)
    assert p.properties[0].Cv == pytest.approx(e.properties.Cv, 1e-2)
