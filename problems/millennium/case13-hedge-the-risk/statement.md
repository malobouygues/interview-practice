**Desk context**

You can't dump the illiquid asset (Asset_3), so offset its risk using the liquid ones (Asset_1, Asset_2). Find the trade in the liquid assets that minimises the variance of your total position.

**Problem**

Implement `hedge_inventory(prices, inventory)` which returns `{'hedge': {'Asset_1': qty, 'Asset_2': qty}, 'residual_variance': float}`.

**Formula**

```text
h_L = -inv(C_LL) @ C_L,all @ v
residual = w.T @ C @ w
```

where `C` is the covariance of asset returns, `v` the inventory vector, `L = {Asset_1, Asset_2}`, and `w = v` with the hedge added to the liquid entries.

**Rules**

- Asset order is the price columns (excluding `timestamp`).
- Add a ridge `1e-12 * I` to `C_LL` before solving.
- Round hedge quantities to 4 dp and residual variance to 10 dp; report -0.0 as 0.0.

**Constraints**

- At least 3 price rows. numpy available.

**Sample I/O**

```python
hedge_inventory(prices, {'Asset_1':0,'Asset_2':0,'Asset_3':0})
-> {'hedge': {'Asset_1':0.0,'Asset_2':0.0}, 'residual_variance':0.0}
```

**Notes**

- This is the variance-minimising hedge restricted to the assets you can actually trade.
