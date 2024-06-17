import * as React from "react";
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
import SideBar from "../components/bars/SideBar";
import AppBar from "../components/bars/AppBar";
import api from "../api";
import PageContainer from "../components/PageContainer";
import Toolbar from "@mui/material/Toolbar";

import Title from "../components/Title";

function preventDefault(event) {
  event.preventDefault();
}

export default function PocketDetail() {
  const defaultTheme = createTheme();
  const [open, setOpen] = React.useState(true);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  React.useEffect(() => {
    getOperations();
  }, []);

  const [operations, setOperations] = React.useState([]);

  const getOperations = () => {
    api
      .get("api/asset-allocations")
      .then((res) => res.data)
      .then((data) => setOperations(data), console.log(data))
      .catch((err) => alert(err));
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar open={open} toggleDrawer={toggleDrawer} />
        <SideBar open={open} toggleDrawer={toggleDrawer} />
        <PageContainer>
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
                      <TableCell>Average purchase price</TableCell>
                      <TableCell>Current price</TableCell>
                      <TableCell>Daily change</TableCell>
                      <TableCell>Daily change PLN</TableCell>
                      <TableCell>Participation in portfolio</TableCell>
                      <TableCell>Rate of return</TableCell>
                      <TableCell>Rate of return [PLN]</TableCell>
                      <TableCell>Profit [PLN]</TableCell>
                      <TableCell align="right">Dividend</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {operations.map((row) => (
                      <TableRow key={row.id}>
                        <TableCell>{row.asset.name}</TableCell>
                        <TableCell>{row.asset.asset_class}</TableCell>
                        <TableCell>{row.asset.currency}</TableCell>
                        <TableCell>{row.quantity}</TableCell>
                        <TableCell>{row.average_purchase_price}</TableCell>
                        <TableCell>{row.asset.current_price}</TableCell>
                        <TableCell>{row.daily_change_percent}</TableCell>
                        <TableCell>{row.daily_change_XXX}</TableCell>
                        <TableCell>{row.participation}</TableCell>
                        <TableCell>{row.rate_of_return}</TableCell>
                        <TableCell>{row.rate_of_return_XXX}</TableCell>
                        <TableCell>{row.profit_XXX}</TableCell>
                        <TableCell align="right">{`$${row.dividends}`}</TableCell>
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
