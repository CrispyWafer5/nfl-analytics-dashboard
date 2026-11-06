from src.player_stats import get_player_season_stats


def test_jared_goff():
    stats = get_player_season_stats("Jared Goff")

    assert stats["passing_yards"][0] > 0


def test_jahmyr_gibbs():
    stats = get_player_season_stats("Jahmyr Gibbs")

    assert stats["rushing_yards"][0] > 0


def test_amon_ra_st_brown():
    stats = get_player_season_stats("Amon-Ra St. Brown")

    assert stats["receiving_yards"][0] > 0