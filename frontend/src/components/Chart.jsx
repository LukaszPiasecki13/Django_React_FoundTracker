import * as React from "react";
import { LineChart, axisClasses } from "@mui/x-charts";
import CircularProgress from '@mui/material/CircularProgress';


export default function Chart({x, y}) {
  const [loading, setLoading] = React.useState(true);

  // Effect for setting the charging state
  React.useEffect(() => {
    if (x && y) {
      setLoading(false);
    } else {
      setLoading(true);
    }
  }, [x, y]);

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
