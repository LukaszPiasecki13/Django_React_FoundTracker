import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from "@mui/material/TextField";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Grid from "@mui/material/Grid";

export default function SellDialog(props) {
  const { open, onClose, pocket } = props;
  const pocketAssetAllocationDetail = props.pocketAssetAllocationDetail;

  const [showCurrencyPriceBox, setShowCurrencyPriceBox] = React.useState([]);

  const [formValues, setFormValues] = React.useState({
    operation_type: "sell",
    asset_class: "",
    ticker: "",
    date: new Date().toISOString().split("T")[0],
    currency: "",
    purchase_currency_price: 0.0,
    quantity: "",
    price: "",
    fee: 0.0,
    comment: "",
    pocket_name: pocket.name,
  });

  const getUniqueValues = (data, key) => {
    const values = data.map((item) =>
      key.split(".").reduce((acc, curr) => acc[curr], item)
    );
    return [...new Set(values)]; // Usuwa duplikaty
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    const numValue = !isNaN(value) ? parseInt(value) : value;
    setFormValues({
      ...formValues,
      [name]: numValue,
    });
  };

  const handleSubmit = (event) => {
    s;
    event.preventDefault();
    s;
    onClose();
  };

  const assetClasses = getUniqueValues(
    pocketAssetAllocationDetail,
    "asset.asset_class"
  );
  const currencies = getUniqueValues(
    pocketAssetAllocationDetail,
    "asset.currency.name"
  );
  const tickers = getUniqueValues(pocketAssetAllocationDetail, "asset.ticker");

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs">
      <DialogTitle>SELL</DialogTitle>
      <DialogContent>
        <Box component="form" noValidate onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel size="small">Asset class</InputLabel>
                <Select
                  id="asset_class"
                  name="asset_class"
                  defaultValue=""
                  onChange={handleChange}
                  required
                  size="small"
                >
                  {assetClasses.map((assetClass) => (
                    <MenuItem key={assetClass} value={assetClass}>
                      {assetClass}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel size="small">Ticker</InputLabel>
                <Select
                  fullWidth
                  label="Ticker"
                  name="ticker"
                  onChange={handleChange}
                  required
                  size="small"
                >
                  {tickers.map((ticker) => (
                    <MenuItem key={ticker} value={ticker}>
                      {ticker}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Date"
                name="date"
                type="date"
                defaultValue={new Date().toISOString().split("T")[0]}
                onChange={handleChange}
                required
                size="small"
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel size="small">Currency</InputLabel>
                <Select
                  id="currency"
                  name="currency"
                  defaultValue={pocket?.currency?.name || ''} // set pocket.currency.name if is loaded or ''
                  onChange={handleChange}
                  required
                  size="small"
                >
                  {currencies.map((currency) => (
                    <MenuItem key={currency} value={currency}>
                      {currency}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Quantity"
                name="quantity"
                type="number"
                onChange={handleChange}
                required
                size="small"
              />
            </Grid>
            {showCurrencyPriceBox === true && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Currency Price"
                  name="purchase_currency_price"
                  type="number"
                  onChange={handleChange}
                  required
                  size="small"
                />
              </Grid>
            )}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Price"
                name="price"
                type="number"
                onChange={handleChange}
                required
                size="small"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Fee"
                name="fee"
                type="number"
                onChange={handleChange}
                size="small"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Comment"
                name="comment"
                defaultValue=""
                onChange={handleChange}
                size="small"
              />
            </Grid>
          </Grid>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button type="submit" onClick={handleSubmit}>
          SELL
        </Button>
      </DialogActions>
    </Dialog>
  );
}
