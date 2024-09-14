import * as React from "react";
import { styled, alpha } from "@mui/material/styles";
import Button from "@mui/material/Button";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import EditIcon from "@mui/icons-material/Edit";
import Divider from "@mui/material/Divider";
import ArchiveIcon from "@mui/icons-material/Archive";
import FileCopyIcon from "@mui/icons-material/FileCopy";
import MoreHorizIcon from "@mui/icons-material/MoreHoriz";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";

import BuyDialog from "./Dialogs/BuyDialog";
import SellDialog from "./Dialogs/SellDialog";
import AddWithdrawFundsDialog from "./Dialogs/AddWithdrawFundsDialog";

const StyledMenu = styled((props) => (
  <Menu
    elevation={0}
    anchorOrigin={{
      vertical: "bottom",
      horizontal: "right",
    }}
    transformOrigin={{
      vertical: "top",
      horizontal: "right",
    }}
    {...props}
  />
))(({ theme }) => ({
  "& .MuiPaper-root": {
    borderRadius: 6,
    marginTop: theme.spacing(1),
    minWidth: 180,
    color:
      theme.palette.mode === "light"
        ? "rgb(55, 65, 81)"
        : theme.palette.grey[300],
    boxShadow:
      "rgb(255, 255, 255) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px",
    "& .MuiMenu-list": {
      padding: "4px 0",
    },
    "& .MuiMenuItem-root": {
      "& .MuiSvgIcon-root": {
        fontSize: 18,
        color: theme.palette.text.secondary,
        marginRight: theme.spacing(1.5),
      },
      "&:active": {
        backgroundColor: alpha(
          theme.palette.primary.main,
          theme.palette.action.selectedOpacity
        ),
      },
    },
  },
}));

export default function AddMenus(props) {
  const pocket = props.pocket;
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [buyDialogOpen, setBuyDialogOpen] = React.useState(false);
  const [sellDialogOpen, setSellDialogOpen] = React.useState(false);
  const [addFundsDialogOpen, setAddFundsDialogOpen] = React.useState(false);
  const [withdrawFundsDialogOpen, setWithdrawFundsDialogOpen] =
    React.useState(false);

  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleBuyDialogOpen = () => {
    setBuyDialogOpen(true);
  };

  const handleSellDialogOpen = () => {
    setSellDialogOpen(true);
  };

  const handleAddFundsDialogOpen = () => {
    setAddFundsDialogOpen(true);
  };

  const handleWithdrawFundsDialogOpen = () => {
    setWithdrawFundsDialogOpen(true);
  };

  const handleDialogClose = () => {
    setBuyDialogOpen(false);
    setSellDialogOpen(false);
    setAddFundsDialogOpen(false);
    setWithdrawFundsDialogOpen(false);
  };
  return (
    <div>
      <Button
        id="demo-customized-button"
        aria-controls={open ? "demo-customized-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        variant="contained"
        disableElevation
        onClick={handleClick}
        endIcon={<KeyboardArrowDownIcon />}
      >
        Add
      </Button>
      <StyledMenu
        id="demo-customized-menu"
        MenuListProps={{
          "aria-labelledby": "demo-customized-button",
        }}
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
      >
        <MenuItem
          onClick={() => {
            handleClose();
            handleBuyDialogOpen();
          }}
          disableRipple
        >
          Buy
        </MenuItem>
        <MenuItem
          onClick={() => {
            handleClose();
            handleSellDialogOpen();
          }}
          disableRipple
        >
          Sell
        </MenuItem>
        <Divider sx={{ my: 0.5 }} />
        <MenuItem
          onClick={() => {
            handleClose();
            handleAddFundsDialogOpen();
          }}
          disableRipple
        >
          Add funds
        </MenuItem>
        <MenuItem
          onClick={() => {
            handleClose();
            handleWithdrawFundsDialogOpen();
          }}
          disableRipple
        >
          Withdraw funds
        </MenuItem>
      </StyledMenu>
      <BuyDialog
        open={buyDialogOpen}
        onClose={handleDialogClose}
        pocket={pocket}
      />
      <SellDialog
        open={sellDialogOpen}
        onClose={handleDialogClose}
        pocket={pocket}
        pocketAssetAllocationDetail={props.pocketAssetAllocationDetail}
      />
      <AddWithdrawFundsDialog
        open={addFundsDialogOpen || withdrawFundsDialogOpen}
        onClose={handleDialogClose}
        pocket={pocket}
        addFunds={addFundsDialogOpen}
        withdraw={withdrawFundsDialogOpen}
      />
    </div>
  );
}
