import React from "react";
import MUIDataTable from "mui-datatables";
import { createTheme, ThemeProvider } from "@mui/material/styles";

class DataTable extends React.Component {
  getMuiTheme = () =>
    createTheme({
      components: {
        MUIDataTableBodyCell: {
          styleOverrides: {
            root: {
              fontSize: "0.85rem",
              padding: "0px 0px",
              textAlign: "center",
            },
          },
        },
      },
    });

  render() {
    const { title, options, columns, data } = this.props;
    return (
      <ThemeProvider theme={this.getMuiTheme()}>
        <MUIDataTable
          title={title}
          options={options}
          columns={columns}
          data={data}
        />
      </ThemeProvider>
    );
  }
}

export default DataTable;
