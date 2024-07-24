import * as React from "react";
import { LineChart, axisClasses } from "@mui/x-charts";
import CircularProgress from '@mui/material/CircularProgress';


export default function Chart({x, y, loading}) {


  return (
    <React.Fragment>

      <div style={{ width: "100%", flexGrow: 1, overflow: "hidden" }}>
      {loading ? (
          <CircularProgress />
        ) : (
        <LineChart
          
          xAxis={[{ 
            data: x,
            dataKey: "date", 
            scaleType: "band",

          }]}
          series={[
            {
              curve: "linear",
              data: y,
              showMark:false
            },
          ]}      
        />
        )}
      </div>
    </React.Fragment>
  );
};
