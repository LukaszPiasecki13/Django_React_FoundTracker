import * as React from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from './Title';

function preventDefault(event) {
  event.preventDefault();
}

export default function RecentScore({value}) {
  
  return (
    <React.Fragment>
      <Title>Recent Score</Title>
      <Typography component="p" variant="h4">
        ${value}
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        on 24 July, 2024
      </Typography>
      <div>
        <Link color="primary" href="#" onClick={preventDefault}>
          View balance
        </Link>
      </div>
    </React.Fragment>
  );
}
