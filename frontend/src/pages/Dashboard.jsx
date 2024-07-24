import React, { useState, useEffect } from 'react';
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import Toolbar from "@mui/material/Toolbar";
import Title from "../components/Title";

import Chart from "../components/Chart";
import Deposits from "../components/Deposits";
import SideBar from "../components/bars/SideBar";
import AppBar from "../components/bars/AppBar";
import PageContainer from "../components/PageContainer";
import Pockets from "../components/Pockets";
import api from "../api";

const defaultTheme = createTheme();


export default function Dashboard() {
  const [open, setOpen] = React.useState(true);
  const toggleDrawer = () => {
    setOpen(!open);
  };

  const [data, setData] = React.useState([]);

  const getProfitOverTime = () => {
    api
      .get("/api/profit-data", {
        params: {
          pocketName: null,
          startDate: "2023-07-22",
          endDate: "2024-07-22",
        },
      })
      .then((response) => {
        const chartData = ({
          date: response.data.Date,
          value: response.data.Close,
        });
        setData(chartData);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  React.useEffect(() => {
    getProfitOverTime();
  }, []);
  

  return (
    <ThemeProvider theme={defaultTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <AppBar open={open} toggleDrawer={toggleDrawer} />
        <SideBar open={open} toggleDrawer={toggleDrawer} />

        <PageContainer>
          <Grid item xs={12} md={8} lg={9}>
            <Paper
              sx={{
                p: 2,
                display: "flex",
                flexDirection: "column",
                height: 400,
              }}
            >
              <Title>Portfolio Score</Title>
              <Chart x={data.date} y={data.value} />
            </Paper>
          </Grid>
          {/* Recent Deposits */}
          <Grid item xs={12} md={4} lg={3}>
            <Paper
              sx={{
                p: 2,
                display: "flex",
                flexDirection: "column",
                height: 240,
              }}
            >
              <Deposits />
            </Paper>
          </Grid>
          <Grid item xs={4}>
            <Paper
              sx={{ p: 2, display: "flex", flexDirection: "column" }}
            >
              <Pockets />



            </Paper>
          </Grid>
        </PageContainer>
      </Box>
    </ThemeProvider>
  );
}
