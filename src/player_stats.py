import polars as pl
import nflreadpy as nfl

player_stats = nfl.load_player_stats(seasons=[2025])


def get_player_info(player_name):
    player = player_stats.filter(
        pl.col("player_display_name") == player_name
    )

    player_info = player.select([
        "player_id",
        "player_display_name",
        "position",
        "headshot_url",
        "team"
    ]).unique()

    return player_info


def get_qb_season_stats(player_name):
    player = player_stats.filter(
        pl.col("player_display_name") == player_name
    )

    season_stats = player.select([
        pl.col("completions").sum().alias("completions"),
        pl.col("attempts").sum().alias("attempts"),
        pl.col("passing_yards").sum().alias("passing_yards"),
        pl.col("passing_tds").sum().alias("passing_tds"),
        pl.col("passing_interceptions").sum().alias("interceptions")
    ])

    season_stats = season_stats.with_columns(
        (
            (pl.col("completions") / pl.col("attempts")) * 100
        ).round(2).alias("completion_percentage")
    )

    return season_stats


def get_rb_season_stats(player_name):
    player = player_stats.filter(
        pl.col("player_display_name") == player_name
    )

    season_stats = player.select([
        # Rushing
        pl.col("carries").sum().alias("carries"),
        pl.col("rushing_yards").sum().alias("rushing_yards"),
        pl.col("rushing_tds").sum().alias("rushing_tds"),
        pl.col("rushing_first_downs").sum().alias("rushing_first_downs"),
        pl.col("rushing_fumbles").sum().alias("rushing_fumbles"),

        # Receiving
        pl.col("targets").sum().alias("targets"),
        pl.col("receptions").sum().alias("receptions"),
        pl.col("receiving_yards").sum().alias("receiving_yards"),
        pl.col("receiving_tds").sum().alias("receiving_tds")
    ])

    season_stats = season_stats.with_columns([
        (
            pl.col("rushing_yards") / pl.col("carries")
        ).round(2).alias("yards_per_carry"),

        (
            pl.col("receiving_yards") / pl.col("receptions")
        ).round(2).alias("yards_per_reception")
    ])

    return season_stats


def get_wr_season_stats(player_name):
    player = player_stats.filter(
        pl.col("player_display_name") == player_name
    )

    season_stats = player.select([
        pl.col("targets").sum().alias("targets"),
        pl.col("receptions").sum().alias("receptions"),
        pl.col("receiving_yards").sum().alias("receiving_yards"),
        pl.col("receiving_tds").sum().alias("receiving_tds"),
        pl.col("receiving_first_downs").sum().alias("receiving_first_downs"),
        pl.col("receiving_fumbles").sum().alias("receiving_fumbles")
    ])

    season_stats = season_stats.with_columns(
        (
            pl.col("receiving_yards") / pl.col("receptions")
        ).round(2).alias("yards_per_reception")
    )

    return season_stats


def get_player_season_stats(player_name):
    player = player_stats.filter(
        pl.col("player_display_name") == player_name
    )

    if player.is_empty():
        return "Player not found"

    position = player["position"][0]

    if position == "QB":
        return get_qb_season_stats(player_name)

    elif position == "RB":
        return get_rb_season_stats(player_name)

    elif position == "WR":
        return get_wr_season_stats(player_name)

    else:
        return f"Stats for position {position} are not built yet."


if __name__ == "__main__":
    print("Jared Goff (QB):")
    print(get_player_season_stats("Jared Goff"))

    print("\nJahmyr Gibbs (RB):")
    print(get_player_season_stats("Jahmyr Gibbs"))

    print("\nAmon-Ra St. Brown (WR):")
    print(get_player_season_stats("Amon-Ra St. Brown"))