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

import api from "../../api";

export default function BuyDialog(props) {
  const { open, onClose, pocketName } = props;
  const [currencies, setCurrencies] = React.useState([]);
  const [assetClasses, setAssetClasses] = React.useState([]);

  const getCurrencies = () => {
    api
      .get("api/currencies")
      .then((res) => res.data)
      .then((data) => {
        setCurrencies(data);
      })
      .catch((err) => alert(err));
  };

  const getAssetClasses = () => {
    api
      .get("api/asset-classes")
      .then((res) => res.data)
      .then((data) => {
        setAssetClasses(data);
      })
      .catch((err) => alert(err));
  };

  const buyAsset = (e) => {
    api
      .post("api/operations/", formValues)
      .then((res) => {
        if (res.status === 201) alert("Operation created successfully");
        else alert("Error creating operation");
      })
      .catch((err) => alert(err));
  };

  React.useEffect(() => {
    getCurrencies();
    getAssetClasses();
  }, []);

  const [formValues, setFormValues] = React.useState({
    operation_type: "buy",
    asset_class: "",
    ticker: "",
    date: "",
    currency: "",
    quantity: "",
    price: "",
    fee: 0.0,
    comment: "",
    pocket_name: pocketName 
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    const numValue = !isNaN(value) ? parseInt(value) : value;
    setFormValues({
      ...formValues,
      [name]: numValue,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    buyAsset(event);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs">
      <DialogTitle>BUY</DialogTitle>
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
                  autoWidth
                  size="small"
                >
                  {assetClasses.map((assetClass) => (
                    <MenuItem key={assetClass.name} value={assetClass.name}>
                      {assetClass.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Ticker"
                name="ticker"
                onChange={handleChange}
                required
                size="small"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Date"
                name="date"
                type="date"
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
                  defaultValue=""
                  onChange={handleChange}
                  required
                  size="small"
                >
                  {currencies.map((currency) => (
                    <MenuItem key={currency.name} value={currency.name}>
                      {currency.name}
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
          Buy
        </Button>
      </DialogActions>
    </Dialog>
  );
}
