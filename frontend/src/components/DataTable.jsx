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
    const { title, options, columns, data, colloredColumns } = this.props;

    const customBodyRender = (value, tableMeta, colloredColumns) => {
      const columnName = tableMeta.columnData.name;
      if (colloredColumns.includes(columnName)) {
        if (typeof value === "number") {
          if (value < 0) {
            return <div style={{ color: "red" }}>{value}</div>;
          } else if (value > 0) {
            return <div style={{ color: "green" }}>{value}</div>;
          }
        }
      }

      // Jeśli nie jest liczbą lub jest równe 0, zwróć wartość z domyślnym stylem
      return <div style={{ color: "black" }}>{value}</div>;
    };

    // Zaktualizowane kolumny z funkcją niestandardowego renderowania
    const updatedColumns = columns.map((col) => ({
      ...col,
      options: {
        ...col.options,
        customBodyRender: (value, tableMeta) =>
          customBodyRender(value, tableMeta, colloredColumns),
      },
    }));

    return (
      <ThemeProvider theme={this.getMuiTheme()}>
        <MUIDataTable
          title={title}
          options={options}
          columns={updatedColumns}
          data={data}
        />
      </ThemeProvider>
    );
  }
}

export default DataTable;
