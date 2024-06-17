import * as React from "react";
import { styled, createTheme, ThemeProvider } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Paper from "@mui/material/Paper";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import SideBar from "../components/bars/SideBar";
import AppBar from "../components/bars/AppBar";
import api from "../api";
import PageContainer from "../components/PageContainer";

import Title from "../components/Title";

const defaultTheme = createTheme();

export default function Pocket() {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(true);
  const [pockets, setPockets] = React.useState([]);

  const toggleDrawer = () => {
    setOpen(!open);
  };

  React.useEffect(() => {
    getPockets();
  }, []);

  const getPockets = () => {
    api
      .get("api/pockets/")
      .then((res) => res.data)
      .then((data) => {
        setPockets(data);
      })
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
                <Title>Pockets</Title>
                {pockets.map((pocket) => (
                  <ListItemButton
                    onClick={() => navigate("/pockets/${pocket.id}")}
                  >
                    <ListItemIcon></ListItemIcon>
                    <ListItemText primary={pocket.name} />
                  </ListItemButton>
                ))}
              </React.Fragment>
            </Paper>
          </Grid>
        </PageContainer>
      </Box>
    </ThemeProvider>
  );
}
