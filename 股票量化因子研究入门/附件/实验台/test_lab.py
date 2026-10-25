"""关键口径测试；python -m unittest -v test_lab.py。"""
import unittest

import numpy as np
import pandas as pd

from lab import (assign_groups, backtest_groups, forward_returns, load_panel,
                 neutralize_factor, reversal_factor, sample_dates,
                 standardize_factor, time_splits, trade_to_target)


def tiny_panel(days=30, assets=10):
    sessions = pd.bdate_range("2024-01-02", periods=days)
    rows = []
    for t, date in enumerate(sessions):
        for a in range(assets):
            rows.append({"date": date, "asset": f"{a:06d}", "open": 10.0 + a * 100 + t * (a + 1),
                         "close": 10.5 + a * 100 + t * (a + 1), "adj_factor": 1.0,
                         "industry": f"行业{a % 2}", "log_mv": 20 + a / 10})
    frame = pd.DataFrame(rows)
    return frame, sessions


class TimeAndDataTests(unittest.TestCase):
    def test_next_open_and_holding_days(self):
        frame, dates = tiny_panel()
        panel = load_panel(frame, sessions=dates)
        label = forward_returns(panel, horizon=5)
        # t=6，入场=7，出场=12；不是 close(6)，也不是 open(11)。
        expected = (10 + 12) / (10 + 7) - 1
        self.assertAlmostEqual(label.loc[dates[6], "000000"], expected)
        expected_other = (10 + 900 + 12 * 10) / (10 + 900 + 7 * 10) - 1
        self.assertAlmostEqual(label.loc[dates[6], "000009"], expected_other)
        self.assertTrue(label.iloc[-6:].isna().all().all())

    def test_no_cross_asset_shift(self):
        frame, dates = tiny_panel()
        panel = load_panel(frame.sample(frac=1, random_state=7), sessions=dates)
        raw = reversal_factor(panel, 5)
        expected = -((10.5 + 6) / (10.5 + 1) - 1)
        self.assertAlmostEqual(raw.loc[dates[6], "000000"], expected)
        untouched = raw["000000"].copy()
        frame.loc[frame["asset"].eq("000009"), "close"] *= 100
        changed = reversal_factor(load_panel(frame, sessions=dates), 5)
        pd.testing.assert_series_equal(untouched, changed["000000"])

    def test_missing_session_does_not_jump(self):
        frame, dates = tiny_panel()
        frame = frame[~(frame["date"].eq(dates[4]) & frame["asset"].eq("000000"))]
        panel = load_panel(frame, sessions=dates)
        self.assertEqual(panel.quality["missing_grid_rows"], 1)
        label = forward_returns(panel, 5)
        self.assertTrue(np.isnan(label.loc[dates[3], "000000"]))  # 入场日期缺价。
        raw = reversal_factor(panel, 5)
        self.assertTrue(np.isnan(raw.loc[dates[9], "000000"]))  # 回看端点缺价。
        self.assertTrue(np.isnan(raw.loc[dates[7], "000000"]))  # 完整窗口过滤。
        self.assertTrue(np.isfinite(raw.loc[dates[10], "000000"]))

    def test_explicit_calendar_catches_whole_missing_day(self):
        frame, dates = tiny_panel()
        frame = frame[~frame["date"].eq(dates[4])]
        panel = load_panel(frame, sessions=dates)
        self.assertTrue(panel.wide("open").loc[dates[4]].isna().all())
        self.assertEqual(panel.quality["missing_grid_rows"], 10)

    def test_future_close_cannot_change_past_signal(self):
        frame, dates = tiny_panel()
        before = reversal_factor(load_panel(frame, sessions=dates), 5)
        frame.loc[frame["date"].gt(dates[10]), "close"] *= 100
        after = reversal_factor(load_panel(frame, sessions=dates), 5)
        pd.testing.assert_frame_equal(before.loc[:dates[10]], after.loc[:dates[10]])

    def test_purge_label_crossing_split_boundary(self):
        _, dates = tiny_panel(days=100)
        splits = time_splits(dates)
        train_start, train_end = splits["训练"]
        kept = sample_dates(dates, train_start, train_end, horizon=5)
        self.assertEqual(kept[-1], dates[53])  # t+1+5=59，刚好训练末日。
        self.assertNotIn(dates[54], kept)  # 出场第60日，跨到验证期。
        valid = sample_dates(dates, *splits["验证"], horizon=5)
        self.assertGreaterEqual(valid.min(), dates[60])
        self.assertLessEqual(dates[dates.get_loc(valid.max()) + 6], dates[79])

    def test_adjustment_and_explicit_declaration(self):
        frame, dates = tiny_panel()
        frame.loc[frame["date"].ge(dates[15]), ["open", "close"]] /= 2
        frame.loc[frame["date"].ge(dates[15]), "adj_factor"] = 2
        adjusted = load_panel(frame, sessions=dates)
        self.assertEqual(adjusted.wide("open").loc[dates[15], "000000"], 25)
        with self.assertRaisesRegex(ValueError, "显式"):
            load_panel(frame.drop(columns="adj_factor"), sessions=dates)
        load_panel(frame.drop(columns="adj_factor"), sessions=dates, already_adjusted=True)

    def test_duplicate_rejected(self):
        frame, dates = tiny_panel()
        with self.assertRaisesRegex(ValueError, "重复"):
            load_panel(pd.concat([frame, frame.iloc[:1]]), sessions=dates)


