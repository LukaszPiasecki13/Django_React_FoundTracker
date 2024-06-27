import * as React from "react";
import { useNavigate } from "react-router-dom";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";

import api from "../api";


import Title from "./Title";


export default function Pockets() {
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
    <React.Fragment>
      <Title>Pockets</Title>
      {pockets.map((pocket) => (
        <ListItemButton key={pocket.id} onClick={() => navigate("/pockets/" + pocket.name )}>
          <ListItemIcon></ListItemIcon>
          <ListItemText primary={pocket.name} />
        </ListItemButton>
      ))}
    </React.Fragment>
  );
}
