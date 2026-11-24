import numpy as np
import pandas as pd
import statsmodels.api as sm

FEATURES = ["surprise_mbbl", "demand_growth_known_pct"]
TARGET = "ret_fwd_10d"
TRAIN_END = pd.Timestamp("2022-12-31")
TEST_START = pd.Timestamp("2023-01-01")
TEST_END = pd.Timestamp("2024-12-31")


def validate_out_of_sample(decisions):
    table = decisions.copy()
    table["date"] = pd.to_datetime(table["date"])
    table["target_end_date"] = pd.to_datetime(table["target_end_date"])
    table = table.dropna(subset=FEATURES + [TARGET])

    # ---- FIXED SPLIT. Estimation: rows whose 10-day target was fully realised by the end of 2022
    train = table[table["target_end_date"] <= TRAIN_END]
    test = table[(table["date"] >= TEST_START) & (table["target_end_date"] <= TEST_END)]
    model = sm.OLS(train[TARGET], sm.add_constant(train[FEATURES])).fit()     # frozen from here on

    in_error = train[TARGET] - model.fittedvalues
    prediction = model.predict(sm.add_constant(test[FEATURES], has_constant="add"))
    out_error = test[TARGET] - prediction
    zero_error = test[TARGET]                               # baseline 1: no change expected
    mean_error = test[TARGET] - train[TARGET].mean()        # baseline 2: the training average
    fixed = {"n_train": len(train), "n_test": len(test), "r2_in": model.rsquared,
             "mae_in": in_error.abs().mean(), "rmse_in": np.sqrt((in_error ** 2).mean()),
             "mae_out": out_error.abs().mean(), "rmse_out": np.sqrt((out_error ** 2).mean()),
             "mae_zero": zero_error.abs().mean(), "rmse_zero": np.sqrt((zero_error ** 2).mean()),
             "mae_mean": mean_error.abs().mean(), "rmse_mean": np.sqrt((mean_error ** 2).mean()),
             "hit_rate": (np.sign(prediction) == np.sign(test[TARGET])).mean()}

    # ---- WALK-FORWARD, expanding window: re-estimate at the start of each quarter of 2023-2024
    walk = []
    path = []
    origin = TEST_START
    while origin <= TEST_END:
        next_origin = origin + pd.DateOffset(months=3)
        # only the rows whose target was already realised before the origin
        known = table[table["target_end_date"] < origin]
        quarter_model = sm.OLS(known[TARGET], sm.add_constant(known[FEATURES])).fit()
        quarter = test[(test["date"] >= origin) & (test["date"] < next_origin)]
        quarter_prediction = quarter_model.predict(sm.add_constant(quarter[FEATURES], has_constant="add"))
        walk.append(pd.DataFrame({"date": quarter["date"], "origin": origin,
                                  "realised": quarter[TARGET], "prediction": quarter_prediction}))
        path.append({"origin": origin, "n_train": int(quarter_model.nobs),
                     "coef_surprise": quarter_model.params["surprise_mbbl"],
                     "coef_demand": quarter_model.params["demand_growth_known_pct"]})
        origin = next_origin

    walk = pd.concat(walk, ignore_index=True)
    walk_error = walk["realised"] - walk["prediction"]
    return {"fixed": fixed, "coefficients": model.params,
            "walk_forward": walk, "walk_forward_path": pd.DataFrame(path),
            "walk_forward_mae": walk_error.abs().mean(),
            "walk_forward_rmse": np.sqrt((walk_error ** 2).mean())}