class FactorTests(unittest.TestCase):
    def test_cross_section_standardization(self):
        raw = pd.DataFrame([[1., 2., 3., 4., 100.], [4., 4., 4., 4., 4.]])
        score = standardize_factor(raw)
        self.assertAlmostEqual(score.iloc[0].mean(), 0)
        self.assertAlmostEqual(score.iloc[0].std(ddof=0), 1)
        self.assertTrue(score.iloc[1].isna().all())

    def test_neutralization_is_residual_orthogonal(self):
        frame, dates = tiny_panel(30, 20)
        panel = load_panel(frame, sessions=dates)
        score = standardize_factor(reversal_factor(panel))
        neutral = neutralize_factor(score, panel)
        day = dates[10]
        residual = neutral.loc[day].dropna()
        self.assertAlmostEqual(residual.mean(), 0, places=8)
        self.assertAlmostEqual(float(residual @ panel.wide("log_mv").loc[day, residual.index]), 0, places=8)
        with self.assertRaisesRegex(ValueError, "历史"):
            neutralize_factor(score, load_panel(frame.drop(columns="industry"), sessions=dates))

    def test_group_ties_are_not_hidden(self):
        with self.assertRaises(ValueError):
            assign_groups(pd.Series([1., 1., 1., 1., 1., 1.]))
        group = assign_groups(pd.Series(np.arange(10.)))
        self.assertEqual(group.value_counts().to_dict(), {1: 2, 2: 2, 3: 2, 4: 2, 5: 2})


class TurnoverTests(unittest.TestCase):
    def test_warmup_dates_before_first_signal_are_never_traded(self):
        frame, dates = tiny_panel(days=40, assets=10)
        panel = load_panel(frame, sessions=dates)
        score = standardize_factor(reversal_factor(panel, lookback=5))
        periods, _ = backtest_groups(panel, score, start=dates[0], end=dates[30], horizon=5)
        self.assertEqual(periods["signal_date"].min(), dates[5])
        self.assertGreaterEqual(periods["signal_date"].min(), score.dropna(how="all").index[0])

    def test_hand_calculated_drift_turnover(self):
        target = pd.Series({"甲": 0.5, "乙": 0.5})
        growth = pd.Series({"甲": 2.0, "乙": 1.0})
        pre = target * growth / (target * growth).sum()  # 2/3、1/3。
        result = trade_to_target(pre, target, fee_rate=0)
        self.assertAlmostEqual(result["buy_fraction"], 1 / 6)
        self.assertAlmostEqual(result["sell_fraction"], 1 / 6)
        self.assertAlmostEqual(result["turnover_total"], 1 / 3)
        self.assertEqual(trade_to_target(target, target, 0)["turnover_total"], 0)

    def test_exact_fee_equation(self):
        pre = pd.Series({"甲": 2 / 3, "乙": 1 / 3})
        target = pd.Series({"甲": 0.5, "乙": 0.5})
        result = trade_to_target(pre, target, fee_rate=0.001)
        self.assertAlmostEqual(result["remaining_fraction"] + result["cost_fraction"], 1)
        self.assertAlmostEqual(result["turnover_total"], 1 / 3)
        self.assertAlmostEqual(result["cost_fraction"], 0.001 / 3)

    def test_initial_and_final_cost_flat_prices(self):
        frame, dates = tiny_panel(days=30, assets=10)
        frame["open"], frame["close"] = 10., 10.
        panel = load_panel(frame, sessions=dates)
        score = pd.DataFrame(np.tile(np.arange(10), (30, 1)), index=dates, columns=panel.assets)
        periods, trades = backtest_groups(panel, score, start=dates[0], end=dates[20], fee_rate=0.001)
        q5 = periods[periods["portfolio"].eq("Q5")]
        self.assertAlmostEqual(q5["nav"].iloc[-1], (1 - 0.001) / (1 + 0.001))
        q5_trades = trades[trades["portfolio"].eq("Q5")]
        self.assertAlmostEqual(q5_trades["turnover_total"].iloc[0], 1 / 1.001)
        self.assertAlmostEqual(q5_trades["turnover_total"].iloc[-1], 1)
        self.assertTrue(np.allclose(q5_trades["turnover_total"].iloc[1:-1], 0))
        # 相邻持有区间首尾相接，没有每日叠加出五倍仓位。
        self.assertTrue(np.array_equal(q5["exit_date"].iloc[:-1].to_numpy(), q5["entry_date"].iloc[1:].to_numpy()))

    def test_missing_future_price_stops_without_lookahead_filter(self):
        frame, dates = tiny_panel()
        frame.loc[frame["date"].eq(dates[6]) & frame["asset"].eq("000009"), "open"] = np.nan
        panel = load_panel(frame, sessions=dates)
        score = pd.DataFrame(np.tile(np.arange(10), (30, 1)), index=dates, columns=panel.assets)
        with self.assertRaisesRegex(ValueError, "缺进/出场"):
            backtest_groups(panel, score, start=dates[0], end=dates[20])


if __name__ == "__main__":
    unittest.main(verbosity=2)
