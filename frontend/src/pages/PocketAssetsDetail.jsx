import * as React from "react";
import { useParams } from "react-router-dom";
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Link from "@mui/material/Link";

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableFooter,
} from "@mui/material";

import Toolbar from "@mui/material/Toolbar";
import { useNavigate, useLocation } from "react-router-dom";

import api from "../api";
import SideBar from "../components/bars/SideBar";
import AppBar from "../components/bars/AppBar";
import PageContainer from "../components/PageContainer";
import Title from "../components/Title";
import AddMenus from "../components/AddMenus";
import DataTable from "../components/DataTable";
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

  const [pocketAssetAllocationDetail, setPocketAssetAllocationDetail] =
    React.useState([]);
  const [pocket, setPocket] = React.useState([]);

  const getOperations = () => {
    api
      .get("api/asset-allocations", {
        params: {
          pocket_name: pocketName,
        },
      })
      .then((res) => res.data)
      .then((data) => {
        const transformedData = transformData(data);
        setPocketAssetAllocationDetail(transformedData);
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
      });
  };

  const transformData = (data) => {
    return data.map((item) => {
      const id = item.id;
      const ticker = item.asset.ticker;
      const name = item.asset.name;
      const asset_class = item.asset.asset_class;
      const currency = item.asset.currency.name;
      const quantity = Number(parseFloat(item.quantity).toFixed(2));
      const average_purchase_currency_price = Number(
        parseFloat(item.average_purchase_currency_price).toFixed(2)
      );
      const average_purchase_price = Number(
        parseFloat(item.average_purchase_price).toFixed(2)
      );
      const current_price = Number(
        parseFloat(item.asset.current_price).toFixed(2)
      );
      const daily_change_percent = Number(
        parseFloat(item.daily_change_percent).toFixed(2)
      );
      const daily_change = Number(parseFloat(item.daily_change_XXX).toFixed(2));
      const participation = Number(parseFloat(item.participation).toFixed(1));
      const total_value = Number(parseFloat(item.total_value_XXX).toFixed(1));
      const rate_of_return_percent = Number(
        parseFloat(item.rate_of_return).toFixed(1)
      );
      const rate_of_return_currency = Number(
        parseFloat(item.rate_of_return_XXX).toFixed(1)
      );
      const profit = Number(parseFloat(item.profit_XXX).toFixed(1));

      // Zwrócenie nowej płaskiej struktury
      return {
        id,
        ticker,
        name,
        asset_class,
        currency,
        quantity,
        average_purchase_currency_price,
        average_purchase_price,
        current_price,
        daily_change_percent,
        daily_change,
        participation,
        total_value,
        rate_of_return_percent,
        rate_of_return_currency,
        profit,
      };
    });
  };

  const toggleDrawer = () => {
    setOpen(!open);
  };

  React.useEffect(() => {
    getOperations();
    getPocketDetail();
  }, []);

  const columns = [
    {
      name: "id",
      label: "ID",
      options: {
        filter: true,
        sort: true,
        display: false,
      },
    },
    {
      name: "ticker",
      label: "Ticker",
      options: {
        filter: true,
        sort: true,
        display: false,
      },
    },
    {
      name: "name",
      label: "Name",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "asset_class",
      label: "Asset Class",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "currency",
      label: "Currency",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "quantity",
      label: "Quantity",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "average_purchase_currency_price",
      label: `Average purchase currency price [${pocket.currency?.name}]`,
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "average_purchase_price",
      label: `Average purchase price [${pocket.currency?.name}]`,
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "current_price",
      label: `Current price [${pocket.currency?.name}]`,
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "daily_change_percent",
      label: "Daily change %",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "daily_change",
      label: `Daily change [${pocket.currency?.name}]`,
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "participation",
      label: "Participation in portfolio",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "total_value",
      label: `Total value [${pocket.currency?.name}]`,
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "rate_of_return_percent",
      label: "Rate of return %",
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "rate_of_return_currency",
      label: `Rate of return % [${pocket.currency?.name}]`,
      options: {
        filter: true,
        sort: true,
      },
    },
    {
      name: "profit",
      label: `Profit [${pocket.currency?.name}]`,
      options: {
        filter: true,
        sort: true,
      },
    },
  ];

  const options = {
    filter: true,
    selectableRows: "none",
    expandableRows: true,
    // rowsPerPage: 50,
    responsive: "standard",

    setTableProps: () => ({
      // size: 'small',
      stickyHeader: true,
      padding: "none",
    }),

    renderExpandableRow: (rowData, rowMeta) => {
      return (
        <tr>
          <td colSpan={4}>
            <TableContainer>
              <Table style={{ margin: "0 auto" }}>
                <TableHead>
                  <TableCell align="right">Name</TableCell>
                  <TableCell align="right">Color</TableCell>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell component="th" scope="row" align="right">
                      ABXD
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </td>
        </tr>
      );
    },

    customTableBodyFooterRender: (opts) => {
      const theme = createTheme({
        components: {
          MuiTableCell: {
            styleOverrides: {
              root: {
                textAlign: "center",
                verticalAlign: "middle",
                fontWeight: "bolder",
                fontSize: 14,
              },
            },
          },
          MuiTableFooter: {
            styleOverrides: {
              root: {
                backgroundColor: "#f5f5dc", // Kolor beżowy
              },
            },
          },
        },
      });

      return (
        <>
          <ThemeProvider theme={theme}>
            <TableFooter>
              <TableRow>
                <TableCell />
                {opts.columns.map((col, index) => {
                  if (col.display === "true") {
                    if (col.name === "id") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "ticker") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "name") {
                      return <TableCell key={index}>Total</TableCell>;
                    } else if (col.name === "asset_class") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "currency") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "quantity") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "average_purchase_currency_price") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "average_purchase_price") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "current_price") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "daily_change_percent") {
                      return <TableCell key={index}>123</TableCell>;
                    } else if (col.name === "daily_change") {
                      return <TableCell key={index}>123</TableCell>;
                    } else if (col.name === "participation") {
                      return <TableCell key={index}></TableCell>;
                    } else if (col.name === "total_value") {
                      return <TableCell key={index}>123</TableCell>;
                    } else if (col.name === "rate_of_return_percent") {
                      return <TableCell key={index}>123</TableCell>;
                    } else if (col.name === "rate_of_return_currency") {
                      return <TableCell key={index}>123</TableCell>;
                    } else if (col.name === "profit") {
                      return <TableCell key={index}>123</TableCell>;
                    }
                  }
                })}
              </TableRow>
            </TableFooter>
          </ThemeProvider>
        </>
      );
    },
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar open={open} toggleDrawer={toggleDrawer} />
        <SideBar open={open} toggleDrawer={toggleDrawer} />
        <PageContainer>
          <Grid item xs={2}>
            <AddMenus
              pocket={pocket}
              pocketAssetAllocationDetail={pocketAssetAllocationDetail}
            />
          </Grid>
          <Grid item xs={1}>
            <Button
              variant="contained"
              size="medium"
              onClick={() => navigate(`${location.pathname}/charts`)}
            >
              Charts
            </Button>
          </Grid>
          <Grid item xs={1}>
            <Button
              variant="contained"
              size="medium"
              onClick={() => navigate(`${location.pathname}/history`)}
            >
              History
            </Button>
          </Grid>
          <Grid item xs={12}>
            <DataTable
              title={"Pocket Composition"}
              options={options}
              columns={columns}
              data={
                pocketAssetAllocationDetail ? pocketAssetAllocationDetail : []
              }
              colloredColumns={[
                "daily_change",
                "daily_change_percent",
                "rate_of_return_percent",
                "rate_of_return_currency",
                "profit",
              ]}
            />
          </Grid>
        </PageContainer>
      </Box>
    </ThemeProvider>
  );
}
