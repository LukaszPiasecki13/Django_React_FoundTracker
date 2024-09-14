import * as React from "react";
import { useParams } from "react-router-dom";
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Link from "@mui/material/Link";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Toolbar from "@mui/material/Toolbar";
import { useNavigate, useLocation  } from "react-router-dom";

import api from "../api";
import SideBar from "../components/bars/SideBar";
import AppBar from "../components/bars/AppBar";
import PageContainer from "../components/PageContainer";
import Title from "../components/Title";
import AddMenus from "../components/AddMenus";
import { Button } from "@mui/material";

function preventDefault(event) {
  event.preventDefault();
}

export default function PocketAssetsDetail() {
  const navigate = useNavigate();
  const location = useLocation();
  const pocketName = useParams().slug;
  const defaultTheme = createTheme();
  const [open, setOpen] = React.useState(true);

  const [pocketAssetAllocationDetail, setPocketAssetAllocationDetail] = React.useState([]);
  const [pocket, setPocket] = React.useState([]);

  const getOperations = () => {
    api
    .get("api/asset-allocations", {
      params: {
        pocket_name: pocketName
      }
    })
      .then((res) => res.data)
      .then((data) => {
        setPocketAssetAllocationDetail(data);
      })
      .catch((err) => alert(err.response.data.error));
  };

  const getPocketDetail = () => {
    api
      .get("api/pockets", {
        params: {
          name: pocketName,
        },
      })
      .then((res) => res.data)
      .then((data) => {
        setPocket(data[0]);
      })}

  const toggleDrawer = () => {
    setOpen(!open);
  };

  React.useEffect(() => {
    getOperations();
    getPocketDetail();
  }, []);

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar open={open} toggleDrawer={toggleDrawer} />
        <SideBar open={open} toggleDrawer={toggleDrawer} />
        <PageContainer>
          <Grid item xs={2}>
            <AddMenus pocket={pocket} pocketAssetAllocationDetail={pocketAssetAllocationDetail} />
          </Grid>
          <Grid item xs={1}>
            <Button
              variant="contained"
              size="medium"
              onClick={() =>navigate(`${location.pathname}/charts`)}
            >
              Charts
            </Button>
          </Grid>
          <Grid item xs={1}>
            <Button variant="contained" size="medium" onClick={() =>navigate(`${location.pathname}/history`)}>
              History
            </Button>
          </Grid>
          <Grid item xs={12}>
            <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
              <React.Fragment>
                <Title>Pocket Composition</Title>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Asset Class</TableCell>
                      <TableCell>Currency</TableCell>
                      <TableCell>Quantity</TableCell>
                      <TableCell>Average purchase currency price [{pocket.currency?.name}]</TableCell>
                      <TableCell>Average purchase price [{pocket.currency?.name}]</TableCell>
                      <TableCell>Current price [{pocket.currency?.name}]</TableCell>
                      <TableCell>Daily change %</TableCell>
                      <TableCell>Daily change [{pocket.currency?.name}]</TableCell>
                      <TableCell>Participation in portfolio</TableCell>
                      <TableCell>Total value [{pocket.currency?.name}]</TableCell>
                      <TableCell>Rate of return %</TableCell>
                      <TableCell>Rate of return % [{pocket.currency?.name}]</TableCell>
                      <TableCell>Profit [{pocket.currency?.name}]</TableCell>
                      {/* <TableCell align="right">Dividend</TableCell> */}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {pocketAssetAllocationDetail.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell>{row.asset.name}</TableCell>
                        <TableCell>{row.asset.asset_class}</TableCell>
                        <TableCell>{row.asset.currency.name}</TableCell>
                        <TableCell>{parseFloat(row.quantity).toFixed(2)}</TableCell>
                        <TableCell>{parseFloat(row.average_purchase_currency_price).toFixed(2)}</TableCell>
                        <TableCell>{parseFloat(row.average_purchase_price).toFixed(2)}</TableCell>
                        <TableCell>{parseFloat(row.asset.current_price).toFixed(2)}</TableCell>
                        <TableCell
                          style={{
                            color:
                              row.daily_change_percent < 0 ? "red" : "green",
                          }}
                        >
                          {parseFloat(row.daily_change_percent).toFixed(2)}%
                        </TableCell>
                        <TableCell
                          style={{
                            color: row.daily_change_XXX < 0 ? "red" : "green",
                          }}
                        >
                          {parseFloat(row.daily_change_XXX).toFixed(2)}
                        </TableCell>
                        <TableCell>{parseFloat(row.participation).toFixed(1)}%</TableCell>
                        <TableCell>{parseFloat(row.total_value_XXX).toFixed(1)}</TableCell>
                        <TableCell
                          style={{
                            color: row.rate_of_return < 0 ? "red" : "green",
                          }}
                        >
                          {parseFloat(row.rate_of_return).toFixed(1)}%
                        </TableCell>
                        <TableCell
                          style={{
                            color: row.rate_of_return_XXX < 0 ? "red" : "green",
                          }}
                        >
                          {parseFloat(row.rate_of_return_XXX).toFixed(1)} %
                        </TableCell>
                        <TableCell
                          style={{
                            color: row.profit_XXX < 0 ? "red" : "green",
                          }}
                        >
                          {parseFloat(row.profit_XXX).toFixed(1)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                <Link
                  color="primary"
                  href="#"
                  onClick={preventDefault}
                  sx={{ mt: 3 }}
                >
                  See more
                </Link>
              </React.Fragment>
            </Paper>
          </Grid>
        </PageContainer>
      </Box>
    </ThemeProvider>
  );
}
